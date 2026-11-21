from PySide6.QtWidgets import (QWidget, QHBoxLayout, QListWidget, QListWidgetItem,
                            QFrame, QAbstractItemView, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
from ui.components.icons import get_icon

class SideMenuLayout:
    MENU_ITEMS = ["Home", "Video", "Audio", "History", "Settings", "Profile", "Queue", "Scheduler"]

    def __init__(self, parent):
        self.parent = parent
        self.container = QWidget()
        self.container.setFixedWidth(240)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self.container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.side_menu = QListWidget()
        self.side_menu.setFixedWidth(220)
        self.side_menu.setIconSize(QSize(20, 20))
        self.side_menu.setSelectionMode(QAbstractItemView.SingleSelection)
        self.side_menu.setFlow(QListWidget.TopToBottom)
        self.side_menu.setSpacing(2)
        self.side_menu.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.side_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.side_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for item_name in self.MENU_ITEMS:
            item = QListWidgetItem(item_name)
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.side_menu.addItem(item)

        self.update_icons()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.side_menu.setGraphicsEffect(shadow)

        self.side_menu.setCurrentRow(0)
        self.side_menu.currentRowChanged.connect(self.parent.side_menu_changed)

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.VLine)

        layout.addWidget(self.side_menu)
        layout.addWidget(separator)

    def update_icons(self):
        is_dark = True
        if hasattr(self.parent, "theme_manager"):
            is_dark = self.parent.theme_manager.current_theme == "Dark"
        icon_color = "#cbd5e1" if is_dark else "#475569"
        for i, item_name in enumerate(self.MENU_ITEMS):
            item = self.side_menu.item(i)
            if item is not None:
                item.setIcon(get_icon(item_name, color=icon_color, selected_color="#ffffff", size=20))
