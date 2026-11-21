import os, sys, platform, subprocess, shutil, json
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QProgressBar, QStatusBar, QDockWidget, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, QListWidgetItem, QFileDialog, QMenuBar, QMessageBox, QSystemTrayIcon, QMenu, QDialog, QFormLayout, QDialogButtonBox, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QGroupBox, QDateTimeEdit, QStackedWidget, QAbstractItemView, QGraphicsDropShadowEffect, QFrame
from PySide6.QtCore import Qt, Signal, QThreadPool, QTimer, QDateTime
from PySide6.QtGui import QAction, QIcon, QFont, QPixmap, QPainter, QColor
from core.profile import UserProfile
from core.utils import set_circular_pixmap, format_speed, format_time
from core.downloader import DownloadTask, DownloadQueueWorker
from core.history import load_history_initial, save_history, add_history_entry, delete_selected_history, delete_all_history, search_history
from core.utils import get_data_dir
from core.version import get_version
from core.updater import UpdateManager

from ui.pages.home_page import HomePage
from ui.pages.mp3_page import AudioPage
from ui.pages.mp4_page import VideoPage
from ui.pages.settings_page import SettingsPage
from ui.pages.profile_page import ProfilePage
from ui.pages.history_page import HistoryPage
from ui.pages.queue_page import QueuePage
from ui.pages.scheduler_page import SchedulerPage
from ui.components.animated_button import AnimatedButton
from ui.components.drag_drop_line_edit import DragDropLineEdit
from ui.components.tray_icon import TrayIconManager
from ui.components.menu_bar import MenuBarManager
from ui.components.log_dock import LogDockManager
from ui.dialogs import ProfileDialog, QueueAddDialog, ScheduleAddDialog
from ui.layouts import StatusBarLayout, SideMenuLayout, TopBarLayout
from ui.components.theme_manager import ThemeManager
from ui.components.search_system import SearchSystem
from ui.components.profile_manager import ProfileManager

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class MainWindow(QMainWindow):
    progress_signal = Signal(int, float)
    status_signal = Signal(int, str)
    log_signal = Signal(str)
    info_signal = Signal(int, str, str)
    def __init__(self, ffmpeg_found=None, ffmpeg_path=None):
        super().__init__()
        self.setWindowTitle(f"YoutubeGO {get_version()}")
        screen = QApplication.primaryScreen().geometry()
        width = min(1280, screen.width() - 100)
        height = min(1150, screen.height() - 100)
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(788, 600)
        self.ffmpeg_found = ffmpeg_found if ffmpeg_found is not None else False
        self.ffmpeg_path = ffmpeg_path if ffmpeg_path is not None else ""
        if self.ffmpeg_found and self.ffmpeg_path:
            print(f"FFmpeg path set to: {self.ffmpeg_path}")
        self.ffmpeg_label = QLabel()
        self.user_profile = UserProfile()
        self.thread_pool = QThreadPool()
        self.active_workers = []
        self.max_concurrent_downloads = 3
        self.progress_signal.connect(self.update_progress)
        self.status_signal.connect(self.update_status)
        self.log_signal.connect(self.append_log)
        self.info_signal.connect(self.update_queue_info)
        self.theme_manager = ThemeManager(self)
        
       
        self.update_manager = UpdateManager(self)
        
        
        self.profile_manager = ProfileManager(self)
        self.tray_manager = TrayIconManager(self)
        self.tray_manager.show_ffmpeg_warning()
        self.menu_bar_manager = MenuBarManager(self)
        self.log_manager = LogDockManager(self)
        
       
        self.init_ui()
        self.theme_manager.apply_current_theme()
        if not self.user_profile.is_profile_complete():
            self.prompt_user_profile()
            
      
        QTimer.singleShot(2000, self.check_for_updates)
    def init_ui(self):
        self.status_bar_layout = StatusBarLayout(self)
        self.progress_bar = self.status_bar_layout.progress_bar
        

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.top_bar_layout = TopBarLayout(self)
        self.profile_pic_label = self.top_bar_layout.profile_pic_label
        self.profile_name_label = self.top_bar_layout.profile_name_label
        self.top_search_edit = self.top_bar_layout.search_edit
        self.search_btn = self.top_bar_layout.search_btn
        self.search_result_list = self.top_bar_layout.search_result_list
        main_layout.addWidget(self.top_bar_layout.container)

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
        self.search_system = SearchSystem(self)
    def create_page_home(self):
        return HomePage(self)
    def create_page_mp4(self):
        return VideoPage(self)
    def create_page_mp3(self):
        return AudioPage(self)
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
        download_path = self.user_profile.get_download_path()
        if not os.path.exists(download_path):
            QMessageBox.warning(self, "Invalid Download Path",
                f"Download folder does not exist:\n{download_path}\n\n"
                "The folder may have been deleted or the drive may be disconnected.\n"
                "Please select a new download location in Settings.")
            self.append_log(f"Queue start aborted - invalid path: {download_path}")
            return
        
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
                    tsk = DownloadTask(url, self.user_profile.get_default_resolution(), download_path, self.user_profile.get_proxy(), audio_only=audio, playlist=playlist, output_format=current_format, audio_format=self.user_profile.get_audio_format() if audio else None, audio_quality=self.user_profile.get_audio_quality() if audio else "320", from_queue=True)
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
        download_path = self.user_profile.get_download_path()
        if not os.path.exists(download_path):
            self.append_log(f"Scheduled download skipped - invalid path: {download_path}")
            return
        
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
                task = DownloadTask(u, self.user_profile.get_default_resolution(), download_path, self.user_profile.get_proxy(), audio_only=audio, playlist=False, subtitles=s, audio_format=self.user_profile.get_audio_format() if audio else None, audio_quality=self.user_profile.get_audio_quality() if audio else "320", from_queue=True)
                self.run_task(task, r)
                self.scheduler_table.setItem(r, 4, QTableWidgetItem("Started"))
    def start_download_simple(self, url_edit, audio=False, playlist=False):
        link = url_edit.text().strip()
        if not link:
            QMessageBox.warning(self, "Error", "No URL given.")
            return
        
        download_path = self.user_profile.get_download_path()
        if not os.path.exists(download_path):
            QMessageBox.warning(self, "Invalid Download Path",
                f"Download folder does not exist:\n{download_path}\n\n"
                "The folder may have been deleted or the drive may be disconnected.\n"
                "Please select a new download location in Settings.")
            self.append_log(f"Download aborted - invalid path: {download_path}")
            return
        
        task = DownloadTask(link, self.user_profile.get_default_resolution(), download_path, self.user_profile.get_proxy(), audio_only=audio, playlist=playlist, audio_format=self.user_profile.get_audio_format() if audio else None, audio_quality=self.user_profile.get_audio_quality() if audio else "320", from_queue=False)
        self.run_task(task, None)
    def run_task(self, task, row):
        if not getattr(task, "ffmpeg_path", None) and getattr(self, "ffmpeg_path", None):
            task.ffmpeg_path = self.ffmpeg_path
        if task.playlist:
            self.tray_manager.show_playlist_indexing_message()
            self.update_status(row, "Indexing Playlist...")
        else:
            self.update_status(row, "Preparing Download...")
            self.tray_manager.show_message("Download", "Preparing to download...")
        
        worker = DownloadQueueWorker(task, row, self.progress_signal, self.status_signal, self.log_signal, self.info_signal, self.user_profile)
        self.thread_pool.start(worker)
        self.active_workers.append(worker)
    def update_progress(self, row, percent):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 4, QTableWidgetItem(f"{int(percent)}%"))
        
        if not self.progress_bar.isVisible():
            self.progress_bar.setVisible(True)
            
        self.progress_bar.setValue(int(percent))
        self.progress_bar.setFormat(f"Downloading... {int(percent)}%")
    def update_status(self, row, st):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 4, QTableWidgetItem(st))
        
        if "Download Completed" in st:
            self.progress_bar.setVisible(True)
            self.progress_bar.setFormat("Download Completed ✓")
            self.progress_bar.setValue(100)
            QTimer.singleShot(3000, lambda: (
                self.progress_bar.setVisible(False),
                self.progress_bar.setFormat("Ready"),
                self.progress_bar.setValue(0)
            ))
        elif "Download Error" in st:
            self.progress_bar.setVisible(True)
            self.progress_bar.setFormat("Download Failed ✗")
            self.progress_bar.setValue(0)
            QTimer.singleShot(3000, lambda: (
                self.progress_bar.setVisible(False),
                self.progress_bar.setFormat("Ready"),
                self.progress_bar.setValue(0)
            ))
        elif "Cancelled" in st:
            self.progress_bar.setVisible(True)
            self.progress_bar.setFormat("Download Cancelled")
            self.progress_bar.setValue(0)
            QTimer.singleShot(2000, lambda: (
                self.progress_bar.setVisible(False),
                self.progress_bar.setFormat("Ready"),
                self.progress_bar.setValue(0)
            ))
        elif st and st != "Ready":
            self.progress_bar.setVisible(True)
            self.progress_bar.setFormat(st)
        else:
            self.progress_bar.setVisible(False)
            self.progress_bar.setFormat("Ready")
            self.progress_bar.setValue(0)
        if "Download Completed" in st:
            self.tray_manager.show_download_completed_message()
            # History page refreshes automatically via showEvent when visible
            user_choice = QMessageBox.question(self, "Download Completed", "Open Download Folder?", QMessageBox.Yes | QMessageBox.No)
            if user_choice == QMessageBox.Yes:
                self.open_download_folder()
        elif "Download Error" in st:
            self.tray_manager.show_download_error_message()
            QMessageBox.critical(self, "Error", st)
        elif "Cancelled" in st:
            self.tray_manager.show_download_cancelled_message()
    def update_queue_info(self, row, title, channel):
        if row is not None and hasattr(self, 'page_queue') and hasattr(self.page_queue, 'queue_table'):
            if row < self.page_queue.queue_table.rowCount():
                self.page_queue.queue_table.setItem(row, 0, QTableWidgetItem(title))
                self.page_queue.queue_table.setItem(row, 1, QTableWidgetItem(channel))
                url = self.page_queue.queue_table.item(row, 2).text()
                # History will be written directly by the downloader
    def open_download_folder(self):
        folder = self.user_profile.get_download_path()
        if not os.path.exists(folder):
            QMessageBox.warning(self, "Folder Not Found", 
                f"Download folder does not exist:\n{folder}\n\n"
                "The folder may have been deleted or the drive may be disconnected.\n"
                "Please select a new download location in Settings.")
            self.append_log(f"Cannot open folder - path does not exist: {folder}")
            return
        
        try:
            if sys.platform.startswith('win'):
                os.startfile(folder)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', folder])
            else:
                subprocess.run(['xdg-open', folder])
        except (OSError, subprocess.SubprocessError, FileNotFoundError) as e:
            QMessageBox.warning(self, "Error", f"Could not open folder: {str(e)}")
            self.append_log(f"Failed to open folder: {str(e)}")
    def append_log(self, text):
        self.log_manager.append_log(text)
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
        
        from core.history import HISTORY_FILE
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            
        if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
            self.page_history.history_table.setRowCount(0)
            
        if self.user_profile.data.get("profile_picture") and os.path.exists(self.user_profile.data["profile_picture"]):
            try:
                os.remove(self.user_profile.data["profile_picture"])
            except OSError as e:
                self.append_log(f"Warning: Could not remove profile picture: {e}")
        
        QMessageBox.information(self, "Reset Profile", "Profile data, history, and profile picture removed. Please restart.")
        self.append_log("Profile, history, and profile picture have been reset.")
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
        self.theme_manager.change_theme(theme)
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
    def initialize_history(self):
       
        if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
            from core.history import load_history_initial
            load_history_initial(self.page_history.history_table)

    def quit_app(self):
        if hasattr(self, 'tray_manager'):
            self.tray_manager.hide()
        QApplication.quit()

    def closeEvent(self, event):
        if event.spontaneous():  
            self.tray_manager.handle_window_close()
            event.ignore()
        else: 
            self.quit_app()
            event.accept()

    def show_warning(self, title, message):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, title, message)

    def show_question(self, title, message):
        from PySide6.QtWidgets import QMessageBox
        return QMessageBox.question(self, title, message) == QMessageBox.Yes

    def add_history_entry(self, url, title="", channel=""):
        if hasattr(self, 'page_history') and hasattr(self.page_history, 'history_table'):
            from core.history import add_history_entry
            add_history_entry(self.page_history.history_table, title, channel, url, True)

    def check_for_updates(self):
        self.update_manager.check_for_updates()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    
    window = MainWindow()
    theme = window.user_profile.get_theme()
    if theme == "Dark":
        window.setStyleSheet(window.theme_manager.get_current_theme_stylesheet())
    else:
        window.setStyleSheet(window.theme_manager.get_current_theme_stylesheet())
    
    window.show()
    sys.exit(app.exec_())