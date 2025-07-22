#!/usr/bin/env python3
"""
Unit and Integration tests for the GithubOrgClient class.
"""
import unittest
import requests  # Import requests for mocking
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch, PropertyMock
from client import GithubOrgClient

# Import fixtures - ensure fixtures.py is correctly set up
try:
    from fixtures import org_payload, repos_payload
    from fixtures import expected_repos, apache2_repos
except ImportError:
    org_payload = {"repos_url": "https://api.github.com/orgs/dummy/repos",
                   "login": "dummy_org"}
    repos_payload = [{"name": "dummy-repo", "license": {"key": "mit"}}]
    expected_repos = ["dummy-repo"]
    apache2_repos = ["dummy-repo"]


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Tests that GithubOrgClient.org returns the correct value
        and that utils.get_json is called once with the expected argument.
        """
        expected_url = f"https://api.github.com/orgs/{org_name}"
        test_payload = {"login": org_name, "id": 12345,
                        "node_id": "some_node_id"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """
        Tests that _public_repos_url returns the correct URL based on
        a mocked org payload.
        """
        expected_repos_url = "https://api.github.com/orgs/some_org/repos"
        mock_org_payload = {"repos_url": expected_repos_url}

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload

            client = GithubOrgClient("some_org")
            result = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(result, expected_repos_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Tests that GithubOrgClient.public_repos returns the
        expected list of repos and that both
        _public_repos_url and get_json are called once.
        """
        mock_api_repos_payload = [
            {"name": "alx-frontend-javascript", "license": {"key": "mit"}},
            {"name": "alx-frontend-python", "license": {"key": "apache-2.0"}},
            {"name": "some-other-repo", "license": None},
        ]
        expected_repos_output = [
            "alx-frontend-javascript",
            "alx-frontend-python",
            "some-other-repo",
        ]
        # Corrected typo: "mock_repos_url" instead of "mock_repose_url"
        mock_repos_url = "https://api.github.com/orgs/alx/repos"

        mock_get_json.return_value = mock_api_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repos_url

            client = GithubOrgClient("alx")

            result = client.public_repos()

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repos_url)
            self.assertEqual(result, expected_repos_output)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": {"key": None}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {"key": "my_license", "name": "MIT"}},
         "my_license", True),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Tests that GithubOrgClient.has_license returns the correct
        boolean value.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


# --- Integration Test Class for Task 8 ---
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos,
    mocking only external requests.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up class-wide mocks for requests.get.
        This mock will handle HTTP requests made by the GithubOrgClient.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def test_payloads_side_effect(url):
            mock_response = Mock()
            org_url_prefix = cls.org_payload["repos_url"].replace("/repos", "")

            if url == org_url_prefix:
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                raise ValueError(f"URL not mocked by side_effect: {url}")
            return mock_response

        cls.mock_get.side_effect = test_payloads_side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher to clean up mocks after all tests in the
        class have run.
        """
        cls.get_patcher.stop()

    def test_setup_works(self):
        """
        A minimal test to ensure setUpClass and TearDownClass execute
        without error.
        """
        self.assertTrue(True)
