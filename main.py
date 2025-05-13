import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSharedMemory, QSystemSemaphore, Qt
from ui.main_window import MainWindow

def check_ffmpeg():
    """Check if FFmpeg is available and return its status."""
    ffmpeg_path = "ffmpeg"  
    if os.system(f"{ffmpeg_path} -version") == 0:
        return True
    return False

def main():
    
    shared_mem = QSharedMemory("YoutubeGO4.4")
    
    
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
    
 
    if not check_ffmpeg():
        print("FFmpeg not found. Please ensure it is installed and in PATH.")
    else:
        print("FFmpeg found.")
    
    win = MainWindow()
    win.show()
    
    
    app.aboutToQuit.connect(lambda: shared_mem.detach())
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
