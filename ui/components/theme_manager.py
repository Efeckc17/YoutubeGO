import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
        base_path = os.path.abspath(os.path.join(base_path, "..", ".."))
    return os.path.join(base_path, relative_path)

class ThemeManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.user_profile = main_window.user_profile
        self.current_theme = self.user_profile.get_theme()

    def get_dark_theme(self):
        css_path = resource_path("ui/themes/dark.qss")
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_light_theme(self):
        css_path = resource_path("ui/themes/light.qss")
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_current_theme_stylesheet(self):
        if self.current_theme == "Dark":
            return self.get_dark_theme()
        else:
            return self.get_light_theme()

    def apply_current_theme(self):
        self.main_window.setStyleSheet(self.get_current_theme_stylesheet())
        if hasattr(self.main_window, "side_menu_layout"):
            self.main_window.side_menu_layout.update_icons()
        if hasattr(self.main_window, "page_home") and hasattr(self.main_window.page_home, "refresh_dashboard"):
            self.main_window.page_home.refresh_dashboard()

    def change_theme(self, theme):
        self.user_profile.set_theme(theme)
        self.current_theme = theme
        self.apply_current_theme()
        self.main_window.append_log(f"Theme changed to '{theme}'.") 