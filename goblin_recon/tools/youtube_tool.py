"""YouTube search, metadata, and transcript helpers."""

from __future__ import annotations

import json
import re
import sys
from argparse import ArgumentParser
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def extract_video_id(url_or_id: str) -> str:
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


def get_transcript(video_id_or_url: str, languages: list[str] | None = None) -> list[dict]:
    video_id = extract_video_id(video_id_or_url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=languages or ["en"])
    result = []
    for snippet in transcript:
        text = " ".join(snippet.text.strip().split())
        if text:
            result.append(
                {
                    "time": int(snippet.start),
                    "duration": round(float(snippet.duration), 2),
                    "text": text,
                }
            )
    return result


def _yt_dlp_options() -> dict:
    return {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }


def search_youtube(query: str, limit: int = 10) -> list[dict]:
    from yt_dlp import YoutubeDL

    with YoutubeDL(_yt_dlp_options()) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
    entries = info.get("entries") or []
    return [_normalize_video(entry) for entry in entries if entry]


def get_video_metadata(url_or_id: str) -> dict:
    from yt_dlp import YoutubeDL

    video_id = extract_video_id(url_or_id)
    url = f"https://www.youtube.com/watch?v={video_id}"
    with YoutubeDL(_yt_dlp_options()) as ydl:
        info = ydl.extract_info(url, download=False)
    return _normalize_video(info)


def _normalize_video(info: dict) -> dict:
    video_id = info.get("id")
    return {
        "id": video_id,
        "title": info.get("title"),
        "url": info.get("webpage_url") or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_id": info.get("channel_id") or info.get("uploader_id"),
        "published_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "description": info.get("description"),
    }


def error_response(message: str, video_id: str | None = None) -> list[dict]:
    response = {"error": message, "recoverable": True}
    if video_id:
        response["video_id"] = video_id
    return [response]


def main() -> int:
    parser = ArgumentParser(description="Pull a YouTube transcript with timestamps.")
    parser.add_argument("video", help="YouTube URL or 11-character video ID")
    parser.add_argument("--languages", default="en", help="Comma-separated language preference order. Default: en")
    args = parser.parse_args()

    video_id = None
    try:
        video_id = extract_video_id(args.video)
        languages = [lang.strip() for lang in args.languages.split(",") if lang.strip()]
        transcript = get_transcript(video_id, languages)
    except Exception as exc:
        print(json.dumps(error_response(str(exc), video_id), indent=2))
        return 1

    print(json.dumps(transcript, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
