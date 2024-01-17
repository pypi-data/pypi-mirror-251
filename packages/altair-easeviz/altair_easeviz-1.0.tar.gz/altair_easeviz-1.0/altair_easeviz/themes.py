"""Altair theme configuration."""
from .models import FillerPatternTheme, AccessibleTheme, DarkAccessibleTheme, \
    PrintFriendlyTheme

accessible = AccessibleTheme()
dark_accessible = DarkAccessibleTheme()
filler_pattern = FillerPatternTheme()
print_friendly = PrintFriendlyTheme()


def accessible_theme():
    return accessible.get_theme()


def dark_accessible_theme():
    return dark_accessible.get_theme()


def filler_pattern_theme():
    return filler_pattern.get_theme()


def print_friendly_theme():
    return print_friendly.get_theme()
