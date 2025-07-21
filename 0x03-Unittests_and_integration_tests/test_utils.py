#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function in utils.py.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


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
