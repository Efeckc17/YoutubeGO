from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
from PySide6.QtCore import Qt
import os
import sys
from pathlib import Path


def set_circular_pixmap(label, image_path):
    if not image_path:
        label.setPixmap(QPixmap())
        return

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        label.setPixmap(QPixmap())
        return

    scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    mask = QPixmap(scaled_pixmap.size())
    mask.fill(Qt.transparent)
    
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(Qt.white))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
    painter.end()
    
    scaled_pixmap.setMask(mask.createMaskFromColor(Qt.transparent))
    label.setPixmap(scaled_pixmap)

def format_speed(speed):
    if speed > 1000000:
        return f"{speed / 1000000:.2f} MB/s"
    elif speed > 1000:
        return f"{speed / 1000:.2f} KB/s"
    else:
        return f"{speed} B/s"

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{int(h)}h {int(m)}m {int(s)}s"
    elif m:
        return f"{int(m)}m {int(s)}s"
    else:
        return f"{int(s)}s"

def get_data_dir():
    """
    Get the application data directory path.
    On Windows: %APPDATA%/YoutubeGO
    On Linux: ~/.local/share/YoutubeGO
    On macOS: ~/Library/Application Support/YoutubeGO
    """
    if sys.platform.startswith("win"):
        base_dir = os.getenv('APPDATA')
    elif sys.platform.startswith("darwin"):
        base_dir = os.path.expanduser('~/Library/Application Support')
    else:  
        base_dir = os.path.expanduser('~/.local/share')
    
    data_dir = os.path.join(base_dir, 'YoutubeGO')
    os.makedirs(data_dir, exist_ok=True)

   
    images_dir = os.path.join(data_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    return data_dir

def get_images_dir():
    
    return os.path.join(get_data_dir(), 'images')


def restore_linux_ld_library_path():
    """Restore LD_LIBRARY_PATH when running frozen on Linux so external tools like ffmpeg don't load bundled libs."""
    if not sys.platform.startswith("linux") or not getattr(sys, "frozen", False):
        return
    if "LD_LIBRARY_PATH_ORIG" in os.environ:
        ld_source = os.environ["LD_LIBRARY_PATH_ORIG"]
    else:
        ld_source = os.environ.get("LD_LIBRARY_PATH", "")

    if not ld_source:
        os.environ.pop("LD_LIBRARY_PATH", None)
        return

    blocked_prefixes = []
    for raw in (getattr(sys, "_MEIPASS", None), os.environ.get("APPDIR")):
        if raw:
            blocked_prefixes.append(os.path.normpath(raw))

    filtered = []
    for entry in ld_source.split(os.pathsep):
        if not entry:
            continue
        norm = os.path.normpath(entry)
        if any(norm == p or norm.startswith(p + os.sep) for p in blocked_prefixes):
            continue
        filtered.append(entry)

    if filtered:
        os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(filtered)
    else:
        os.environ.pop("LD_LIBRARY_PATH", None)
