import os, sys, platform, subprocess, shutil, json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QProgressBar, QStatusBar, QDockWidget, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, QListWidgetItem, QFileDialog, QMenuBar, QAction, QMessageBox, QSystemTrayIcon, QMenu, QDialog, QFormLayout, QDialogButtonBox, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QGroupBox, QDateTimeEdit, QStackedWidget, QAbstractItemView, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QThreadPool, QTimer, QDateTime
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from core.profile import UserProfile
from core.utils import set_circular_pixmap, format_speed, format_time
from core.downloader import DownloadTask, DownloadQueueWorker
from core.history import load_history_initial, save_history, add_history_entry, delete_selected_history, delete_all_history, search_history
from core.utils import get_data_dir

from ui.pages.home_page import HomePage
from ui.pages.mp3_page import MP3Page
from ui.pages.mp4_page import MP4Page
from ui.pages.settings_page import SettingsPage
from ui.pages.profile_page import ProfilePage
from ui.pages.history_page import HistoryPage
from ui.pages.queue_page import QueuePage
from ui.pages.scheduler_page import SchedulerPage
from ui.components.animated_button import AnimatedButton
from ui.components.drag_drop_line_edit import DragDropLineEdit
from ui.dialogs import ProfileDialog, QueueAddDialog, ScheduleAddDialog
from ui.layouts import StatusBarLayout, SideMenuLayout, TopBarLayout

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class MainWindow(QMainWindow):
    progress_signal = pyqtSignal(int, float)
    status_signal = pyqtSignal(int, str)
    log_signal = pyqtSignal(str)
    info_signal = pyqtSignal(int, str, str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YoutubeGO 4.4")
        self.setGeometry(100, 100, 1280, 800)
        self.ffmpeg_found = False
        self.ffmpeg_path = ""
        self.ffmpeg_label = QLabel()
        self.log_dock_visible = True
        self.show_logs_btn = AnimatedButton("Logs")
        self.user_profile = UserProfile()
        self.thread_pool = QThreadPool()
        self.active_workers = []
        self.max_concurrent_downloads = 3
        self.search_map = {"proxy": (4, "Proxy configuration is in Settings."), "resolution": (4, "Resolution configuration is in Settings."), "profile": (5, "Profile page for user details."), "queue": (6, "Queue page for multiple downloads."), "mp4": (1, "MP4 page for video downloads."), "mp3": (2, "MP3 page for audio downloads."), "history": (3, "History page for download logs."), "settings": (4, "Settings page for various options."), "scheduler": (7, "Scheduler for planned downloads."), "download path": (4, "Download path is in Settings."), "theme": (4, "Theme switch is in Settings."), "logs": (8, "Logs section."), "home": (0, "Home page."), "download": (1, "Download pages."), "audio": (2, "Audio download page."), "video": (1, "Video download page."), "planned": (7, "Scheduler for planned downloads."), "issues": (8, "Download issues have been fixed."), "speed": (8, "Speed has been optimized."), "youtubego.org": (0, "Visit youtubego.org for more information.")}
        self.progress_signal.connect(self.update_progress)
        self.status_signal.connect(self.update_status)
        self.log_signal.connect(self.append_log)
        self.info_signal.connect(self.update_queue_info)
        self.current_theme = self.user_profile.get_theme()  
        self.init_ui()
        self.check_ffmpeg()
        self.apply_current_theme()  
        if not self.user_profile.is_profile_complete():
            self.prompt_user_profile()
        self.init_tray_icon()
    def init_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "app.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            p = QPainter(pixmap)
            f = QFont()
            f.setPointSize(32)
            p.setFont(f)
            p.drawText(pixmap.rect(), Qt.AlignCenter, "▶️")
            p.end()
            icon = QIcon(pixmap)

        self.tray_icon = QSystemTrayIcon(icon, self)
        tray_menu = QMenu()
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.showNormal)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("YoutubeGO 4.4")
        self.tray_icon.show()
        if not self.ffmpeg_found:
            self.tray_icon.showMessage("FFmpeg missing", "Please download it from the official website.", QSystemTrayIcon.Critical, 3000)
    def closeEvent(self, event):
        
        if event.spontaneous():  
            self.hide()
            self.tray_icon.showMessage("YoutubeGO 4.4", "Application is running in the tray", QSystemTrayIcon.Information, 2000)
            event.ignore()
        else: 
            self.quit_app()
            event.accept()
    def quit_app(self):
        
        self.tray_icon.hide()
        QApplication.quit()
    def check_ffmpeg(self):
        
        self.append_log(f"Current PATH: {os.environ.get('PATH', '')}")
        
        
        path = shutil.which("ffmpeg")
        self.append_log(f"FFmpeg found in PATH: {path}")
        
        
        if not path and platform.system() == "Darwin":
            common_paths = [
                "/usr/local/bin/ffmpeg",
                "/opt/homebrew/bin/ffmpeg",
                os.path.expanduser("~/homebrew/bin/ffmpeg")
            ]
            for brew_path in common_paths:
                self.append_log(f"Checking path: {brew_path}")
                if os.path.exists(brew_path):
                    path = brew_path
                    self.append_log(f"Found FFmpeg at: {brew_path}")
                    break
        
        if path:
            self.ffmpeg_found = True
            self.ffmpeg_path = path
            self.append_log(f"FFmpeg successfully found at: {path}")
        else:
            self.ffmpeg_found = False
            self.ffmpeg_path = ""
            self.append_log("FFmpeg not found in any location")
    def init_ui(self):
        
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        reset_profile_action = QAction("Reset Profile", self)
        reset_profile_action.triggered.connect(self.reset_profile)
        export_profile_action = QAction("Export Profile", self)
        export_profile_action.triggered.connect(self.export_profile)
        import_profile_action = QAction("Import Profile", self)
        import_profile_action.triggered.connect(self.import_profile)
        file_menu.addAction(exit_action)
        file_menu.addAction(reset_profile_action)
        file_menu.addAction(export_profile_action)
        file_menu.addAction(import_profile_action)
        
        help_menu = menu_bar.addMenu("Help")
        mail_action = QAction("Contact: toxi360@workmail.com", self)
        mail_action.triggered.connect(lambda: QMessageBox.information(self, "Contact", "For support: toxi360@workmail.com"))
        help_menu.addAction(mail_action)
        github_action = QAction("Github: https://github.com/Efeckc17", self)
        github_action.triggered.connect(lambda: QMessageBox.information(self, "GitHub", "https://github.com/Efeckc17"))
        help_menu.addAction(github_action)

       
        self.status_bar_layout = StatusBarLayout(self)
        self.progress_bar = self.status_bar_layout.progress_bar
        self.status_label = self.status_bar_layout.status_label
        self.ffmpeg_label = self.status_bar_layout.ffmpeg_label
        self.show_logs_btn = self.status_bar_layout.show_logs_btn

        
        self.log_dock = QDockWidget("Logs", self)
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_dock.setWidget(self.log_text_edit)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

       
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

       
        self.top_bar_layout = TopBarLayout(self)
        self.profile_pic_label = self.top_bar_layout.profile_pic_label
        self.profile_name_label = self.top_bar_layout.profile_name_label
        self.logo_label = self.top_bar_layout.logo_label
        self.top_search_edit = self.top_bar_layout.search_edit
        self.search_btn = self.top_bar_layout.search_btn
        self.search_result_list = self.top_bar_layout.search_result_list
        main_layout.addWidget(self.top_bar_layout.container)
        main_layout.addWidget(self.search_result_list)

       
        bottom_area = QWidget()
        bottom_layout = QHBoxLayout(bottom_area)
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        
        self.main_stack = QStackedWidget()
        self.page_home = self.create_page_home()
        self.page_mp4 = self.create_page_mp4()
        self.page_mp3 = self.create_page_mp3()
        self.page_history = self.create_page_history()
        self.page_settings = self.create_page_settings()
        self.page_profile = self.create_page_profile()
        self.page_queue = self.create_page_queue()
        self.page_scheduler = self.create_page_scheduler()
        
        self.main_stack.addWidget(self.page_home)
        self.main_stack.addWidget(self.page_mp4)
        self.main_stack.addWidget(self.page_mp3)
        self.main_stack.addWidget(self.page_history)
        self.main_stack.addWidget(self.page_settings)
        self.main_stack.addWidget(self.page_profile)
        self.main_stack.addWidget(self.page_queue)
        self.main_stack.addWidget(self.page_scheduler)
        
        self.initialize_history()

        
        self.side_menu_layout = SideMenuLayout(self)
        self.side_menu = self.side_menu_layout.side_menu
        bottom_layout.addWidget(self.side_menu_layout.container)
        bottom_layout.addWidget(self.main_stack, stretch=1)
        
        main_layout.addWidget(bottom_area)
        self.search_btn.clicked.connect(self.top_search_clicked)
    def toggle_logs(self):
        if self.log_dock_visible:
            self.log_dock.hide()
            self.log_dock_visible = False
        else:
            self.log_dock.show()
            self.log_dock_visible = True
    def create_page_home(self):
        return HomePage(self)
    def create_page_mp4(self):
        return MP4Page(self)
    def create_page_mp3(self):
        return MP3Page(self)
    def create_page_history(self):
        self.page_history = HistoryPage(self)
        return self.page_history
    def create_page_settings(self):
        return SettingsPage(self)
    def create_page_profile(self):
        return ProfilePage(self)
    def create_page_queue(self):
        self.page_queue = QueuePage(self)
        return self.page_queue
    def create_page_scheduler(self):
        return SchedulerPage(self)
    def side_menu_changed(self, index):
        self.main_stack.setCurrentIndex(index)
    def top_search_clicked(self):
        query = self.top_search_edit.text().lower().strip()
        self.search_result_list.clear()
        self.search_result_list.setVisible(False)
        if not query:
            return
        matches_found = False
        for k, v in self.search_map.items():
            if query in k:
                item = QListWidgetItem(f"{k.capitalize()}: {v[1]}")
                item.setData(Qt.UserRole, v[0])
                self.search_result_list.addItem(item)
                matches_found = True
        if matches_found:
            self.search_result_list.setVisible(True)
    def search_item_clicked(self, item):
        page_index = item.data(Qt.UserRole)
        self.side_menu.setCurrentRow(page_index)
        self.search_result_list.clear()
        self.search_result_list.setVisible(False)
    def prompt_user_profile(self):
        dialog = ProfileDialog(self)
        dialog.exec_()
    def add_queue_item_dialog(self):
        dialog = QueueAddDialog(self)
        dialog.exec_()
    def add_scheduled_dialog(self):
        dialog = ScheduleAddDialog(self)
        dialog.exec_()
    def start_queue(self):
        count_started = 0
        for r in range(self.queue_table.rowCount()):
            st_item = self.queue_table.item(r, 4)
            if st_item and ("Queued" in st_item.text() or "0%" in st_item.text()):
                if count_started < self.max_concurrent_downloads:
                    url = self.queue_table.item(r, 2).text()
                    typ = self.queue_table.item(r, 3).text().lower()
                    audio = ("audio" in typ)
                    playlist = ("playlist" in typ)
                    current_format = "mp4"
                    row_idx = r
                    tsk = DownloadTask(url, self.user_profile.get_default_resolution(), self.user_profile.get_download_path(), self.user_profile.get_proxy(), audio_only=audio, playlist=playlist, output_format=current_format, from_queue=True)
                    self.run_task(tsk, row_idx)
                    self.queue_table.setItem(r, 4, QTableWidgetItem("Started"))
                    count_started += 1
        self.append_log("Queue started.")
    def remove_scheduled_item(self):
        sel = set()
        for it in self.scheduler_table.selectedItems():
            sel.add(it.row())
        for r in sorted(sel, reverse=True):
            self.scheduler_table.removeRow(r)
    def check_scheduled_downloads(self):
        now = QDateTime.currentDateTime()
        for r in range(self.scheduler_table.rowCount()):
            dt_str = self.scheduler_table.item(r, 0).text()
            scheduled_dt = QDateTime.fromString(dt_str, "yyyy-MM-dd HH:mm:ss")
            st_item = self.scheduler_table.item(r, 4)
            if st_item and scheduled_dt <= now and st_item.text() == "Scheduled":
                u = self.scheduler_table.item(r, 1).text()
                t = self.scheduler_table.item(r, 2).text().lower()
                s = (self.scheduler_table.item(r, 3).text() == "Yes")
                audio = ("audio" in t)
                task = DownloadTask(u, self.user_profile.get_default_resolution(), self.user_profile.get_download_path(), self.user_profile.get_proxy(), audio_only=audio, playlist=False, subtitles=s, from_queue=True)
                self.run_task(task, r)
                self.scheduler_table.setItem(r, 4, QTableWidgetItem("Started"))
    def start_download_simple(self, url_edit, audio=False, playlist=False):
        link = url_edit.text().strip()
        if not link:
            QMessageBox.warning(self, "Error", "No URL given.")
            return
        task = DownloadTask(link, self.user_profile.get_default_resolution(), self.user_profile.get_download_path(), self.user_profile.get_proxy(), audio_only=audio, playlist=playlist, from_queue=False)
        add_history_entry(self.history_table, "Fetching...", "Fetching...", link, "Queued", self.user_profile.is_history_enabled())
        self.run_task(task, None)
    def run_task(self, task, row):
        if task.playlist:
            self.tray_icon.showMessage("YoutubeGO 4.4", "Playlist indexing, please wait...", QSystemTrayIcon.Information, 5000)
        worker = DownloadQueueWorker(task, row, self.progress_signal, self.status_signal, self.log_signal, self.info_signal)
        self.thread_pool.start(worker)
        self.active_workers.append(worker)
    def update_progress(self, row, percent):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 4, QTableWidgetItem(f"{int(percent)}%"))
        self.progress_bar.setValue(int(percent))
        self.progress_bar.setFormat(f" {int(percent)}%")
        self.status_label.setText(f"Downloading... {percent:.1f}%")
    def update_status(self, row, st):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 4, QTableWidgetItem(st))
        self.status_label.setText(st)
        if "Download Completed" in st:
            self.tray_icon.showMessage("YoutubeGO 4.4", "Download Completed", QSystemTrayIcon.Information, 3000)
            user_choice = QMessageBox.question(self, "Download Completed", "Open Download Folder?", QMessageBox.Yes | QMessageBox.No)
            if user_choice == QMessageBox.Yes:
                self.open_download_folder()
        elif "Download Error" in st:
            self.tray_icon.showMessage("YoutubeGO 4.4", "Download Error Occurred", QSystemTrayIcon.Critical, 3000)
            QMessageBox.critical(self, "Error", st)
        elif "Cancelled" in st:
            self.tray_icon.showMessage("YoutubeGO 4.4", "Download Cancelled", QSystemTrayIcon.Warning, 3000)
    def update_queue_info(self, row, title, channel):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 0, QTableWidgetItem(title))
                self.page_queue.queue_table.setItem(row, 1, QTableWidgetItem(channel))
                url = self.page_queue.queue_table.item(row, 2).text()
                self.add_history_entry(title, channel, url, "Downloading")
    def open_download_folder(self):
        folder = self.user_profile.get_download_path()
        if platform.system() == "Windows":
            os.startfile(folder)
        elif platform.system() == "Darwin":
            subprocess.run(["open", folder])
        else:
            subprocess.run(["xdg-open", folder])
    def append_log(self, text):
        def get_timestamp():
            from datetime import datetime
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def format_error_text(msg):
            timestamp = get_timestamp()
            return f"[{timestamp}] ❌ {msg}"

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
                text = f"⚠️ {text}"
            elif "[yt-dlp Error]" in text:
                color = "#FF4444"
                text = format_error_text(text)
        else:
            if any(k in text.lower() for k in ["error", "fail", "http status code"]):
                color = "#FF4444"
                text = format_error_text(text)
            elif any(k in text.lower() for k in ["warning", "warn"]):
                color = "#FFD93D"
                text = f"⚠️ {text}"
            elif any(k in text.lower() for k in ["completed", "success", "finished"]):
                color = "#6BCB77"
                text = f"✅ {text}"
            elif any(k in text.lower() for k in ["started", "queued", "fetching", "downloading"]):
                color = "#4D96FF"
                text = f"ℹ️ {text}"
            elif "cancel" in text.lower():
                color = "#FF9F45"
                text = f"🚫 {text}"

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
            self.tray_icon.showMessage("YoutubeGO 4.4 - Error", text.split("\n")[0], QSystemTrayIcon.Critical, 5000)
        elif "playlist indexing in progress" in text.lower():
            self.tray_icon.showMessage("YoutubeGO 4.4", "Playlist indexing in progress. Please wait...", QSystemTrayIcon.Information, 5000)
    def toggle_history_logging(self, state):
        en = (state == Qt.Checked)
        self.user_profile.set_history_enabled(en)
        self.append_log(f"History logging {'enabled' if en else 'disabled'}.")
    def search_history_in_table(self):
        txt = self.search_hist_edit.text().lower().strip()
        search_history(self.history_table, txt)
    def confirm_delete_all(self):
        ans = QMessageBox.question(self, "Delete All", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        return ans == QMessageBox.Yes
    def reset_profile(self):
        if os.path.exists(self.user_profile.profile_path):
            os.remove(self.user_profile.profile_path)
        QMessageBox.information(self, "Reset Profile", "Profile data removed. Please restart.")
        self.append_log("Profile has been reset.")
    def update_profile_ui(self):
        if self.user_profile.data["profile_picture"]:
            pixmap = QPixmap(self.user_profile.data["profile_picture"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.profile_pic_label.setPixmap(pixmap)
        else:
            self.profile_pic_label.setPixmap(QPixmap())
        self.profile_name_label.setText(self.user_profile.data["name"] if self.user_profile.data["name"] else "User")
    def set_max_concurrent_downloads(self, idx):
        val = self.concurrent_combo.currentText()
        self.max_concurrent_downloads = int(val)
        self.append_log(f"Max concurrent downloads set to {val}")
    def change_theme_clicked(self):
        theme = self.theme_combo.currentText()
        self.user_profile.set_theme(theme)
        if theme == "Dark":
            self.setStyleSheet(self.get_dark_theme())
        else:
            self.setStyleSheet(self.get_light_theme())
        self.append_log(f"Theme changed to '{theme}'.")
    def apply_current_theme(self):
        if self.current_theme == "Dark":
            self.setStyleSheet(self.get_dark_theme())
        else:
            self.setStyleSheet(self.get_light_theme())
    def get_dark_theme(self):
        css_path = os.path.join(os.path.dirname(__file__), "themes", "dark.qss")
        with open(css_path, "r") as f:
            return f.read()

    def get_light_theme(self):
        css_path = os.path.join(os.path.dirname(__file__), "themes", "light.qss")
        with open(css_path, "r") as f:
            return f.read()

    def apply_resolution(self):
        sr = self.res_combo.currentText()
        self.user_profile.set_default_resolution(sr)
        prx = self.proxy_edit.text().strip()
        self.user_profile.set_proxy(prx)
        self.append_log(f"Resolution set: {sr}, Proxy: {prx}")
        QMessageBox.information(self, "Settings", f"Resolution: {sr}\nProxy: {prx}")
    def select_download_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.user_profile.set_profile(self.user_profile.data["name"], self.user_profile.data["profile_picture"], folder)
            self.download_path_edit.setText(folder)
            self.append_log(f"Download path changed to {folder}")
    def cancel_active(self):
        for w in self.active_workers:
            w.cancel = True

    def export_profile(self):
        
        try:
            temp_dir = os.path.join(get_data_dir(), "temp_export")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            
            profile_file = os.path.join(temp_dir, "user_profile.json")
            with open(profile_file, "w") as f:
                json.dump(self.user_profile.data, f, indent=4)

            
            history_file = os.path.join(temp_dir, "history.json")
            from core.history import export_history
            export_history(history_file)

            
            if self.user_profile.data["profile_picture"] and os.path.exists(self.user_profile.data["profile_picture"]):
                shutil.copy2(self.user_profile.data["profile_picture"], os.path.join(temp_dir, "profile_picture.png"))

            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Profile",
                os.path.join(os.path.expanduser("~"), "youtubego_profile.zip"),
                "Zip Files (*.zip)"
            )

            if file_path:
                shutil.make_archive(file_path.replace(".zip", ""), 'zip', temp_dir)
                QMessageBox.information(self, "Success", "Profile exported successfully!")
            else:
                QMessageBox.warning(self, "Cancelled", "Profile export cancelled.")

            shutil.rmtree(temp_dir)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export profile: {str(e)}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def import_profile(self):
        
        import zipfile
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Profile",
                os.path.expanduser("~"),
                "Zip Files (*.zip)"
            )
            if not file_path:
                return
            temp_dir = os.path.join(get_data_dir(), "temp_import")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            
            profile_file = os.path.join(temp_dir, "user_profile.json")
            if os.path.exists(profile_file):
                with open(profile_file, "r") as f:
                    profile_data = json.load(f)
                self.user_profile.data = profile_data
                self.user_profile.save_profile()
            
        
            history_file = os.path.join(temp_dir, "history.json")
            if os.path.exists(history_file):
                data_dir = get_data_dir()
                shutil.copy2(history_file, os.path.join(data_dir, "history.json"))
            
            
            pic_file = os.path.join(temp_dir, "profile_picture.png")
            if os.path.exists(pic_file):
                dest_pic = os.path.join(get_data_dir(), "profile_picture.png")
                shutil.copy2(pic_file, dest_pic)
                self.user_profile.data["profile_picture"] = dest_pic
                self.user_profile.save_profile()
            
            shutil.rmtree(temp_dir)
            
           
            try:
                if hasattr(self, 'res_combo'):
                    self.res_combo.setCurrentText(self.user_profile.get_default_resolution())
                if hasattr(self, 'proxy_edit'):
                    self.proxy_edit.setText(self.user_profile.get_proxy())
                self.update_profile_ui()
                if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
                    self.initialize_history()
                self.apply_current_theme()
            except Exception as ui_error:
                QMessageBox.warning(self, "Warning", f"Some UI elements couldn't be updated: {str(ui_error)}\nPlease restart the application.")
            
            QMessageBox.information(self, "Success", "Profile imported successfully! Please restart the app for all changes to take effect.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import profile: {str(e)}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_question(self, title, message):
        return QMessageBox.question(self, title, message) == QMessageBox.Yes

    def add_history_entry(self, title, channel, url, status):
        if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
            add_history_entry(self.page_history.history_table, title, channel, url, status, self.user_profile.is_history_enabled())

    def initialize_history(self):
       
        if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
            from core.history import load_history_initial
            load_history_initial(self.page_history.history_table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    
    window = MainWindow()
    theme = window.user_profile.get_theme()
    if theme == "Dark":
        window.setStyleSheet(window.get_dark_theme())
    else:
        window.setStyleSheet(window.get_light_theme())
    
    window.show()
    sys.exit(app.exec_())
