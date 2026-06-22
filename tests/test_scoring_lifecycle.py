"""Tests for lifecycle-aware scoring."""

from datetime import datetime, timedelta, timezone

from goblin_recon.tools.scoring import calculate_velocity_with_lifecycle


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
