"""
Module for extracting video and filter information from HTML responses.

Provides helper classes for parsing the HTML returned from the external API.
"""

from bs4 import BeautifulSoup
from typing import Dict, List
from youtube_caption_finder.video import VideoInfo

class VideoInfoExtractor:
    @staticmethod
    def extract(html: bytes) -> List[VideoInfo]:
        """
        Extracts video information from the HTML content.

        Args:
            html (bytes): The HTML response content.

        Returns:
            List[VideoInfo]: A list of VideoInfo objects.
        """
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", id=lambda x: x and x.startswith("vcard"))
        video_list: List[VideoInfo] = []
        for card in cards:
            # Extract various fields from the video card
            vcard_id = card.get("id")
            idx = card.get("idx")
            fullpage_anchor = card.find("a", class_="fullpagelnk")
            video_id = fullpage_anchor.get("vid") if fullpage_anchor else None
            thumb_img = card.find("img", class_="thumb-image")
            thumbnail_url = thumb_img.get("src") if thumb_img else None
            yt_anchor = card.find("a", href=lambda h: h and "youtube.com/watch" in h)
            video_link = yt_anchor.get("href") if yt_anchor else None
            title_div = card.find("div", class_="d-inline")
            title = title_div.get_text(strip=True) if title_div else None
            channel_anchor = card.find("a", href=lambda h: h and h.startswith("/channel/"))
            channel = channel_anchor.get_text(strip=True) if channel_anchor else None

            # Extract badge information (views, likes, upload date)
            badges = card.find_all("span", class_="badge")
            views = None
            likes = None
            upload_date = None
            for span in badges:
                if span.find("i", class_="fa-eye"):
                    views = span.get_text(strip=True)
                elif span.find("i", class_="fa-thumbs-up"):
                    likes = span.get_text(strip=True)
                else:
                    text = span.get_text(strip=True)
                    if text and any(char.isalpha() for char in text):
                        upload_date = text

            lang_anchor = card.find("a", href=lambda h: h and "/sidebyside" in h)
            if lang_anchor:
                lang_img = lang_anchor.find("img")
                language = lang_img.get("alt") if lang_img else None
            else:
                language = None

            scroll_box = card.find("div", class_="scroll-box")
            scroll_text = scroll_box.get_text(separator="\n", strip=True) if scroll_box else None
            scroll_text = " ".join(scroll_text.split()) # Remove extra whitespace

            video_info = VideoInfo(
                vcard_id=vcard_id,
                idx=idx,
                video_id=video_id,
                thumbnail_url=thumbnail_url,
                video_link=video_link,
                title=title,
                channel=channel,
                views=views,
                likes=likes,
                upload_date=upload_date,
                language=language,
                scroll_text=scroll_text,
            )
            video_list.append(video_info)
        return video_list

class FilterExtractor:
    @staticmethod
    def extract(html: bytes) -> Dict:
        """
        Extracts available filter options from the HTML content.

        Args:
            html (bytes): HTML response content.

        Returns:
            Dict: Dictionary with available filter options.
        """
        soup = BeautifulSoup(html, "html.parser")
        filters_data: Dict[str, object] = {}
        accordion = soup.find("div", id="accordion")
        if not accordion:
            return filters_data

        # Extract "Sort By" filter options
        sort_by_options = []
        sort_header = accordion.find("div", class_="card-header", string=lambda s: s and "Sort By" in s)
        if sort_header:
            collapse_id = sort_header.get("href", "").lstrip("#")
            sort_div = accordion.find("div", id=collapse_id)
            if sort_div:
                import re
                for a in sort_div.find_all("a", href=True):
                    text = a.get_text(strip=True)
                    href = a["href"]
                    m = re.search(r"orderByField\('([^']+)','([^']+)'\)", href)
                    if m:
                        sort_by_options.append({
                            "text": text,
                            "field": m.group(1),
                            "order": m.group(2)
                        })
                    else:
                        sort_by_options.append({
                            "text": text,
                            "href": href
                        })
        filters_data["Sort By"] = sort_by_options

        # Extract UI filter controls
        filters_controls = {}
        filters_div = accordion.find("div", id="collapseZero")
        if filters_div:
            title_input = filters_div.find("input", id="qtitle")
            if title_input:
                filters_controls["Video Title"] = {
                    "type": "text",
                    "id": title_input.get("id"),
                    "default": title_input.get("value", "")
                }
            for slider_id, label in [("sliderviews", "Views"),
                                       ("sliderlikes", "Likes"),
                                       ("sliderduration", "Video Duration")]:
                slider = filters_div.find("input", id=slider_id)
                if slider:
                    filters_controls[label] = {
                        "type": "slider",
                        "id": slider_id,
                        "default": slider.get("value", None)
                    }
            license_select = filters_div.find("select", id="licenseFilter")
            if license_select:
                options = []
                for option in license_select.find_all("option"):
                    options.append({
                        "value": option.get("value"),
                        "text": option.get_text(strip=True),
                        "selected": option.has_attr("selected")
                    })
                filters_controls["Licence"] = {
                    "type": "select",
                    "id": "licenseFilter",
                    "options": options
                }
            date_range = {}
            start_date = filters_div.find("input", id="startdate")
            end_date = filters_div.find("input", id="enddate")
            if start_date:
                date_range["start_date"] = {
                    "type": "date",
                    "id": start_date.get("id"),
                    "default": start_date.get("value")
                }
            if end_date:
                date_range["end_date"] = {
                    "type": "date",
                    "id": end_date.get("id"),
                    "default": end_date.get("value")
                }
            dropdown = filters_div.find("div", class_="dropdown-menu")
            extra_date_options = []
            if dropdown:
                for btn in dropdown.find_all("button", class_="dateoptionselect"):
                    btn_label = btn.get_text(strip=True)
                    onclick = btn.get("onclick", "")
                    m_date = re.search(r"\$\(\'#startdate\'\)\.val\('([^']+)'\)", onclick)
                    if m_date:
                        extra_date_options.append({
                            "label": btn_label,
                            "start_date": m_date.group(1)
                        })
            date_range["extra_options"] = extra_date_options
            filters_controls["Date Range"] = date_range
        filters_data["Filters"] = filters_controls

        return filters_data
