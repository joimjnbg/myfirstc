import unittest
from unittest.mock import patch, MagicMock
import io # For capturing print output

# It's important to import the functions we want to test *after* potential global patches
# or ensure that patches are applied correctly around them.
# For module-level mocks like pygame.mixer, we often patch where it's *looked up*,
# which is in the 'music_player' module.
import music_player # This will be the module we are testing

class TestVolumeControl(unittest.TestCase):

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    def test_set_volume_valid(self, mock_music):
        """Test set_volume with a valid level."""
        music_player.set_volume(0.5)
        mock_music.set_volume.assert_called_once_with(0.5)

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_too_low(self, mock_stdout, mock_music):
        """Test set_volume with a level too low."""
        music_player.set_volume(-0.1)
        mock_music.set_volume.assert_not_called()
        self.assertIn("Error: Volume must be between 0.0 and 1.0.", mock_stdout.getvalue())

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_too_high(self, mock_stdout, mock_music):
        """Test set_volume with a level too high."""
        music_player.set_volume(1.1)
        mock_music.set_volume.assert_not_called()
        self.assertIn("Error: Volume must be between 0.0 and 1.0.", mock_stdout.getvalue())

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_set_volume_invalid_type(self, mock_stdout, mock_music):
        """Test set_volume with a non-numeric type."""
        # The function itself doesn't raise TypeError, it's caught in CLI.
        # The set_volume function itself expects a float.
        # This tests the direct call to set_volume.
        # The CLI part handles the string-to-float conversion.
        # If we were to test the CLI 'set_volume abc', that would be different.
        # Here, we are unit testing the function `music_player.set_volume`
        with self.assertRaises(TypeError): # Expecting a TypeError if a string is passed directly
             music_player.set_volume("abc")
        mock_music.set_volume.assert_not_called()
        # No stdout check here as a TypeError is raised before print

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    def test_volume_up_normal(self, mock_music):
        """Test volume_up from a normal level."""
        mock_music.get_volume.return_value = 0.5
        music_player.volume_up()
        # Check that new_volume is calculated approximately
        mock_music.set_volume.assert_called_once()
        args, _ = mock_music.set_volume.call_args
        self.assertAlmostEqual(args[0], 0.6)

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    def test_volume_up_at_max(self, mock_music):
        """Test volume_up when already at max volume."""
        mock_music.get_volume.return_value = 1.0
        music_player.volume_up()
        mock_music.set_volume.assert_called_once_with(1.0) # Should still call to ensure it's set to 1.0

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    def test_volume_down_normal(self, mock_music):
        """Test volume_down from a normal level."""
        mock_music.get_volume.return_value = 0.5
        music_player.volume_down()
        mock_music.set_volume.assert_called_once()
        args, _ = mock_music.set_volume.call_args
        self.assertAlmostEqual(args[0], 0.4)


    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    def test_volume_down_at_min(self, mock_music):
        """Test volume_down when already at min volume."""
        mock_music.get_volume.return_value = 0.0
        music_player.volume_down()
        mock_music.set_volume.assert_called_once_with(0.0)

if __name__ == '__main__':
    # Need to ensure pygame is not actually initialized by music_player if it had such top-level calls
    # For music_player, pygame.init() is under `if __name__ == "__main__":`
    # so importing music_player won't run it.
    # However, pygame.mixer.init() *is* called at the top level in music_player.
    # This is a problem. It should also be guarded.

    # Let's assume for now that pygame.mixer.init() in music_player is also guarded
    # or we mock it out globally before importing music_player.
    # For now, the tests above use @patch('music_player.pygame.mixer.music', ...)
    # which targets the lookup in the music_player module.

    # The critical part is that `import music_player` should not have side effects
    # like `pygame.mixer.init()`. If it does, those need to be mocked *before* import.

    # Let's check music_player.py structure.
    # `pygame.init()` and `pygame.mixer.init()` are in the `if __name__ == "__main__":` block.
    # This is correct. So, importing music_player is safe.
    unittest.main()


