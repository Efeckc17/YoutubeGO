#!/usr/bin/env bash
set -euo pipefail
apt-get update
apt-get install -y curl ca-certificates file libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 libxcb-xinerama0 libxcb-image0 libxcb-xkb1 libxcb-shape0 libxcb-icccm4 appstream libfuse2 || apt-get install -y libfuse2t64
python -m pip install --no-cache-dir -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name YoutubeGo --add-data 'assets:assets' --add-data 'ui/themes:ui/themes' main.py
mkdir -p AppDir/usr/bin AppDir/usr/share/icons/hicolor/256x256/apps
cp dist/YoutubeGo AppDir/usr/bin/YoutubeGo
cp assets/app.png AppDir/usr/share/icons/hicolor/256x256/apps/YoutubeGo.png
cp assets/app.png AppDir/YoutubeGo.png
printf '[Desktop Entry]\nName=YoutubeGo\nExec=YoutubeGo\nIcon=YoutubeGo\nType=Application\nCategories=AudioVideo;Video;\nComment=YouTube video downloader\n' > AppDir/YoutubeGo.desktop
printf '#!/bin/sh\nexec "$APPDIR/usr/bin/YoutubeGo" "$@"\n' > AppDir/AppRun
chmod +x AppDir/AppRun
curl -fL --retry 3 https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage -o appimagetool
chmod +x appimagetool
ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 ./appimagetool AppDir
mv YoutubeGo-x86_64.AppImage dist/
