# youtube_caption_finder

**youtube_caption_finder** is a Python library for searching YouTube videos by their captions via an external API (Filmot).
It provides an object‐oriented interface for configuring search filters, sorting options, and performing queries to retrieve video information.
The library supports lazy loading of paginated results so that additional pages are fetched on demand.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Programmatic Usage](#programmatic-usage)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
  - [Working with Channels](#working-with-channels)
- [API Reference](#api-reference)
  - [YoutubeCaptionFinder](#youtubecaptionfinder)
  - [Filters](#filters)
  - [Sorting Options](#sorting-options)
  - [VideoInfo](#videoinfo)
- [Lazy Loading of Results](#lazy-loading-of-results)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

**youtube_caption_finder** allows you to search for YouTube videos based on caption content.
Using an external API (Filmot), the library sends search queries and returns results as structured `VideoInfo` objects.
Filters and sorting options can be configured, and results are loaded lazily—only the requested page is fetched when needed.

## Features

- **Search by Caption:** Query YouTube videos based on caption content.
- **Flexible Filters:** Configure filters (e.g. video title, views, likes, duration, date range, license type).
- **Sorting Options:** Sort results by various fields such as view count, upload date, etc.
- **Lazy Pagination:** Load additional pages on demand using a generator interface (via `search_all()`).
- **Channel Extraction:** Extract the canonical channel ID from a channel URL (even from vanity URLs like `@nomadcapitalist`).
- **Command-Line Interface:** Use the library from the command line for quick searches.

> **Note:** The library does not implement caption processing functionality itself. Users can implement caption handling on top of the library using other tools.

## Installation

### Using pip

Clone the repository and install with pip:

```bash
git clone https://github.com/yourusername/youtube_caption_finder.git
cd youtube_caption_finder
pip install .
```

## Development Installation

For development purposes, install in editable mode:

```bash
pip install -e .
```

## Usage

### Programmatic Usage
Below is an example of how to use the library in your code:

```python
from youtube_caption_finder import (
    YoutubeCaptionFinder,
    Filters,
    SortOption,
    SortField,
    SortOrder,
    LicenseType,
    VideoInfo
)

# Create a client instance
client = YoutubeCaptionFinder()

# Configure filters
filters = Filters()
filters.set_license(LicenseType.CREATIVE_COMMONS)

# Configure sorting options
sort_option = SortOption(SortField.VIEW_COUNT, SortOrder.DESC)

query = "USA taxes"

# Retrieve the first page of results
videos = client.search(query, filters=filters, sort_option=sort_option)
for video in videos:
    print(video)

# Lazy iteration over all pages (fetch next results on demand)
video_generator = client.search_all(query, filters=filters, sort_option=sort_option)
first_video = next(video_generator)
print("First video:", first_video)
second_video = next(video_generator)
print("Second video:", second_video)
```

### Command-Line Interface (CLI)

The library provides a CLI. Once installed, you can run:

```bash
youtube_caption_finder --license CREATIVE_COMMONS --sort VIEW_COUNT --order desc "USA taxes"
```

This command will perform a search with the specified parameters and print out the results.

### Working with Channels

The library includes a module to extract a channel’s canonical ID from its URL—even for vanity URLs. For example:

```python
from youtube_caption_finder.channel import Channel

channel_url = "https://www.youtube.com/@nomadcapitalist"
channel = Channel(channel_url)
print("Channel ID:", channel.channel_id)
```

## API Reference
### YoutubeCaptionFinder
The main client class.

- search(query, channel_id=None, filters=None, sort_option=None)
Returns a list of VideoInfo objects from the first page of search results.

- search_all(query, channel_id=None, filters=None, sort_option=None)
Returns a generator yielding VideoInfo objects across pages. You can use next() to fetch additional results.

- get_filters(query, channel_id=None, filters=None, sort_option=None)
Returns a dictionary of available filter options from the search page.

### Filters
A dataclass that encapsulates filtering options.

- set_title(title): Set a video title filter.
- set_views(min_views, max_views): Set a views range filter.
- set_likes(min_likes, max_likes): Set a likes range filter.
- set_duration(start_duration, end_duration): Set a duration filter (in seconds).
- set_date_range(start, end): Set a date range filter (using ISO date strings or date objects).
- set_license(license_type): Set the license type using the LicenseType enum.
- to_dict(): Serializes filter settings into a dictionary suitable for URL parameters.

### Sorting Options
- SortField: Enum defining sorting fields (e.g., UPLOAD_DATE, VIEW_COUNT).
- SortOrder: Enum defining sort order (ASC or DESC).
- SortOption: Class that combines a SortField and SortOrder. Use the to_dict() method to serialize sorting options.

### VideoInfo
A dataclass representing a YouTube video result.
Attributes include video_id, title, channel, views, likes, upload_date, etc.

## Lazy Loading of Results
The library supports lazy loading of search results through the search_all() method in the YoutubeCaptionFinder class.
This method returns a generator that:

- Requests a page of results based on an internal page counter.
- Yields individual VideoInfo objects one by one.
- Automatically advances to the next page when the current page is exhausted.
This allows you to process search results on demand without waiting for all pages to load.

### Example of On-Demand Loading
```python
client = YoutubeCaptionFinder()
results = client.search_all("USA taxes")
# Get the next result by calling next()
first_result = next(results)
print(first_result)
# Subsequent calls to next() will fetch additional videos (and pages if needed)
```

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Follow PEP‑8 and include proper docstrings and tests.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the Apache-2.0 license. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please contact sergei.o.belousov@gmail.com.
