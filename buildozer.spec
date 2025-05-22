[app]
# (all) App Name
title = KivyMusicPlayer

# (all) Package name
package.name = kivymusicplayer

# (all) Package domain (needed for android/ios packaging)
package.domain = org.example

# (all) Source code where the main.py live
# Suffix is py, so main_kivy.py will be the entry point if a main.py is not found
source.dir = . 

# (all) Source files to include (let buildozer figure it out)
source.include_exts = py,png,jpg,kv,atlas,mp3,json,pyc # Added mp3 for test.mp3

# (all) Source files to exclude (let buildozer figure it out)
# source.exclude_exts = spec

# (all) Version of the application
version = 0.1

# (all) Kivy requirements
requirements = python3,kivy,pygame,plyer

# (all) Custom kivy/python-for-android recipes folder (if any)
# requirements.recipe_dir = recipes

# (all) Presplash background color (for new kivy splash screen)
# presplash.color = #000000

# (all) Presplash image
# presplash.filename = %(source.dir)s/data/presplash.png

# (all) Icon filename
# icon.filename = %(source.dir)s/data/icon.png

# (all) Supported orientations
orientation = portrait

# (all) Describe the application
# description =

# (all) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (android) Android NDK version to use
# android.ndk = 23b # Let buildozer choose default

# (android) Android SDK version to use
# android.sdk = 20 # Let buildozer choose default

# (android) Minimum API level
android.api = 21 # Kivy typically needs 21+

# (android) Target API level (important for Google Play)
# Set to 34 for Android 14, as Android 15/API 35 might still be too new for some CI tools
# or default NDK/SDK versions used by buildozer if not explicitly set.
android.target_api = 34

# (android) Fullscreen mode
# fullscreen = 0

# (android) Android Archs
android.archs = arm64-v8a # For ARMv8

# (android) Permissions
# For API 33+, READ_MEDIA_AUDIO is preferred for audio files.
# However, since we allow manual path input, READ_EXTERNAL_STORAGE might still
# be functionally what we need, though it's more restricted.
# If using READ_MEDIA_AUDIO, the app might only see audio files or need a system picker.
# Let's use READ_MEDIA_AUDIO and INTERNET (Pygame might need it for some audio backends, good to have).
android.permissions = READ_MEDIA_AUDIO,INTERNET

# (android) Presplash on Android
# android.presplash_filename = %(source.dir)s/data/presplash_android.png

# (android) Icon for Android
# android.icon_filename = %(source.dir)s/data/icon_android.png

# (android) Python for android branch to use
# p4a.branch = master

# (android) Android entry point, default is org.kivy.android.PythonActivity
# Ensure this correctly points to your main Kivy script if it's not main.py
# By default, buildozer looks for main.py. If your Kivy main script is main_kivy.py,
# you might need to rename main_kivy.py to main.py or configure p4a to use main_kivy.py.
# For simplicity, assume main_kivy.py will be renamed to main.py before build.

# (android) If you need to upload your app to the Google Play Store
# you should create a key and certificate to sign your app
# android.release_keystore = /path/to/your/release.keystore
# android.release_keystore_alias = myalias
# android.release_keystore_password = mypassword
# android.release_key_alias_password = mypassword


[buildozer]
# (buildozer) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (buildozer) Warn on deprecated commands
# warn_on_deprecated_commands = 1
