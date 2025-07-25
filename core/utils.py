from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
from PySide6.QtCore import Qt
import os
import sys
from pathlib import Path


def set_circular_pixmap(label, source):
    """Set a circular pixmap on the given *label*.

    *source* may be either a ``QPixmap`` instance or a *str* / *Path* pointing
    to an image file. The function gracefully handles invalid input and will
    clear the label if the image cannot be loaded.
    """

    # Determine the input type -------------------------------------------------
    if source is None:
        label.setPixmap(QPixmap())
        return

    if isinstance(source, QPixmap):
        pixmap = source
    else:
        # Assume string / Path representing a file location
        pixmap = QPixmap(str(source))

    if pixmap.isNull():
        # Fallback: clear label if pixmap could not be loaded
        label.setPixmap(QPixmap())
        return

    # Scale and mask to obtain a circular avatar ------------------------------
    scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # Create a circular mask (noop when running with the stub implementation)
    mask = QPixmap(scaled_pixmap.size())
    mask.fill(Qt.transparent)

    painter = QPainter(mask)
    try:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
    finally:
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
