from PySide6.QtWidgets import QMenuBar, QMessageBox, QDialog, QVBoxLayout, QTextBrowser
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import requests

class LicenseDialog(QDialog):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml(content)
        layout.addWidget(text_browser)

class MenuBarManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = None
        self.init_menu_bar()

    def init_menu_bar(self):
        self.menu_bar = self.main_window.menuBar()
        
        # File Menu
        file_menu = self.menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        
        reset_profile_action = QAction("Reset Profile", self.main_window)
        reset_profile_action.triggered.connect(self.main_window.reset_profile)
        
        export_profile_action = QAction("Export Profile", self.main_window)
        export_profile_action.triggered.connect(self.main_window.profile_manager.export_profile)
        
        import_profile_action = QAction("Import Profile", self.main_window)
        import_profile_action.triggered.connect(self.main_window.profile_manager.import_profile)
        
        file_menu.addAction(exit_action)
        file_menu.addAction(reset_profile_action)
        file_menu.addAction(export_profile_action)
        file_menu.addAction(import_profile_action)
        
        
        help_menu = self.menu_bar.addMenu("Help")
        
        mail_action = QAction("Contact: toxi360@workmail.com", self.main_window)
        mail_action.triggered.connect(self.show_contact_info)
        
        github_action = QAction("Github: https://github.com/Efeckc17", self.main_window)
        github_action.triggered.connect(self.show_github_info)
        
        # Licenses submenu
        licenses_menu = help_menu.addMenu("Licenses")
        
        # YoutubeGO License
        youtubego_license = QAction("YoutubeGO License", self.main_window)
        youtubego_license.triggered.connect(self.show_youtubego_license)
        licenses_menu.addAction(youtubego_license)
        
        # Qt/PySide6 License
        qt_license = QAction("Qt/PySide6 License", self.main_window)
        qt_license.triggered.connect(self.show_qt_license)
        licenses_menu.addAction(qt_license)
        
        # FFmpeg License
        ffmpeg_license = QAction("FFmpeg License", self.main_window)
        ffmpeg_license.triggered.connect(self.show_ffmpeg_license)
        licenses_menu.addAction(ffmpeg_license)
        
        help_menu.addAction(mail_action)
        help_menu.addAction(github_action)

    def show_contact_info(self):
        QMessageBox.information(self.main_window, "Contact", "For support: toxi360@workmail.com")

    def show_github_info(self):
        QMessageBox.information(self.main_window, "GitHub", "https://github.com/Efeckc17")

    def show_youtubego_license(self):
        github_license_url = "https://raw.githubusercontent.com/Efeckc17/YoutubeGO/main/LICENSE"
        try:
            response = requests.get(github_license_url)
            if response.status_code == 200:
                license_text = response.text
            else:
                
                with open("LICENSE", "r", encoding="utf-8") as f:
                    license_text = f.read()
        except:
            
            with open("LICENSE", "r", encoding="utf-8") as f:
                license_text = f.read()
        
        dialog = LicenseDialog("YoutubeGO License (GPL v3)", f"<pre>{license_text}</pre>", self.main_window)
        dialog.exec()

    def show_qt_license(self):
        qt_license_url = "https://www.qt.io/licensing/"
        try:
            response = requests.get(qt_license_url)
            content = response.text
        except:
            content = """
            <h3>Qt/PySide6 License Information</h3>
            <p>Qt and PySide6 are licensed under the LGPL v3 license.</p>
            <p>For more information, visit: <a href="https://www.qt.io/licensing/">Qt Licensing</a></p>
            """
        
        dialog = LicenseDialog("Qt/PySide6 License", content, self.main_window)
        dialog.exec()

    def show_ffmpeg_license(self):
        ffmpeg_license_url = "https://www.ffmpeg.org/legal.html"
        try:
            response = requests.get(ffmpeg_license_url)
            content = response.text
        except:
            content = """
            <h3>FFmpeg License Information</h3>
            <p>FFmpeg is licensed under the LGPL v2.1+ and GPL v2+.</p>
            <p>For more information, visit: <a href="https://www.ffmpeg.org/legal.html">FFmpeg Legal</a></p>
            """
        
        dialog = LicenseDialog("FFmpeg License", content, self.main_window)
        dialog.exec()