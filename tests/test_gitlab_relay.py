import unittest
from unittest.mock import MagicMock, patch

from core.updater import UpdateChecker
from relay.gitlab_relay import GitLabRelay, ReleaseInfo


class TestGitLabRelay(unittest.TestCase):
    @patch("relay.gitlab_relay.requests.get")
    def test_fetch_latest_release_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "tag_name": "v2.5.0",
                "_links": {
                    "self": "https://gitlab.com/efecekic17/youtubego/-/releases/v2.5.0"
                },
            }
        ]
        mock_get.return_value = mock_response

        relay = GitLabRelay()
        info = relay.fetch_latest_release()

        self.assertEqual(
            info,
            ReleaseInfo(
                version="v2.5.0",
                url="https://gitlab.com/efecekic17/youtubego/-/releases/v2.5.0",
                source="GitLab",
            ),
        )

    @patch("relay.gitlab_relay.requests.get")
    def test_fetch_latest_release_empty_raises(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        relay = GitLabRelay()
        with self.assertRaises(ValueError):
            relay.fetch_latest_release()


class TestUpdateCheckerFallback(unittest.TestCase):
    @patch("core.updater.requests.get")
    def test_fallback_to_gitlab_when_github_fails_update_available(self, mock_github_get):
        github_resp = MagicMock()
        github_resp.status_code = 403
        mock_github_get.return_value = github_resp

        checker = UpdateChecker()
        checker.current_version = "1.0.0"
        checker.gitlab_relay = MagicMock()
        checker.gitlab_relay.fetch_latest_release.return_value = ReleaseInfo(
            version="v1.2.0",
            url="https://gitlab.com/efecekic17/youtubego/-/releases/v1.2.0",
            source="GitLab",
        )

        available_calls = []
        status_calls = []
        checker.update_available.connect(lambda v, u: available_calls.append((v, u)))
        checker.version_status.connect(lambda s, t: status_calls.append((s, t)))

        checker.check_for_updates()

        self.assertEqual(
            available_calls,
            [("v1.2.0", "https://gitlab.com/efecekic17/youtubego/-/releases/v1.2.0")],
        )
        self.assertEqual(
            status_calls,
            [("Update to v1.2.0 available", "update-available")],
        )

    @patch("core.updater.requests.get")
    def test_fallback_to_gitlab_up_to_date(self, mock_github_get):
        github_resp = MagicMock()
        github_resp.status_code = 404
        mock_github_get.return_value = github_resp

        checker = UpdateChecker()
        checker.current_version = "1.2.0"
        checker.gitlab_relay = MagicMock()
        checker.gitlab_relay.fetch_latest_release.return_value = ReleaseInfo(
            version="v1.2.0",
            url="https://gitlab.com/efecekic17/youtubego/-/releases/v1.2.0",
            source="GitLab",
        )

        available_calls = []
        status_calls = []
        checker.update_available.connect(lambda v, u: available_calls.append((v, u)))
        checker.version_status.connect(lambda s, t: status_calls.append((s, t)))

        checker.check_for_updates()

        self.assertEqual(available_calls, [])
        self.assertEqual(status_calls, [("Up to date", "up-to-date")])

    @patch("core.updater.requests.get")
    def test_both_relays_fail_emits_error(self, mock_github_get):
        github_resp = MagicMock()
        github_resp.status_code = 500
        mock_github_get.return_value = github_resp

        checker = UpdateChecker()
        checker.gitlab_relay = MagicMock()
        checker.gitlab_relay.fetch_latest_release.side_effect = RuntimeError("GitLab down")

        error_calls = []
        status_calls = []
        checker.update_error.connect(lambda msg: error_calls.append(msg))
        checker.version_status.connect(lambda s, t: status_calls.append((s, t)))

        checker.check_for_updates()

        self.assertEqual(len(error_calls), 1)
        self.assertEqual(status_calls, [("Update check failed", "error")])


if __name__ == "__main__":
    unittest.main()
