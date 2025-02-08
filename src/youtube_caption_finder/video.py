"""
Module defining the VideoInfo data structure.

Each search result is returned as an instance of VideoInfo, which contains
fields such as video id, title, channel name, views, likes, and more.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoInfo:
    """
    Data class representing a YouTube video.

    Attributes:
        vcard_id (Optional[str]): The id of the video card.
        idx (Optional[str]): The index attribute.
        video_id (Optional[str]): The YouTube video identifier.
        thumbnail_url (Optional[str]): URL to the video thumbnail.
        video_link (Optional[str]): Direct link to the YouTube video.
        title (Optional[str]): Video title.
        channel (Optional[str]): Name of the channel.
        views (Optional[str]): View count as text.
        likes (Optional[str]): Like count as text.
        upload_date (Optional[str]): Upload date as text.
        language (Optional[str]): Language of the video.
        scroll_text (Optional[str]): Additional text (e.g., description snippet).
    """
    vcard_id: Optional[str]
    idx: Optional[str]
    video_id: Optional[str]
    thumbnail_url: Optional[str]
    video_link: Optional[str]
    title: Optional[str]
    channel: Optional[str]
    views: Optional[str]
    likes: Optional[str]
    upload_date: Optional[str]
    language: Optional[str]
    scroll_text: Optional[str]

    def __repr__(self):
        return f"<VideoInfo id={self.video_id} title={self.title}>"
