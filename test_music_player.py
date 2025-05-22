import unittest
from unittest.mock import patch, MagicMock
import io # For capturing print output

# It's important to import the functions we want to test *after* potential global patches
# or ensure that patches are applied correctly around them.
# For module-level mocks like pygame.mixer, we often patch where it's *looked up*,
# which is in the 'music_player' module.
import music_player 
from music_player import Player # Import Player class

# Mock pygame globally for all tests to prevent actual pygame.init etc.
# These are started in specific test classes/methods if needed for Player instantiation
# but generally, we want to avoid side effects from music_player.pygame import.
# However, Player class calls pygame.init() in its constructor.
# So, we must mock pygame's components like init, mixer.init, mixer.music.
# It's cleaner to do this where Player is instantiated or where its methods are called.

class TestVolumeControl(unittest.TestCase):

    def setUp(self):
        """Set up for volume control tests."""
        # Mock pygame.init and pygame.mixer.init called by Player constructor
        self.pygame_init_patch = patch('music_player.pygame.init')
        self.pygame_mixer_init_patch = patch('music_player.pygame.mixer.init')
        self.mock_pygame_init = self.pygame_init_patch.start()
        self.mock_pygame_mixer_init = self.pygame_mixer_init_patch.start()

        # Mock pygame.mixer.music object that Player methods will use
        self.mock_mixer_music_patch = patch('music_player.pygame.mixer.music', new_callable=MagicMock)
        self.mock_music = self.mock_mixer_music_patch.start()

        self.player = Player()
        # Player.__init__ sets volume to 0.5. Reset mock if that call is not desired for a specific test.
        self.mock_music.reset_mock() 


    def tearDown(self):
        self.pygame_init_patch.stop()
        self.pygame_mixer_init_patch.stop()
        self.mock_mixer_music_patch.stop()

    def test_set_volume_valid(self):
        """Test Player.set_volume with a valid level."""
        self.player.set_volume(0.7)
        self.mock_music.set_volume.assert_called_once_with(0.7)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_too_low(self, mock_stdout):
        """Test Player.set_volume with a level too low."""
        self.player.set_volume(-0.1)
        self.mock_music.set_volume.assert_not_called()
        self.assertIn("Error: Volume must be between 0.0 and 1.0.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_too_high(self, mock_stdout):
        """Test Player.set_volume with a level too high."""
        self.player.set_volume(1.1)
        self.mock_music.set_volume.assert_not_called()
        self.assertIn("Error: Volume must be between 0.0 and 1.0.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_type(self, mock_stdout):
        """Test Player.set_volume with a non-numeric type."""
        self.player.set_volume("abc") # Player.set_volume handles this by printing error
        self.mock_music.set_volume.assert_not_called()
        self.assertIn("Error: Volume level must be a number.", mock_stdout.getvalue())


    def test_volume_up_normal(self):
        """Test Player.volume_up from a normal level."""
        self.mock_music.get_volume.return_value = 0.5
        self.player.volume_up()
        self.mock_music.set_volume.assert_called_once_with(0.6) # volume_up rounds

    def test_volume_up_at_max(self):
        """Test Player.volume_up when already at max volume."""
        self.mock_music.get_volume.return_value = 1.0
        self.player.volume_up()
        self.mock_music.set_volume.assert_called_once_with(1.0)

    def test_volume_down_normal(self):
        """Test Player.volume_down from a normal level."""
        self.mock_music.get_volume.return_value = 0.5
        self.player.volume_down()
        self.mock_music.set_volume.assert_called_once_with(0.4) # volume_down rounds

    def test_volume_down_at_min(self):
        """Test Player.volume_down when already at min volume."""
        self.mock_music.get_volume.return_value = 0.0
        self.player.volume_down()
        self.mock_music.set_volume.assert_called_once_with(0.0)


class TestPlaybackControl(unittest.TestCase): # Renamed from TestFileHandling

    def setUp(self):
        self.pygame_init_patch = patch('music_player.pygame.init')
        self.pygame_mixer_init_patch = patch('music_player.pygame.mixer.init')
        self.mock_pygame_init = self.pygame_init_patch.start()
        self.mock_pygame_mixer_init = self.pygame_mixer_init_patch.start()
        
        self.mock_mixer_music_patch = patch('music_player.pygame.mixer.music', new_callable=MagicMock)
        self.mock_music = self.mock_mixer_music_patch.start()
        
        self.player = Player()
        # Reset mock for mixer.music calls made in Player.__init__ (like set_volume)
        self.mock_music.reset_mock()


    def tearDown(self):
        self.pygame_init_patch.stop()
        self.pygame_mixer_init_patch.stop()
        self.mock_mixer_music_patch.stop()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_music_non_mp3(self, mock_stdout):
        """Test Player.play_music with a non-MP3 file."""
        result = self.player.play_music("test.wav")
        self.assertIsNone(result)
        self.mock_music.load.assert_not_called()
        self.mock_music.play.assert_not_called()
        self.assertFalse(self.player.is_playing)
        self.assertIsNone(self.player.current_track)
        self.assertIn("Error: Only .mp3 files are currently supported.", mock_stdout.getvalue())

    @patch('music_player.os.path.basename', return_value="test.mp3") # Mock basename for display name
    @patch('sys.stdout', new_callable=io.StringIO) 
    def test_play_music_valid_mp3(self, mock_stdout, mock_basename):
        """Test Player.play_music with a valid MP3 file."""
        filepath = "path/to/test.mp3"
        result = self.player.play_music(filepath)
        
        self.assertEqual(result, "test.mp3")
        self.mock_music.load.assert_called_once_with(filepath)
        self.mock_music.play.assert_called_once()
        self.assertTrue(self.player.is_playing)
        self.assertFalse(self.player.is_paused)
        self.assertEqual(self.player.current_track, filepath)
        self.assertIn(f"Now playing: {result}", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_music_pygame_error_on_load(self, mock_stdout):
        """Test Player.play_music when pygame.mixer.music.load raises pygame.error."""
        class MockPygameError(Exception): pass # Define dummy exception
        
        # Patch pygame.error in music_player module's scope
        with patch('music_player.pygame.error', MockPygameError):
            self.mock_music.load.side_effect = MockPygameError("Test Pygame Load Error")
            result = self.player.play_music("error.mp3")

        self.assertIsNone(result)
        self.mock_music.load.assert_called_once_with("error.mp3")
        self.mock_music.play.assert_not_called()
        self.assertFalse(self.player.is_playing)
        self.assertFalse(self.player.is_paused)
        self.assertIsNone(self.player.current_track)
        self.assertIn("Error playing music: Test Pygame Load Error", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pause_music_when_playing(self, mock_stdout):
        """Test Player.pause_music when music is playing."""
        self.player.is_playing = True # Simulate playing state
        self.player.is_paused = False
        self.player.current_track = "test.mp3"
        
        self.player.pause_music()
        
        self.mock_music.pause.assert_called_once()
        self.assertFalse(self.player.is_playing) # is_playing means sound is coming out
        self.assertTrue(self.player.is_paused)
        self.assertIn("Music paused.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pause_music_when_paused(self, mock_stdout):
        """Test Player.pause_music when music is already paused."""
        self.player.is_playing = False
        self.player.is_paused = True
        self.player.current_track = "test.mp3"

        self.player.pause_music()
        self.mock_music.pause.assert_not_called()
        self.assertIn("Music is already paused.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pause_music_when_stopped(self, mock_stdout):
        """Test Player.pause_music when music is stopped."""
        self.player.is_playing = False
        self.player.is_paused = False
        
        self.player.pause_music()
        self.mock_music.pause.assert_not_called()
        self.assertIn("No music is currently playing to pause.", mock_stdout.getvalue())


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_unpause_music_when_paused(self, mock_stdout):
        """Test Player.unpause_music when music is paused."""
        self.player.is_playing = False 
        self.player.is_paused = True
        self.player.current_track = "test.mp3"

        self.player.unpause_music()
        self.mock_music.unpause.assert_called_once()
        self.assertTrue(self.player.is_playing)
        self.assertFalse(self.player.is_paused)
        self.assertIn("Music resumed.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_unpause_music_when_playing(self, mock_stdout):
        """Test Player.unpause_music when music is already playing."""
        self.player.is_playing = True
        self.player.is_paused = False
        self.player.current_track = "test.mp3"

        self.player.unpause_music()
        self.mock_music.unpause.assert_not_called() # Should not call unpause if already playing
        self.assertIn("Music is already playing.", mock_stdout.getvalue())


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_stop_music_when_playing(self, mock_stdout):
        """Test Player.stop_music when music is playing."""
        self.player.is_playing = True
        self.player.current_track = "test.mp3"
        
        self.player.stop_music()
        
        self.mock_music.stop.assert_called_once()
        self.assertFalse(self.player.is_playing)
        self.assertFalse(self.player.is_paused)
        # self.assertIsNone(self.player.current_track) # As per Player.stop_music logic
        self.assertIn("Music stopped.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_stop_music_when_stopped(self, mock_stdout):
        """Test Player.stop_music when music is already stopped."""
        self.player.is_playing = False
        self.player.is_paused = False
        
        self.player.stop_music()
        self.mock_music.stop.assert_not_called()
        self.assertIn("No music is currently playing to stop.", mock_stdout.getvalue())


class TestPlayerGetters(unittest.TestCase):
    def setUp(self):
        # Mock pygame.init and pygame.mixer.init called by Player constructor
        # These are needed if Player constructor relies on them, even if mixer.music is mocked later.
        self.pygame_init_patch = patch('music_player.pygame.init')
        self.pygame_mixer_init_patch = patch('music_player.pygame.mixer.init')
        self.mock_pygame_init = self.pygame_init_patch.start()
        self.mock_pygame_mixer_init = self.pygame_mixer_init_patch.start()
        
        # Mock the mixer.music object for Player methods if they use it (not directly by getters)
        self.mock_mixer_music_patch = patch('music_player.pygame.mixer.music', new_callable=MagicMock)
        self.mock_mixer_music_patch.start()

        self.player = Player()

    def tearDown(self):
        self.pygame_init_patch.stop()
        self.pygame_mixer_init_patch.stop()
        self.mock_mixer_music_patch.stop()

    @patch('music_player.os.path.basename')
    def test_get_current_track_display_name(self, mock_basename):
        """Test Player.get_current_track_display_name."""
        self.assertEqual(self.player.get_current_track_display_name(), "None")
        
        self.player.current_track = "path/to/some song.mp3"
        mock_basename.return_value = "some song.mp3"
        self.assertEqual(self.player.get_current_track_display_name(), "some song.mp3")
        mock_basename.assert_called_once_with("path/to/some song.mp3")

    def test_get_playback_status(self):
        """Test Player.get_playback_status."""
        self.player.is_playing = False
        self.player.is_paused = False
        self.assertEqual(self.player.get_playback_status(), "Stopped")
        
        self.player.is_playing = True
        self.player.is_paused = False
        self.assertEqual(self.player.get_playback_status(), "Playing")
        
        self.player.is_playing = False # is_playing is False when paused
        self.player.is_paused = True
        self.assertEqual(self.player.get_playback_status(), "Paused")


class TestCLICommands(unittest.TestCase):

    def setUp(self):
        # Pygame init/quit are called by Player's init/shutdown, which are part of run_cli
        # So, we mock them here.
        patch('music_player.pygame.init', MagicMock()).start()
        patch('music_player.pygame.mixer.init', MagicMock()).start()
        patch('music_player.pygame.quit', MagicMock()).start()
        # We also need to patch the Player class instantiation in run_cli
        self.player_class_patch = patch('music_player.Player', autospec=True)
        self.MockPlayerClass = self.player_class_patch.start()
        self.mock_player_instance = self.MockPlayerClass.return_value # This is the mock Player instance
        
        # Ensure the mock player instance has the necessary attributes if run_cli checks them
        self.mock_player_instance.current_track = None
        self.mock_player_instance.is_playing = False
        self.mock_player_instance.is_paused = False
        # Mock get_volume for the initial volume print in CLI
        # This needs to be on the actual pygame.mixer.music object if run_cli uses it directly
        # or on the player instance if run_cli uses player.get_volume()
        # The Player class sets initial volume, run_cli prints it.
        # run_cli's print: print(f"Initial volume: {pygame.mixer.music.get_volume():.1f}")
        # So we need to mock pygame.mixer.music for this.
        self.mixer_music_patch_cli = patch('music_player.pygame.mixer.music', new_callable=MagicMock)
        mock_cli_mixer_music = self.mixer_music_patch_cli.start()
        mock_cli_mixer_music.get_volume.return_value = 0.5


    def tearDown(self):
        patch.stopall() # Stops all patches started with patch()

    @patch('builtins.input', side_effect=['play test.mp3', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO) 
    def test_cli_play_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.play_music.assert_called_once_with('test.mp3')
        # Check if shutdown was called on the instance
        self.mock_player_instance.shutdown.assert_called_once()


    @patch('builtins.input', side_effect=['pause', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_pause_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.pause_music.assert_called_once()
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['resume', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_resume_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.unpause_music.assert_called_once()
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['stop', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_stop_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        # Stop is called for the command, and also by run_cli before player.shutdown()
        # The player.shutdown() also calls stop if playing.
        # If run_cli calls player.stop_music() then player.shutdown(),
        # and shutdown itself calls player.stop_music(), it might be called multiple times.
        # Current Player.shutdown() calls pygame.mixer.music.stop() directly.
        # run_cli calls player.stop_music() then player.shutdown().
        # So, player.stop_music() should be called once by CLI, then shutdown.
        self.mock_player_instance.stop_music.assert_called_once() # Once from CLI
        self.mock_player_instance.shutdown.assert_called_once()


    @patch('builtins.input', side_effect=['volume_up', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_volume_up_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.volume_up.assert_called_once()
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['volume_down', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_volume_down_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.volume_down.assert_called_once()
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['set_volume 0.7', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_valid(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.set_volume.assert_called_once_with(0.7)
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['set_volume abc', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_invalid_arg(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.mock_player_instance.set_volume.assert_not_called() 
        self.assertIn("Volume level must be a number.", mock_stdout.getvalue())
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['set_volume', 'quit']) 
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_missing_arg(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.assertIn("Usage: set_volume <level", mock_stdout.getvalue()) # Allow for different messages
        self.mock_player_instance.shutdown.assert_called_once()
        
    @patch('builtins.input', side_effect=['play', 'quit']) 
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_play_command_missing_arg(self, mock_stdout, mock_input):
        # Mock the get_current_track_display_name to simulate no track loaded for the prompt
        self.mock_player_instance.get_current_track_display_name.return_value = "None"
        self.mock_player_instance.get_playback_status.return_value = "Stopped"
        
        music_player.run_cli()
        self.assertIn("Usage: play <filepath.mp3>", mock_stdout.getvalue())
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', side_effect=['unknown_command', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_unknown_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        self.assertIn("Unknown command:", mock_stdout.getvalue())
        self.mock_player_instance.shutdown.assert_called_once()

    @patch('builtins.input', return_value='quit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_quit_command(self, mock_stdout, mock_input):
        music_player.run_cli()
        # self.mock_player_instance.stop_music.assert_called_once() # run_cli calls player.stop_music()
        self.mock_player_instance.shutdown.assert_called_once() 
        self.assertIn("Exiting music player", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
