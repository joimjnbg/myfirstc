# This script implements a simple music player using Pygame.

import pygame
import os # For basename in get_current_track_display_name

class Player:
    def __init__(self):
        """Initializes the music player, Pygame, and Pygame mixer."""
        pygame.init()
        pygame.mixer.init()
        self.current_track = None
        self.is_playing = False # True if music is actively playing
        self.is_paused = False  # True if music is paused
        pygame.mixer.music.set_volume(0.5) # Default volume
        # print("Player initialized, volume set to 0.5") # CLI feedback

    def shutdown(self):
        """Shuts down Pygame."""
        # print("Shutting down player.") # CLI feedback
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop() # Stop music before quitting
        pygame.quit()

    def play_music(self, filepath):
        """Plays the music file at the given filepath.
        Returns the display name of the track on success, None on failure.
        """
        if not filepath.lower().endswith(".mp3"):
            print("Error: Only .mp3 files are currently supported.") # CLI feedback
            return None

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.current_track = filepath
            self.is_playing = True
            self.is_paused = False
            display_name = self.get_current_track_display_name()
            print(f"Now playing: {display_name}") # CLI feedback
            return display_name
        except pygame.error as e:
            print(f"Error playing music: {e}") # CLI feedback
            print("Please check the file path and ensure it's a valid MP3 file.") # CLI feedback
            self.current_track = None
            self.is_playing = False
            self.is_paused = False
            return None

    def pause_music(self):
        """Pauses the currently playing music."""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            # self.is_playing remains true as per typical player logic (music is loaded and 'active')
            # or set self.is_playing = False if it means "sound is currently coming out"
            # For this implementation, let's use is_playing for "sound is coming out"
            self.is_playing = False 
            print("Music paused.") # CLI feedback
        elif self.is_paused:
            print("Music is already paused.") # CLI feedback
        else: # Not playing and not paused (i.e., stopped)
            print("No music is currently playing to pause.") # CLI feedback

    def unpause_music(self): # Or resume_music
        """Resumes the currently paused music."""
        if self.is_paused: # Only unpause if currently paused
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.is_paused = False
            print("Music resumed.") # CLI feedback
        elif self.is_playing:
             print("Music is already playing.") # CLI feedback
        else: # Stopped
            print("No music is currently paused to resume.") # CLI feedback


    def stop_music(self):
        """Stops the currently playing music."""
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            # Store track for CLI display, but it's effectively stopped
            # display_name = self.get_current_track_display_name()
            # print(f"Music stopped. Track '{display_name}' cleared from active playback.")
            print(f"Music stopped.") # CLI feedback
            # self.current_track = None # Keep current_track to allow "play" to resume it if desired by future CLI/GUI
        else:
            print("No music is currently playing to stop.") # CLI feedback


    def set_volume(self, volume_level):
        """Sets the volume of the music player.
        Volume should be a float between 0.0 and 1.0.
        """
        if not isinstance(volume_level, (int, float)):
            # This check is good, but CLI already does float conversion which might raise ValueError
            print("Error: Volume level must be a number.") # CLI feedback
            return

        if 0.0 <= volume_level <= 1.0:
            pygame.mixer.music.set_volume(volume_level)
            print(f"Volume set to: {volume_level:.1f}") # CLI feedback
        else:
            print("Error: Volume must be between 0.0 and 1.0.") # CLI feedback

    def volume_up(self):
        """Increases the volume by 0.1."""
        current_volume = pygame.mixer.music.get_volume()
        # Round to avoid floating point inaccuracies causing many decimal places
        new_volume = min(round(current_volume + 0.1, 1), 1.0)
        pygame.mixer.music.set_volume(new_volume)
        print(f"Volume increased to: {new_volume:.1f}") # CLI feedback

    def volume_down(self):
        """Decreases the volume by 0.1."""
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(round(current_volume - 0.1, 1), 0.0)
        pygame.mixer.music.set_volume(new_volume)
        print(f"Volume decreased to: {new_volume:.1f}") # CLI feedback

    def get_current_track_display_name(self):
        """Returns a user-friendly name of the current track or 'None'."""
        if self.current_track:
            return os.path.basename(self.current_track)
        return "None" # Return string "None" for display consistency

    def get_playback_status(self):
        """Returns the current playback status as a string."""
        if self.is_playing: # Sound is coming out
             return "Playing"
        elif self.is_paused: # Paused, but a track is loaded and ready to resume
            return "Paused"
        else: # No music loaded or explicitly stopped
            return "Stopped"


def run_cli():
    """Initializes Pygame and runs the command-line interface for the music player."""
    player = Player() # Create an instance of the Player

    # Initial feedback for CLI
    print("Player initialized. Music Player CLI. Type 'quit' to exit.")
    print(f"Initial volume: {pygame.mixer.music.get_volume():.1f}")


    while True:
        # Display current status in prompt
        status_str = player.get_playback_status()
        track_name_str = player.get_current_track_display_name()
        
        prompt_display = f"({status_str}"
        if status_str != "Stopped" or (status_str == "Stopped" and player.current_track is not None):
            prompt_display += f": {track_name_str}"
        prompt_display += f" | Vol: {pygame.mixer.music.get_volume():.1f})"
        
        command_input = input(f"Cmd {prompt_display} > ").strip().lower().split()
        
        if not command_input:
            continue

        command = command_input[0]

        if command == "play":
            if len(command_input) > 1:
                filepath = command_input[1]
                player.play_music(filepath)
            elif player.current_track and not player.is_playing: # Play current track if one exists and not playing
                print(f"Resuming track: {player.get_current_track_display_name()}")
                player.play_music(player.current_track) # Effectively unpauses or restarts stopped track
            else:
                print("Usage: play <filepath.mp3> or play (to resume current track if stopped/paused)")
        elif command == "pause":
            player.pause_music()
        elif command == "resume": 
            player.unpause_music()
        elif command == "stop":
            player.stop_music()
        elif command == "volume_up" or command == "vol_up":
            player.volume_up()
        elif command == "volume_down" or command == "vol_down":
            player.volume_down()
        elif command == "set_volume" or command == "vol":
            if len(command_input) > 1:
                try:
                    volume_level_str = command_input[1]
                    volume_level = float(volume_level_str)
                    player.set_volume(volume_level)
                except ValueError:
                    print("Volume level must be a number.")
            else:
                print("Usage: set_volume <level (0.0-1.0)>")
        elif command == "status": 
            print(f"Status: {player.get_playback_status()}, Track: {player.get_current_track_display_name()}, Volume: {pygame.mixer.music.get_volume():.1f}")
        elif command == "quit" or command == "exit":
            print("Exiting music player...")
            # player.stop_music() # stop_music is called in player.shutdown()
            break 
        else:
            print(f"Unknown command: '{command}'. Type 'quit' or 'exit' to close.")

        # Minimal event pumping for Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Pygame quit event received. Exiting...")
                command = "quit" # Force main loop to exit
                break
        if command == "quit":
            break
            
    player.shutdown()

if __name__ == "__main__":
    # This part is now clean, just calling run_cli.
    # The previous duplication of run_cli's content here is removed.
    run_cli()
