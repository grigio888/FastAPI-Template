"""
Test Log Module.

This module tests the logging utilities in src/libs/log/.
"""

import logging
import re
import unittest
from unittest.mock import MagicMock, patch

from colorama import Fore, Style

from src.libs.log import get_context, get_logger, setup_logging
from src.libs.log.colors import ColoredFormatter
from src.libs.log.config import LOG_FORMAT, LOG_LEVEL, LOG_NAME
from src.libs.log.filters import SENSITIVE_PATTERNS, SensitiveDataFilter, replacement
from src.libs.log.levels import MaxLevelFilter


class TestLogConfig(unittest.TestCase):
    """Test log configuration."""

    def test_log_config_constants(self):
        """Test that log configuration constants are properly defined."""
        self.assertIsInstance(LOG_LEVEL, str)
        self.assertIsInstance(LOG_FORMAT, str)
        self.assertIsInstance(LOG_NAME, str)

        # Should have reasonable defaults
        self.assertIn("%(", LOG_FORMAT)  # Should contain format placeholders
        self.assertTrue(len(LOG_NAME) > 0)  # Should not be empty


class TestColoredFormatter(unittest.TestCase):
    """Test colored formatter for logs."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = ColoredFormatter()

    def test_colors_defined(self):
        """Test that colors are defined for all log levels."""
        expected_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in expected_levels:
            self.assertIn(level, ColoredFormatter.COLORS)

    def test_format_with_color(self):
        """Test formatting log record with color."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)

        # Should contain the color code for INFO
        self.assertIn(Fore.BLUE, formatted)
        # Should contain the reset code
        self.assertIn(Style.RESET_ALL, formatted)
        # Should contain the message
        self.assertIn("Test message", formatted)

    def test_format_unknown_level(self):
        """Test formatting with unknown log level."""
        record = logging.LogRecord(
            name="test",
            level=99,  # Unknown level
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)

        # Should use default white color
        self.assertIn(Fore.WHITE, formatted)
        self.assertIn(Style.RESET_ALL, formatted)


class TestSensitiveDataFilter(unittest.TestCase):
    """Test sensitive data filter for logs."""

    def setUp(self):
        """Set up test fixtures."""
        self.filter = SensitiveDataFilter()

    def test_filter_authorization_header(self):
        """Test filtering authorization header."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Authorization: token123",  # Single token after Authorization:
            args=(),
            exc_info=None,
        )

        result = self.filter.filter(record)

        self.assertTrue(result)  # Should always return True
        self.assertIn("[FILTERED]", record.msg)
        self.assertNotIn("token123", record.msg)

    def test_filter_password_in_logs(self):
        """Test filtering password from logs."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="User login with password=secret123",
            args=(),
            exc_info=None,
        )

        result = self.filter.filter(record)

        self.assertTrue(result)
        self.assertIn("[FILTERED]", record.msg)
        self.assertNotIn("secret123", record.msg)

    def test_filter_bearer_token(self):
        """Test filtering Bearer token from logs."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Request with Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            args=(),
            exc_info=None,
        )

        result = self.filter.filter(record)

        self.assertTrue(result)
        self.assertIn("[FILTERED]", record.msg)
        self.assertNotIn("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", record.msg)

    def test_filter_json_authorization(self):
        """Test filtering authorization in JSON format."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg='Request body: {"authorization": "Bearer token123"}',
            args=(),
            exc_info=None,
        )

        result = self.filter.filter(record)

        self.assertTrue(result)
        self.assertIn("[FILTERED]", record.msg)
        self.assertNotIn("token123", record.msg)

    def test_filter_no_sensitive_data(self):
        """Test filter with no sensitive data."""
        original_msg = "Normal log message without sensitive data"
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg=original_msg,
            args=(),
            exc_info=None,
        )

        result = self.filter.filter(record)

        self.assertTrue(result)
        self.assertEqual(record.msg, original_msg)  # Should be unchanged

    def test_replacement_function_with_three_groups(self):
        """Test replacement function with three capture groups."""
        # Create a mock match with 3 groups
        mock_match = MagicMock()
        mock_match.group.side_effect = lambda x: {
            1: "Authorization: ",
            2: "secret_token",
            3: " end",
        }[x]
        mock_match.lastindex = 3

        result = replacement(mock_match)

        self.assertEqual(result, "Authorization: [FILTERED] end")

    def test_replacement_function_with_two_groups(self):
        """Test replacement function with two capture groups."""
        mock_match = MagicMock()
        mock_match.group.side_effect = lambda x: {
            1: "password=",
            2: "secret123",
        }[x]
        mock_match.lastindex = 2

        result = replacement(mock_match)

        self.assertEqual(result, "password=[FILTERED]")

    def test_replacement_function_with_one_group(self):
        """Test replacement function with one capture group."""
        mock_match = MagicMock()
        mock_match.group.side_effect = lambda x: {1: "Bearer "}[x]
        mock_match.lastindex = 1

        result = replacement(mock_match)

        self.assertEqual(result, "Bearer [FILTERED]")

    def test_sensitive_patterns_defined(self):
        """Test that sensitive patterns are properly defined."""
        self.assertIsInstance(SENSITIVE_PATTERNS, list)
        self.assertGreater(len(SENSITIVE_PATTERNS), 0)

        # Test that patterns are valid regex
        for pattern in SENSITIVE_PATTERNS:
            try:
                re.compile(pattern)
            except re.error:
                self.fail(f"Invalid regex pattern: {pattern}")