class TestFileHandling(unittest.TestCase):

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_music_non_mp3(self, mock_stdout, mock_music):
        """Test play_music with a non-MP3 file."""
        music_player.play_music("test.wav")
        mock_music.load.assert_not_called()
        mock_music.play.assert_not_called()
        self.assertIn("Error: Only .mp3 files are currently supported.", mock_stdout.getvalue())

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO) # To capture print output
    def test_play_music_valid_mp3(self, mock_stdout, mock_music):
        """Test play_music with a valid MP3 file."""
        music_player.play_music("test.mp3")
        mock_music.load.assert_called_once_with("test.mp3")
        mock_music.play.assert_called_once()
        self.assertIn("Now playing: test.mp3", mock_stdout.getvalue())

    @patch('music_player.pygame.mixer.music', new_callable=MagicMock)
    @patch('music_player.pygame.error', create=True) # Mock pygame.error
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_music_pygame_error_on_load(self, mock_stdout, mock_pygame_error, mock_music):
        """Test play_music when pygame.mixer.music.load raises pygame.error."""
        # Configure the mock_music.load to raise pygame.error
        # The error needs to be an instance, so we can give it a message.
        # Pygame errors are typically `pygame.error(message_string)`
        # We need music_player.pygame.error to be the actual exception class
        # that can be caught.
        
        # Redefine pygame.error in the music_player module for this test
        # This is tricky because pygame.error is usually a C extension type.
        # A simple class will do for `except pygame.error as e:`
        class MockPygameError(Exception):
            pass
        
        # We need to patch where pygame.error is looked up: music_player.pygame.error
        # The create=True in @patch for pygame.error is not enough for `except pygame.error`.
        # It's better to patch it directly in the music_player module's namespace.
        with patch('music_player.pygame.error', MockPygameError):
            mock_music.load.side_effect = MockPygameError("Test Pygame Error")
            music_player.play_music("error.mp3")
        
        mock_music.load.assert_called_once_with("error.mp3")
        mock_music.play.assert_not_called() # Should not be called if load fails
        output = mock_stdout.getvalue()
        self.assertIn("Error playing music: Test Pygame Error", output)
        self.assertIn("Please check the file path and ensure it's a valid MP3 file.", output)


