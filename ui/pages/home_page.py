import platform
import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton
from PySide6.QtCore import Qt, QObject, Signal, QRunnable, QThreadPool
from PySide6.QtGui import QFont
from core.version import VERSION, get_version
from relay.gitlab_relay import GitLabRelay
from ui.components.icons import get_icon


def _compare_versions(v1, v2):
    p1 = [int(x) for x in v1.lstrip("v").split(".")]
    p2 = [int(x) for x in v2.lstrip("v").split(".")]
    for i in range(max(len(p1), len(p2))):
        a = p1[i] if i < len(p1) else 0
        b = p2[i] if i < len(p2) else 0
        if a > b:
            return 1
        if a < b:
            return -1
    return 0


class _ReleaseCheckSignals(QObject):
    finished = Signal(str, str, str)  # source, status_text, state ("ok"|"update"|"error")


class _ReleaseCheckWorker(QRunnable):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

    def run(self):
        ua = f"YouTubeGO/{VERSION} ({platform.system()} {platform.release()})"
        try:
            resp = requests.get(
                "https://api.github.com/repos/Efeckc17/YouTubeGO/releases/latest",
                headers={"User-Agent": ua, "Accept": "application/vnd.github.v3+json"},
                timeout=6,
            )
            if resp.status_code == 200:
                tag = resp.json().get("tag_name", "")
                if tag and _compare_versions(tag, VERSION) > 0:
                    self.signals.finished.emit("github", f"{tag} available", "update")
                else:
                    self.signals.finished.emit("github", f"Up to date ({tag or VERSION})", "ok")
            else:
                self.signals.finished.emit("github", f"HTTP {resp.status_code}", "error")
        except Exception:
            self.signals.finished.emit("github", "Unreachable", "error")

        try:
            rel = GitLabRelay().fetch_latest_release(headers={"User-Agent": ua}, timeout=6)
            if _compare_versions(rel.version, VERSION) > 0:
                self.signals.finished.emit("gitlab", f"{rel.version} available", "update")
            else:
                self.signals.finished.emit("gitlab", f"Up to date ({rel.version})", "ok")
        except Exception:
            self.signals.finished.emit("gitlab", "Unreachable", "error")


class FeatureCard(QFrame):
    def __init__(self, title, description, page_index, parent=None):
        super().__init__(parent)
        self.setObjectName("featureCard")
        self.page_index = page_index

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        button = QPushButton("Go")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)

    def on_button_clicked(self):
        main_window = self.window()
        if main_window:
            main_window.side_menu_changed(self.page_index)


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._release_checked = False
        self._release_signals = _ReleaseCheckSignals()
        self._release_signals.finished.connect(self._on_release_status)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)

        welcome_label = QLabel(f"YoutubeGO {get_version()}")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(welcome_label)

        subtitle_label = QLabel("Video & Audio Downloader")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)

        # GitHub & GitLab Release Mirror Status
        mirror_row = QHBoxLayout()
        mirror_row.setSpacing(12)
        mirror_row.addStretch()

        self.github_badge = self._create_mirror_badge("GitHub", "Checking...")
        self.gitlab_badge = self._create_mirror_badge("GitLab", "Checking...")
        mirror_row.addWidget(self.github_badge)
        mirror_row.addWidget(self.gitlab_badge)
        mirror_row.addStretch()
        header_layout.addLayout(mirror_row)

        main_layout.addWidget(header_frame)

        features_frame = QFrame()
        features_frame.setObjectName("featuresFrame")
        features_layout = QVBoxLayout(features_frame)

        features_title = QLabel("Features")
        features_title.setFont(QFont("Arial", 16, QFont.Bold))
        features_layout.addWidget(features_title)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        features = [
            ("Video Download", "Download videos with various quality options", 1),
            ("Audio Download", "Download audio in your preferred format", 2),
            ("Download History", "View and manage your download history", 3),
            ("Settings", "Configure download settings and preferences", 4),
            ("Profile", "Manage your user profile and preferences", 5),
            ("Queue", "Manage multiple downloads in queue", 6)
        ]

        for i, (title, desc, page_index) in enumerate(features):
            card = FeatureCard(title, desc, page_index, self)
            grid_layout.addWidget(card, i // 2, i % 2)

        features_layout.addLayout(grid_layout)
        main_layout.addWidget(features_frame)

        main_layout.addStretch()

    def _create_mirror_badge(self, name, initial_text):
        badge = QFrame()
        badge.setObjectName("mirrorBadge")
        row = QHBoxLayout(badge)
        row.setContentsMargins(12, 6, 12, 6)
        row.setSpacing(8)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(16, 16)
        icon_lbl.setPixmap(get_icon(name, color="#94a3b8", selected_color="#94a3b8", size=16).pixmap(16, 16))
        row.addWidget(icon_lbl)

        text_lbl = QLabel(f"{name}: {initial_text}")
        text_lbl.setStyleSheet("font-size: 9.5pt; font-weight: 600;")
        row.addWidget(text_lbl)

        badge._icon_lbl = icon_lbl
        badge._text_lbl = text_lbl
        badge._name = name
        self._style_badge(badge, "#64748b")
        return badge

    def _style_badge(self, badge, accent):
        is_dark = True
        if self.parent and hasattr(self.parent, "theme_manager"):
            is_dark = self.parent.theme_manager.current_theme == "Dark"
        bg = "#181a20" if is_dark else "#ffffff"
        border = "#282c34" if is_dark else "#e2e8f0"
        badge.setStyleSheet(
            f"QFrame#mirrorBadge {{ background-color: {bg}; border: 1px solid {border}; border-radius: 10px; }}"
        )
        badge._icon_lbl.setPixmap(
            get_icon(badge._name, color=accent, selected_color=accent, size=16).pixmap(16, 16)
        )
        badge._accent = accent

    def _on_release_status(self, source, status_text, state):
        color_map = {"ok": "#22c55e", "update": "#f59e0b", "error": "#ef4444"}
        accent = color_map.get(state, "#64748b")
        badge = self.github_badge if source == "github" else self.gitlab_badge
        badge._text_lbl.setText(f"{badge._name}: {status_text}")
        self._style_badge(badge, accent)

    def refresh_dashboard(self):
        self._style_badge(self.github_badge, getattr(self.github_badge, "_accent", "#64748b"))
        self._style_badge(self.gitlab_badge, getattr(self.gitlab_badge, "_accent", "#64748b"))

    def showEvent(self, event):
        super().showEvent(event)
        if not self._release_checked:
            self._release_checked = True
            QThreadPool.globalInstance().start(_ReleaseCheckWorker(self._release_signals))
