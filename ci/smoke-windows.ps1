$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectId = $env:CI_PROJECT_ID
$tag = 'v5.0.25'
$api = "https://gitlab.com/api/v4/projects/$projectId/pipelines?ref=$tag&per_page=5"
$pipelines = Invoke-RestMethod -Uri $api
if (-not $pipelines) { throw "No pipeline found for $tag" }
$jobs = Invoke-RestMethod -Uri "https://gitlab.com/api/v4/projects/$projectId/pipelines/$($pipelines[0].id)/jobs?per_page=100"
$exeJob = $jobs | Where-Object { $_.name -eq 'windows_exe' -and $_.status -eq 'success' } | Select-Object -First 1
if (-not $exeJob) { throw "No successful Windows EXE job found for $tag" }
$url = "$($env:CI_PROJECT_URL)/-/jobs/$($exeJob.id)/artifacts/raw/dist/YoutubeGo.exe"
New-Item -ItemType Directory -Force smoke | Out-Null
Invoke-WebRequest -Uri $url -OutFile smoke/YoutubeGo.exe
if ((Get-Item smoke/YoutubeGo.exe).Length -lt 1000000) { throw 'EXE download is unexpectedly small' }
Write-Host "Downloaded EXE from job $($exeJob.id)"
$proc = $null
try {
  $proc = Start-Process -FilePath (Resolve-Path smoke/YoutubeGo.exe) -PassThru
  Start-Sleep -Seconds 20
  $proc.Refresh()
  if ($proc.HasExited) { throw "YoutubeGo exited during startup with code $($proc.ExitCode)" }
  Write-Host "PASS: YoutubeGo.exe remains running (PID $($proc.Id))"
  $ffmpeg = Get-ChildItem "$env:TEMP" -Filter ffmpeg.exe -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match '_MEI' } | Select-Object -First 1
  if (-not $ffmpeg) { throw 'Bundled FFmpeg was not found in PyInstaller extraction directory' }
  $output = & $ffmpeg.FullName -version 2>&1
  if ($LASTEXITCODE -ne 0 -or -not ($output | Select-String 'ffmpeg version')) { throw 'Bundled FFmpeg failed to execute' }
  Write-Host "PASS: Bundled FFmpeg runs: $($output[0])"
} finally {
  if ($proc) { $proc.Refresh(); if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force } }
}
