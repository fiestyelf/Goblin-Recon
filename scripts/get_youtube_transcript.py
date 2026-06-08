#!/usr/bin/env python3
"""
Goblin Recon — YouTube Transcript Extractor
Pulls subtitles/captions from YouTube videos with timestamps.

Usage:
    python get_youtube_transcript.py <video_id_or_url>

Output:
    JSON array of {"time": <seconds>, "text": "<text>"} objects

Dependencies:
    uv pip install youtube-transcript-api

Example:
    python get_youtube_transcript.py "https://youtube.com/watch?v=xyz123"
    python get_youtube_transcript.py "xyz123"
"""

from __future__ import annotations

import sys
import json
import re
from argparse import ArgumentParser
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi


VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return as-is if already an ID."""
    if VIDEO_ID_RE.match(url_or_id):
        return url_or_id

    parsed = urlparse(url_or_id)
    host = parsed.netloc.lower()
    video_id = ""
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        elif parsed.path.startswith("/v/"):
            video_id = parsed.path.split("/v/", 1)[1].split("/", 1)[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]

    if VIDEO_ID_RE.match(video_id):
        return video_id

    raise ValueError("Input must be a valid YouTube URL or 11-character video ID")


def get_transcript(video_id: str, languages: list[str]) -> list:
    """Get transcript with timestamps."""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=languages)
    result = []
    for snippet in transcript:
        text = " ".join(snippet.text.strip().split())
        if text:
            result.append({
                "time": int(snippet.start),
                "duration": round(float(snippet.duration), 2),
                "text": text,
            })
    return result


def error_response(message: str, video_id: str | None = None) -> list[dict]:
    """Return structured JSON errors without exposing tracebacks."""
    response = {"error": message, "recoverable": True}
    if video_id:
        response["video_id"] = video_id
    return [response]


def main():
    parser = ArgumentParser(description="Pull a YouTube transcript with timestamps.")
    parser.add_argument("video", help="YouTube URL or 11-character video ID")
    parser.add_argument(
        "--languages",
        default="en",
        help="Comma-separated language preference order. Default: en",
    )
    args = parser.parse_args()

    video_id = None
    try:
        video_id = extract_video_id(args.video)
        languages = [lang.strip() for lang in args.languages.split(",") if lang.strip()]
        transcript = get_transcript(video_id, languages)
    except Exception as exc:
        transcript = error_response(str(exc), video_id)
        print(json.dumps(transcript, indent=2))
        sys.exit(1)

    print(json.dumps(transcript, indent=2))


if __name__ == "__main__":
    main()
