class YoutubeDL:
    """Very small stub mimicking yt_dlp.YoutubeDL context manager used in downloader."""
    def __init__(self, params=None):
        self.params = params or {}
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def extract_info(self, url, download=False):
        # Return dummy info dictionary sufficient for tests/statements
        return {
            "title": "Dummy Title",
            "uploader": "Dummy Channel",
            "url": url,
            "formats": [],
            "entries": []
        }
    def download(self, urls):
        # No actual download in tests
        pass

class utils:  # noqa: N801 (mimic submodule)
    class DownloadError(Exception):
        pass