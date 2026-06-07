#!/usr/bin/env python3
"""
Goblin Recon — Clip Extractor
Generates YouTube clip metadata from video timestamps.

Usage:
    python extract_clip.py <video_url> <start_sec> <end_sec>

Output:
    JSON with clip metadata including:
    - url_with_timestamp: Direct YouTube link to clip starting point
    - duration: Clip length in seconds
    - start_time: Formatted start time
    - end_time: Formatted end time

Example:
    python extract_clip.py "https://youtube.com/watch?v=xyz" 1842 1902
"""

from __future__ import annotations

import sys
import json
import re
from argparse import ArgumentParser
from urllib.parse import parse_qs, urlparse


VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def format_time(seconds: int) -> str:
    """Convert seconds to MM:SS format."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def extract_youtube_id(video_url: str) -> str | None:
    parsed = urlparse(video_url)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        return None
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    else:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if not video_id and parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
    if not VIDEO_ID_RE.match(video_id):
        raise ValueError("YouTube URL does not contain a valid video ID")
    return video_id


def validate_url(video_url: str) -> None:
    parsed = urlparse(video_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("video_url must be a valid http(s) URL")


def extract_clip_metadata(video_url: str, start_sec: int, end_sec: int) -> dict:
    """Generate YouTube clip metadata from timestamps."""
    try:
        validate_url(video_url)
        if start_sec < 0 or end_sec < 0:
            raise ValueError("start_sec and end_sec must be non-negative")
        if start_sec >= end_sec:
            raise ValueError("Start time must be before end time")

        duration = end_sec - start_sec

        if duration < 15 or duration > 60:
            raise ValueError(f"Clip duration must be 15-60 seconds, got {duration} seconds")

        video_id = extract_youtube_id(video_url)
        if not video_id:
            raise ValueError("video_url must be a supported YouTube URL")
    except Exception as exc:
        return {"error": str(exc)}

    url_with_timestamp = f"https://youtube.com/watch?v={video_id}&t={start_sec}"
    embed_url = f"https://youtube.com/embed/{video_id}?start={start_sec}&end={end_sec}"

    return {
        "url_with_timestamp": url_with_timestamp,
        "embed_url": embed_url,
        "video_url": video_url,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "duration": duration,
        "start_time": format_time(start_sec),
        "end_time": format_time(end_sec),
        "clip_range": f"{format_time(start_sec)} -> {format_time(end_sec)}"
    }


def main():
    parser = ArgumentParser(description="Generate clip metadata from video timestamps.")
    parser.add_argument("video_url")
    parser.add_argument("start_sec", type=int)
    parser.add_argument("end_sec", type=int)
    args = parser.parse_args()

    video_url = args.video_url
    start_sec = args.start_sec
    end_sec = args.end_sec

    result = extract_clip_metadata(video_url, start_sec, end_sec)
    print(json.dumps(result, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
