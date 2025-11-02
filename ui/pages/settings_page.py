from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QGroupBox, QFormLayout, QLineEdit, QComboBox, 
                            QFileDialog, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.components.animated_button import AnimatedButton
from core.version import get_version

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)
        
    
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        lbl = QLabel("Settings")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        
        version_label = QLabel(f"Version {get_version()}")
        version_label.setObjectName("version_label")
        version_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                padding: 6px 16px;
                border-radius: 15px;
                background: rgba(76, 175, 80, 0.1);
                font-size: 12pt;
                font-weight: bold;
                border: 1px solid rgba(76, 175, 80, 0.2);
                margin: 5px;
            }
            QLabel:hover {
                background: rgba(76, 175, 80, 0.15);
                border: 1px solid rgba(76, 175, 80, 0.3);
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setCursor(Qt.CursorShape.PointingHandCursor)
        version_label.mousePressEvent = lambda e: self.parent.check_for_updates()
        version_label.setToolTip(
            "YoutubeGO Version Information\n\n"
            "Click to check for updates:\n"
            "• Automatic update detection\n"
            "• Download latest features\n"
            "• Get bug fixes and improvements\n\n"
            "Stay updated for best performance!"
        )
        
        header_layout.addStretch()
        header_layout.addWidget(lbl, alignment=Qt.AlignCenter)
        header_layout.addStretch()
        header_layout.addWidget(version_label, alignment=Qt.AlignVCenter)
        
        layout.addWidget(header_container)

        # Concurrent Downloads Group
        g_con = QGroupBox("Max Concurrent Downloads")
        g_con.setMinimumWidth(300)
        g_layout = QHBoxLayout(g_con)
        g_layout.setContentsMargins(10, 10, 10, 10)
        self.concurrent_combo = QComboBox()
        self.concurrent_combo.addItems(["1","2","3","4","5","10"])
        self.concurrent_combo.setCurrentText(str(self.parent.max_concurrent_downloads))
        self.concurrent_combo.currentIndexChanged.connect(self.set_max_concurrent_downloads)
        self.concurrent_combo.setToolTip(
            "Maximum simultaneous downloads:\n"
            "• 1 - Single download (safest, slowest)\n"
            "• 2-3 - Balanced performance\n"
            "• 4-5 - Fast downloads (recommended)\n"
            "• 10 - Maximum speed (may cause issues)\n\n"
            "Higher numbers = faster but more CPU/network usage"
        )
        g_layout.addWidget(QLabel("Concurrent:"))
        g_layout.addWidget(self.concurrent_combo)
        layout.addWidget(g_con)

        # Technical Group
        g_tech = QGroupBox("Technical / Appearance")
        g_tech.setMinimumWidth(300)
        fl = QFormLayout(g_tech)
        fl.setContentsMargins(10, 10, 10, 10)
        fl.setSpacing(10)
        self.proxy_edit = QLineEdit()
        self.proxy_edit.setText(self.parent.user_profile.get_proxy())
        self.proxy_edit.setPlaceholderText("Proxy or bandwidth limit...")
        self.proxy_edit.textChanged.connect(self.proxy_changed)
        self.proxy_edit.setToolTip(
            "Proxy/Bandwidth settings:\n"
            "• HTTP Proxy: http://proxy.server.com:8080\n"
            "• SOCKS5 Proxy: socks5://proxy.server.com:1080\n"
            "• Bandwidth limit: --limit-rate 1M\n\n"
            "Leave empty for direct connection"
        )
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark","Light"])
        self.theme_combo.setCurrentText(self.parent.user_profile.get_theme())
        self.theme_combo.currentTextChanged.connect(self.theme_changed)
        self.theme_combo.setToolTip(
            "Application theme:\n"
            "• Dark - Easy on eyes, modern look\n"
            "• Light - Traditional interface\n\n"
            "Changes apply immediately"
        )
        fl.addRow("Proxy/BW:", self.proxy_edit)
        fl.addRow("Theme:", self.theme_combo)
        layout.addWidget(g_tech)

        # Resolution Group
        g_res = QGroupBox("Default Resolution")
        g_res.setMinimumWidth(300)
        r_hl = QHBoxLayout(g_res)
        r_hl.setContentsMargins(10, 10, 10, 10)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["144p","240p","360p","480p","720p","1080p","1440p","2160p","4320p"])
        self.res_combo.setCurrentText(self.parent.user_profile.get_default_resolution())
        self.res_combo.currentTextChanged.connect(self.resolution_changed)
        self.res_combo.setToolTip(
            "Default video resolution:\n"
            "• 144p-360p - Low quality, small files\n"
            "• 480p-720p - Good balance (recommended)\n"
            "• 1080p-1440p - High quality, larger files\n"
            "• 2160p-4320p - Ultra HD, very large files\n\n"
            "Higher resolution = better quality but slower downloads"
        )
        r_hl.addWidget(QLabel("Resolution:"))
        r_hl.addWidget(self.res_combo)
        layout.addWidget(g_res)

        # Audio Format Group
        g_audio = QGroupBox("Audio Format")
        g_audio.setMinimumWidth(300)
        a_hl = QHBoxLayout(g_audio)
        a_hl.setContentsMargins(10, 10, 10, 10)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(self.parent.user_profile.get_available_audio_formats())
        self.audio_format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        self.audio_format_combo.currentTextChanged.connect(self.audio_format_changed)
        self.audio_format_combo.setToolTip(
            "Audio format selection:\n"
            "• MP3 - Universal compatibility, lossy\n"
            "• M4A/AAC - Good quality, iOS friendly\n"
            "• FLAC - Lossless quality (large files)\n"
            "• OPUS - Modern, efficient codec\n"
            "• WAV - Uncompressed (very large files)\n"
            "• VORBIS - Open source alternative\n\n"
            "For best quality: FLAC > OPUS > M4A > MP3"
        )
        a_hl.addWidget(QLabel("Format:"))
        a_hl.addWidget(self.audio_format_combo)
        layout.addWidget(g_audio)

        # Audio Quality Group
        g_quality = QGroupBox("Audio Quality")
        g_quality.setMinimumWidth(300)
        q_layout = QFormLayout(g_quality)
        q_layout.setContentsMargins(10, 10, 10, 10)
        
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(self.parent.user_profile.get_available_audio_qualities())
        self.audio_quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        self.audio_quality_combo.currentTextChanged.connect(self.audio_quality_changed)
        self.audio_quality_combo.setToolTip(
            "Audio bitrate quality:\n"
            "• 128k - Basic quality (small file size)\n"
            "• 192k - Good quality\n"
            "• 256k - High quality\n"
            "• 320k - Maximum quality (larger file size)\n"
            "• best - Use original quality without re-encoding"
        )
        
        self.preserve_quality_combo = QComboBox()
        self.preserve_quality_combo.addItems(["Yes", "No"])
        current_preserve = "Yes" if self.parent.user_profile.get_preserve_quality() else "No"
        self.preserve_quality_combo.setCurrentText(current_preserve)
        self.preserve_quality_combo.currentTextChanged.connect(self.preserve_quality_changed)
        self.preserve_quality_combo.setToolTip(
            "Preserve Original Quality:\n"
            "• Yes - Use copy mode when possible (no quality loss)\n"
            "• No - Always re-encode audio (may reduce quality)\n\n"
            "Recommended: Yes for best audio quality"
        )
        
        q_layout.addRow("Bitrate (kbps):", self.audio_quality_combo)
        q_layout.addRow("Preserve Original:", self.preserve_quality_combo)
        layout.addWidget(g_quality)

        
        g_geo = QGroupBox("Geo-Bypass Settings")
        g_geo.setMinimumWidth(300)
        geo_layout = QFormLayout(g_geo)
        geo_layout.setContentsMargins(10, 10, 10, 10)
        
        self.geo_country_combo = QComboBox()
        countries = self.parent.user_profile.get_available_geo_bypass_countries()
        for code, name in countries.items():
            self.geo_country_combo.addItem(f"{name} ({code})", code)
        
        current_country = self.parent.user_profile.get_geo_bypass_country()
        for i in range(self.geo_country_combo.count()):
            if self.geo_country_combo.itemData(i) == current_country:
                self.geo_country_combo.setCurrentIndex(i)
                break
        
        self.geo_country_combo.currentIndexChanged.connect(self.geo_country_changed)
        self.geo_country_combo.setToolTip(
            "Geographic bypass country:\n"
            "• Don't Use - Disable geo-bypass (direct connection)\n"
            "• US - United States (default, most content)\n"
            "• RU - Russia (bypass EU restrictions)\n"
            "• DE - Germany (EU region access)\n"
            "• GB - United Kingdom (UK content)\n"
            "• JP - Japan (Asian content)\n"
            "• Other countries for specific regional content\n\n"
            "Changes which country's IP is simulated to bypass geo-blocks"
        )
        
        geo_layout.addRow("Country:", self.geo_country_combo)
        layout.addWidget(g_geo)

        # Download Path Group
        g_path = QGroupBox("Download Path")
        g_path.setMinimumWidth(300)
        p_hl = QHBoxLayout(g_path)
        p_hl.setContentsMargins(10, 10, 10, 10)
        self.download_path_edit = QLineEdit()
        self.download_path_edit.setReadOnly(True)
        self.download_path_edit.setText(self.parent.user_profile.get_download_path())
        self.download_path_edit.setToolTip(
            "Download destination folder:\n"
            "• All downloads will be saved here\n"
            "• Playlists create subfolders automatically\n"
            "• Make sure you have enough disk space\n\n"
            "Click Browse to change location"
        )
        
        b_br = AnimatedButton("Browse")
        b_br.clicked.connect(self.select_download_path)
        b_br.setToolTip("Click to select a different download folder")
        p_hl.addWidget(QLabel("Folder:"))
        p_hl.addWidget(self.download_path_edit)
        p_hl.addWidget(b_br)
        layout.addWidget(g_path)

        g_ffmpeg = QGroupBox("FFmpeg Status")
        g_ffmpeg.setMinimumWidth(300)
        ffmpeg_layout = QHBoxLayout(g_ffmpeg)
        ffmpeg_layout.setContentsMargins(10, 10, 10, 10)
        
        status_label = QLabel("Status:")
        status_label.setFixedWidth(60)
        
        self.ffmpeg_status_label = QLabel()
        self.ffmpeg_status_label.setAlignment(Qt.AlignCenter)
        
        if self.parent.ffmpeg_found:
            self.ffmpeg_status_label.setText("✓ FFmpeg Ready")
            self.ffmpeg_status_label.setStyleSheet("""
                QLabel {
                    color: #fff;
                    font-weight: bold;
                    font-size: 12pt;
                    padding: 8px 16px;
                    border-radius: 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #4CAF50, stop:1 #66BB6A);
                    border: 2px solid rgba(76, 175, 80, 0.3);
                }
            """)
            
            self.ffmpeg_status_label.setToolTip(
                f"FFmpeg Status: Ready\n"
                f"Path: {self.parent.ffmpeg_path}\n\n"
                "FFmpeg enables:\n"
                "• High-quality audio conversion\n"
                "• Copy mode (no quality loss)\n"
                "• Multiple format support\n"
                "• Advanced audio processing"
            )
            
        else:
            self.ffmpeg_status_label.setText("⚠️ FFmpeg Required")
            self.ffmpeg_status_label.setStyleSheet("""
                QLabel {
                    color: #fff;
                    font-weight: bold;
                    font-size: 12pt;
                    padding: 8px 16px;
                    border-radius: 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #ff9800, stop:1 #ffa726);
                    border: 2px solid rgba(255, 152, 0, 0.3);
                }
            """)
            
            self.ffmpeg_status_label.setToolTip(
                "FFmpeg Status: Not Found\n\n"
                "Why you need FFmpeg:\n"
                "• High-quality audio conversion\n"
                "• Multiple format support\n"
                "• Copy mode for lossless extraction\n\n"
                "How to install:\n"
                "• Download from: https://ffmpeg.org\n"
                "• Add to system PATH\n"
                "• Restart YoutubeGO after installation"
            )
        
        ffmpeg_layout.addWidget(status_label)
        ffmpeg_layout.addWidget(self.ffmpeg_status_label)
        ffmpeg_layout.addStretch()
        
        layout.addWidget(g_ffmpeg)

        g_logs = QGroupBox("Developer Tools")
        g_logs.setMinimumWidth(300)
        logs_layout = QHBoxLayout(g_logs)
        logs_layout.setContentsMargins(10, 10, 10, 10)
        
        logs_label = QLabel("Logs:")
        logs_label.setFixedWidth(60)
        
        self.show_logs_btn = AnimatedButton("Show Logs")
        self.show_logs_btn.setFixedWidth(120)
        self.show_logs_btn.setFixedHeight(36) 
        self.show_logs_btn.clicked.connect(self.toggle_logs)
        self.show_logs_btn.setToolTip(
            "Developer logs and debug information:\n"
            "• View real-time download progress\n"
            "• See detailed error messages\n"
            "• Monitor FFmpeg operations\n"
            "• Debug connection issues\n\n"
            "Useful for troubleshooting problems"
        )
        
        self.show_logs_btn.setStyleSheet("""
            AnimatedButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff4444, stop:1 #ff6666);
                color: #fff;
                border: none;
                border-radius: 12px;
                padding: 8px 16px;
                font-size: 11pt;
                font-weight: bold;
                min-height: 20px;
            }
            AnimatedButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff6666, stop:1 #ff4444);
            }
            AnimatedButton:pressed {
                background-color: #cc3333;
            }
        """)
        
        logs_info = QLabel("View application logs and debug information")
        logs_info.setStyleSheet("color: #666; font-size: 10pt;")
        
        logs_layout.addWidget(logs_label)
        logs_layout.addWidget(self.show_logs_btn)
        logs_layout.addWidget(logs_info)
        logs_layout.addStretch()
        
        layout.addWidget(g_logs)
        
        layout.addStretch()
        
        
        scroll.setWidget(container)

    def set_max_concurrent_downloads(self, idx):
        val = self.concurrent_combo.currentText()
        self.parent.max_concurrent_downloads = int(val)
        self.parent.append_log(f"Max concurrent downloads set to {val}")

    def proxy_changed(self, text):
        self.parent.user_profile.set_proxy(text)
        self.parent.append_log(f"Proxy setting updated: {text}")

    def theme_changed(self, theme):
        self.parent.user_profile.set_theme(theme)
        self.parent.theme_manager.change_theme(theme)
        self.parent.append_log(f"Theme changed to: {theme}")

    def resolution_changed(self, resolution):
        self.parent.user_profile.set_default_resolution(resolution)
        self.parent.append_log(f"Default resolution set to: {resolution}")

    def audio_format_changed(self, format):
        self.parent.user_profile.set_audio_format(format)
        self.parent.append_log(f"Audio format set to: {format}")

    def audio_quality_changed(self, quality):
        self.parent.user_profile.set_audio_quality(quality)
        self.parent.append_log(f"Audio quality set to: {quality} kbps")

    def preserve_quality_changed(self, preserve_text):
        preserve = preserve_text == "Yes"
        self.parent.user_profile.set_preserve_quality(preserve)
        mode = "enabled" if preserve else "disabled"
        self.parent.append_log(f"Quality preservation {mode}")

    def geo_country_changed(self, index):
        country_code = self.geo_country_combo.itemData(index)
        country_name = self.geo_country_combo.currentText()
        self.parent.user_profile.set_geo_bypass_country(country_code)
        self.parent.append_log(f"Geo-bypass country set to: {country_name}")

    def select_download_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.parent.user_profile.set_profile(
                self.parent.user_profile.data["name"],
                self.parent.user_profile.data["profile_picture"],
                folder
            )
            self.download_path_edit.setText(folder)
            self.parent.append_log(f"Download path changed to {folder}")

    def toggle_logs(self):
        self.parent.log_manager.toggle_visibility()
        
        if self.parent.log_manager.log_dock_visible:
            self.show_logs_btn.setText("Hide Logs")
        else:
            self.show_logs_btn.setText("Show Logs") 