class TestMaxLevelFilter(unittest.TestCase):
    """Test max level filter for logs."""

    def test_filter_allows_lower_level(self):
        """Test that filter allows logs at or below max level."""
        filter_instance = MaxLevelFilter(logging.INFO)

        # Create DEBUG record (lower than INFO)
        debug_record = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="test.py",
            lineno=1,
            msg="Debug message",
            args=(),
            exc_info=None,
        )

        # Create INFO record (equal to max level)
        info_record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Info message",
            args=(),
            exc_info=None,
        )

        self.assertTrue(filter_instance.filter(debug_record))
        self.assertTrue(filter_instance.filter(info_record))

    def test_filter_blocks_higher_level(self):
        """Test that filter blocks logs above max level."""
        filter_instance = MaxLevelFilter(logging.INFO)

        # Create WARNING record (higher than INFO)
        warning_record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=1,
            msg="Warning message",
            args=(),
            exc_info=None,
        )

        # Create ERROR record (higher than INFO)
        error_record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Error message",
            args=(),
            exc_info=None,
        )

        self.assertFalse(filter_instance.filter(warning_record))
        self.assertFalse(filter_instance.filter(error_record))


class TestLogSetup(unittest.TestCase):
    """Test log setup functionality."""

    def test_get_context(self):
        """Test get_context function returns proper context."""
        context = get_context()

        # Should contain filename and function name
        self.assertIsInstance(context, str)
        self.assertIn(".", context)  # Should have filename.function format
        self.assertIn("test_get_context", context)  # Should have current function name

    @patch("src.libs.log.logging.config.dictConfig")
    @patch("src.libs.log.logging.getLogger")
    def test_setup_logging(self, mock_get_logger, mock_dict_config):
        """Test setup_logging function."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        result = setup_logging()

        # Should call dictConfig with proper configuration
        mock_dict_config.assert_called_once()
        config_dict = mock_dict_config.call_args[0][0]

        self.assertIn("version", config_dict)
        self.assertIn("formatters", config_dict)
        self.assertIn("handlers", config_dict)
        self.assertIn("filters", config_dict)
        self.assertIn("loggers", config_dict)

        # Should return logger
        self.assertEqual(result, mock_logger)

    @patch("src.libs.log.setup_logging")
    @patch("src.libs.log.logging.getLogger")
    def test_get_logger_with_handlers(self, mock_get_logger, mock_setup):
        """Test get_logger when logger already has handlers."""
        mock_logger = MagicMock()
        mock_logger.handlers = ["some_handler"]  # Non-empty handlers
        mock_get_logger.return_value = mock_logger

        result = get_logger("test_logger")

        # Should not call setup_logging since logger has handlers
        mock_setup.assert_not_called()
        self.assertEqual(result, mock_logger)

    @patch("src.libs.log.setup_logging")
    @patch("src.libs.log.logging.getLogger")
    def test_get_logger_without_handlers(self, mock_get_logger, mock_setup):
        """Test get_logger when logger has no handlers."""
        mock_logger = MagicMock()
        mock_logger.handlers = []  # Empty handlers
        mock_get_logger.return_value = mock_logger

        result = get_logger("test_logger")

        # Should call setup_logging since logger has no handlers
        mock_setup.assert_called_once()
        self.assertEqual(result, mock_logger)

    def test_setup_logging_with_custom_parameters(self):
        """Test setup_logging with custom parameters."""
        with patch("src.libs.log.logging.config.dictConfig") as mock_dict_config:
            with patch("src.libs.log.logging.getLogger") as mock_get_logger:
                mock_logger = MagicMock()
                mock_get_logger.return_value = mock_logger

                result = setup_logging(
                    level="ERROR",
                    output_format="%(message)s",
                    name="custom_logger",
                )

                # Should use custom parameters
                config_dict = mock_dict_config.call_args[0][0]
                self.assertIn("custom_logger", config_dict["loggers"])
                self.assertEqual(
                    config_dict["loggers"]["custom_logger"]["level"],
                    "ERROR",
                )

                mock_get_logger.assert_called_with("custom_logger")
                self.assertEqual(result, mock_logger)


if __name__ == "__main__":
    unittest.main()
