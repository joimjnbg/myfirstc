import tkinter as tk
from tkinter import ttk, filedialog
# Need to import pygame directly for pygame.mixer.music.get_busy()
import pygame 
from music_player import Player 
import os

class MusicPlayerApp:
    def __init__(self, root):
        """
        Initializes the Music Player GUI application.
        """
        self.root = root
        self.root.title("Music Player")
        self.is_closing = False # Flag to manage closing state for polling

        # Initialize ttk.Style. This will be used for custom styles or if themes are unavailable.
        self.style = ttk.Style(self.root)

        # If not using ThemedTk (i.e., in fallback), self.root.configure might be needed.
        # However, the theme (arc or clam) should handle background.
        # self.root.configure(bg='#f0f0f0') # Removed: Let theme handle background

        self.root.minsize(380, 240) 

        # Style configurations - these will apply on top of the theme or if no theme is active.
        # Prioritize letting the theme define the look. Customizations should be minimal.

        # For TButton, let's rely on the theme's default first.
        # If needed, we can add specific styling like padding or font later.
        # self.style.configure('TButton', padding=5, font=('TkDefaultFont', 10)) # Commented out to test theme's default

        # SongTitle.TLabel: Font and padding are good for emphasis. Ensure no background for theme transparency.
        self.style.configure('SongTitle.TLabel', font=("TkDefaultFont", 11, "bold"), padding=(5, 5, 5, 10))
        
        # TLabel: Basic font styling. Ensure no background.
        self.style.configure('TLabel', font=('TkDefaultFont', 10))
        
        # TScale: Attempt to style if the theme's default is not distinct enough.
        # These values are examples; they might need adjustment or removal if 'arc' styles it well.
        self.style.configure('Horizontal.TScale', 
                             # background='#d3d3d3', # Theme should handle background
                             # troughcolor='#c0c0c0', # Theme should handle trough
                             sliderrelief='flat', 
                             borderwidth=0)
        # Note: If 'arc' theme styles TScale well, the above 'Horizontal.TScale' config might be removed or simplified.
        # For now, keeping sliderrelief and borderwidth as they are less likely to clash with color schemes.

        # Initialize the Player backend
        try:
            self.player = Player()
        except Exception as e:
            print(f"Error initializing Player: {e}")
            self.player = None # Ensure player is None if init fails

        self._create_widgets()
        if self.player: # Start polling only if player was initialized
            self.root.after(250, self._update_status) # Start periodic status check

    def _create_widgets(self):
        """
        Creates and lays out the GUI widgets.
        """
        # Main content frame for better padding control around all elements
        main_frame = ttk.Frame(self.root, style='TFrame', padding=(10, 10, 10, 10))
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Song Display Area ---
        self.song_label = ttk.Label(main_frame, text="No song loaded.", anchor=tk.W, style='SongTitle.TLabel')
        self.song_label.pack(fill=tk.X, pady=10) # Consistent padding above and below

        # --- Control Buttons Frame ---
        self.controls_frame = ttk.Frame(main_frame, style='TFrame')
        self.controls_frame.pack(pady=10)

        self.load_button = ttk.Button(self.controls_frame, text="📂 Load Song", command=self._load_song_ui, style='TButton')
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Consolidated Play/Pause Button
        self.play_pause_button = ttk.Button(self.controls_frame, text="▶ Play", command=self._toggle_play_pause_ui, style='TButton')
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.controls_frame, text="⏹ Stop", command=self._stop_music_ui, style='TButton')
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Initially disable Play/Pause and Stop buttons
        self.play_pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

        # --- Volume Control Frame ---
        self.volume_frame = ttk.Frame(main_frame, style='TFrame')
        self.volume_frame.pack(pady=10, fill=tk.X)
        
        self.volume_label = ttk.Label(self.volume_frame, text="Volume:", style='TLabel')
        self.volume_label.pack(side=tk.LEFT, padx=(0,5)) # Padding only on right

        self.volume_slider = ttk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self._set_volume_ui)
        
        initial_volume_percent = 50.0
        if hasattr(self, 'player') and self.player: # Check if player exists and initialized
             try:
                 # Access pygame.mixer.music directly as Player class doesn't have get_volume method
                 initial_volume_percent = pygame.mixer.music.get_volume() * 100
             except Exception: 
                 initial_volume_percent = 50.0 # Default if pygame not fully ready
        
        self.volume_slider.set(initial_volume_percent) 
        self.volume_slider.pack(side=tk.LEFT, expand=True, fill=tk.X)

    # --- Event Handler Methods for UI Logic ---

    def _load_song_ui(self):
        """Handles the Load Song button click, updates GUI."""
        if not self.player: return # Do nothing if player failed to initialize
        filepath = filedialog.askopenfilename(
            title="Select MP3 File",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filepath:
            track_name = self.player.play_music(filepath) # This also starts playing
            if track_name:
                self._update_gui_for_playing()
            else:
                self.song_label.config(text="Error loading song.")
                self._update_gui_for_stopped() 

    def _toggle_play_pause_ui(self):
        """Handles the Play/Pause button click event."""
        if not self.player : return
        
        if not self.player.current_track: 
            # This case should ideally not happen if Play/Pause button is disabled
            # when no track is loaded. But as a fallback or for first load via play:
            self._load_song_ui() 
            return

        if self.player.is_playing: # If playing, then action is to pause
            self.player.pause_music()
            self._update_gui_for_paused()
        elif self.player.is_paused: # If paused, action is to resume
            self.player.unpause_music()
            self._update_gui_for_playing()
        else: # Was stopped (or no track loaded, though covered above)
            if self.player.current_track: 
                self.player.play_music(self.player.current_track) 
                self._update_gui_for_playing()

    def _stop_music_ui(self):
        """Handles the Stop button click, updates GUI."""
        if not self.player: return
        self.player.stop_music()
        self._update_gui_for_stopped()

    def _set_volume_ui(self, event=None): 
        """Handles the Volume slider move event, updates player volume."""
        if not self.player: return
        volume_percent = self.volume_slider.get()
        volume_float = volume_percent / 100.0
        self.player.set_volume(volume_float)

    # --- GUI Update Helper Methods ---
    def _update_gui_for_playing(self):
        if not self.player: return
        self.song_label.config(text=f"Playing: {self.player.get_current_track_display_name()}")
        self.play_pause_button.config(text="⏸ Pause", state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def _update_gui_for_paused(self):
        if not self.player: return
        self.song_label.config(text=f"Paused: {self.player.get_current_track_display_name()}")
        self.play_pause_button.config(text="▶ Play", state=tk.NORMAL)
        # Stop button remains normal

    def _update_gui_for_stopped(self, song_ended_naturally=False):
        if not self.player: 
            self.song_label.config(text="Player not available.")
            self.play_pause_button.config(text="Play", state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            return

        current_track_name = self.player.get_current_track_display_name()
        if song_ended_naturally: # current_track should still be set by player logic
            self.song_label.config(text=f"Finished: {current_track_name}")
        elif not self.player.current_track: # No song loaded or explicitly stopped and cleared
             self.song_label.config(text="No song loaded.")
        else: # Stopped by user, track remains
            self.song_label.config(text=f"Stopped: {current_track_name}")

        self.play_pause_button.config(text="▶ Play", state=tk.NORMAL if self.player.current_track else tk.DISABLED)
        # Stop button should be enabled if a track is loaded (even if stopped), disabled if no track ever loaded
        self.stop_button.config(state=tk.NORMAL if self.player.current_track else tk.DISABLED)


    # --- Periodic Status Check ---
    def _update_status(self):
        """Periodically checks music status and updates GUI."""
        if self.is_closing or not self.player: 
            return

        # Check if a song is loaded and was playing but is no longer busy (i.e., finished)
        # Player's is_playing state should be the source of truth for "was it intentionally started?"
        # pygame.mixer.music.get_busy() is the source of truth for "is sound currently outputting?"
        if self.player.current_track and self.player.is_playing and not pygame.mixer.music.get_busy():
            # print("GUI: Song finished naturally detected by polling.") # Debug
            self.player.is_playing = False # Update internal player state as it's no longer outputting sound
            # self.player.is_paused = False # Ensure consistent state, though should be false if it was playing
            self._update_gui_for_stopped(song_ended_naturally=True)
        
        # Reschedule the check
        self.root.after(250, self._update_status) 

    def on_closing(self):
        """
        Handles the application closing event.
        Ensures Pygame is shut down properly and stops status updates.
        """
        print("GUI: Closing application...") 
        self.is_closing = True # Signal to stop periodic updates
        
        if hasattr(self, 'player') and self.player:
            try:
                self.player.shutdown() 
                print("GUI: Player shutdown successful.") 
            except Exception as e:
                print(f"GUI: Error during player shutdown: {e}") 
        
        self.root.destroy() 

if __name__ == "__main__":
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")
        # root.set_theme_advanced("arc", True, True) # Optional: For themes supporting advanced settings
        print("Using 'arc' theme from ttkthemes.")
    except (ImportError, tk.TclError) as e:
        print(f"Failed to use ttkthemes 'arc' (Error: {e}). Falling back to default ttk theme.")
        # Ensure tk is imported if ThemedTk failed, though it should be at the top
        if 'tk' not in globals():
             import tkinter as tk # Should already be imported at the top
        if 'ttk' not in globals():
            from tkinter import ttk # Should already be imported at the top

        root = tk.Tk()
        style = ttk.Style(root)
        try:
            style.theme_use('clam') 
            print("Using 'clam' ttk theme as fallback.")
        except tk.TclError:
            print("Fallback theme 'clam' also not available. Using system default ttk theme.")
            # System default ttk theme will be used if 'clam' also fails

    app = MusicPlayerApp(root)
    # is_closing flag is set in app's __init__
    # _update_status is started in __init__ if player is available
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()
