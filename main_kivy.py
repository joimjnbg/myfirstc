from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput # For file path input
from kivy.clock import Clock 
from music_player import Player 
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex, platform 
from kivy.metrics import dp
from plyer import permissions

class MusicPlayerLayout(BoxLayout):
    def __init__(self, player_instance, **kwargs):
        super().__init__(**kwargs)
        self.player = player_instance
        self.orientation = 'vertical'
        self.padding = dp(10) # Overall padding for the root layout
        self.spacing = dp(10) # Spacing between direct children of root layout

        # Define Colors
        self.COLOR_BACKGROUND = get_color_from_hex('#FFFFFF') # White
        self.COLOR_PRIMARY_ACCENT = get_color_from_hex('#2196F3') # Blue
        self.COLOR_TEXT_ON_ACCENT = get_color_from_hex('#FFFFFF') # White
        self.COLOR_TEXT_ON_BACKGROUND = get_color_from_hex('#333333') # Dark Grey
        self.COLOR_ALBUM_ART_PLACEHOLDER = get_color_from_hex('#EEEEEE') # Very Light Grey

        # Set Root Background Color
        with self.canvas.before:
            Color(*self.COLOR_BACKGROUND)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)


        # --- Song Label ---
        self.song_label = Label(
            text="No song loaded.",
            size_hint_y=None,
            height=dp(40),
            font_size=dp(18),
            color=self.COLOR_TEXT_ON_BACKGROUND,
            halign='center', 
            valign='middle'
        )
        self.song_label.bind(size=self.song_label.setter('text_size')) 
        self.add_widget(self.song_label)

        # --- File Path Input ---
        file_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48), spacing=dp(10), padding=(0,dp(5)))
        file_input_label = Label(text="Path:", size_hint_x=0.2, font_size=dp(15), color=self.COLOR_TEXT_ON_BACKGROUND)
        self.file_path_input = TextInput(
            text="test.mp3", # Default to local test.mp3 for easier desktop testing
            hint_text="Enter full path to MP3 file",
            size_hint_y=None,
            height=dp(40), # Adjusted height to fit within layout
            font_size=dp(15),
            multiline=False
        )
        file_input_layout.add_widget(file_input_label)
        file_input_layout.add_widget(self.file_path_input)
        self.add_widget(file_input_layout)

        # --- Album Art Placeholder ---
        # Reduced size_hint_y to accommodate the new TextInput field
        self.album_art_placeholder = Widget(size_hint_y=0.4) 
        with self.album_art_placeholder.canvas:
            Color(*self.COLOR_ALBUM_ART_PLACEHOLDER) 
            self.album_art_rect = Rectangle(
                pos=self.album_art_placeholder.pos,
                size=self.album_art_placeholder.size
            )
        self.album_art_placeholder.bind(pos=self._update_album_art_rect, size=self._update_album_art_rect)
        self.add_widget(self.album_art_placeholder)

        # --- Volume Control Sub-Layout ---
        volume_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48), # Keep height fixed
            spacing=dp(10) # Spacing between label and slider
        )
        volume_label_text = Label(
            text="Volume:",
            size_hint_x=None, # Let width be determined by text
            width=dp(70),     # Fixed width for "Volume:" label
            font_size=dp(15),
            color=self.COLOR_TEXT_ON_BACKGROUND
        )
        self.volume_slider = Slider(
            min=0,
            max=100,
            value=self.player.get_initial_volume() * 100 if self.player else 50,
            size_hint_x=1, # Slider takes remaining width
            value_track=True,
            value_track_color=self.COLOR_PRIMARY_ACCENT
        )
        self.volume_slider.bind(value=self._set_volume)
        volume_layout.add_widget(volume_label_text)
        volume_layout.add_widget(self.volume_slider)
        self.add_widget(volume_layout)

        # --- Control Buttons Sub-Layout ---
        controls_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60), # Fixed height for button bar
            spacing=dp(10) # Spacing between buttons
        )
        button_style = {
            'font_size': dp(15),
            'background_normal': '',
            'background_color': self.COLOR_PRIMARY_ACCENT,
            'color': self.COLOR_TEXT_ON_ACCENT,
            'size_hint_x': 1 # Make buttons share width
        }
        self.load_button = Button(text="Load", **button_style)
        self.load_button.bind(on_press=self._load_song)
        
        self.play_pause_button = Button(text="Play", **button_style)
        self.play_pause_button.bind(on_press=self._toggle_play_pause)

        self.stop_button = Button(text="Stop", **button_style)
        self.stop_button.bind(on_press=self._stop_music)

        controls_layout.add_widget(self.load_button)
        controls_layout.add_widget(self.play_pause_button)
        controls_layout.add_widget(self.stop_button)
        self.add_widget(controls_layout)

        # Start periodic status update
        Clock.schedule_interval(self._update_status, 0.25)

    def _update_bg_rect(self, instance, value):
        """Callback to update the background rectangle's position and size."""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
        
    def _update_album_art_rect(self, instance, value):
        """Callback to update the rectangle's position and size."""
        self.album_art_rect.pos = instance.pos
        self.album_art_rect.size = instance.size

    def _load_song(self, instance):
        """Handles load song button press using the path from TextInput."""
        filepath_from_input = self.file_path_input.text.strip()
        if not filepath_from_input:
            self.song_label.text = "File path cannot be empty."
            print("Load button pressed. File path input is empty.")
            return

        print(f"Load button pressed. Attempting to play: {filepath_from_input}")
        # Ensure the player instance is available
        if not self.player:
            self.song_label.text = "Player not initialized."
            return

        track_name = self.player.play_music(filepath_from_input)
        if track_name:
            # Player's get_current_track_display_name() will be used by _update_status
            # self.song_label.text = f"Playing: {self.player.get_current_track_display_name()}"
            # No explicit GUI update here, _update_status will handle it
            pass
        else:
            self.song_label.text = f"Error: {self.player.get_current_track_display_name()}"
            # _update_status will reset Play button text if needed

    def _toggle_play_pause(self, instance):
        """Handles play/pause button press."""
        if not self.player or not self.player.current_track:
            if self.player: self._load_song(instance) 
            return

        if self.player.is_playing: 
            self.player.pause_music()
        elif self.player.is_paused: 
            self.player.unpause_music()
        else: 
            if self.player.current_track:
                self.player.play_music(self.player.current_track)
            else: 
                self._load_song(instance)
        # _update_status will update the GUI text and button states

    def _stop_music(self, instance):
        """Handles stop button press."""
        if not self.player: return
        self.player.stop_music()
        # _update_status will update the GUI text and button states

    def _set_volume(self, instance, value):
        """Handles volume slider value change."""
        volume_float = value / 100.0
        self.player.set_volume(volume_float)
        # Optional: Update a volume label if you add one that shows percentage
        # print(f"Volume set to {volume_float:.2f}")

    def _update_status(self, dt):
        """Periodically updates GUI based on player state."""
        if not self.player:
            return

        # Update GUI elements based on player state
        current_display_track = self.player.get_current_track_display_name()
        is_song_loaded = self.player.current_track is not None

        if self.player.is_playing:
            self.song_label.text = f"Playing: {current_display_track}"
            self.play_pause_button.text = "Pause"
            self.play_pause_button.disabled = False
            self.stop_button.disabled = False
        elif self.player.is_paused:
            self.song_label.text = f"Paused: {current_display_track}"
            self.play_pause_button.text = "Play"
            self.play_pause_button.disabled = False
            self.stop_button.disabled = False
        else: # Stopped
            if is_song_loaded:
                self.song_label.text = f"Stopped: {current_display_track}"
            else:
                self.song_label.text = "No song loaded."
            self.play_pause_button.text = "Play"
            self.play_pause_button.disabled = not is_song_loaded # Disable if no song loaded
            self.stop_button.disabled = not is_song_loaded     # Disable if no song loaded
        
        # Handle song finishing naturally
        try:
            if self.player.is_playing and not pygame.mixer.music.get_busy():
                print("Kivy GUI: Song finished naturally.")
                self.player.is_playing = False 
                # This will be caught by the next _update_status call to update text to "Stopped: ..."
                # Or force update here:
                self.song_label.text = f"Finished: {current_display_track}"
                self.play_pause_button.text = "Play"
                # Buttons state will be handled by the main logic above in the next call
        except Exception as e:
            pass # Pygame mixer might not be available if player init failed


class MusicPlayerKivyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None # Initialize player attribute

    def build(self):
        self.title = "Kivy Music Player"
        try:
            self.player = Player()
            print("Player initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize Player: {e}")
            # Optionally, display an error to the user in the Kivy UI
            # For now, player remains None, and UI elements should handle this.
        return MusicPlayerLayout(player_instance=self.player)

    def on_start(self):
        """Called when the Kivy app is starting, after build()."""
        if platform == 'android':
            print("Kivy App: Running on Android, requesting permissions...")
            
            def request_perms_callback(requested_permissions, grant_results):
                print("Kivy App: Permission request callback received.")
                if all(grant_results):
                    print("Kivy App: READ_EXTERNAL_STORAGE permission granted.")
                else:
                    print("Kivy App: READ_EXTERNAL_STORAGE permission DENIED.")
                    # Handle denied permission (e.g., show a message, disable functionality)
                    if hasattr(self.root, 'song_label'): # self.root is MusicPlayerLayout
                         self.root.song_label.text = "Storage permission denied. Cannot load songs."
            
            try:
                permissions.request_permissions(
                    [permissions.Permission.READ_EXTERNAL_STORAGE],
                    callback=request_perms_callback
                )
                print("Kivy App: permissions.request_permissions called.")
            except Exception as e:
                print(f"Kivy App: Error requesting permissions: {e}")
                if hasattr(self.root, 'song_label'):
                    self.root.song_label.text = "Error requesting permissions."
        else:
            print("Kivy App: Not running on Android, skipping Android permission request.")


    def on_stop(self):
        """Called when the Kivy app is stopping."""
        if hasattr(self, 'player') and self.player:
            print("Kivy app stopping, shutting down player.")
            self.player.shutdown()


if __name__ == "__main__":
    import pygame # For pygame.mixer.music.get_busy() in _update_status
    MusicPlayerKivyApp().run()
