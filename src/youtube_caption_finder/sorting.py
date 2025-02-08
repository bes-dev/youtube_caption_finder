"""
Module defining sorting options and related enumerations.

This module defines enums for license types, sorting fields, and sort orders,
as well as a SortOption class that serializes the sorting configuration.
"""

from enum import Enum
from typing import Dict

class LicenseType(Enum):
    """Enumeration of video license types."""
    ANY = "0"
    CREATIVE_COMMONS = "2"
    YOUTUBE_LICENSE = "1"

class SortField(Enum):
    """Enumeration of sorting fields."""
    UPLOAD_DATE = "uploaddate"
    ID = "id"
    VIEW_COUNT = "viewcount"
    LIKE_COUNT = "likecount"
    CHAN_RANK = "chanrank"
    DURATION = "duration"

class SortOrder(Enum):
    """Enumeration of sorting orders."""
    DESC = "desc"
    ASC = "asc"

class SortOption:
    """
    Represents sorting options for a search query.

    Attributes:
        field (SortField): The field to sort by.
        order (SortOrder): The order of sorting.
    """
    def __init__(self, field: SortField, order: SortOrder):
        self.field = field
        self.order = order

    def to_dict(self) -> Dict[str, str]:
        """
        Serializes sorting options into a dictionary.

        Returns:
            Dict[str, str]: Dictionary with keys 'sortField' and 'sortOrder'.
        """
        return {"sortField": self.field.value, "sortOrder": self.order.value}

    def __repr__(self):
        return f"<SortOption field={self.field} order={self.order}>"
