"""
Helper functions for youtube_caption_finder.

This module provides utility functions such as safe_filename to sanitize strings
for filesystem usage.
"""

import re

def safe_filename(s: str, max_length: int = 255) -> str:
    """
    Sanitizes a string to be safe for use as a filename by removing invalid characters.

    Args:
        s (str): The input string.
        max_length (int): Maximum allowed filename length.

    Returns:
        str: Sanitized filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", s)[:max_length]
