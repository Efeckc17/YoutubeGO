import os
import sys
import json
import platform
import requests
import webbrowser
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox, QLabel
from core.version import VERSION, get_version
from relay.gitlab_relay import GitLabRelay

class UpdateChecker(QObject):
    update_available = Signal(str, str)
    update_error = Signal(str)
    version_status = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.current_version = VERSION
        self.github_api_url = "https://api.github.com/repos/Efeckc17/YouTubeGO/releases/latest"
        self.gitlab_relay = GitLabRelay()
        self.headers = {
            "User-Agent": f"YouTubeGO/{VERSION} ({platform.system()} {platform.release()})",
            "Accept": "application/vnd.github.v3+json"
        }

    def check_for_updates(self):
        try:
            latest_version, html_url = self._fetch_from_github()
        except Exception as github_error:
            try:
                release_info = self.gitlab_relay.fetch_latest_release(
                    headers={"User-Agent": self.headers["User-Agent"]}
                )
                latest_version, html_url = release_info.version, release_info.url
            except Exception as gitlab_error:
                self.update_error.emit(
                    f"Error checking for updates (GitHub: {github_error}; GitLab: {gitlab_error})"
                )
                self.version_status.emit("Update check failed", "error")
                return

        if self._compare_versions(latest_version, self.current_version) > 0:
            self.update_available.emit(latest_version, html_url)
            self.version_status.emit(f"Update to {latest_version} available", "update-available")
        else:
            self.version_status.emit("Up to date", "up-to-date")

    def _fetch_from_github(self):
        response = requests.get(self.github_api_url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}")
        release_data = response.json()
        latest_version = release_data["tag_name"]
        html_url = release_data["html_url"]
        return latest_version, html_url

    def _compare_versions(self, version1, version2):
        v1_parts = [int(x) for x in version1.lstrip('v').split('.')]
        v2_parts = [int(x) for x in version2.lstrip('v').split('.')]
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0

class UpdateManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.checker = UpdateChecker()
        self.checker.update_available.connect(self._handle_update_available)
        self.checker.update_error.connect(self._handle_update_error)
        self.checker.version_status.connect(self._handle_version_status)

    def check_for_updates(self):
        self.checker.check_for_updates()

    def _handle_update_available(self, version, html_url):
        source = "GitLab" if "gitlab.com" in html_url else "GitHub"
        reply = QMessageBox.question(
            self.parent,
            "Update Available",
            f"A new version ({version}) is available. Would you like to download it from {source}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            webbrowser.open(html_url)

    def _handle_update_error(self, error_message):
        QMessageBox.warning(self.parent, "Update Error", error_message)

    def _handle_version_status(self, status, status_type):
        if hasattr(self.parent, 'page_settings'):
            version_label = self.parent.page_settings.findChild(QLabel, "version_label")
            if version_label:
                version_label.setText(f"Version {get_version()} • {status}")
                if status_type == "up-to-date":
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
                elif status_type == "update-available":
                    version_label.setStyleSheet("""
                        QLabel {
                            color: #FFC107;
                            padding: 6px 16px;
                            border-radius: 15px;
                            background: rgba(255, 193, 7, 0.1);
                            font-size: 12pt;
                            font-weight: bold;
                            border: 1px solid rgba(255, 193, 7, 0.2);
                            margin: 5px;
                        }
                        QLabel:hover {
                            background: rgba(255, 193, 7, 0.15);
                            border: 1px solid rgba(255, 193, 7, 0.3);
                        }
                    """)
                else:  
                    version_label.setStyleSheet("""
                        QLabel {
                            color: #F44336;
                            padding: 6px 16px;
                            border-radius: 15px;
                            background: rgba(244, 67, 54, 0.1);
                            font-size: 12pt;
                            font-weight: bold;
                            border: 1px solid rgba(244, 67, 54, 0.2);
                            margin: 5px;
                        }
                        QLabel:hover {
                            background: rgba(244, 67, 54, 0.15);
                            border: 1px solid rgba(244, 67, 54, 0.3);
                        }
                    """) 