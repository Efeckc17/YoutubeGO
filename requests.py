import json

class _Resp:
    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self._data = data or {}
    def json(self):
        return self._data

# Fake latest version older so no update.
_latest_release = {"tag_name": "v0.0.0", "html_url": "https://example.com"}

def get(url, headers=None):
    return _Resp(200, _latest_release)