class TestCLICommands(unittest.TestCase):

    def setUp(self):
        # This patch will apply to all test methods in this class.
        # It mocks the actual pygame mixer object within the music_player module.
        self.mock_mixer_music_patch = patch('music_player.pygame.mixer.music', new_callable=MagicMock)
        self.mock_mixer_music = self.mock_mixer_music_patch.start()
        
        # Mock Pygame's init and quit as they are called in the main block
        self.mock_pygame_init_patch = patch('music_player.pygame.init')
        self.mock_pygame_init = self.mock_pygame_init_patch.start()
        
        self.mock_pygame_mixer_init_patch = patch('music_player.pygame.mixer.init')
        self.mock_pygame_mixer_init = self.mock_pygame_mixer_init_patch.start()

        self.mock_pygame_quit_patch = patch('music_player.pygame.quit')
        self.mock_pygame_quit = self.mock_pygame_quit_patch.start()


    def tearDown(self):
        self.mock_mixer_music_patch.stop()
        self.mock_pygame_init_patch.stop()
        self.mock_pygame_mixer_init_patch.stop()
        self.mock_pygame_quit_patch.stop()
        # Ensure any other patches started in tests are stopped
        patch.stopall()


    @patch('music_player.play_music')
    @patch('builtins.input', side_effect=['play test.mp3', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO) # To capture any prints from CLI
    def test_cli_play_command(self, mock_stdout, mock_input, mock_play_music_func):
        """Test CLI 'play' command dispatch."""
        music_player.run_cli() # Call the refactored main loop
        mock_play_music_func.assert_called_once_with('test.mp3')
        self.mock_pygame_init.assert_called_once()
        self.mock_pygame_mixer_init.assert_called_once()
        # Pygame quit is called at the end of run_cli
        self.mock_pygame_quit.assert_called_once()

    @patch('music_player.pause_music')
    @patch('builtins.input', side_effect=['pause', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_pause_command(self, mock_stdout, mock_input, mock_pause_music_func):
        """Test CLI 'pause' command dispatch."""
        music_player.run_cli()
        mock_pause_music_func.assert_called_once()

    @patch('music_player.unpause_music')
    @patch('builtins.input', side_effect=['resume', 'quit']) # 'resume' is the CLI command
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_resume_command(self, mock_stdout, mock_input, mock_unpause_music_func):
        """Test CLI 'resume' command dispatch."""
        music_player.run_cli()
        mock_unpause_music_func.assert_called_once()

    @patch('music_player.stop_music') # This will be called twice: once by 'stop', once by 'quit'
    @patch('builtins.input', side_effect=['stop', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_stop_command(self, mock_stdout, mock_input, mock_stop_music_func):
        """Test CLI 'stop' command dispatch."""
        music_player.run_cli()
        # It's called for the 'stop' command, and then again when 'quit' is processed.
        self.assertEqual(mock_stop_music_func.call_count, 2)


    @patch('music_player.volume_up')
    @patch('builtins.input', side_effect=['volume_up', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_volume_up_command(self, mock_stdout, mock_input, mock_volume_up_func):
        """Test CLI 'volume_up' command dispatch."""
        music_player.run_cli()
        mock_volume_up_func.assert_called_once()

    @patch('music_player.volume_down')
    @patch('builtins.input', side_effect=['volume_down', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_volume_down_command(self, mock_stdout, mock_input, mock_volume_down_func):
        """Test CLI 'volume_down' command dispatch."""
        music_player.run_cli()
        mock_volume_down_func.assert_called_once()

    @patch('music_player.set_volume')
    @patch('builtins.input', side_effect=['set_volume 0.7', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_valid(self, mock_stdout, mock_input, mock_set_volume_func):
        """Test CLI 'set_volume' command dispatch with valid numeric arg."""
        music_player.run_cli()
        mock_set_volume_func.assert_called_once_with(0.7) # CLI converts to float

    @patch('music_player.set_volume') # We patch set_volume to ensure it's not called
    @patch('builtins.input', side_effect=['set_volume abc', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_invalid_arg(self, mock_stdout, mock_input, mock_set_volume_func):
        """Test CLI 'set_volume' command with invalid non-numeric arg."""
        music_player.run_cli()
        mock_set_volume_func.assert_not_called() # Should not be called due to ValueError
        self.assertIn("Volume level must be a number.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['set_volume', 'quit']) # Missing argument
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_set_volume_command_missing_arg(self, mock_stdout, mock_input):
        """Test CLI 'set_volume' command with missing argument."""
        music_player.run_cli()
        self.assertIn("Usage: set_volume <level>", mock_stdout.getvalue())
        
    @patch('builtins.input', side_effect=['play', 'quit']) # Missing argument
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_play_command_missing_arg(self, mock_stdout, mock_input):
        """Test CLI 'play' command with missing argument."""
        music_player.run_cli()
        self.assertIn("Usage: play <filepath.mp3>", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['unknown_command', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_unknown_command(self, mock_stdout, mock_input):
        """Test CLI with an unknown command."""
        music_player.run_cli()
        self.assertIn("Unknown command: unknown_command", mock_stdout.getvalue())

    @patch('music_player.stop_music') # stop_music is called by quit
    @patch('builtins.input', return_value='quit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_quit_command(self, mock_stdout, mock_input, mock_stop_music_func):
        """Test CLI 'quit' command dispatch."""
        music_player.run_cli()
        mock_stop_music_func.assert_called_once() # stop_music is called by quit
        self.mock_pygame_quit.assert_called_once() # Pygame quit is called at the end
        self.assertIn("Exiting music player.", mock_stdout.getvalue())
