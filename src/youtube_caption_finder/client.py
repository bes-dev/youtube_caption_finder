"""
Client module for youtube_caption_finder.

This module defines the main class :class:`YoutubeCaptionFinder` which builds search URLs,
executes search queries, and provides lazy pagination via the search_all() method.
"""

import urllib.parse
import posixpath
from typing import Optional, Dict, List, Iterator

import requests
from youtube_caption_finder.filters import Filters
from youtube_caption_finder.sorting import SortOption
from youtube_caption_finder.video import VideoInfo
from youtube_caption_finder.exceptions import YoutubeCaptionFinderError
from youtube_caption_finder.extractor import VideoInfoExtractor, FilterExtractor

class YoutubeCaptionFinder:
    BASE_URL = "https://filmot.com/search/"

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        """
        Initializes the YoutubeCaptionFinder client.

        Args:
            session (requests.Session, optional): A custom session instance. Defaults to a new session.
        """
        self.session = session or requests.Session()

    def _build_search_url(
        self,
        query: str,
        channel_id: Optional[str] = None,
        filters: Optional[Filters] = None,
        sort_option: Optional[SortOption] = None,
        page_id: int = 1,
    ) -> str:
        """
        Constructs the search URL with the specified parameters.

        Args:
            query (str): The search query.
            channel_id (str, optional): Channel identifier.
            filters (Filters, optional): Filter configuration.
            sort_option (SortOption, optional): Sorting options.
            page_id (int, optional): Page number (default: 1).

        Returns:
            str: Complete URL for performing the search.
        """
        params = {"gridView": 1}
        if channel_id:
            params["channelID"] = channel_id
        if filters:
            params.update(filters.to_dict())
        if sort_option:
            params.update(sort_option.to_dict())
        # Convert all parameter values to strings
        params = {k: str(v) for k, v in params.items()}
        query_encoded = urllib.parse.quote(query)
        path = f"1/{page_id}?{urllib.parse.urlencode(params)}"
        suburl = posixpath.join(query_encoded, path)
        return urllib.parse.urljoin(self.BASE_URL, suburl)

    def _search_page(
        self,
        query: str,
        channel_id: Optional[str] = None,
        filters: Optional[Filters] = None,
        sort_option: Optional[SortOption] = None,
        page_id: int = 1,
    ) -> List[VideoInfo]:
        """
        Fetches search results for a given page number.

        Args:
            query (str): The search query.
            channel_id (str, optional): Channel identifier.
            filters (Filters, optional): Filter configuration.
            sort_option (SortOption, optional): Sorting options.
            page_id (int, optional): Page number.

        Returns:
            List[VideoInfo]: A list of VideoInfo objects for the page.
        """
        url = self._build_search_url(query, channel_id, filters, sort_option, page_id)
        response = self.session.get(url)
        if response.status_code != 200:
            raise YoutubeCaptionFinderError(f"Error fetching search results: {response.status_code}")
        return VideoInfoExtractor.extract(response.content)

    def search(
        self,
        query: str,
        channel_id: Optional[str] = None,
        filters: Optional[Filters] = None,
        sort_option: Optional[SortOption] = None,
        page_id: int = 1
    ) -> List[VideoInfo]:
        """
        Returns the first page of search results.

        Args:
            query (str): The search query.
            channel_id (str, optional): Channel identifier.
            filters (Filters, optional): Filter configuration.
            sort_option (SortOption, optional): Sorting options.
            page_id (int, optional): Page number.

        Returns:
            List[VideoInfo]: List of VideoInfo objects.
        """
        return self._search_page(query, channel_id, filters, sort_option, page_id=page_id)

    def search_all(
        self,
        query: str,
        channel_id: Optional[str] = None,
        filters: Optional[Filters] = None,
        sort_option: Optional[SortOption] = None,
    ) -> Iterator[VideoInfo]:
        """
        Lazily iterates over all search result pages, yielding VideoInfo objects.

        Args:
            query (str): The search query.
            channel_id (str, optional): Channel identifier.
            filters (Filters, optional): Filter configuration.
            sort_option (SortOption, optional): Sorting options.

        Yields:
            VideoInfo: Next video result.
        """
        page_id = 1
        while True:
            videos = self._search_page(query, channel_id, filters, sort_option, page_id)
            if not videos:
                break
            for video in videos:
                yield video
            page_id += 1

    def get_filters(
        self,
        query: str,
        channel_id: Optional[str] = None,
        filters: Optional[Filters] = None,
        sort_option: Optional[SortOption] = None,
    ) -> Dict:
        """
        Extracts available filter options from the search page.

        Args:
            query (str): The search query.
            channel_id (str, optional): Channel identifier.
            filters (Filters, optional): Filter configuration.
            sort_option (SortOption, optional): Sorting options.

        Returns:
            Dict: A dictionary of filter options.
        """
        url = self._build_search_url(query, channel_id, filters, sort_option, page_id=1)
        response = self.session.get(url)
        if response.status_code != 200:
            raise YoutubeCaptionFinderError(f"Error fetching filters: {response.status_code}")
        return FilterExtractor.extract(response.content)
