# 🎙️ Voice God Voice Changer Tutorial for Linux 🎵
**Supported Distributions**: Ubuntu, Kali, Debian, Arch Linux, and other Debian-based or Arch-based systems with compatible package managers (`apt-get` or `pacman`).

Welcome to the **Voice God Voice Changer** tutorial, the *first Linux voice changer with an integrated soundboard*! This epic tool transforms your microphone input into a deep, booming voice that sounds like it’s coming through a $1000 mic 🎤. It also includes a Voicemod-style GUI soundboard to play sound effects (`.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`) with a click. This guide covers manual installation, adding sounds, and running the app with flair and emojis to keep it 🔥. Let’s make you sound like a vocal deity! 😎

---

## 📋 What is Voice God Voice Changer? 🌟
- **Purpose**: The pioneering Linux voice changer that deepens your voice in real-time and lets you trigger sound effects via a sleek GUI, perfect for gaming, streaming, or just having fun.
- **Features**:
  - 🎚️ **Real-time Voice Deepening**: Adjustable pitch slider (0 to -12 semitones) for a godly bass tone.
  - 🎶 **Soundboard**: Play `.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac` files with a click, mixed with your voice—first of its kind on Linux!
  - 🛠️ **Auto/Manual Setup**: Supports Ubuntu, Kali, Debian, or Arch with dependency installation.
  - 🎙️ **Pro Mic Quality**: Enhances audio with compression and noise gating for a studio-grade sound.
- **Requirements**: Linux, microphone, speakers, Python 3, and internet (for installs).

---

## 🚀 Step-by-Step Tutorial

### 1. Save the Script 📝
- Copy the Python script from the previous response into a file named `voice_god.py`.
- Make it executable:
  ```bash
  chmod +x voice_god.py
  ```
  ✅ This lets you run the script like a boss.

### 2. Set Up the `voice` Command Alias ⚡
- Run the script once to get the alias command:
  ```bash
  ./voice_god.py
  ```
- It’ll display something like:
  ```
  Setting up 'voice' command alias. Add to ~/.bashrc for persistence:
  alias voice="python3 /path/to/voice_god.py"
  ```
- Add the alias to your shell configuration for easy access:
  ```bash
  echo 'alias voice="python3 /path/to/voice_god.py"' >> ~/.bashrc
  source ~/.bashrc
  ```
  - **For Zsh users** (e.g., Kali’s default shell):
    ```bash
    echo 'alias voice="python3 /path/to/voice_god.py"' >> ~/.zshrc
    source ~/.zshrc
    ```
  - Now you can use `voice` or `voice add <file>` commands anywhere! 🎉

### 3. Install Dependencies Manually 🛠️
The script attempts to auto-install dependencies, but if it fails or you prefer manual control, here’s how to set up everything for **Voice God Voice Changer**.

#### For Ubuntu, Kali, or Debian-based Distros 🐧
1. **Update Package Lists**:
   ```bash
   sudo apt-get update
   ```
   🔄 Ensures you have the latest package info.
2. **Install System Dependencies**:
   - `libportaudio2`, `portaudio19-dev`: Handles audio input/output.
   - `libsndfile1-dev`: Reads audio files for the soundboard.
   - `python3-tk`: Powers the GUI for the soundboard and pitch slider.
   ```bash
   sudo apt-get install -y libportaudio2 portaudio19-dev libsndfile1-dev python3-tk
   ```
3. **Install Python Dependencies**:
   - These libraries handle audio processing and GUI functionality.
   ```bash
   pip3 install sounddevice numpy scipy librosa soundfile
   ```
   💡 Run as `sudo pip3 install ...` if permission issues arise.

#### For Arch Linux 🏹
1. **Update Package Lists**:
   ```bash
   sudo pacman -Syu
   ```
   🔄 Keeps your system fresh.
2. **Install System Dependencies**:
   - `portaudio`: For audio input/output.
   - `libsndfile`: For soundboard file handling.
   - `tk`: For the GUI.
   ```bash
   sudo pacman -S --noconfirm portaudio libsndfile tk
   ```
3. **Install Python Dependencies**:
   ```bash
   pip3 install sounddevice numpy scipy librosa soundfile
   ```
   💡 Use `sudo` if needed: `sudo pip3 install ...`.

#### Troubleshooting Dependency Issues ⚠️
- **Permission Denied**: Run commands with `sudo` or check file permissions.
- **Pip Errors**: Ensure `pip3` is installed:
  ```bash
  sudo apt-get install python3-pip  # Ubuntu/Kali/Debian
  sudo pacman -S python-pip  # Arch
  ```
