# flake8: noqa: F401
"""
youtube_caption_finder: a Python library for searching YouTube captions via the Filmot API.
"""

__title__ = "youtube_caption_finder"
__author__ = "Sergei Belousov aka BeS"
__license__ = "MIT License"

from youtube_caption_finder.version import __version__
from youtube_caption_finder.client import YoutubeCaptionFinder
from youtube_caption_finder.filters import Filters
from youtube_caption_finder.sorting import SortOption, SortField, SortOrder, LicenseType
from youtube_caption_finder.video import VideoInfo
from youtube_caption_finder.exceptions import YoutubeCaptionFinderError
from youtube_caption_finder.channel import Channel
