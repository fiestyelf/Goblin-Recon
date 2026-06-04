#!/usr/bin/env python3
"""
Goblin Recon — Engagement Velocity Calculator
Calculates how fast a post is gaining engagement (catches things going viral).

Usage:
    python score_engagement.py <platform> <post_url> <timestamp> <engagement_count>

Platforms:
    - twitter
    - reddit
    - youtube
    - instagram

Output:
    JSON with velocity score (0-20) and engagement metrics

Example:
    python score_engagement.py twitter "https://x.com/user/status/123" "2026-06-01T10:00:00Z" 1500
"""

from __future__ import annotations

import sys
import json
from argparse import ArgumentParser
from datetime import datetime, timezone
from urllib.parse import urlparse


SUPPORTED_PLATFORMS = {"twitter", "x", "reddit", "youtube", "instagram"}


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("post_url must be a valid http(s) URL")


def parse_timestamp(timestamp_str: str) -> datetime:
    if "T" in timestamp_str:
        post_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    else:
        post_time = datetime.fromisoformat(timestamp_str + "+00:00")
    if post_time.tzinfo is None:
        post_time = post_time.replace(tzinfo=timezone.utc)
    return post_time.astimezone(timezone.utc)


def calculate_velocity(platform: str, post_url: str, timestamp_str: str, engagement_count: int) -> dict:
    """Calculate engagement velocity."""
    try:
        platform = platform.lower()
        if platform not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        if engagement_count < 0:
            raise ValueError("engagement_count must be non-negative")
        validate_url(post_url)
        post_time = parse_timestamp(timestamp_str)
        now = datetime.now(timezone.utc)
        hours_since = (now - post_time).total_seconds() / 3600

        if hours_since < -0.1:
            raise ValueError("timestamp is in the future")
        if hours_since <= 0:
            hours_since = 0.1

        velocity = engagement_count / hours_since

        # Normalize to 0-20 scale based on platform benchmarks
        # These are rough thresholds for "going viral"
        benchmarks = {
            'twitter': {'low': 10, 'mid': 50, 'high': 200},
            'reddit': {'low': 5, 'mid': 25, 'high': 100},
            'youtube': {'low': 50, 'mid': 500, 'high': 2000},
            'instagram': {'low': 20, 'mid': 100, 'high': 500}
        }
        
        platform_key = "twitter" if platform == "x" else platform
        bench = benchmarks[platform_key]

        if velocity >= bench['high']:
            score = 20
        elif velocity >= bench['mid']:
            score = 15 + (velocity - bench['mid']) / (bench['high'] - bench['mid']) * 5
        elif velocity >= bench['low']:
            score = 10 + (velocity - bench['low']) / (bench['mid'] - bench['low']) * 5
        else:
            score = velocity / bench['low'] * 10
        
        score = min(20, max(0, score))
        
        return {
            "score": round(score, 1),
            "velocity_per_hour": round(velocity, 2),
            "hours_since_post": round(hours_since, 2),
            "engagement_count": engagement_count,
            "platform": platform,
            "post_url": post_url
        }
    except Exception as e:
        return {"error": str(e), "score": 0}


def main():
    parser = ArgumentParser(description="Calculate engagement velocity score.")
    parser.add_argument("platform", choices=sorted(SUPPORTED_PLATFORMS))
    parser.add_argument("post_url")
    parser.add_argument("timestamp", help="ISO timestamp, e.g. 2026-06-01T10:00:00Z")
    parser.add_argument("engagement_count", type=int)
    args = parser.parse_args()

    platform = args.platform
    post_url = args.post_url
    timestamp = args.timestamp
    engagement_count = args.engagement_count

    result = calculate_velocity(platform, post_url, timestamp, engagement_count)
    print(json.dumps(result, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
