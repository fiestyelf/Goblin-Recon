"""Compatibility entry point for clip URL extraction.

The canonical implementation lives in ``goblin_recon.tools.clip_extractor``.
This module keeps ``python -m goblin_recon.tools.extract_clip`` working.
"""

from __future__ import annotations

from .clip_extractor import extract_clip_metadata, extract_youtube_id, format_time, main


def extract_clip_url(source_url: str, start_sec: int, end_sec: int) -> str:
    """Return a YouTube timestamp URL for a validated 15-60 second clip."""
    metadata = extract_clip_metadata(source_url, start_sec, end_sec)
    if "error" in metadata:
        raise ValueError(str(metadata["error"]))
    return str(metadata["url_with_timestamp"])


__all__ = ["extract_clip_metadata", "extract_clip_url", "extract_youtube_id", "format_time"]


if __name__ == "__main__":
    raise SystemExit(main())
