"""Small scoring helpers for Goblin Recon.

Ponytail rule: one velocity path, one lifecycle classifier, one diversity pass.
"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

SUPPORTED_PLATFORMS = {"twitter", "x", "reddit", "youtube", "instagram", "tiktok"}
BENCHMARKS = {
    "twitter": (10, 50, 200),
    "x": (10, 50, 200),
    "reddit": (5, 25, 100),
    "youtube": (50, 500, 2000),
    "instagram": (20, 100, 500),
    "tiktok": (50, 300, 1500),
}
DOMAIN_WEIGHTS = {
    "instagram": 1.0,
    "tiktok": 0.9,
    "x_twitter": 0.8,
    "twitter": 0.8,
    "x": 0.8,
    "youtube": 0.7,
    "reddit": 0.6,
    "tech_news": 0.5,
    "hacker_news": 0.5,
    "github": 0.4,
    "arxiv": 0.3,
}
MIN_ENGAGEMENT_FLOOR = 1000


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("post_url must be a valid http(s) URL")


def parse_timestamp(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00") if "T" in value else value + "+00:00")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _hours_since(timestamp: str) -> float:
    hours = (datetime.now(timezone.utc) - parse_timestamp(timestamp)).total_seconds() / 3600
    if hours < -0.1:
        raise ValueError("timestamp is in the future")
    return max(hours, 0.1)


def _velocity_score(platform: str, velocity: float) -> float:
    low, mid, high = BENCHMARKS[platform]
    if velocity >= high:
        return 20.0
    if velocity >= mid:
        return 15 + (velocity - mid) / (high - mid) * 5
    if velocity >= low:
        return 10 + (velocity - low) / (mid - low) * 5
    return max(0.0, velocity / low * 10)


def calculate_velocity(platform: str, post_url: str, timestamp_str: str, engagement_count: int) -> dict:
    try:
        platform = platform.lower()
        if platform not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        if engagement_count < 0:
            raise ValueError("engagement_count must be non-negative")
        validate_url(post_url)
        hours = _hours_since(timestamp_str)
        velocity = engagement_count / hours
        return {
            "score": round(_velocity_score(platform, velocity), 1),
            "velocity_per_hour": round(velocity, 2),
            "hours_since_post": round(hours, 2),
            "engagement_count": engagement_count,
            "platform": platform,
            "post_url": post_url,
        }
    except Exception as exc:
        return {"error": str(exc), "score": 0}


def _classify(velocity: float, acceleration: float, engagement: int, hours: float) -> tuple[str, str]:
    if engagement < MIN_ENGAGEMENT_FLOOR:
        return "BASELINE", f"Below {MIN_ENGAGEMENT_FLOOR} engagement floor. Monitor don't act."
    if velocity > 1000:
        return "VIRAL", "Already viral. Confirm with 2+ sources before clipping."
    if hours <= 6 and acceleration > 0:
        return "EMERGING", "Fresh story, growing and accelerating."
    if velocity > 200 and acceleration < -0.1:
        return "PEAKING", "Already peaking. Clip only with a unique angle."
    if velocity > 50 and acceleration < -0.3:
        return "DECLINING", "Past peak. Skip unless timeless."
    if velocity > 20:
        return "GROWING", "Steady growth. Good for analytical content."
    return "BASELINE", "Below velocity threshold. Not newsworthy yet."


def _acceleration_score(acceleration: float, engagement: int) -> float:
    if engagement < MIN_ENGAGEMENT_FLOOR:
        return 0.0
    if acceleration >= 1:
        return 1.0
    if acceleration > 0:
        return acceleration
    if acceleration <= -2:
        return 0.0
    return max(0.0, 0.5 + acceleration / 4)


def calculate_velocity_with_lifecycle(
    platform: str,
    post_url: str,
    timestamp_str: str,
    engagement_count: int,
    *,
    previous_engagement: int | None = None,
    previous_timestamp_str: str | None = None,
) -> dict:
    try:
        base = calculate_velocity(platform, post_url, timestamp_str, engagement_count)
        if "error" in base:
            return {**base, "lifecycle_state": "BASELINE"}

        velocity = base["velocity_per_hour"]
        hours = base["hours_since_post"]
        recent_velocity = trend_velocity = None
        if previous_engagement and previous_timestamp_str:
            prev_hours = max(_hours_since(previous_timestamp_str), hours + 0.01)
            trend_velocity = previous_engagement / prev_hours
            recent_velocity = velocity
            acceleration = (velocity - trend_velocity) / max(trend_velocity, 0.01)
        elif hours <= 2 and velocity > 500:
            acceleration = 1.0
        elif hours <= 6 and velocity > 100:
            acceleration = 0.5
        elif hours <= 24 and velocity > 50:
            acceleration = 0.2
        elif hours > 48:
            acceleration = -0.5
        else:
            acceleration = 0.0

        lifecycle, recommendation = _classify(velocity, acceleration, engagement_count, hours)
        accel_score = _acceleration_score(acceleration, engagement_count)
        score = min(20.0, max(0.0, base["score"] * 0.6 + accel_score * 20 * 0.4))
        return {
            **base,
            "score": round(score, 1),
            "acceleration_score": round(accel_score, 2),
            "lifecycle_state": lifecycle,
            "recent_velocity": round(recent_velocity, 2) if recent_velocity is not None else None,
            "trend_velocity": round(trend_velocity, 2) if trend_velocity is not None else None,
            "recommendation": recommendation,
        }
    except Exception as exc:
        return {"error": str(exc), "score": 0, "lifecycle_state": "BASELINE"}


def _story_domain(story: dict[str, Any]) -> str:
    for key in ("source_domain", "domain", "source_type", "source_platform", "platform", "primary_source", "source"):
        value = str(story.get(key) or "").strip().lower()
        if value:
            return value.replace("/", "_").replace(" ", "_")
    for key in ("url", "source_url", "post_url"):
        host = urlparse(str(story.get(key) or "")).netloc.lower().removeprefix("www.")
        if not host:
            continue
        for token, domain in {
            "instagram": "instagram",
            "tiktok": "tiktok",
            "x.com": "x_twitter",
            "twitter": "x_twitter",
            "youtube": "youtube",
            "youtu.be": "youtube",
            "reddit": "reddit",
            "github": "github",
            "arxiv": "arxiv",
            "news.ycombinator": "hacker_news",
        }.items():
            if token in host:
                return domain
        return host
    return "unknown"


def enforce_source_diversity(
    stories: list[dict[str, Any]],
    *,
    limit: int = 5,
    min_source_domains: int = 3,
    max_per_domain: int = 3,
    domain_weights: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    if limit <= 0 or not stories:
        return []
    if max_per_domain <= 0:
        raise ValueError("max_per_domain must be positive")

    weights = {**DOMAIN_WEIGHTS, **(domain_weights or {})}
    candidates = [(_story_domain(story), i, story) for i, story in enumerate(stories)]
    selected: list[tuple[str, int, dict[str, Any]]] = []
    seen: set[int] = set()
    counts: dict[str, int] = {}

    first_by_domain: dict[str, tuple[str, int, dict[str, Any]]] = {}
    for candidate in candidates:
        first_by_domain.setdefault(candidate[0], candidate)

    target_domains = min(max(min_source_domains, 1), len(first_by_domain), limit)
    for domain in sorted(first_by_domain, key=lambda d: (-weights.get(d, 0), first_by_domain[d][1]))[:target_domains]:
        selected.append(first_by_domain[domain])
        seen.add(first_by_domain[domain][1])
        counts[domain] = 1

    for domain, i, story in candidates:
        if len(selected) >= limit:
            break
        if i not in seen and counts.get(domain, 0) < max_per_domain:
            selected.append((domain, i, story))
            seen.add(i)
            counts[domain] = counts.get(domain, 0) + 1

    for domain, i, story in candidates:
        if len(selected) >= min(limit, len(stories)):
            break
        if i not in seen:
            selected.append((domain, i, story))
            seen.add(i)

    return [story for _, _, story in selected]


def main() -> int:
    parser = ArgumentParser(description="Calculate engagement velocity score.")
    parser.add_argument("platform", choices=sorted(SUPPORTED_PLATFORMS))
    parser.add_argument("post_url")
    parser.add_argument("timestamp")
    parser.add_argument("engagement_count", type=int)
    args = parser.parse_args()
    result = calculate_velocity(args.platform, args.post_url, args.timestamp, args.engagement_count)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
