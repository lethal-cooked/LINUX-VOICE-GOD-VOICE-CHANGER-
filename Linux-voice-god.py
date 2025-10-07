#!/usr/bin/env python3
# Real-time Voice Changer with GUI Soundboard for Linux
# Usage:
# 1. Run: ./voice_changer.py (starts voice changer with GUI menu).
# 2. Add sound: voice add <file_path> (e.g., voice add example.mp3). Note: sudo is optional if permissions allow.
# 3. In GUI: Click sound buttons to play, adjust pitch slider for voice depth.
# Automatically installs dependencies for Ubuntu/Kali/Debian or Arch, including Tkinter for GUI.

import platform
import subprocess
import os
import sys
import sounddevice as sd
import numpy as np
import librosa
import scipy.signal as signal
import soundfile as sf
import shutil
import threading
import argparse
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Audio settings
samplerate = 44100  # Standard sample rate
channels = 1  # Mono for simplicity
blocksize = 2048  # Balance between latency and quality
dtype = np.float32
pitch_shift_steps = -7  # Initial deepen voice (adjustable in GUI)
noise_gate_threshold = 0.01  # Noise reduction threshold

# Soundboard settings
soundboard_dir = os.path.expanduser("~/.voice_changer_soundboard")
soundboard_files = []
soundboard_playing = None  # Track currently playing sound
soundboard_lock = threading.Lock()
stream = None  # Global stream reference

def check_and_install_dependencies():
    """Check Linux distro and install required dependencies."""
    distro = platform.freedesktop_os_release().get('ID', '').lower()
    print(f"Detected Linux distribution: {distro}")

    # Define system dependencies
    if distro in ['ubuntu', 'kali', 'debian']:
        pkg_manager = 'apt-get'
        system_deps = ['libportaudio2', 'portaudio19-dev', 'libsndfile1-dev', 'python3-tk']
        install_cmd = ['sudo', 'apt-get', 'install', '-y'] + system_deps
    elif distro == 'arch':
        pkg_manager = 'pacman'
        system_deps = ['portaudio', 'libsndfile', 'tk']
        install_cmd = ['sudo', 'pacman', '-S', '--noconfirm'] + system_deps
    else:
        print("Unsupported Linux distribution. Please install dependencies manually.")
        print("Required system packages: portaudio, libsndfile, python3-tk (or tk)")
        print("Required Python packages: sounddevice, numpy, scipy, librosa, soundfile")
        sys.exit(1)

    # Install system dependencies
    print(f"Installing system dependencies: {', '.join(system_deps)}")
    try:
        subprocess.run(install_cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to install system dependencies with {pkg_manager}. Please install them manually.")
        sys.exit(1)

    # Install Python dependencies
    python_deps = ['sounddevice', 'numpy', 'scipy', 'librosa', 'soundfile']
    print(f"Installing Python dependencies: {', '.join(python_deps)}")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + python_deps, check=True)
    except subprocess.CalledProcessError:
        print("Failed to install Python dependencies. Please install them manually with:")
        print(f"pip install {' '.join(python_deps)}")
        sys.exit(1)

def setup_soundboard():
    """Set up soundboard directory and load files."""
    global soundboard_files
    if not os.path.exists(soundboard_dir):
        os.makedirs(soundboard_dir)
    soundboard_files = sorted([f for f in os.listdir(soundboard_dir) if f.endswith(('.mp3', '.m4a', '.wav', '.ogg', '.flac'))])
    print(f"Loaded soundboard files: {soundboard_files}")

def add_soundboard_file(file_path):
    """Add an audio file to the soundboard."""
    if not os.path.isfile(file_path) or not file_path.endswith(('.mp3', '.m4a', '.wav', '.ogg', '.flac')):
        print(f"Error: {file_path} is not a valid audio file (.mp3, .m4a, .wav, .ogg, .flac).")
        sys.exit(1)
    dest_path = os.path.join(soundboard_dir, os.path.basename(file_path))
    try:
        shutil.copy(file_path, dest_path)
        print(f"Added {file_path} to soundboard as {dest_path}")
    except Exception as e:
        print(f"Error adding file: {e}")
        sys.exit(1)

def play_soundboard(file_name):
    """Play soundboard file."""
    global soundboard_playing
    file_path = os.path.join(soundboard_dir, file_name)
    try:
        data, fs = sf.read(file_path)
        if fs != samplerate:
            data = librosa.resample(data.T, orig_sr=fs, target_sr=samplerate).T
        if data.ndim > 1:
            data = data[:, 0]  # Convert to mono
        with soundboard_lock:
            soundboard_playing = data.astype(dtype)
    except Exception as e:
        print(f"Error playing {file_path}: {e}")

