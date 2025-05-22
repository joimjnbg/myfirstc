document.addEventListener('DOMContentLoaded', () => {
    // DOM Element References
    const audioPlayer = document.getElementById('audio-player');
    const songInfo = document.getElementById('song-info');
    const albumArtPlaceholder = document.getElementById('album-art-placeholder'); // Referenced for future use
    const playPauseButton = document.getElementById('play-pause-button');
    const stopButton = document.getElementById('stop-button');
    const volumeSlider = document.getElementById('volume-slider');
    const fileInput = document.getElementById('file-input');
    // const playPauseIcon = playPauseButton.querySelector('.icon'); // If icon needs separate manipulation

    // Initial State (Volume is set by HTML, but can be reinforced here if needed)
    // audioPlayer.volume = 0.5; // HTML already sets this

    // Helper Function for Play/Pause Button UI
    function updatePlayPauseButton(isPlaying) {
        if (isPlaying) {
            playPauseButton.innerHTML = '<span class="icon">⏸</span> Pause';
            playPauseButton.setAttribute('aria-label', 'Pause');
        } else {
            playPauseButton.innerHTML = '<span class="icon">▶</span> Play';
            playPauseButton.setAttribute('aria-label', 'Play');
        }
    }

    // Event Listener Functions
    function loadSong(event) {
        const file = event.target.files[0];
        if (file) {
            const fileURL = URL.createObjectURL(file);
            audioPlayer.src = fileURL;
            songInfo.textContent = `Now Playing: ${file.name}`;
            audioPlayer.play(); // Autoplay the loaded song
            // updatePlayPauseButton(true); // Handled by 'play' event on audioPlayer
        }
    }

    function togglePlayPause() {
        if (!audioPlayer.src || audioPlayer.src === window.location.href) { // No src or src is the page itself
            // Trigger file input if no song is loaded
            fileInput.click(); 
            return;
        }
        if (audioPlayer.paused || audioPlayer.ended) {
            audioPlayer.play();
            // updatePlayPauseButton(true); // Handled by 'play' event
        } else {
            audioPlayer.pause();
            // updatePlayPauseButton(false); // Handled by 'pause' event
        }
    }

    function stopSong() {
        if (!audioPlayer.src || audioPlayer.src === window.location.href) return; // No song loaded
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        songInfo.textContent = "Stopped"; // Or "No song loaded." or clear
        updatePlayPauseButton(false); // Explicitly set to "Play"
    }

    function changeVolume(event) {
        audioPlayer.volume = event.target.value;
    }

    // Audio Player Event Handlers
    function handlePlay() {
        updatePlayPauseButton(true);
        // If songInfo was "Stopped" or "Finished", update it
        if (fileInput.files.length > 0 && (songInfo.textContent === "Stopped" || songInfo.textContent.startsWith("Finished"))) {
            songInfo.textContent = `Now Playing: ${fileInput.files[0].name}`;
        }
    }

    function handlePause() {
        updatePlayPauseButton(false);
        // Avoid changing songInfo if it's "Stopped" due to stop button
        if (audioPlayer.currentTime > 0 && !audioPlayer.ended && songInfo.textContent !== "Stopped") {
             if (fileInput.files.length > 0) {
                songInfo.textContent = `Paused: ${fileInput.files[0].name}`;
            }
        }
    }

    function handleEnded() {
        updatePlayPauseButton(false);
        if (fileInput.files.length > 0) {
            songInfo.textContent = `Finished: ${fileInput.files[0].name}`;
        } else {
            songInfo.textContent = "Finished";
        }
        // Optional: Implement playlist logic to play next song here
    }
    
    function handleLoadedMetadata() {
        // This can be used to get duration etc.
        // console.log('Metadata loaded. Duration:', audioPlayer.duration);
        // Update song info here if not already done by loadSong, to ensure it's shown once metadata is available.
        // This is particularly useful if `loadSong` doesn't set it immediately or if src is set directly.
        if (fileInput.files.length > 0 && !songInfo.textContent.startsWith("Now Playing:")) {
             songInfo.textContent = `Now Playing: ${fileInput.files[0].name}`;
        }
    }


    // Attach Event Listeners
    fileInput.addEventListener('change', loadSong);
    playPauseButton.addEventListener('click', togglePlayPause);
    stopButton.addEventListener('click', stopSong);
    volumeSlider.addEventListener('input', changeVolume);

    audioPlayer.addEventListener('play', handlePlay);
    audioPlayer.addEventListener('pause', handlePause);
    audioPlayer.addEventListener('ended', handleEnded);
    audioPlayer.addEventListener('loadedmetadata', handleLoadedMetadata);

    // Initial UI setup
    updatePlayPauseButton(false); // Set to "Play" initially
});

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js') // Assuming sw.js is in the root
            .then(registration => {
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            })
            .catch(error => {
                console.log('ServiceWorker registration failed: ', error);
            });
    });
}
