# This script implements a simple music player using Pygame.

import pygame

def play_music(filepath):
    """Plays the music file at the given filepath."""
    if not filepath.lower().endswith(".mp3"):
        print("Error: Only .mp3 files are currently supported.")
        return

    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        print(f"Now playing: {filepath}")
    except pygame.error as e:
        print(f"Error playing music: {e}")
        print("Please check the file path and ensure it's a valid MP3 file.")

def pause_music():
    """Pauses the currently playing music."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        print("Music paused.")
    else:
        print("No music is currently playing to pause.")

def unpause_music():
    """Unpauses the currently paused music."""
    # pygame.mixer.music.unpause() only works if music is paused.
    # It doesn't have a direct way to check if it's "paused" vs "stopped" or "not playing".
    # get_busy() returns True if playing or paused.
    # For simplicity, we'll allow unpause even if it was already playing,
    # though it might be better to check if it was specifically paused.
    # Pygame's unpause doesn't error if called when not paused but playing.
    if pygame.mixer.music.get_busy(): # True if playing or paused
        pygame.mixer.music.unpause()
        print("Music resumed/unpaused.") # Message adjusted for broader case
    else:
        print("No music is currently active to unpause/resume.")


def stop_music():
    """Stops the currently playing music."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("Music stopped.")
    else:
        print("No music is currently playing to stop.")

def set_volume(volume):
    """Sets the volume of the music player.
    Volume should be a float between 0.0 and 1.0.
    """
    if 0.0 <= volume <= 1.0:
        pygame.mixer.music.set_volume(volume)
        print(f"Volume set to: {volume}")
    else:
        print("Error: Volume must be between 0.0 and 1.0.")

def volume_up():
    """Increases the volume by 0.1."""
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(current_volume + 0.1, 1.0)
    pygame.mixer.music.set_volume(new_volume)
    print(f"Volume increased to: {new_volume:.1f}")

def volume_down():
    """Decreases the volume by 0.1."""
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(current_volume - 0.1, 0.0)
    pygame.mixer.music.set_volume(new_volume)
    print(f"Volume decreased to: {new_volume:.1f}")

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    print("Music Player CLI. Type 'quit' to exit.")
    # Set a default volume
    set_volume(0.5)

    while True:
        command_input = input("Enter command: ").strip().lower().split()
        if not command_input:
            continue

        command = command_input[0]

        if command == "play":
            if len(command_input) > 1:
                filepath = command_input[1]
                # In a real scenario, you'd want to check if the file exists
                play_music(filepath)
            else:
                print("Usage: play <filepath.mp3>")
        elif command == "pause":
            pause_music()
        elif command == "resume": # Changed from unpause to resume for CLI consistency
            unpause_music()
        elif command == "stop":
            stop_music()
        elif command == "volume_up":
            volume_up()
        elif command == "volume_down":
            volume_down()
        elif command == "set_volume":
            if len(command_input) > 1:
                try:
                    volume_level = float(command_input[1])
                    set_volume(volume_level)
                except ValueError:
                    print("Volume level must be a number.")
            else:
                print("Usage: set_volume <level>")
        elif command == "quit":
            print("Exiting music player.")
            stop_music() # Stop music before quitting
            break
        else:
            print(f"Unknown command: {command}")

        # Minimal event pumping, mainly for internal Pygame processing if needed
        # and to allow pygame.QUIT if a window was ever created (not in this CLI version)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Should not be triggered in pure CLI
                print("Pygame quit event received.") # For debugging
                running = False # This would be relevant if we had a mixed mode
                break
        if not command_input or command_input[0] == "quit": # ensure break from outer loop
             if command_input and command_input[0] == "quit": break

    pygame.quit()

def run_cli():
    """Initializes Pygame and runs the command-line interface for the music player."""
    pygame.init()
    pygame.mixer.init()

    print("Music Player CLI. Type 'quit' to exit.")
    # Set a default volume
    set_volume(0.5)

    while True:
        command_input = input("Enter command: ").strip().lower().split()
        if not command_input:
            continue

        command = command_input[0]

        if command == "play":
            if len(command_input) > 1:
                filepath = command_input[1]
                play_music(filepath)
            else:
                print("Usage: play <filepath.mp3>")
        elif command == "pause":
            pause_music()
        elif command == "resume":
            unpause_music()
        elif command == "stop":
            stop_music()
        elif command == "volume_up":
            volume_up()
        elif command == "volume_down":
            volume_down()
        elif command == "set_volume":
            if len(command_input) > 1:
                try:
                    volume_level = float(command_input[1])
                    set_volume(volume_level)
                except ValueError:
                    print("Volume level must be a number.")
            else:
                print("Usage: set_volume <level>")
        elif command == "quit":
            print("Exiting music player.")
            stop_music() # Stop music before quitting
            break
        else:
            print(f"Unknown command: {command}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Pygame quit event received.")
                # In a pure CLI, this break might not be strictly necessary
                # if the input loop's 'quit' is the primary exit mechanism.
                # However, good to have if a window context could appear.
                if command != "quit": # Avoid breaking twice if 'quit' was already issued
                    break
        if command == "quit": # Ensure outer loop breaks if inner loop broke due to quit event
            break
            
    pygame.quit()

if __name__ == "__main__":
    run_cli()
