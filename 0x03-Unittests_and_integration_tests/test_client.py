#!/usr/bin/env python3

# 4. --- Parameterize and patch as decorators ---

"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),    # org_name for the first test case
        ("abc",),       # org_name for the second test case
    ])
    @patch('client.get_json')   # Patches 'client.get_json'
    def test_org(self, org_name, mock_get_json):
        """
        Tests that GithubOrgClient.org returns the correct value
        and theat utils.get_json is called once with the expected argument.
        """
        # The expected expected_url that GithubOrgClient.org will
        # construct will bebe defined based ont the org_name.
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Mock payload that the patched get_json should be returned.
        test_payload = {"login": org_name, "id": 12345,
                        "node_id": "some_node_id"}

        # Configured mock_json that will return the test_payload.
        mock_get_json.return_value = test_payload

        # Instantiate the GithubOrgClient with the current org_name from the
        # paramentrization.
        client = GithubOrgClient(org_name)

        result = client.org

        # Assertions:

        # 1. Verify that the mocked get_json was called exactly once
        # and with the correct expected expected_url.
        mock_get_json.assert_called_once_with(expected_url)

        # 2. Verify that the result returned by client.org is
        #    exactly the test_payload we configured for the mock.
        self.assertEqual(result, test_payload)

    # 5. --- Mocking a Property ---

    def test_public_repos_url(self):
        """
        Tests that _public_repos_url returns the correct URL based on
        a mocked org payload.
        """
        # The expected URL to be returned by _public_repos_url
        expected_repos_url = "https://api.github.com/orgs/some_org/repos"

        # The payload that the mocked GithubOrgClient.org property should
        # return.
        mock_org_payload = {"repos_url": expected_repos_url}

        # Context manager to mock the 'org' property of GithubOrgClient.
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload

            client = GithubOrgClient("some_org")

            # Access the _public_repos_url property.
            result = client._public_repos_url

            # Assertions:
            mock_org.assert_called_once()
            self.assertEqual(result, expected_repos_url)

    # 6. --- More Patching ---

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Tests that GithubOrgClient.public_repos returns the
        expected list of repos and that both
        _public_ropos_url and get_json are called once.
        """
        mock_api_repos_payload = [
            {"name": "alx-frontend-javascript", "license": {"key": "mit"}},
            {"name": "alx-frontend-python", "license": {"key": "apache-2.0"}},
            {"name": "some-other-repo", "license": None},
        ]
        expected_repos_payload = [
            "alx-frontend-javascript",
            "alx-frontend-python",
            "some-other-repo",
        ]
        mock_repose_url = "https://api.github.com/orgs/alx/repos"

        mock_get_json.return_value = mock_api_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repose_url

            client = GithubOrgClient("alx")

            result = client.public_repos()

            # Asserions:
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repose_url)
            self.assertEqual(result, expected_repos_payload)

    # 7. --- Parameterize ---
    @parameterized.expand([
        # Test case 1: Repo has the specific license
        ({"license": {"key": "my_license"}}, "my_license", True),
        # Test case 2: Repo has a different license
        ({"license": {"key": "other_license"}}, "my_license", False),
        # Test case 3: Repo has a license but key is None
        ({"license": {"key": None}}, "my_license", False),
        # Test case 4: Repo has no license key
        ({"license": None}, "my_license", False),
        # Test case 5: Repo directory desn't even have a license key
        ({}, "my_license", False),
        # Matching license but additional fileds present (shouldn't break)
        ({"license": {"key": "my_license", "name": "MIT"}},
         "my_license", True),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Tests that GithubOrgClient.has_license returns the correc
        boolean value
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)
