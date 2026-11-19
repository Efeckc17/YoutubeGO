param([ValidateSet('test','exe','portable')][string]$Mode)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
function Run-Python([string[]]$ArgsList) {
  & python @ArgsList
  if ($LASTEXITCODE -ne 0) { throw "Python failed: $LASTEXITCODE" }
}
# GitLab Windows images may not have Python 3.13. Install it reproducibly.
choco install python313 -y --no-progress
if ($LASTEXITCODE -ne 0) { throw 'Python installation failed' }
$python = 'C:\Python313\python.exe'
if (-not (Test-Path $python)) { $python = (Get-ChildItem 'C:\Python313*\python.exe' -ErrorAction SilentlyContinue | Select-Object -First 1).FullName }
if (-not $python) { throw 'Python 3.13 executable not found' }
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'pip upgrade failed' }
if ($Mode -eq 'test') {
  & $python -m pip install -r requirements.txt
} else {
  & $python -m pip install -r requirements.txt pyinstaller
}
if ($LASTEXITCODE -ne 0) { throw 'Dependencies failed' }
if ($Mode -eq 'test') {
  & $python -m pip install -r requirements-dev.txt Pillow numpy
  if ($LASTEXITCODE -ne 0) { throw 'Test dependencies failed' }
  choco install ffmpeg -y --no-progress
  if ($LASTEXITCODE -ne 0) { throw 'FFmpeg installation failed' }
  $env:PATH = [Environment]::GetEnvironmentVariable('PATH','Machine') + ';' + [Environment]::GetEnvironmentVariable('PATH','User')
  $env:PYTHONPATH = (Get-Location).Path
  $env:PYTEST_TIMEOUT = '30'
  & $python -m pytest tests/ -v --tb=short --durations=0 --timeout=30
  if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
  exit 0
}
$url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
Invoke-WebRequest -Uri $url -OutFile ffmpeg.zip
Expand-Archive ffmpeg.zip -DestinationPath ffmpeg -Force
$ffmpeg = Get-ChildItem ffmpeg -Recurse -Filter ffmpeg.exe | Select-Object -First 1
if (-not $ffmpeg) { throw 'FFmpeg executable missing' }
Copy-Item $ffmpeg.FullName ffmpeg.exe
$version = $env:CI_COMMIT_TAG -replace '^v',''
if ($version -match '^\d+\.\d+\.\d+$') {
  $manifest = 'build_meta/YoutubeGo.manifest'
  $content = Get-Content $manifest -Raw
  $content = $content -replace 'version="[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"', "version=`"$version.0`""
  $content = $content -replace 'Version [0-9]+\.[0-9]+\.[0-9]+', "Version $version"
  Set-Content $manifest $content
}
$argsList = @('--noconfirm', '--windowed', '--name', 'YoutubeGo', '--icon=assets/app.ico', '--add-data=assets;assets', '--add-data=ui/themes;ui/themes', '--add-data=assets/app.png;assets', '--add-data=assets/app.ico;assets', '--add-data=ffmpeg.exe;.')
if ($Mode -eq 'exe') { $argsList += @('--onefile', '--manifest=build_meta/YoutubeGo.manifest') } else { $argsList += '--onedir' }
$argsList += 'main.py'
& $python -m PyInstaller @argsList
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed' }
if ($Mode -eq 'portable') {
  New-Item -ItemType Directory YoutubeGo-Win -Force | Out-Null
  Copy-Item 'dist/YoutubeGo/*' 'YoutubeGo-Win/' -Recurse -Force
  Copy-Item QtLicense.md, LICENSE YoutubeGo-Win/
  Compress-Archive -Path 'YoutubeGo-Win/*' -DestinationPath YoutubeGo-Win.zip -Force
}
