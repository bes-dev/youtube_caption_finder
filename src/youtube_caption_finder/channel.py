"""
Module for working with YouTube channels.

Provides functions to extract the canonical channel ID from a channel page,
and a Channel class that encapsulates this functionality.
"""

import json
import re
import requests

def extract_yt_initial_data(html: str) -> dict:
    """
    Extract the JSON object assigned to ytInitialData from the given HTML.

    Searches for patterns like:
      window['ytInitialData'] = { ... };
      or
      ytInitialData = { ... };

    Performs a balanced-brace extraction and returns the parsed JSON.

    Args:
        html (str): The HTML content.

    Returns:
        dict: Parsed JSON data.

    Raises:
        ValueError: If ytInitialData is not found.
        json.JSONDecodeError: If the extracted text is not valid JSON.
    """
    pattern = r'(?:window\[\s*[\'"]ytInitialData[\'"]\s*\]|ytInitialData)\s*=\s*({)'
    match = re.search(pattern, html)
    if not match:
        raise ValueError("ytInitialData not found in HTML")
    start_index = match.start(1)
    brace_count = 0
    in_string = False
    string_char = ''
    escape = False
    end_index = start_index

    # Iterate character by character to extract the complete JSON object.
    for i, ch in enumerate(html[start_index:], start=start_index):
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == string_char:
                in_string = False
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
            elif ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_index = i + 1
                    break
    json_text = html[start_index:end_index]
    return json.loads(json_text)

def get_channel_id_from_html(html: str) -> str:
    """
    Extracts the canonical channel ID from the ytInitialData in the HTML.

    The expected value is located at:
      metadata.channelMetadataRenderer.externalId

    Args:
        html (str): The HTML content of the channel page.

    Returns:
        str: The canonical channel ID.

    Raises:
        ValueError: If the channel ID cannot be found.
    """
    data = extract_yt_initial_data(html)
    try:
        return data['metadata']['channelMetadataRenderer']['externalId']
    except KeyError:
        raise ValueError("Channel ID not found in initial data.")

def get_channel_id(channel_url: str) -> str:
    """
    Fetches the channel page for the given URL and extracts the canonical channel ID.

    For example, for a vanity URL like:
      https://www.youtube.com/@nomadcapitalist
    it may return:
      UC3k3floOm_HtKOv0l6JU-xQ

    Args:
        channel_url (str): The YouTube channel URL.

    Returns:
        str: The canonical channel ID.

    Raises:
        Exception: If the page cannot be fetched or the ID is not found.
    """
    response = requests.get(channel_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch channel page, status code {response.status_code}")
    html = response.text
    return get_channel_id_from_html(html)

class Channel:
    """
    Represents a YouTube channel.

    This class fetches the channel page and extracts the canonical channel ID from
    the embedded JSON (ytInitialData).

    Attributes:
        channel_url (str): The URL of the channel.
        channel_id (str): The canonical channel ID.
    """
    def __init__(self, channel_url: str):
        self.channel_url = channel_url
        self._channel_id = None

    @property
    def channel_id(self) -> str:
        """
        Returns the canonical channel ID.

        The result is cached after the first retrieval.

        Returns:
            str: The channel ID.
        """
        if self._channel_id is None:
            self._channel_id = get_channel_id(self.channel_url)
        return self._channel_id

    def __repr__(self) -> str:
        return f"<Channel url={self.channel_url} id={self.channel_id}>"
