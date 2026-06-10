"""Tests for social signal intake normalization."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
from goblin_recon.tools.social_intake import (
    append_records,
    infer_platform,
    load_records,
    normalize_social_record,
    recommend_next_step,
)


def test_infers_common_social_platforms():
    assert infer_platform("https://www.instagram.com/reel/abc/") == "instagram"
    assert infer_platform("https://www.tiktok.com/@creator/video/123") == "tiktok"
    assert infer_platform("https://x.com/user/status/123") == "x_twitter"
    assert infer_platform("https://www.reddit.com/r/artificial/comments/abc") == "reddit"
    assert infer_platform("https://youtu.be/dQw4w9WgXcQ") == "youtube"


def test_normalizes_manual_instagram_signal():
    record = normalize_social_record(
        {
            "url": "https://www.instagram.com/reel/abc/",
            "creator": "therundownai",
            "published_date": "2026-06-09",
            "topic": "OpenAI agent launch",
            "views": "123,456",
            "caption": "New agent workflow just dropped",
            "hook": "AI agents are replacing the first draft",
            "access_status": "manual_ok",
            "capture_method": "manual_assisted",
        }
    )

    assert record["platform"] == "instagram"
    assert record["views"] == 123456
    assert record["validation"]["ok"]
    assert record["recommendation"] == "use_in_social_pulse"


def test_normalizes_abbreviated_metric_formats():
    record = normalize_social_record(
        {
            "url": "https://www.tiktok.com/@creator/video/123",
            "published_date": "2026-06-09",
            "topic": "AI workflow demo",
            "caption": "This AI workflow is spreading",
            "views": "1.2K views",
            "likes": "3M likes",
            "comments": "456 comments",
            "access_status": "manual_ok",
        }
    )

    assert record["views"] == 1200
    assert record["likes"] == 3000000
    assert record["comments"] == 456
    assert record["shares"] is None
    assert record["validation"]["ok"] is True


def test_rejects_negative_and_malformed_metrics():
    record = normalize_social_record(
        {
            "url": "https://www.instagram.com/reel/abc/",
            "published_date": "2026-06-09",
            "topic": "AI workflow demo",
            "caption": "Workflow demo",
            "views": "-5",
            "likes": "abc123",
            "comments": -3,
            "access_status": "manual_ok",
        }
    )

    assert record["views"] is None
    assert record["likes"] is None
    assert record["comments"] is None
    assert record["validation"]["ok"] is False
    assert record["validation"]["invalid_metrics"] == ["comments", "likes", "views"]
    assert record["recommendation"] == "needs_review"


def test_blocked_signal_requires_manual_input_when_notes_missing():
    record = normalize_social_record(
        {
            "url": "https://www.tiktok.com/@creator/video/123",
            "topic": "AI workflow demo",
            "access_status": "blocked",
        }
    )

    assert record["validation"]["ok"] is False
    assert "source blocked" in record["validation"]["warnings"][0]
    assert recommend_next_step(record) == "manual_assisted_input"


def test_youtube_signal_moves_to_clip_mine():
    record = normalize_social_record(
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "published_date": "2026-06-09",
            "topic": "AI agents in sales",
            "caption": "Founder explains AI SDR replacement",
            "access_status": "public_ok",
            "capture_method": "public_browser",
        }
    )

    assert record["platform"] == "youtube"
    assert record["recommendation"] == "move_to_clip_mine"


def test_missing_published_date_does_not_advance():
    record = normalize_social_record(
        {
            "url": "https://www.instagram.com/reel/abc/",
            "topic": "AI demos",
            "caption": "A simple workflow demo",
            "access_status": "manual_ok",
        }
    )

    assert record["validation"]["ok"] is False
    assert "published_date" in record["validation"]["missing"]
    assert record["recommendation"] == "needs_review"


def test_append_records_stores_jsonl(tmp_path):
    input_path = tmp_path / "signal.json"
    store_path = tmp_path / "signals.jsonl"
    input_path.write_text(
        json.dumps(
            {
                "url": "https://www.instagram.com/reel/abc/",
                "published_date": "2026-06-09",
                "topic": "AI demos",
                "caption": "A simple workflow demo",
                "access_status": "manual_ok",
            }
        ),
        encoding="utf-8",
    )

    records = [normalize_social_record(record) for record in load_records(input_path)]
    append_records(records, store_path)

    lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    stored = json.loads(lines[0])
    assert stored["platform"] == "instagram"
    assert stored["recommendation"] == "use_in_social_pulse"


def test_invalid_record_is_not_stored(tmp_path):
    input_path = tmp_path / "signal.json"
    store_path = tmp_path / "signals.jsonl"
    input_path.write_text(
        json.dumps(
            {
                "url": "https://www.instagram.com/reel/abc/",
                "topic": "AI demos",
                "caption": "A simple workflow demo",
                "access_status": "manual_ok",
            }
        ),
        encoding="utf-8",
    )

    records = [normalize_social_record(record) for record in load_records(input_path)]
    valid_records = [record for record in records if record["validation"]["ok"]]
    if valid_records:
        append_records(valid_records, store_path)

    assert not store_path.exists()


def test_load_records_rejects_non_object_list(tmp_path):
    input_path = tmp_path / "signal.json"
    input_path.write_text(json.dumps(["bad"]), encoding="utf-8")

    try:
        load_records(input_path)
    except ValueError as exc:
        assert "list must contain only objects" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
