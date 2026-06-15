"""Engagement velocity + acceleration scoring with lifecycle classification.

Inspired by neelmanivispute/trends-engine: velocity alone is misleading.
A story at 155% above baseline looks hot, but if it was at 250% last window,
acceleration is -0.95 — it's *peaking*, not *growing*.

Lifecycle states:
    BASELINE → EMERGING → GROWING → PEAKING → DECLINING → VIRAL
"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal
from urllib.parse import urlparse


SUPPORTED_PLATFORMS = {"twitter", "x", "reddit", "youtube", "instagram"}
DEFAULT_DOMAIN_WEIGHTS = {
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
    "github_trending": 0.4,
    "arxiv": 0.3,
}

LifecycleState = Literal[
    "BASELINE", "EMERGING", "GROWING", "PEAKING", "DECLINING", "VIRAL"
]

# Minimum absolute engagement before acceleration matters.
# Prevents noise: 10→50 views = meaningless 5x spike.
MIN_ENGAGEMENT_FLOOR = 1000


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
    try:
        platform = platform.lower()
        if platform not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        if engagement_count < 0:
            raise ValueError("engagement_count must be non-negative")
        validate_url(post_url)
        post_time = parse_timestamp(timestamp_str)
        hours_since = (datetime.now(timezone.utc) - post_time).total_seconds() / 3600
        if hours_since < -0.1:
            raise ValueError("timestamp is in the future")
        if hours_since <= 0:
            hours_since = 0.1

        velocity = engagement_count / hours_since
        benchmarks = {
            "twitter": {"low": 10, "mid": 50, "high": 200},
            "reddit": {"low": 5, "mid": 25, "high": 100},
            "youtube": {"low": 50, "mid": 500, "high": 2000},
            "instagram": {"low": 20, "mid": 100, "high": 500},
        }
        bench = benchmarks["twitter" if platform == "x" else platform]
        if velocity >= bench["high"]:
            score = 20
        elif velocity >= bench["mid"]:
            score = 15 + (velocity - bench["mid"]) / (bench["high"] - bench["mid"]) * 5
        elif velocity >= bench["low"]:
            score = 10 + (velocity - bench["low"]) / (bench["mid"] - bench["low"]) * 5
        else:
            score = velocity / bench["low"] * 10
        score = min(20, max(0, score))
        return {
            "score": round(score, 1),
            "velocity_per_hour": round(velocity, 2),
            "hours_since_post": round(hours_since, 2),
            "engagement_count": engagement_count,
            "platform": platform,
            "post_url": post_url,
        }
    except Exception as exc:
        return {"error": str(exc), "score": 0}


# ── Lifecycle Classification ────────────────────────────────────────────────


@dataclass
class LifecycleResult:
    """Full scoring result with lifecycle awareness."""
    score: float
    velocity_per_hour: float
    acceleration_score: float
    lifecycle_state: LifecycleState
    hours_since_post: float
    engagement_count: int
    platform: str
    post_url: str
    # Velocity bracket snapshots for debugging
    recent_velocity: float | None = None   # last 1h snapshot
    trend_velocity: float | None = None    # 1h-6h snapshot
    recommendation: str = ""

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 1),
            "velocity_per_hour": round(self.velocity_per_hour, 2),
            "acceleration_score": round(self.acceleration_score, 2),
            "lifecycle_state": self.lifecycle_state,
            "hours_since_post": round(self.hours_since_post, 2),
            "engagement_count": self.engagement_count,
            "platform": self.platform,
            "post_url": self.post_url,
            "recent_velocity": round(self.recent_velocity, 2) if self.recent_velocity else None,
            "trend_velocity": round(self.trend_velocity, 2) if self.trend_velocity else None,
            "recommendation": self.recommendation,
        }


def classify_lifecycle(
    velocity: float,
    acceleration: float,
    engagement_count: int,
    hours_since: float,
) -> tuple[LifecycleState, str]:
    """Classify a story into one of 6 lifecycle states.

    Args:
        velocity: Current views/engagement per hour.
        acceleration: Rate of velocity change (positive = accelerating, negative = decelerating).
        engagement_count: Absolute engagement count.
        hours_since: Hours since publication.

    Returns:
        (lifecycle_state, recommendation)
    """
    # Low engagement floor check — MUST come before velocity gates
    if engagement_count < MIN_ENGAGEMENT_FLOOR:
        return "BASELINE", f"Below {MIN_ENGAGEMENT_FLOOR} engagement floor. Monitor don't act."

    # Very high velocity regardless of acceleration = viral
    if velocity > 1000:
        return "VIRAL", "Already viral. Confirm with 2+ sources before clipping."

    # Fresh story with decent baseline = emerging
    if hours_since <= 6:
        if acceleration > 0.5:
            return "EMERGING", "Jump on this now — accelerating fast, early window."
        if acceleration > 0:
            return "EMERGING", "Fresh story, growing. Worth monitoring."

    # Strong velocity + strong acceleration = growing
    if velocity > 100 and acceleration > 0.3:
        return "GROWING", "Strong growth phase. Best time to source clips."

    # Strong velocity but negative acceleration = peaking
    if velocity > 200 and acceleration < -0.1:
        return "PEAKING", "Already peaking. Clip if you have something unique, otherwise skip."

    # Decent velocity with declining acceleration = declining
    if velocity > 50 and acceleration < -0.3:
        return "DECLINING", "Past peak. Skip unless the take is timeless."

    # Moderate velocity, slightly accelerating
    if velocity > 20 and acceleration > 0:
        return "EMERGING", "Moderate but accelerating. Worth a spot on the watchlist."

    # Moderate velocity, flat or decelerating
    if velocity > 20:
        return "GROWING", "Steady growth, not explosive. Good for analytical content."

    return "BASELINE", "Below velocity threshold. Not newsworthy yet."


def calculate_acceleration_score(
    velocity: float,
    acceleration: float,
    engagement_count: int,
) -> float:
    """Compute acceleration component (0.0–1.0).

    Guarded by MIN_ENGAGEMENT_FLOOR: stories below the floor get zero
    acceleration weight regardless of percentage growth.
    """
    if engagement_count < MIN_ENGAGEMENT_FLOOR:
        return 0.0

    # Positive acceleration → reward proportionally
    if acceleration >= 1.0:
        return 1.0
    if acceleration > 0:
        return min(1.0, acceleration)

    # Negative acceleration → penalize
    if acceleration <= -2.0:
        return 0.0
    # Linear interpolation from -2.0 (0%) to 0.0 (50%)
    return 0.5 + (acceleration / 4.0)


def calculate_velocity_with_lifecycle(
    platform: str,
    post_url: str,
    timestamp_str: str,
    engagement_count: int,
    *,
    previous_engagement: int | None = None,
    previous_timestamp_str: str | None = None,
) -> dict:
    """Calculate velocity + acceleration with lifecycle classification.

    If previous_engagement and previous_timestamp are provided, acceleration
    is computed as the rate of velocity change between two windows.
    Otherwise, a heuristic acceleration is estimated from single-window velocity.

    Returns:
        Dict with velocity, acceleration, lifecycle state, and recommendation.
    """
    try:
        platform = platform.lower()
        if platform not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        if engagement_count < 0:
            raise ValueError("engagement_count must be non-negative")
        validate_url(post_url)
        post_time = parse_timestamp(timestamp_str)
        hours_since = (datetime.now(timezone.utc) - post_time).total_seconds() / 3600
        if hours_since < -0.1:
            raise ValueError("timestamp is in the future")
        if hours_since <= 0:
            hours_since = 0.1

        velocity = engagement_count / hours_since

        # ── Acceleration computation ──
        if previous_engagement is not None and previous_timestamp_str is not None and previous_engagement > 0:
            # Two-window mode: compute actual acceleration
            prev_time = parse_timestamp(previous_timestamp_str)
            prev_hours_since = (datetime.now(timezone.utc) - prev_time).total_seconds() / 3600
            if prev_hours_since <= hours_since:
                prev_hours_since = hours_since + 0.01
            prev_velocity = previous_engagement / max(prev_hours_since, 0.1)
            # Acceleration = (current_velocity - previous_velocity) / previous_velocity
            acceleration = (velocity - prev_velocity) / max(prev_velocity, 0.01)
            recent_velocity = velocity
            trend_velocity = prev_velocity
        else:
            # Single-window heuristic: estimate acceleration from velocity bracket
            # Higher velocity in a short window implies acceleration
            if hours_since <= 2 and velocity > 500:
                acceleration = 1.0   # Very high short-window velocity → accelerating
            elif hours_since <= 6 and velocity > 100:
                acceleration = 0.5
            elif hours_since <= 24 and velocity > 50:
                acceleration = 0.2
            elif hours_since > 48:
                acceleration = -0.5  # Old content → decelerating
            else:
                acceleration = 0.0
            recent_velocity = None
            trend_velocity = None

        # ── Lifecycle classification ──
        lifecycle_state, recommendation = classify_lifecycle(
            velocity, acceleration, engagement_count, hours_since,
        )

        # ── Acceleration score (0.0-1.0) ──
        accel_score = calculate_acceleration_score(velocity, acceleration, engagement_count)

        # ── Combined score: 60% velocity + 40% acceleration ──
        # Map velocity to 0-20 scale (same as original)
        benchmarks = {
            "twitter": {"low": 10, "mid": 50, "high": 200},
            "reddit": {"low": 5, "mid": 25, "high": 100},
            "youtube": {"low": 50, "mid": 500, "high": 2000},
            "instagram": {"low": 20, "mid": 100, "high": 500},
        }
        bench = benchmarks["twitter" if platform == "x" else platform]
        if velocity >= bench["high"]:
            vel_score = 20
        elif velocity >= bench["mid"]:
            vel_score = 15 + (velocity - bench["mid"]) / (bench["high"] - bench["mid"]) * 5
        elif velocity >= bench["low"]:
            vel_score = 10 + (velocity - bench["low"]) / (bench["mid"] - bench["low"]) * 5
        else:
            vel_score = velocity / bench["low"] * 10
        vel_score = min(20, max(0, vel_score))

        # Acceleration on 0-20 scale for combination
        accel_20 = accel_score * 20
        combined = (vel_score * 0.6) + (accel_20 * 0.4)
        combined = min(20, max(0, combined))

        result = LifecycleResult(
            score=combined,
            velocity_per_hour=velocity,
            acceleration_score=accel_score,
            lifecycle_state=lifecycle_state,
            hours_since_post=hours_since,
            engagement_count=engagement_count,
            platform=platform,
            post_url=post_url,
            recent_velocity=recent_velocity,
            trend_velocity=trend_velocity,
            recommendation=recommendation,
        )
        return result.to_dict()
    except Exception as exc:
        return {"error": str(exc), "score": 0, "lifecycle_state": "BASELINE"}


def _story_domain(story: dict[str, Any]) -> str:
    """Return a stable source-domain key for a trend/story record.

    The agent receives records from different tools, so the source key may be
    named platform, source_type, domain, or only be inferable from a URL.
    """
    for key in (
        "source_domain",
        "domain",
        "source_type",
        "source_platform",
        "platform",
        "primary_source",
        "source",
    ):
        value = str(story.get(key) or "").strip().lower()
        if value:
            return value.replace("/", "_").replace(" ", "_")

    for key in ("url", "source_url", "post_url"):
        value = str(story.get(key) or "").strip()
        if not value:
            continue
        parsed = urlparse(value)
        host = parsed.netloc.lower().removeprefix("www.")
        if not host:
            continue
        if "instagram" in host:
            return "instagram"
        if "tiktok" in host:
            return "tiktok"
        if host in {"x.com", "twitter.com"}:
            return "x_twitter"
        if "youtube" in host or "youtu.be" in host:
            return "youtube"
        if "reddit" in host:
            return "reddit"
        if "github" in host:
            return "github"
        if "arxiv" in host:
            return "arxiv"
        if "news.ycombinator" in host:
            return "hacker_news"
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
    """Select a ranked story set without letting one source dominate.

    Input order is treated as the base ranking. The first pass reserves space
    for the best item from as many unique domains as required/available. The
    second pass fills remaining slots by original rank while respecting
    max_per_domain. This makes the YAML diversity policy deterministic instead
    of merely advisory.
    """
    if limit <= 0 or not stories:
        return []
    if max_per_domain <= 0:
        raise ValueError("max_per_domain must be positive")
    if min_source_domains <= 0:
        min_source_domains = 1

    weights = {**DEFAULT_DOMAIN_WEIGHTS, **(domain_weights or {})}
    candidates = [(_story_domain(story), idx, story) for idx, story in enumerate(stories)]
    available_domains = {domain for domain, _, _ in candidates}
    target_domains = min(min_source_domains, len(available_domains), limit)

    selected: list[tuple[str, int, dict[str, Any]]] = []
    selected_ids: set[int] = set()
    counts: dict[str, int] = {}

    # First pass: best-ranked story per source, weighted only as a tie-breaker.
    first_by_domain: dict[str, tuple[str, int, dict[str, Any]]] = {}
    for candidate in candidates:
        domain = candidate[0]
        first_by_domain.setdefault(domain, candidate)

    domain_order = sorted(
        first_by_domain,
        key=lambda domain: (-weights.get(domain, 0.0), first_by_domain[domain][1]),
    )
    for domain in domain_order:
        if len(selected) >= target_domains:
            break
        candidate = first_by_domain[domain]
        selected.append(candidate)
        selected_ids.add(candidate[1])
        counts[domain] = 1

    # Second pass: fill by original rank, respecting per-domain caps.
    for domain, idx, story in candidates:
        if len(selected) >= limit:
            break
        if idx in selected_ids:
            continue
        if counts.get(domain, 0) >= max_per_domain:
            continue
        selected.append((domain, idx, story))
        selected_ids.add(idx)
        counts[domain] = counts.get(domain, 0) + 1

    # If strict caps leave too few items, fill remaining by rank without caps.
    for domain, idx, story in candidates:
        if len(selected) >= min(limit, len(stories)):
            break
        if idx in selected_ids:
            continue
        selected.append((domain, idx, story))
        selected_ids.add(idx)

    return [story for _, _, story in selected]


def main() -> int:
    parser = ArgumentParser(description="Calculate engagement velocity score.")
    parser.add_argument("platform", choices=sorted(SUPPORTED_PLATFORMS))
    parser.add_argument("post_url")
    parser.add_argument("timestamp", help="ISO timestamp, e.g. 2026-06-01T10:00:00Z")
    parser.add_argument("engagement_count", type=int)
    args = parser.parse_args()

    result = calculate_velocity(args.platform, args.post_url, args.timestamp, args.engagement_count)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
