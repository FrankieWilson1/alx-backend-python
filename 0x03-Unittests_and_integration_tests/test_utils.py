#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function and get_json
functions in utils.py.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test accessing a nested map with a valid path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # --- 1. Using the assertRaises context manager to test for key raises---
    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_message):
        """
        Tests that access_nested_map raises a KeyError with the
        expected message for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_message}'")

# 2. --- Mock HTTP Calls ---


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com/", {"key": "True"}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Tests that get_json returns the expected Json payload
        and mocks HTTP requests.
        """
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


# 3. --- Parameterized and Patch ----

class TestMemoize(unittest.TestCase):
    """
    Tests for the memoize decorator.
    """

    def test_memoize(self):
        """
        Tests that a method decorated with @memoize is called only once
        even if accessed multiple times.
        """
        class TestClass:
            """
            A test class to demonstrate the memoization.
            """

            def a_method(self):
                """
                A simple method that returns 42.
                This method will be mocked to track calls.
                """
                return 42

            @memoize
            def a_property(self):
                """"
                A property that memoize the result of a_method.
                """
                return self.a_method()

        # Tracks if 'a_method' is called and controls it's return value.
        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42

            # An instace of TestClass
            test_instance = TestClass()

            # Access the memoized property twice
            reuslt1 = test_instance.a_property
            reuslt2 = test_instance.a_property

            # Assertions:
            # Case: memoized property returns the correct value on both
            # accesses.
            self.assertEqual(reuslt1, 42)
            self.assertEqual(reuslt2, 42)

            # Original method called once.
            mock_a_method.assert_called_once()
