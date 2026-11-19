#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt pyinstaller
mkdir -p icon.iconset
for item in '16 16 icon_16x16.png' '32 32 icon_16x16@2x.png' '32 32 icon_32x32.png' '64 64 icon_32x32@2x.png' '128 128 icon_128x128.png' '256 256 icon_128x128@2x.png' '256 256 icon_256x256.png' '512 512 icon_256x256@2x.png' '512 512 icon_512x512.png' '1024 1024 icon_512x512@2x.png'; do
  read -r w h name <<< "$item"
  sips -z "$w" "$h" assets/app.png --out "icon.iconset/$name"
done
iconutil -c icns icon.iconset -o assets/app.icns
python3 -m PyInstaller --noconfirm --windowed --name YoutubeGo --add-data 'assets:assets' --add-data 'ui/themes:ui/themes' --icon assets/app.icns --osx-bundle-identifier com.youtubego.app main.py
HOMEBREW_NO_AUTO_UPDATE=1 brew install create-dmg
create-dmg --volname YoutubeGo --volicon assets/app.icns --window-pos 200 120 --window-size 800 400 --icon-size 100 --icon YoutubeGo.app 200 190 --hide-extension YoutubeGo.app --app-drop-link 600 185 dist/YoutubeGo.dmg dist/YoutubeGo.app
