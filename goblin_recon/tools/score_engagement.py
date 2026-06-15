"""Compatibility entry point for engagement velocity + lifecyle scoring.

The canonical implementation lives in ``goblin_recon.tools.scoring``.
This module keeps ``python -m goblin_recon.tools.score_engagement`` working
and adds lifecycle-aware ``score_with_lifecycle``.
"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser

from .scoring import calculate_velocity, calculate_velocity_with_lifecycle


def _source_url(platform: str, video_id_or_url: str) -> str:
    value = video_id_or_url.strip()
    if value.startswith(("http://", "https://")):
        return value
    platform_key = "x" if platform.lower() in {"x", "twitter"} else platform.lower()
    return f"https://{platform_key}.com/{value.lstrip('/')}"


def score_engagement(platform: str, video_id: str, publish_time: str, views: int) -> dict:
    """Score public engagement velocity from platform, source ID/URL, publish time, and views."""
    result = calculate_velocity(platform, _source_url(platform, video_id), publish_time, views)
    if "velocity_score" not in result:
        result["velocity_score"] = result.get("score", 0)
    if "views" not in result:
        result["views"] = views
    return result


def score_with_lifecycle(
    platform: str,
    video_id: str,
    publish_time: str,
    views: int,
    *,
    previous_views: int | None = None,
    previous_time: str | None = None,
) -> dict:
    """Score with lifecycle classification, acceleration, and recommendation.

    Args:
        platform: One of twitter/x, reddit, youtube, instagram.
        video_id: Source ID or full URL.
        publish_time: ISO timestamp of publication.
        views: Current engagement count.
        previous_views: Earlier engagement count for true acceleration (optional).
        previous_time: Earlier ISO timestamp for true acceleration (optional).

    Returns:
        Dict with score, velocity, acceleration_score, lifecycle_state, recommendation.
    """
    return calculate_velocity_with_lifecycle(
        platform,
        _source_url(platform, video_id),
        publish_time,
        views,
        previous_engagement=previous_views,
        previous_timestamp_str=previous_time,
    )


def main() -> int:
    parser = ArgumentParser(description="Calculate engagement velocity score.")
    parser.add_argument("platform")
    parser.add_argument("video_id_or_url")
    parser.add_argument("publish_time", help="ISO timestamp, e.g. 2026-06-01T10:00:00Z")
    parser.add_argument("views", type=int)
    args = parser.parse_args()

    result = score_engagement(args.platform, args.video_id_or_url, args.publish_time, args.views)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


__all__ = ["score_engagement", "score_with_lifecycle"]


if __name__ == "__main__":
    sys.exit(main())
