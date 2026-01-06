"""
Test Utilities Module.

This module tests the utility functions in src/libs/utils.py.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import MagicMock

import unittest
from datetime import UTC, datetime
from unittest.mock import patch

from template.src.libs.utilities.misc import (
    clean_dict,
    generate_log_threshold,
    is_filled,
    order_dict,
    refresh_log_threshold,
    should_log,
)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_is_filled_with_filled_dict(self) -> None:
        """Test is_filled with a filled object."""
        obj = {"name": "test", "value": 123}

        result = is_filled(obj)

        assert result

    def test_is_filled_with_empty_dict(self) -> None:
        """Test is_filled with an empty object."""
        obj: dict = {}

        result = is_filled(obj)

        assert not result

    def test_is_filled_with_none_values(self) -> None:
        """Test is_filled with None values."""
        obj = {"name": None, "value": None}

        result = is_filled(obj)

        assert not result

    def test_is_filled_with_mixed_values(self) -> None:
        """Test is_filled with mixed values."""
        obj = {"name": None, "value": "test", "empty": ""}

        result = is_filled(obj)

        assert result

    def test_order_dict_simple(self) -> None:
        """Test ordering a simple dictionary."""
        data = {"z": 1, "a": 2, "m": 3}

        result = order_dict(data)

        expected = {"a": 2, "m": 3, "z": 1}
        assert result == expected
        assert list(result.keys()) == ["a", "m", "z"]

    def test_order_dict_nested(self) -> None:
        """Test ordering a nested dictionary."""
        data = {
            "z": {"c": 1, "a": 2},
            "a": {"z": 3, "b": 4},
        }

        result = order_dict(data)

        expected = {
            "a": {"b": 4, "z": 3},
            "z": {"a": 2, "c": 1},
        }
        assert result == expected

    def test_order_dict_empty(self) -> None:
        """Test ordering an empty dictionary."""
        data: dict = {}

        result = order_dict(data)

        assert result == {}

    def test_clean_dict_removes_none(self) -> None:
        """Test cleaning dictionary removes None values."""
        data = {"a": 1, "b": None, "c": 3}

        result = clean_dict(data)

        expected = {"a": 1, "c": 3}
        assert result == expected

    def test_clean_dict_removes_empty_collections(self) -> None:
        """Test cleaning dictionary removes empty collections."""
        data = {"a": 1, "b": [], "c": {}, "d": "test"}

        result = clean_dict(data)

        expected = {"a": 1, "d": "test"}
        assert result == expected

    def test_clean_dict_with_custom_values(self) -> None:
        """Test cleaning dictionary with custom values to remove."""
        data = {"a": 1, "b": "remove_me", "c": 3, "d": "remove_me"}

        result = clean_dict(data, values=["remove_me"])

        expected = {"a": 1, "c": 3}

        assert result == expected

    def test_clean_dict_nested(self) -> None:
        """Test cleaning nested dictionary."""
        data: dict = {
            "a": {"x": 1, "y": None, "z": []},
            "b": None,
            "c": {"m": 2, "n": {}},
        }

        result = clean_dict(data)

        expected = {
            "a": {"x": 1},
            "c": {"m": 2},
        }
        assert result == expected

    def test_clean_dict_empty(self) -> None:
        """Test cleaning empty dictionary."""
        data: dict = {}

        result = clean_dict(data)

        assert result == {}

    def test_should_log_true(self) -> None:
        """Test should_log returns True when current time is past threshold."""
        with patch(
            "src.libs.utils.LOG_TIME_THRESHOLD",
            datetime.now(tz=UTC).replace(year=2020),
        ):
            result = should_log()

        assert result

    def test_should_log_false(self) -> None:
        """Test should_log returns False when current time is before threshold."""
        with patch(
            "src.libs.utils.LOG_TIME_THRESHOLD",
            datetime.now(tz=UTC).replace(year=2030),
        ):
            result = should_log()

        assert not result

    @patch("src.libs.utils.LOG_THRESHOLD_UNIT", "minutes")
    @patch("src.libs.utils.LOG_THRESHOLD_VALUE", 30)
    def test_generate_log_threshold(self) -> None:
        """Test generating log threshold."""
        result = generate_log_threshold()

        # Should return a datetime object in the future
        assert isinstance(result, datetime)
        assert result > datetime.now(tz=UTC)

    @patch("src.libs.utils.generate_log_threshold")
    def test_refresh_log_threshold(self, mock_generate: "MagicMock") -> None:
        """Test refreshing log threshold."""
        new_threshold = datetime.now(tz=UTC)
        mock_generate.return_value = new_threshold

        refresh_log_threshold()

        # Should call generate_log_threshold
        mock_generate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
