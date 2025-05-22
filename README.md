# Python Music Player (Desktop and Android)

## Description

This project is a versatile music player application built with Python. It supports playback of MP3 audio files and offers multiple user interfaces:
1.  A command-line interface (CLI) for terminal-based control.
2.  A desktop graphical user interface (GUI) built with Tkinter.
3.  An Android graphical user interface (GUI) developed with Kivy, allowing for mobile usage.

The core playback logic is shared across all versions, ensuring consistent behavior.

## Features

*   Plays MP3 audio files.
*   Shared core playback logic (`Player` class).
*   Core playback controls: Play, Pause, Resume (Unpause), Stop.
*   Volume adjustment.
*   Display of current song title and playback status.

**CLI & Tkinter Desktop Specific Features:**
*   Command-Line Interface (CLI) for detailed playback control.
*   Tkinter-based GUI for a traditional desktop experience.
*   Dynamic GUI updates reflecting player state (e.g., Play/Pause button text, song information) in Tkinter.
*   Enhanced Tkinter GUI styling using the 'arc' theme from `ttkthemes` (with fallback).

**Kivy Android Specific Features:**
*   Mobile-friendly GUI designed for Android using the Kivy framework.
*   Dynamic GUI updates reflecting player state (song title, Play/Pause button text).
*   Android permission handling (READ_MEDIA_AUDIO) for accessing audio files.
*   Manual file path input via a `TextInput` field for song selection on Android.
*   Placeholder for album art display.

## Desktop Version (Tkinter & CLI)

### Requirements
*   Python 3.x (on your development/execution machine)
*   Pygame library (`pygame`)
*   ttkthemes library (`ttkthemes`) (for enhanced Tkinter GUI styling)

### Setup/Installation
1.  Ensure you have Python 3 installed on your system.
2.  Install the required Python libraries for the desktop versions using pip:
    ```bash
    pip install pygame ttkthemes
    ```

### How to Run

#### CLI Version
Navigate to the project directory in your terminal and run:
```bash
python music_player.py
```
**Available CLI Commands:**
*   `play <filepath.mp3>`: Loads and plays the specified MP3 file.
*   `play`: (If a song is loaded but stopped/paused) Resumes playback of the current track.
*   `pause`: Pauses the currently playing music.
*   `resume`: Resumes paused music.
*   `stop`: Stops the music.
*   `volume_up` or `vol_up`: Increases volume by 10%.
*   `volume_down` or `vol_down`: Decreases volume by 10%.
*   `set_volume <level>` or `vol <level>`: Sets volume to a specific level (0.0 to 1.0). Example: `set_volume 0.7`.
*   `status`: Displays the current playback status, track, and volume.
*   `quit` or `exit`: Exits the CLI player.

#### Desktop GUI Version (Tkinter)
Navigate to the project directory in your terminal and run:
```bash
python gui_player_app.py
```
This will launch the Tkinter-based graphical interface, which attempts to use the 'arc' theme from `ttkthemes` for an improved visual experience (or falls back to a default theme if 'arc' is unavailable). Use the buttons to load and control music playback.

## Android Version (Kivy)

### Overview
This version uses the Kivy framework to create an installable Android application, providing a touch-friendly interface for music playback.

### Specific Requirements for Android Version
*   Python 3.x (on your development machine for Kivy and Buildozer)
*   Kivy library (`kivy`)
*   Plyer library (`plyer`) (for Android permission handling)
*   Buildozer (`buildozer`) (for packaging the Android APK)
*   Pygame library (`pygame`) (as a dependency for the core `Player` logic)
*   Android SDK and NDK (typically managed by Buildozer during the build process)

### Setup for Android Development
1.  Install Kivy, Plyer, and Buildozer on your development machine:
    ```bash
    pip install kivy plyer buildozer
    ```
2.  **Buildozer Environment Setup:** For the first-time Buildozer setup (which includes downloading the Android SDK and NDK), Buildozer will typically handle this automatically when you run a build command. If you encounter issues, or for more detailed environment configuration (like specific NDK/SDK versions if needed), refer to the official Kivy and Buildozer documentation.

### Building the APK
1.  **Prepare Entry Point:** The `buildozer.spec` file is configured to look for `main.py` as the Kivy application entry point. In this project, the Kivy GUI is in `main_kivy.py`. Before building, either:
    *   Rename `main_kivy.py` to `main.py`.
    *   Or, copy `main_kivy.py` to `main.py`:
        ```bash
        cp main_kivy.py main.py
        ```
2.  **Run Buildozer:** Navigate to the project root directory (where `buildozer.spec` is located) in your terminal and run the build command. For a debug APK:
    ```bash
    buildozer android debug
    ```
3.  **Locate APK:** After a successful build, the APK file (e.g., `KivyMusicPlayer-0.1-arm64-v8a-debug.apk`) will be located in the `bin/` directory within your project.

### Running on Android Device/Emulator
1.  **Install APK:** Transfer the generated APK file to your Android device or emulator and install it. If using Android Debug Bridge (ADB):
    ```bash
    adb install bin/KivyMusicPlayer-0.1-arm64-v8a-debug.apk 
    ```
    (Replace the APK filename if it differs).
2.  **Launch App:** Find "KivyMusicPlayer" in your app drawer and launch it.
3.  **Permissions:** The app will request "READ_MEDIA_AUDIO" (or "READ_EXTERNAL_STORAGE" depending on Android version and `buildozer.spec` configuration) permission on first launch (on Android 6.0+). Grant this permission to allow the app to access audio files. If denied, the app may not be able to load songs.
4.  **Loading Songs:** Use the "Path:" `TextInput` field to enter the full path to an MP3 file on your Android device (e.g., `/sdcard/Music/your_song.mp3` or `/storage/emulated/0/Music/your_song.mp3`). Then press the "Load" button.

## Project Structure

*   `music_player.py`: Contains the core `Player` class (handling playback logic, state management) and the command-line interface (CLI).
*   `gui_player_app.py`: Implements the Tkinter-based GUI application for desktop use, utilizing the `Player` class.
*   `main_kivy.py`: Implements the Kivy-based GUI application, primarily intended for Android (should be copied/renamed to `main.py` for Buildozer).
*   `test_music_player.py`: Contains unit tests for the `Player` class and CLI functionalities.
*   `buildozer.spec`: Configuration file for Buildozer, used to package the Kivy application for Android.
*   `README.md`: This file, providing information about the project.
*   `test.mp3`: A dummy MP3 file included for quick testing of file loading functionality.

## License

No license provided.
