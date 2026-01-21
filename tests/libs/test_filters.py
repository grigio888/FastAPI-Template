"""
Test Filters Module.

This module tests the filter functions in src/libs/filters.py.
"""

import unittest

from src.libs.utilities.filters import apply_filter, filter_exclude, filter_only


class TestFilters(unittest.TestCase):
    """Test filter functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_info = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secret",
            "role": "admin",
        }

    def test_apply_filter_no_parameters(self):
        """Test apply_filter with no filtering parameters."""
        parameters = {}

        result = apply_filter(parameters, self.test_info)

        self.assertEqual(result, self.test_info)

    def test_apply_filter_only_fields(self):
        """Test apply_filter with 'only' parameter."""
        parameters = {"only": "name,email"}

        result = apply_filter(parameters, self.test_info)

        expected = {"name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_apply_filter_exclude_fields(self):
        """Test apply_filter with 'exclude' parameter."""
        parameters = {"exclude": "password,role"}

        result = apply_filter(parameters, self.test_info)

        expected = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_apply_filter_both_parameters_error(self):
        """Test apply_filter with both 'only' and 'exclude' parameters."""
        parameters = {"only": "name", "exclude": "password"}

        with self.assertRaises(AttributeError) as context:
            apply_filter(parameters, self.test_info)

        self.assertIn(
            "Only one of 'only' and 'exclude' can be used",
            str(context.exception),
        )

    def test_filter_only_valid_fields(self):
        """Test filter_only with valid fields."""
        filters = ["name", "email"]

        result = filter_only(self.test_info, filters)

        expected = {"name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_filter_only_nonexistent_fields(self):
        """Test filter_only with non-existent fields."""
        filters = ["nonexistent1", "nonexistent2"]

        with self.assertRaises(ValueError) as context:
            filter_only(self.test_info, filters)

        self.assertIn("No fields to show after filtering", str(context.exception))

    def test_filter_only_mixed_fields(self):
        """Test filter_only with mix of valid and invalid fields."""
        filters = ["name", "nonexistent", "email"]

        result = filter_only(self.test_info, filters)

        expected = {"name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_filter_only_empty_filters(self):
        """Test filter_only with empty filters list."""
        filters = []

        with self.assertRaises(ValueError) as context:
            filter_only(self.test_info, filters)

        self.assertIn("No fields to show after filtering", str(context.exception))

    def test_filter_exclude_valid_fields(self):
        """Test filter_exclude with valid fields."""
        filters = ["password", "role"]

        result = filter_exclude(self.test_info, filters)

        expected = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_filter_exclude_nonexistent_fields(self):
        """Test filter_exclude with non-existent fields."""
        filters = ["nonexistent1", "nonexistent2"]

        result = filter_exclude(self.test_info, filters)

        # Should return original info since no fields were excluded
        self.assertEqual(result, self.test_info)

    def test_filter_exclude_all_fields(self):
        """Test filter_exclude with all fields."""
        filters = list(self.test_info.keys())

        with self.assertRaises(ValueError) as context:
            filter_exclude(self.test_info, filters)

        self.assertIn("No fields left to show", str(context.exception))

    def test_filter_exclude_empty_filters(self):
        """Test filter_exclude with empty filters list."""
        filters = []

        result = filter_exclude(self.test_info, filters)

        # Should return original info
        self.assertEqual(result, self.test_info)

    def test_filter_exclude_mixed_fields(self):
        """Test filter_exclude with mix of valid and invalid fields."""
        filters = ["password", "nonexistent", "role"]

        result = filter_exclude(self.test_info, filters)

        expected = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_filter_only_single_field(self):
        """Test filter_only with single field."""
        filters = ["name"]

        result = filter_only(self.test_info, filters)

        expected = {"name": "John Doe"}
        self.assertEqual(result, expected)

    def test_filter_exclude_single_field(self):
        """Test filter_exclude with single field."""
        filters = ["password"]

        result = filter_exclude(self.test_info, filters)

        expected = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "role": "admin",
        }
        self.assertEqual(result, expected)

    def test_apply_filter_empty_info(self):
        """Test apply_filter with empty info dict."""
        parameters = {"only": "name,email"}
        empty_info = {}

        with self.assertRaises(ValueError):
            apply_filter(parameters, empty_info)

    def test_apply_filter_only_with_comma_separated_string(self):
        """Test apply_filter with comma-separated string in 'only'."""
        parameters = {"only": "name,email,id"}

        result = apply_filter(parameters, self.test_info)

        expected = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)

    def test_apply_filter_exclude_with_comma_separated_string(self):
        """Test apply_filter with comma-separated string in 'exclude'."""
        parameters = {"exclude": "password,role"}

        result = apply_filter(parameters, self.test_info)

        expected = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
