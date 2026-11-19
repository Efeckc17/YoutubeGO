from dataclasses import dataclass
from typing import Optional
import requests


@dataclass(frozen=True)
class ReleaseInfo:
    """Represents release metadata returned by a release relay."""

    version: str
    url: str
    source: str


class GitLabRelay:
    """Secondary release relay that fetches the latest release from GitLab."""

    DEFAULT_RELEASES_PAGE = "https://gitlab.com/efecekic17/youtubego/-/releases"
    DEFAULT_API_URL = (
        "https://gitlab.com/api/v4/projects/efecekic17%2Fyoutubego/releases"
    )

    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        releases_page_url: str = DEFAULT_RELEASES_PAGE,
        timeout: int = 10,
    ):
        self.api_url = api_url
        self.releases_page_url = releases_page_url
        self.timeout = timeout

    def fetch_latest_release(
        self, headers: Optional[dict] = None
    ) -> ReleaseInfo:
        """Fetch the latest release tag and download page URL from GitLab."""
        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        response = requests.get(
            self.api_url,
            headers=request_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        releases = response.json()
        if not isinstance(releases, list) or not releases:
            raise ValueError("No releases found on GitLab")

        latest = releases[0]
        tag_name = latest.get("tag_name")
        if not tag_name:
            raise ValueError("Latest GitLab release is missing tag_name")

        links = latest.get("_links") or {}
        release_url = links.get("self") or self.releases_page_url
        return ReleaseInfo(version=tag_name, url=release_url, source="GitLab")