def audio_callback(indata, outdata, frames, time, status):
    global pitch_shift_steps
    if status:
        print(status)
    
    # Extract mono audio from mic
    audio = indata[:, 0].flatten()
    
    # Apply high-pass filter to remove low-frequency noise
    sos = signal.butter(4, 80 / (samplerate / 2), btype='high', output='sos')
    audio = signal.sosfilt(sos, audio)
    
    # Pitch shift for deeper voice
    shifted = librosa.effects.pitch_shift(audio, sr=samplerate, n_steps=pitch_shift_steps)
    
    # Compression for professional sound
    shifted = shifted / np.max(np.abs(shifted)) if np.max(np.abs(shifted)) > 0 else shifted
    compressor_gain = 0.5
    shifted = np.sign(shifted) * (np.abs(shifted) ** compressor_gain)
    
    # Noise gate
    shifted[np.abs(shifted) < noise_gate_threshold] = 0
    
    # Mix with soundboard audio if playing
    with soundboard_lock:
        if soundboard_playing is not None:
            mix_len = min(frames, len(soundboard_playing))
            shifted[:mix_len] += soundboard_playing[:mix_len]
            soundboard_playing = soundboard_playing[mix_len:]
            if len(soundboard_playing) == 0:
                soundboard_playing = None
    
    # Output processed audio
    outdata[:, 0] = shifted.reshape(-1, 1)
    if channels > 1:
        outdata[:, 1:] = outdata[:, 0]  # Duplicate for stereo

def start_audio_stream():
    """Start the audio stream in a thread."""
    global stream
    try:
        stream = sd.Stream(samplerate=samplerate,
                           blocksize=blocksize,
                           dtype=dtype,
                           channels=channels,
                           callback=audio_callback)
        stream.start()
        print("Audio stream started.")
    except Exception as e:
        print(f"Error starting audio stream: {e}")
        sys.exit(1)

def stop_audio_stream():
    """Stop the audio stream."""
    global stream
    if stream:
        stream.stop()
        stream.close()
        print("Audio stream stopped.")

def create_gui():
    """Create GUI menu for soundboard and pitch control."""
    root = tk.Tk()
    root.title("Voice Changer Soundboard")
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_audio_stream(), root.destroy()))

    # Pitch slider
    pitch_frame = ttk.Frame(root)
    pitch_frame.pack(pady=10)
    ttk.Label(pitch_frame, text="Pitch Shift (Semitones):").pack(side=tk.LEFT)
    pitch_var = tk.IntVar(value=pitch_shift_steps)
    pitch_scale = ttk.Scale(pitch_frame, from_=-12, to=0, orient=tk.HORIZONTAL, variable=pitch_var, command=lambda v: update_pitch(int(float(v))))
    pitch_scale.pack(side=tk.LEFT, padx=10)

    # Soundboard buttons
    sound_frame = ttk.Frame(root)
    sound_frame.pack(pady=10)
    for file in soundboard_files:
        btn = ttk.Button(sound_frame, text=file, command=lambda f=file: play_soundboard(f))
        btn.pack(fill=tk.X, pady=2)

    # Refresh button to reload sounds
    refresh_btn = ttk.Button(root, text="Refresh Soundboard", command=refresh_soundboard)
    refresh_btn.pack(pady=10)

    # Stop button
    stop_btn = ttk.Button(root, text="Stop", command=lambda: (stop_audio_stream(), root.destroy()))
    stop_btn.pack(pady=10)

    root.mainloop()

def update_pitch(value):
    """Update pitch shift value."""
    global pitch_shift_steps
    pitch_shift_steps = value
    print(f"Pitch updated to {value} semitones.")

def refresh_soundboard():
    """Reload soundboard files."""
    setup_soundboard()
    messagebox.showinfo("Refresh", "Soundboard refreshed. Restart the app to see changes in GUI.")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Voice changer with GUI soundboard")
    parser.add_argument('command', nargs='?', default='run', help="'add' to add sound file, or omit to run")
    parser.add_argument('file', nargs='?', help="Path to audio file for 'add' command")
    args = parser.parse_args()

    # Handle 'add' command
    if args.command == 'add':
        if not args.file:
            print("Error: Please provide a file path (e.g., voice add example.mp3)")
            sys.exit(1)
        add_soundboard_file(args.file)
        sys.exit(0)

    # Install dependencies
    check_and_install_dependencies()

    # Set up soundboard
    setup_soundboard()

    # Start audio stream in background
    threading.Thread(target=start_audio_stream, daemon=True).start()

    # Start GUI
    create_gui()

if __name__ == "__main__":
    # Create alias for 'voice' command
    if os.path.basename(sys.argv[0]) == 'voice':
        main()
    else:
        # Set up alias if running as voice_changer.py
        alias_cmd = 'alias voice="python3 ' + os.path.abspath(__file__) + '"'
        print("Setting up 'voice' command alias. Add to ~/.bashrc for persistence:")
        print(alias_cmd)
        main()