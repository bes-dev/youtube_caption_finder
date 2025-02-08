"""
Module defining filtering parameters for search queries.

This module defines the Filters dataclass which encapsulates filtering options
such as title, views range, likes range, duration, date range, and license type.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple, Dict, Union
from youtube_caption_finder.sorting import LicenseType

# Constants for validation
MIN_VIEWS = 0
MAX_VIEWS = 6000000000
MIN_LIKES = 30
MAX_LIKES = 6000000000
MIN_DURATION = 1       # seconds (1 second)
MAX_DURATION = 86400   # seconds (24 hours)

@dataclass
class Filters:
    """
    Represents filtering parameters for a search query.

    Attributes:
        title (Optional[str]): Video title filter.
        views (Optional[Tuple[int, int]]): Tuple (min_views, max_views).
        likes (Optional[Tuple[int, int]]): Tuple (min_likes, max_likes).
        duration (Optional[Tuple[int, int]]): Tuple (min_duration, max_duration) in seconds.
        date_range (Optional[Tuple[Optional[date], Optional[date]]]): (start_date, end_date).
        license (Optional[LicenseType]): Video license type.
    """
    title: Optional[str] = None
    views: Optional[Tuple[int, int]] = None
    likes: Optional[Tuple[int, int]] = None
    duration: Optional[Tuple[int, int]] = None
    date_range: Optional[Tuple[Optional[date], Optional[date]]] = None
    license: Optional[LicenseType] = None

    def set_title(self, title: str) -> None:
        """Set the title filter."""
        self.title = title

    def set_views(self, min_views: int, max_views: int) -> None:
        """Set the views range filter with validation."""
        if min_views < MIN_VIEWS:
            raise ValueError(f"min_views must be >= {MIN_VIEWS}")
        if max_views > MAX_VIEWS:
            raise ValueError(f"max_views must be <= {MAX_VIEWS}")
        if min_views > max_views:
            raise ValueError("min_views cannot be greater than max_views")
        self.views = (min_views, max_views)

    def set_likes(self, min_likes: int, max_likes: int) -> None:
        """Set the likes range filter with validation."""
        if min_likes < MIN_LIKES:
            raise ValueError(f"min_likes must be >= {MIN_LIKES}")
        if max_likes > MAX_LIKES:
            raise ValueError(f"max_likes must be <= {MAX_LIKES}")
        if min_likes > max_likes:
            raise ValueError("min_likes cannot be greater than max_likes")
        self.likes = (min_likes, max_likes)

    def set_duration(self, start_duration: int, end_duration: int) -> None:
        """Set the duration filter (in seconds) with validation."""
        if start_duration < MIN_DURATION:
            raise ValueError(f"start_duration must be >= {MIN_DURATION}")
        if end_duration > MAX_DURATION:
            raise ValueError(f"end_duration must be <= {MAX_DURATION}")
        if start_duration > end_duration:
            raise ValueError("start_duration cannot be greater than end_duration")
        self.duration = (start_duration, end_duration)

    def set_date_range(self, start: Union[str, date], end: Union[str, date]) -> None:
        """Set the date range filter.

        Args:
            start (str or date): Start date (ISO string or date object).
            end (str or date): End date (ISO string or date object).
        """
        if isinstance(start, str):
            start_date = date.fromisoformat(start)
        else:
            start_date = start
        if isinstance(end, str):
            end_date = date.fromisoformat(end)
        else:
            end_date = end
        if start_date > end_date:
            raise ValueError("start_date cannot be later than end_date")
        self.date_range = (start_date, end_date)

    def set_license(self, license_type: LicenseType) -> None:
        """Set the license filter."""
        self.license = license_type

    def to_dict(self) -> Dict[str, object]:
        """
        Serializes the filter settings into a dictionary for URL parameters.

        Returns:
            Dict[str, object]: Dictionary with filter settings, excluding None values.
        """
        data: Dict[str, object] = {}
        if self.title:
            data["title"] = self.title
        if self.duration:
            data["startDuration"] = self.duration[0]
            data["endDuration"] = self.duration[1]
        if self.views:
            data["minViews"] = self.views[0]
            data["maxViews"] = self.views[1]
        if self.likes:
            data["minLikes"] = self.likes[0]
            data["maxLikes"] = self.likes[1]
        if self.date_range:
            data["startDate"] = self.date_range[0].isoformat() if self.date_range[0] else None
            data["endDate"] = self.date_range[1].isoformat() if self.date_range[1] else None
        if self.license:
            data["license"] = self.license.value
        # Filter out keys with None values
        return {k: v for k, v in data.items() if v is not None}
