import os
import shutil
import subprocess
import sys
from core.utils import restore_linux_ld_library_path

if sys.platform == "win32":
    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW
else:
    CREATE_NO_WINDOW = 0


def _subprocess_kwargs():
    if sys.platform.startswith("win"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return {
            "startupinfo": startupinfo,
            "creationflags": CREATE_NO_WINDOW,
        }
    return {}


def check_ffmpeg():
    try:
        restore_linux_ld_library_path()
        kwargs = _subprocess_kwargs()

        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            command = ["where", "ffmpeg"] if sys.platform.startswith("win") else ["which", "ffmpeg"]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5,
                **kwargs,
            )
            if result.returncode == 0 and result.stdout.strip():
                ffmpeg_path = result.stdout.strip().splitlines()[0]

        if not ffmpeg_path or not os.path.isfile(ffmpeg_path) or not os.access(ffmpeg_path, os.X_OK):
            return False, ""

        # Verify FFmpeg actually executes cleanly in the current environment
        probe = subprocess.run(
            [ffmpeg_path, "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            **kwargs,
        )
        if probe.returncode == 0:
            return True, ffmpeg_path

        print(f"[FFmpeg Execution Error] rc={probe.returncode} stderr={probe.stderr.strip()}")
        return False, ""

    except Exception as e:
        print(f"[FFmpeg Detection Error] {e}")
        return False, ""
