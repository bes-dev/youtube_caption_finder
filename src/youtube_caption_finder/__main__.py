#!/usr/bin/env python
"""
Entry point for the youtube_caption_finder CLI.

This module is executed when running:
    python -m youtube_caption_finder
"""

import argparse
import sys
from youtube_caption_finder import (
    YoutubeCaptionFinder,
    Filters,
    SortOption,
    SortField,
    SortOrder,
    LicenseType,
    __version__,
)

def main():
    # Create an argument parser for CLI options
    parser = argparse.ArgumentParser(description="YouTube Caption Finder CLI")
    parser.add_argument("query", help="Search query for captions", nargs="?")
    parser.add_argument("--channel", help="Optional channel id", default=None)
    parser.add_argument("--license", help="License type (ANY, CREATIVE_COMMONS, YOUTUBE_LICENSE)", default="ANY")
    parser.add_argument("--sort", help="Sort by field (VIEW_COUNT, UPLOAD_DATE, etc.)", default="VIEW_COUNT")
    parser.add_argument("--order", help="Sort order (asc or desc)", default="desc")
    parser.add_argument("--all", action="store_true", help="Lazily iterate over all pages")
    args = parser.parse_args()

    # If no query is provided, show help and exit
    if not args.query:
        parser.print_help()
        sys.exit(0)

    # Configure search filters
    filters = Filters()
    if args.license.upper() == "CREATIVE_COMMONS":
        filters.set_license(LicenseType.CREATIVE_COMMONS)
    elif args.license.upper() == "YOUTUBE_LICENSE":
        filters.set_license(LicenseType.YOUTUBE_LICENSE)
    else:
        filters.set_license(LicenseType.ANY)

    # Determine sort field and order
    try:
        sort_field = SortField[args.sort.upper()]
    except KeyError:
        print(f"Invalid sort field: {args.sort}")
        sys.exit(1)
    sort_order = SortOrder.ASC if args.order.lower() == "asc" else SortOrder.DESC
    sort_option = SortOption(sort_field, sort_order)

    client = YoutubeCaptionFinder()
    try:
        # If the user requested lazy iteration over all pages:
        if args.all:
            for video in client.search_all(
                args.query, channel_id=args.channel, filters=filters, sort_option=sort_option
            ):
                print(video)
        else:
            videos = client.search(
                args.query, channel_id=args.channel, filters=filters, sort_option=sort_option
            )
            for video in videos:
                print(video)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
