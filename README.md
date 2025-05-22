# PWA Music Player

## Description

This project is a simple Progressive Web App (PWA) designed for playing local audio files. It offers a mobile-first, responsive interface, is installable on mobile devices (appearing on the home screen), and provides basic offline support for the application shell.

## Features

*   Plays local audio files selected by the user.
*   Standard playback controls:
    *   Play/Pause (dynamic button)
    *   Stop
*   Volume control using a slider.
*   Displays the name of the currently loaded song.
*   Mobile-first, responsive design that adapts to different screen sizes.
*   **PWA Features:**
    *   **Installable:** Supports "Add to Home Screen" functionality on compatible mobile browsers, allowing it to be launched like a native app.
    *   **Basic Offline Support:** The core application interface (app shell) is cached and loads offline after the first visit, thanks to a service worker. (Note: Audio files themselves are not cached for offline playback in this version).

## Technologies Used

*   HTML5 (for structure)
*   CSS3 (for styling)
*   JavaScript (ES6+) (for application logic and interactivity)
*   Service Workers (for offline caching of the app shell and PWA functionality)
*   Web App Manifest (for "Add to Home Screen" and PWA metadata)

## How to Use / "Install"

This PWA needs to be accessed via a web server, either locally for testing or through a hosting service for general use and installation on mobile.

### On Desktop (for Testing)

1.  Ensure you have all project files (`index.html`, `style.css`, `app.js`, `manifest.json`, `sw.js`, `icons/` folder) in a local directory.
2.  Serve the files using a local web server. Common methods:
    *   **Using VS Code Live Server:** If you use Visual Studio Code, the "Live Server" extension can easily serve the `index.html` file.
    *   **Using Python's HTTP Server:**
        *   Open a terminal or command prompt in the project's root directory.
        *   Run the command: `python -m http.server` (for Python 3) or `python -m SimpleHTTPServer` (for Python 2).
        *   Open your web browser and navigate to `http://localhost:8000` (or the port shown in the terminal).
3.  Use the application in your browser. "Add to Home Screen" functionality is typically more prominent on mobile browsers but may be available on some desktop browsers (e.g., Chrome, Edge).

### On Mobile (Android/iOS - PWA Installation)

1.  **Hosting:** The PWA must be hosted on a secure (HTTPS) server. A simple way to do this is using GitHub Pages (see "Deploying" section below).
2.  **Navigate:** Open a modern mobile browser (e.g., Chrome on Android, Safari on iOS) and navigate to the hosted URL of the PWA.
3.  **Install Prompt:**
    *   **Android (Chrome):** You should see a prompt or an option in the browser menu (usually three dots or lines) saying "Add to Home screen" or "Install app".
    *   **iOS (Safari):** Tap the "Share" button, then scroll down and select "Add to Home Screen".
4.  **Confirm:** Follow the on-screen prompts to add/install the app. An icon for the PWA Music Player will be added to your device's home screen.
5.  **Launch:** You can now launch the PWA Music Player from its home screen icon, just like a native app.
6.  **Offline Use:** After your first visit (and successful service worker installation), the basic app interface will load even if you are offline.

## File Selection

To play a song, use the "Load Song" button (or file input area). This will open your device's file picker, allowing you to select an audio file (e.g., MP3, WAV, OGG, depending on browser support) from your local storage. Each time you want to play a new song that isn't already loaded, you'll need to select it again using this method.

## For Developers / Self-Hosting

### Prerequisites

*   A modern web browser (for testing).
*   A code editor (e.g., VS Code, Sublime Text).
*   Basic knowledge of HTML, CSS, and JavaScript.

### Setup

1.  **Clone/Download:** Get all project files:
    *   `index.html`
    *   `style.css`
    *   `app.js`
    *   `manifest.json`
    *   `sw.js` (Service Worker)
    *   An `icons/` directory.
2.  **Icons:** Ensure you have the following icons in an `icons/` directory at the root of your project (as referenced in `manifest.json` and potentially `sw.js`):
    *   `icons/icon-192x192.png`
    *   `icons/icon-512x512.png`
    If these are not provided with the project source, you will need to create them. They are important for the PWA installation experience.

### Running Locally

Follow the steps in the "How to Use / 'Install'" -> "On Desktop" section above.

### Deploying (Example with GitHub Pages)

1.  **Create GitHub Repository:** Create a new repository on GitHub (or use an existing one).
2.  **Upload Files:** Upload all the project files and the `icons/` directory to the root of your GitHub repository:
    *   `index.html`
    *   `style.css`
    *   `app.js`
    *   `manifest.json`
    *   `sw.js`
    *   `icons/icon-192x192.png`
    *   `icons/icon-512x512.png`
3.  **Enable GitHub Pages:**
    *   In your GitHub repository, go to "Settings".
    *   Navigate to the "Pages" section in the left sidebar.
    *   Under "Build and deployment", for "Source", select "Deploy from a branch".
    *   Choose the branch you want to deploy from (e.g., `main` or `master`).
    *   For the folder, select `/ (root)`.
    *   Click "Save".
4.  **Access URL:** GitHub Pages will provide you with a URL (e.g., `https://your-username.github.io/your-repository-name/`). This URL will host your PWA. Ensure your repository is public for GitHub Pages to work without further configuration. It might take a few minutes for the site to become active after enabling.

## Future Enhancements (Optional)

*   Playlist support and management.
*   Audio seeking (progress bar).
*   Advanced offline audio caching (allowing selected tracks to be played offline).
*   Audio visualizer.
*   Metadata display from audio files (e.g., album, artist from ID3 tags).
*   Integration with media session API for native-like media controls on the device.

---
This README provides a guide to using, installing, and developing the PWA Music Player.
