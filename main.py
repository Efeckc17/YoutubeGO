import sys
import os
import atexit
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QSystemSemaphore, Qt
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from core.ffmpeg_checker import check_ffmpeg
from core.version import get_version

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def set_platform_specific_settings():
    if sys.platform.startswith("win"):
        try:
            app_id = f"YoutubeGO.App.{get_version(short=True)}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception as e:
            print(f"Failed to set Windows-specific settings: {e}")

def cleanup_shared_memory(shared_mem):
    if shared_mem:
        try:
            if shared_mem.isAttached():
                if not shared_mem.detach():
                    # Only force detach if normal detach fails
                    shared_mem.forceDetach()
        except Exception as e:
            print(f"Error during shared memory cleanup: {e}")

def create_shared_memory():
    if sys.platform.startswith("win"):
        shared_mem = QSharedMemory(f"YoutubeGO {get_version(short=True)}")
        semaphore = QSystemSemaphore(f"YoutubeGO_Semaphore_{get_version(short=True)}", 1)
        return shared_mem, semaphore
    return None, None

def main():
    set_platform_specific_settings()
    
    shared_mem, semaphore = create_shared_memory()
    
    if shared_mem:
        atexit.register(cleanup_shared_memory, shared_mem)
        
        if not shared_mem.create(1):
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            for widget in app.topLevelWidgets():
                if isinstance(widget, MainWindow):
                    if widget.isMinimized():
                        widget.showNormal()
                    widget.setWindowState(widget.windowState() & ~Qt.WindowMinimized)
                    widget.activateWindow()
                    widget.raise_()
                    widget.show()
                    return
            return
    
    app = QApplication(sys.argv)
    
    icon_path = resource_path(os.path.join("assets", "app.ico"))
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    
    ffmpeg_found, ffmpeg_path = check_ffmpeg()
    if not ffmpeg_found:
        print("FFmpeg not found. Please ensure it is installed and in PATH.")
    else:
        print(f"FFmpeg found at: {ffmpeg_path}")
    
    win = MainWindow(ffmpeg_found=ffmpeg_found, ffmpeg_path=ffmpeg_path)
    
    if os.path.exists(icon_path):
        win.setWindowIcon(app_icon)
    
    def cleanup():
        if shared_mem:
            cleanup_shared_memory(shared_mem)
        if semaphore and semaphore.acquire():
            semaphore.release()

    if shared_mem:
        atexit.register(cleanup)
    
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()