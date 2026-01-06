"""
Users - Enums.
"""

from enum import Enum


class AvailableImagesEnum(str, Enum):
    """
    Available images enum.
    """

    avatar = "avatar"
    banner = "banner"


class ThemeEnum(str, Enum):
    """
    Theme enum.
    """

    light = "light"
    dark = "dark"


class ColorEnum(str, Enum):
    """
    Color enum.
    """

    purple = "purple"
    amber = "amber"
    red = "red"
    sky = "sky"


class ReadingModeEnum(str, Enum):
    """
    Reading mode enum.
    """

    webtoon = "webtoon"
    vertical = "vertical"
    horizontal = "horizontal"
