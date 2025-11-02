import os
import json
import shutil
from core.utils import get_data_dir, get_images_dir

class UserProfile:
    def __init__(self, profile_path="user_profile.json"):
        self.data_dir = get_data_dir()
        self.images_dir = get_images_dir()
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        self.profile_path = os.path.join(self.data_dir, profile_path)
        self.data = {
            "name": "", 
            "profile_picture": "", 
            "default_resolution": "720p", 
            "download_path": os.getcwd(), 
            "history_enabled": True, 
            "theme": "Dark", 
            "proxy": "", 
            "audio_format": "mp3",
            "audio_quality": "320",
            "preserve_quality": True,
            "geo_bypass_country": "US"
        }
        self.load_profile()

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r", encoding="utf-8") as f:
                try:
                    self.data = json.load(f)
                    if "audio_format" not in self.data:  
                        self.data["audio_format"] = "mp3"
                    if "audio_quality" not in self.data:
                        self.data["audio_quality"] = "320"
                    if "preserve_quality" not in self.data:
                        self.data["preserve_quality"] = True
                    if "geo_bypass_country" not in self.data:
                        self.data["geo_bypass_country"] = "US"
                    self.save_profile()
                except json.JSONDecodeError as e:
                    print(f"Warning: Profile file corrupted, creating new one. Error: {e}")
                    self.save_profile()
                except (IOError, OSError) as e:
                    print(f"Warning: Cannot read profile file: {e}")
                    self.save_profile()
                except Exception as e:
                    print(f"Unexpected error loading profile: {e}")
                    self.save_profile()
        else:
            self.save_profile()

    def save_profile(self):
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def set_profile(self, name, profile_picture, download_path):
        if profile_picture and profile_picture != self.data.get("profile_picture", ""):
            if not os.path.exists(self.images_dir):
                os.makedirs(self.images_dir)
            
            try:
                if os.path.exists(profile_picture):
                    filename = f"profile_{os.path.basename(profile_picture)}"
                    new_path = os.path.join(self.images_dir, filename)
                    
                    old_pic = self.data.get("profile_picture", "")
                    if old_pic and os.path.exists(old_pic) and old_pic.startswith(self.images_dir):
                        try:
                            os.remove(old_pic)
                        except (OSError, PermissionError) as e:
                            print(f"Warning: Could not remove old profile picture: {e}")
                    
                    shutil.copy2(profile_picture, new_path)
                    self.data["profile_picture"] = new_path
                else:
                    print(f"Profile picture source not found: {profile_picture}")
                    if self.data.get("profile_picture") and os.path.exists(self.data["profile_picture"]):
                        pass
                    else:
                        self.data["profile_picture"] = ""
            except (OSError, PermissionError, shutil.Error) as e:
                print(f"Error handling profile picture: {e}")
                if self.data.get("profile_picture") and os.path.exists(self.data["profile_picture"]):
                    pass
                else:
                    self.data["profile_picture"] = ""

        self.data["name"] = name
        self.data["download_path"] = download_path
        self.save_profile()

    def remove_profile_picture(self):
        old_pic = self.data.get("profile_picture", "")
        if old_pic and os.path.exists(old_pic) and old_pic.startswith(self.images_dir):
            try:
                os.remove(old_pic)
            except (OSError, PermissionError) as e:
                print(f"Warning: Could not remove profile picture: {e}")
        self.data["profile_picture"] = ""
        self.save_profile()

    def get_download_path(self):
        return self.data.get("download_path", os.getcwd())

    def get_proxy(self):
        return self.data.get("proxy", "")

    def set_proxy(self, proxy):
        self.data["proxy"] = proxy
        self.save_profile()

    def get_theme(self):
        return self.data.get("theme", "Dark")

    def set_theme(self, theme):
        self.data["theme"] = theme
        self.save_profile()

    def get_default_resolution(self):
        return self.data.get("default_resolution", "720p")

    def set_default_resolution(self, resolution):
        self.data["default_resolution"] = resolution
        self.save_profile()

    def is_history_enabled(self):
        return self.data.get("history_enabled", True)

    def set_history_enabled(self, enabled):
        self.data["history_enabled"] = enabled
        self.save_profile()

    def is_profile_complete(self):
        return bool(self.data["name"])

    def get_audio_format(self):
        return self.data.get("audio_format", "mp3")

    def set_audio_format(self, format):
        self.data["audio_format"] = format
        self.save_profile()

    def get_available_audio_formats(self):
        return ["mp3", "m4a", "wav", "aac", "flac", "opus", "vorbis"]

    def get_audio_quality(self):
        return self.data.get("audio_quality", "320")

    def set_audio_quality(self, quality):
        self.data["audio_quality"] = quality
        self.save_profile()

    def get_available_audio_qualities(self):
        return ["128", "192", "256", "320", "best"]

    def get_preserve_quality(self):
        return self.data.get("preserve_quality", True)

    def set_preserve_quality(self, preserve):
        self.data["preserve_quality"] = preserve
        self.save_profile()

    def get_geo_bypass_country(self):
        return self.data.get("geo_bypass_country", "US")

    def set_geo_bypass_country(self, country):
        self.data["geo_bypass_country"] = country
        self.save_profile()

    def get_available_geo_bypass_countries(self):
        return {
            "NONE": "Don't Use",
            "US": "United States",
            "RU": "Russia",
            "DE": "Germany", 
            "GB": "United Kingdom",
            "FR": "France",
            "JP": "Japan",
            "CA": "Canada",
            "AU": "Australia",
            "NL": "Netherlands",
            "SE": "Sweden"
        }
