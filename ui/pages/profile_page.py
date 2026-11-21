import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QFileDialog, QGroupBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from core.utils import set_circular_pixmap
from ui.components.animated_button import AnimatedButton
from ui.components.icons import get_icon


class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(18)

        # Header
        header_col = QVBoxLayout()
        header_col.setSpacing(4)
        lbl = QLabel("Profile")
        lbl.setFont(QFont("Inter", 20, QFont.Bold))
        header_col.addWidget(lbl)

        sub_lbl = QLabel("Manage your display name, avatar, and active preferences")
        sub_lbl.setStyleSheet("font-size: 10.5pt; opacity: 0.7;")
        header_col.addWidget(sub_lbl)
        layout.addLayout(header_col)

        # Two-column balanced layout filling the page cleanly
        columns_row = QHBoxLayout()
        columns_row.setSpacing(18)

        # Left Column: Identity Card
        profile_group = QGroupBox("Identity")
        profile_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        profile_col = QVBoxLayout(profile_group)
        profile_col.setSpacing(14)

        self.avatar_preview = QLabel()
        self.avatar_preview.setFixedSize(96, 96)
        self.avatar_preview.setAlignment(Qt.AlignCenter)
        profile_col.addWidget(self.avatar_preview, 0, Qt.AlignHCenter)

        name_lbl = QLabel("Display Name")
        name_lbl.setStyleSheet("font-size: 9.5pt; font-weight: 600; opacity: 0.75;")
        profile_col.addWidget(name_lbl)

        self.profile_name_edit = QLineEdit()
        self.profile_name_edit.setPlaceholderText("Enter your name...")
        self.profile_name_edit.setText(self.parent.user_profile.data["name"])
        profile_col.addWidget(self.profile_name_edit)

        pic_controls = QHBoxLayout()
        pic_controls.setSpacing(10)

        pic_btn = AnimatedButton("Change Picture")
        pic_btn.setCursor(Qt.PointingHandCursor)
        pic_btn.clicked.connect(self.pick_pic)
        pic_controls.addWidget(pic_btn)

        self.remove_pic_btn = AnimatedButton("Remove")
        self.remove_pic_btn.setCursor(Qt.PointingHandCursor)
        self.remove_pic_btn.setVisible(bool(self.parent.user_profile.data["profile_picture"]))
        self.remove_pic_btn.clicked.connect(self.remove_pic)
        pic_controls.addWidget(self.remove_pic_btn)

        self.pic_label = QLabel("No file selected")
        self.pic_label.setStyleSheet("font-size: 9.5pt; opacity: 0.7;")
        if self.parent.user_profile.data["profile_picture"]:
            self.pic_label.setText(os.path.basename(self.parent.user_profile.data["profile_picture"]))
        pic_controls.addWidget(self.pic_label, 1)

        profile_col.addLayout(pic_controls)
        profile_col.addStretch(1)
        columns_row.addWidget(profile_group, 1)

        # Right Column: User Preferences Card
        self.preferences_group = QGroupBox("User Preferences")
        self.preferences_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preferences_layout = QGridLayout()
        self.preferences_layout.setVerticalSpacing(14)
        self.preferences_layout.setHorizontalSpacing(24)

        self.theme_value = QLabel()
        self.resolution_value = QLabel()
        self.audio_format_value = QLabel()
        self.download_path_value = QLabel()
        self.download_path_value.setWordWrap(True)
        self.history_value = QLabel()
        self.proxy_value = QLabel()
        self.proxy_value.setWordWrap(True)
        self.geo_country_value = QLabel()

        pref_rows = [
            ("Theme", self.theme_value),
            ("Default Resolution", self.resolution_value),
            ("Audio Format", self.audio_format_value),
            ("Download Path", self.download_path_value),
            ("History Enabled", self.history_value),
            ("Proxy", self.proxy_value),
            ("Geo-Bypass Country", self.geo_country_value),
        ]
        for row_idx, (key_text, val_lbl) in enumerate(pref_rows):
            key_lbl = QLabel(f"{key_text}:")
            key_lbl.setStyleSheet("font-size: 10pt; opacity: 0.7;")
            val_lbl.setStyleSheet("font-size: 10pt; font-weight: 600;")
            self.preferences_layout.addWidget(key_lbl, row_idx, 0, Qt.AlignTop)
            self.preferences_layout.addWidget(val_lbl, row_idx, 1, Qt.AlignTop)

        self.preferences_layout.setColumnStretch(1, 1)
        self.preferences_layout.setRowStretch(len(pref_rows), 1)
        self.preferences_group.setLayout(self.preferences_layout)
        columns_row.addWidget(self.preferences_group, 1)

        layout.addLayout(columns_row, 1)

        # Save Row
        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = AnimatedButton("Save Profile")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setFixedWidth(180)
        save_btn.clicked.connect(self.save_profile)
        save_row.addWidget(save_btn)
        layout.addLayout(save_row)

        self._update_avatar_preview(self.parent.user_profile.data["profile_picture"])
        self.refresh_preferences()

    def _update_avatar_preview(self, pic_path):
        if pic_path and os.path.exists(pic_path):
            set_circular_pixmap(self.avatar_preview, pic_path)
            self.avatar_preview.setStyleSheet("border: 2px solid #ff4444; border-radius: 48px;")
        else:
            self.avatar_preview.setPixmap(
                get_icon("Profile", color="#94a3b8", selected_color="#94a3b8", size=44).pixmap(44, 44)
            )
            self.avatar_preview.setStyleSheet(
                "border: 1px solid rgba(148, 163, 184, 0.35); border-radius: 48px; background-color: rgba(148, 163, 184, 0.08);"
            )

    def refresh_preferences(self):
        self.theme_value.setText(self.parent.user_profile.get_theme())
        self.resolution_value.setText(self.parent.user_profile.get_default_resolution())
        self.audio_format_value.setText(self.parent.user_profile.get_audio_format())
        self.download_path_value.setText(self.parent.user_profile.get_download_path())
        self.history_value.setText("Yes" if self.parent.user_profile.is_history_enabled() else "No")
        self.proxy_value.setText(self.parent.user_profile.get_proxy() or "Not Set")

        geo_country = self.parent.user_profile.get_geo_bypass_country()
        countries = self.parent.user_profile.get_available_geo_bypass_countries()
        country_name = countries.get(geo_country, geo_country)
        self.geo_country_value.setText(f"{country_name} ({geo_country})")

    def pick_pic(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.pic_label.setText(os.path.basename(path))
            self.pic_label.setProperty("selected_path", path)
            self.remove_pic_btn.setVisible(True)
            self._update_avatar_preview(path)

    def remove_pic(self):
        self.parent.user_profile.remove_profile_picture()
        self.pic_label.setText("No file selected")
        self.pic_label.setProperty("selected_path", "")
        self.remove_pic_btn.setVisible(False)
        self._update_avatar_preview("")
        self.parent.profile_pic_label.setPixmap(
            get_icon("Profile", color="#94a3b8", selected_color="#94a3b8", size=26).pixmap(26, 26)
        )
        self.parent.profile_name_label.setText("User")

    def save_profile(self):
        name = self.profile_name_edit.text().strip()
        if not name:
            self.parent.show_warning("Error", "Please provide a name.")
            return

        pic_path = self.pic_label.property("selected_path")
        if not pic_path:
            pic_path = self.parent.user_profile.data["profile_picture"]
        self.parent.user_profile.set_profile(
            name,
            pic_path,
            self.parent.user_profile.get_download_path()
        )
        self.parent.profile_manager.update_profile_ui()
        self.refresh_preferences()
        self.parent.show_info("Success", "Profile settings saved successfully.")

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_preferences()
