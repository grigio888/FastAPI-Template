"""
Logger - Filters.

Custom filters for logging.
"""

import logging
import re

GENERAL_PATTERNS: list = [
    r"(Authorization:\s*)([^\s]+)",
    r"(['\"]authorization['\"]\s*:\s*['\"])([^\"]+)(['\"])",
    r"(['\"]refreshtoken['\"]\s*:\s*['\"])([^\"]+)(['\"])",
    r"(Bearer\s+)([^\s]+)",
    r"(password=\s*)([^\s]+)",
    r"(token=\s*)([^\s]+)",
    r"(secret=\s*)([^\s]+)",
    r"(api_key=\s*)([^\s]+)",
    r"(access_token=\s*)([^\s]+)",
]

SQL_PATTERNS: list = [
    r"(\b\w*(?:(?:password)|(?:id))\w*\b\s*=\s*(?:'|\"|))"
    r"([^'\"]+)(['\"]|)",
]

# Combine patterns
SENSITIVE_PATTERNS: list = [
    *GENERAL_PATTERNS,
    *SQL_PATTERNS,
]


def replacement(match: re.Match) -> str:
    """
    Replace sensitive data with [FILTERED].

    Produce a replacement string by preserving group 1 and, if available, group 3.
    It replaces the sensitive content (group 2) with [FILTERED].
    """
    g1 = match.group(1) if match.lastindex and match.lastindex >= 1 else ""
    g3 = (
        match.group(3)
        if match.lastindex and match.lastindex >= 3 and match.group(3) is not None
        else ""
    )
    return f"{g1}[FILTERED]{g3}"


class SensitiveDataFilter(logging.Filter):
    """
    Custom filter to mask or remove sensitive information from logs.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter sensitive data from logs.
        """

        message = record.getMessage()

        if message:
            filtered_message = message

            for pattern in SENSITIVE_PATTERNS:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                filtered_message = compiled_pattern.sub(replacement, filtered_message)

            record.msg = filtered_message
            record.args = ()

        return True
