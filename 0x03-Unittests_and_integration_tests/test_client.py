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
