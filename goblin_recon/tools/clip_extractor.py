"""YouTube clip URL and timestamp helpers."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse


VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def format_time(seconds: int) -> str:
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
        if not video_id and parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
    if not VIDEO_ID_RE.match(video_id):
        raise ValueError("YouTube URL does not contain a valid video ID")
    return video_id


def validate_url(video_url: str) -> None:
    parsed = urlparse(video_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("video_url must be a valid http(s) URL")


def extract_clip_metadata(video_url: str, start_sec: int, end_sec: int) -> dict:
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

    return {
        "url_with_timestamp": f"https://youtube.com/watch?v={video_id}&t={start_sec}",
        "embed_url": f"https://youtube.com/embed/{video_id}?start={start_sec}&end={end_sec}",
        "video_url": video_url,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "duration": duration,
        "start_time": format_time(start_sec),
        "end_time": format_time(end_sec),
        "clip_range": f"{format_time(start_sec)} -> {format_time(end_sec)}",
    }
