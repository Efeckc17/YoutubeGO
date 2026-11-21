from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QListWidget)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from ui.components.animated_button import AnimatedButton
from ui.components.icons import get_icon
from core.utils import set_circular_pixmap
from core.version import get_version

class TopBarLayout:
    def __init__(self, parent):
        self.parent = parent
        self.container = QWidget()
        self.container.setMinimumHeight(100)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        
        profile_container = QVBoxLayout()
        self.profile_pic_label = QLabel()
        self.profile_pic_label.setFixedSize(50, 50)
        self.profile_pic_label.setAlignment(Qt.AlignCenter)
        pic_path = self.parent.user_profile.data["profile_picture"]
        if pic_path:
            set_circular_pixmap(self.profile_pic_label, pic_path)
        else:
            self.profile_pic_label.setPixmap(
                get_icon("Profile", color="#94a3b8", selected_color="#94a3b8", size=26).pixmap(26, 26)
            )
            self.profile_pic_label.setStyleSheet(
                "border: 1px solid rgba(148, 163, 184, 0.35); border-radius: 25px; background-color: rgba(148, 163, 184, 0.08);"
            )
        
        self.profile_name_label = QLabel(self.parent.user_profile.data["name"] if self.parent.user_profile.data["name"] else "User")
        self.profile_name_label.setFont(QFont("Arial", 10))
        
        profile_container.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)
        profile_container.addWidget(self.profile_name_label, alignment=Qt.AlignCenter)
        
        profile_widget = QWidget()
        profile_widget.setLayout(profile_container)
        
        
        pref_string = (f"Resolution: {self.parent.user_profile.get_default_resolution()}\n"
                      f"Theme: {self.parent.user_profile.get_theme()}\n"
                      f"Download Path: {self.parent.user_profile.get_download_path()}\n"
                      f"Proxy: {self.parent.user_profile.get_proxy()}\n")
        profile_widget.setToolTip(pref_string)
        
        layout.addWidget(profile_widget, alignment=Qt.AlignLeft)
        
        
        search_area_container = QWidget()
        search_area_layout = QVBoxLayout(search_area_container)
        search_area_layout.setContentsMargins(0, 0, 0, 0)
        search_area_layout.setSpacing(0)

        
        search_bar_row = QWidget()
        search_bar_row_layout = QHBoxLayout(search_bar_row)
        search_bar_row_layout.setContentsMargins(0, 0, 0, 0)
        search_bar_row_layout.setSpacing(10)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search in app...")
        self.search_edit.setFixedHeight(40)
        self.search_btn = AnimatedButton("Search")
        self.search_btn.setIcon(get_icon("Search", color="#ffffff", selected_color="#ffffff", size=16))
        self.search_btn.setIconSize(QSize(16, 16))
        self.search_btn.setFixedHeight(40)
        search_bar_row_layout.addWidget(self.search_edit)
        search_bar_row_layout.addWidget(self.search_btn)
        search_area_layout.addWidget(search_bar_row)

        
        self.search_result_list = QListWidget()
        self.search_result_list.setVisible(False)
        self.search_result_list.setMinimumHeight(250)
        self.search_result_list.setMaximumHeight(400)
        self.search_result_list.setMinimumWidth(400)
        self.search_result_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        search_area_layout.addWidget(self.search_result_list)

        layout.addWidget(search_area_container, stretch=1, alignment=Qt.AlignVCenter)
        