# Python CLI and GUI Music Player

## Description

This project is a simple music player application built with Python. It supports playback of MP3 audio files and offers both a command-line interface (CLI) and a graphical user interface (GUI) built with Tkinter.

## Features

*   Plays MP3 audio files.
*   Command-Line Interface (CLI) for playback control.
*   Graphical User Interface (GUI) using Tkinter for a visual experience.
*   Core playback controls:
    *   Play
    *   Pause
    *   Resume (Unpause)
    *   Stop
*   Volume adjustment.
*   Display of current song title and playback status.
*   Dynamic GUI updates reflecting player state (e.g., Play/Pause button text, song information).

## Requirements

*   Python 3.x
*   Pygame library (`pygame`)

## Setup/Installation

1.  Ensure you have Python 3 installed on your system.
2.  Install the Pygame library using pip:
    ```bash
    pip install pygame
    ```

## How to Run

### CLI Version

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

### GUI Version

Navigate to the project directory in your terminal and run:

```bash
python gui_player_app.py
```

This will launch the Tkinter-based graphical interface. Use the buttons to load and control music playback.

## Project Structure

*   `music_player.py`: Contains the core `Player` class (handling playback logic, state management) and the command-line interface (CLI).
*   `gui_player_app.py`: Implements the Tkinter-based GUI application, utilizing the `Player` class from `music_player.py`.
*   `test_music_player.py`: Contains unit tests for the `Player` class and CLI functionalities.
*   `README.md`: This file, providing information about the project.

## License

No license provided.