- **Missing Tkinter**: If the GUI fails, verify `python3-tk` (Ubuntu) or `tk` (Arch) is installed.
- **Audio Issues**: Check your mic/speakers with `pavucontrol` or `alsamixer`.

### 4. Add Sounds to the Soundboard 🎶
- The soundboard lives in `~/.voice_god_soundboard/` (created automatically).
- Add audio files (`.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`) with the `voice add` command:
  ```bash
  voice add /path/to/example.mp3
  ```
  - Example: If you have a file `epic_laugh.mp3` in `~/Downloads`, run:
    ```bash
    voice add ~/Downloads/epic_laugh.mp3
    ```
  - The file is copied to `~/.voice_god_soundboard/epic_laugh.mp3`.
  - **Note**: If you get a permission error, try:
    ```bash
    sudo voice add /path/to/example.mp3
    ```
  - Supported formats: `.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`. Other formats may not work.
- **Verify**: Check the soundboard directory:
  ```bash
  ls ~/.voice_god_soundboard/
  ```
  ✅ Files appear as buttons in the GUI when you run the app.

### 5. Run Voice God Voice Changer 🎙️
- Start the app:
  ```bash
  ./voice_god.py
  ```
  or
  ```bash
  voice
  ```
  - If you encounter permission errors for audio or the soundboard directory, try:
    ```bash
    sudo ./voice_god.py
    ```
- **What Happens**:
  - A GUI window opens with:
    - 🎚️ **Pitch Slider**: Adjust from 0 (normal voice) to -12 (super deep, god-like bass). Default is -7 for a powerful tone.
    - 🎶 **Sound Buttons**: Each file in `~/.voice_god_soundboard/` gets a button. Click to play, and it mixes with your voice.
    - 🔄 **Refresh Button**: Reloads soundboard files (restart the app to update buttons).
    - 🛑 **Stop Button**: Stops the audio stream and closes the app.
  - Speak into your microphone, and your deepened voice plays through your speakers. Click sound buttons to trigger effects! 😎
- **Stop**: Click the “Stop” button or close the GUI window.

### 6. Customize Your Godly Voice 🎨
- **Adjust Pitch**:
  - Slide the pitch control to change voice depth in real-time.
  - `-12` = ultra-deep (think Zeus or Darth Vader). `0` = no change (normal voice).
- **Add More Sounds**:
  - Keep adding files with `voice add`. Restart the app to see new buttons in the GUI.
  - Example: Add a dramatic thunder effect:
    ```bash
    voice add ~/Downloads/thunder.wav
    ```
  - Find cool sounds on [Freesound.org](https://freesound.org) or record your own! 🎵
- **Tweak Audio Settings**:
  - Edit `voice_god.py` to adjust:
    - `blocksize`: Set to 1024 for lower latency or 4096 for better quality (higher latency).
    - `pitch_shift_steps`: Default pitch (-7). Change for a different starting depth.
- **Pro Tip**: Test with friends on Discord or Zoom to show off your godly voice and soundboard effects! 🗣️

### 7. Troubleshooting 😵
- **No GUI?** Ensure `python3-tk` (Ubuntu/Kali/Debian) or `tk` (Arch) is installed.
- **No Sound?**:
  - Verify mic/speakers with `pavucontrol` (GUI) or `alsamixer` (terminal).
  - Ensure `pulseaudio` or `alsa` is running:
    ```bash
    pulseaudio --start
    ```
- **Soundboard Empty?** Check files in `~/.voice_god_soundboard/` and restart the app.
- **Permission Issues?** Fix directory permissions or use `sudo`:
  ```bash
  sudo chown $USER:$USER ~/.voice_god_soundboard
  ```
- **Dependency Errors?** Re-run manual install commands or check error messages.
- **Laggy Audio?** Adjust `blocksize` in the script or check CPU usage.
- **GUI Cluttered?** Too many sound files? Delete unused ones from `~/.voice_god_soundboard/`:
  ```bash
  rm ~/.voice_god_soundboard/unwanted_file.mp3
  ```

---

## 🎉 Final Notes
You’re now ready to unleash the **Voice God Voice Changer**, the first Linux voice changer with a soundboard! Transform your voice into a deep, commanding tone and spice up your streams or calls with epic sound effects. 🌩️ If you want more features (e.g., scrollable GUI, custom effects, or keybinds), let me know, and I’ll make it even more godly! 😇

**Have fun sounding like a legend!** 🎤🚀
