from PySide6.QtWidgets import QDockWidget, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from datetime import datetime

class LogDockManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.log_dock = None
        self.log_text_edit = None
        self.log_dock_visible = False
        self.init_log_dock()

    def init_log_dock(self):
        self.log_dock = QDockWidget("Logs", self.main_window)
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_dock.setWidget(self.log_text_edit)
        self.main_window.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)
        self.log_dock.hide()

    def toggle_visibility(self):
        if self.log_dock_visible:
            self.log_dock.hide()
            self.log_dock_visible = False
        else:
            self.log_dock.show()
            self.log_dock_visible = True

    def append_log(self, text):
        def get_timestamp():
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def format_error_text(msg):
            timestamp = get_timestamp()
            return f"[{timestamp}] [ERROR] {msg}"

        color = "white"
        
        if text.startswith("[yt-dlp"):
            if "[yt-dlp Debug]" in text:
                color = "#4D96FF"
            elif "[yt-dlp Info]" in text:
                if any(s in text.lower() for s in ["download completed", "has already been downloaded", "finished downloading", "merged", "success"]):
                    color = "#6BCB77"
                else:
                    color = "#4D96FF"
            elif "[yt-dlp Warning]" in text:
                color = "#FFD93D"
                text = f"[WARN] {text}"
            elif "[yt-dlp Error]" in text:
                color = "#FF4444"
                text = format_error_text(text)
        else:
            if any(k in text.lower() for k in ["error", "fail", "http status code"]):
                color = "#FF4444"
                text = format_error_text(text)
            elif any(k in text.lower() for k in ["warning", "warn"]):
                color = "#FFD93D"
                text = f"[WARN] {text}"
            elif any(k in text.lower() for k in ["completed", "success", "finished"]):
                color = "#6BCB77"
                text = f"[OK] {text}"
            elif any(k in text.lower() for k in ["started", "queued", "fetching", "downloading"]):
                color = "#4D96FF"
                text = f"[INFO] {text}"
            elif "cancel" in text.lower():
                color = "#FF9F45"
                text = f"[CANCELLED] {text}"

        if "error details:" in text.lower():
            lines = text.split("\n")
            formatted_lines = []
            for line in lines:
                if ":" in line and not line.lower().startswith(("error type", "error details", "http status")):
                    formatted_lines.append("    " + line)
                else:
                    formatted_lines.append(line)
            text = "\n".join(formatted_lines)

        self.log_text_edit.setTextColor(QColor(color))
        self.log_text_edit.append(text)
        self.log_text_edit.setTextColor(QColor("white"))

        scrollbar = self.log_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        if "[yt-dlp Error]" in text or ("error" in text.lower() and not text.startswith("[yt-dlp")):
            self.main_window.tray_manager.show_error_message(text)
        elif "playlist indexing in progress" in text.lower():
            self.main_window.tray_manager.show_playlist_indexing_message() 