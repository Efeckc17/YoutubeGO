from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QPainter, QAction, QColor, QPolygon
from PySide6.QtCore import Qt, Signal, QPoint
import os
from core.version import get_version

class TrayIconManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tray_icon = None
        self.init_tray_icon()

    def init_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "app.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            p = QPainter(pixmap)
            p.setRenderHint(QPainter.Antialiasing)
            p.setBrush(QColor("#ff4444"))
            p.setPen(Qt.NoPen)
            p.drawPolygon(QPolygon([QPoint(20, 14), QPoint(50, 32), QPoint(20, 50)]))
            p.end()
            icon = QIcon(pixmap)

        self.tray_icon = QSystemTrayIcon(icon, self.main_window)
        tray_menu = QMenu()
        
        restore_action = QAction("Restore", self.main_window)
        restore_action.triggered.connect(self.main_window.showNormal)
        
        quit_action = QAction("Quit", self.main_window)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip(f"YoutubeGO {get_version(short=True)}")
        self.tray_icon.show()

    def quit_application(self):
        
        self.hide()
        QApplication.quit()

    def handle_window_close(self):
       
        self.main_window.hide()
        self.show_running_message()

    def show_ffmpeg_warning(self):
        if not self.main_window.ffmpeg_found:
            self.tray_icon.showMessage(
                "FFmpeg missing",
                "Please download it from the official website.",
                QSystemTrayIcon.Critical,
                3000
            )

    def show_running_message(self):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            "Application is running in the tray",
            QSystemTrayIcon.Information,
            2000
        )

    def show_download_completed_message(self):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            "Download Completed",
            QSystemTrayIcon.Information,
            3000
        )

    def show_download_error_message(self):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            "Download Error Occurred",
            QSystemTrayIcon.Critical,
            3000
        )

    def show_download_cancelled_message(self):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            "Download Cancelled",
            QSystemTrayIcon.Warning,
            3000
        )

    def show_playlist_indexing_message(self):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            "Playlist indexing, please wait...",
            QSystemTrayIcon.Information,
            5000
        )

    def show_error_message(self, text):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)} - Error",
            text.split("\n")[0],
            QSystemTrayIcon.Critical,
            5000
        )

    def hide(self):
        if self.tray_icon:
            self.tray_icon.hide()

    def show_message(self, title, message, icon=QSystemTrayIcon.Information):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)}",
            message,
            icon,
            3000
        )

    def show_error(self, message):
        self.tray_icon.showMessage(
            f"YoutubeGO {get_version(short=True)} - Error",
            message,
            QSystemTrayIcon.Critical,
            3000
        ) 