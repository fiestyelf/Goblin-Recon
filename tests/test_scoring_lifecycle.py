"""Tests for lifecycle-aware scoring and source diversity enforcement."""

from datetime import datetime, timedelta, timezone

from goblin_recon.tools.scoring import (
    calculate_velocity_with_lifecycle,
    enforce_source_diversity,
)


def iso_hours_ago(hours: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()


def test_lifecycle_marks_low_engagement_as_baseline():
    result = calculate_velocity_with_lifecycle(
        "youtube",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        iso_hours_ago(1),
        50,
    )

    assert result["lifecycle_state"] == "BASELINE"
    assert result["acceleration_score"] == 0


def test_lifecycle_detects_fresh_emerging_story():
    result = calculate_velocity_with_lifecycle(
        "youtube",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        iso_hours_ago(2),
        2000,
    )

    assert result["lifecycle_state"] == "EMERGING"
    assert result["score"] > 0
    assert "growing" in result["recommendation"].lower() or "accelerating" in result["recommendation"].lower()


def test_lifecycle_detects_peaking_with_two_windows():
    result = calculate_velocity_with_lifecycle(
        "reddit",
        "https://reddit.com/r/artificial/comments/example",
        iso_hours_ago(2),
        1500,
        previous_engagement=6000,
        previous_timestamp_str=iso_hours_ago(6),
    )

    assert result["lifecycle_state"] == "PEAKING"
    assert result["trend_velocity"] > result["recent_velocity"]


def test_enforce_source_diversity_limits_single_domain_dominance():
    stories = [
        {"headline": "ig 1", "platform": "instagram", "score": 99},
        {"headline": "ig 2", "platform": "instagram", "score": 98},
        {"headline": "ig 3", "platform": "instagram", "score": 97},
        {"headline": "ig 4", "platform": "instagram", "score": 96},
        {"headline": "reddit 1", "platform": "reddit", "score": 80},
        {"headline": "youtube 1", "platform": "youtube", "score": 75},
        {"headline": "tiktok 1", "platform": "tiktok", "score": 70},
    ]

    selected = enforce_source_diversity(
        stories,
        limit=5,
        min_source_domains=3,
        max_per_domain=2,
    )

    platforms = [story["platform"] for story in selected]
    assert len(selected) == 5
    assert len(set(platforms)) >= 3
    assert platforms.count("instagram") <= 2
    assert {"reddit", "youtube"}.issubset(platforms)
