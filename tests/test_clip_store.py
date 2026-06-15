"""Tests for the persistent Clip Mine SQLite store."""

from goblin_recon.tools.clip_store import (
    check_duplicate,
    check_novelty,
    find_clips,
    get_clip,
    render_clip_brief,
    save_clip,
    update_status,
)


def sample_clip(**overrides):
    clip = {
        "status": "pending_review",
        "brand_angle": "B2B",
        "brand_alignment_score": 12,
        "trend_headline": "AI agents replace manual SDR workflows",
        "source_title": "AI Sales Debate",
        "source_channel_or_account": "Example Channel",
        "source_url": "https://www.youtube.com/watch?si=abc&v=dQw4w9WgXcQ",
        "start_timestamp": "0:45",
        "end_timestamp": "1:15",
        "start_sec": 45,
        "end_sec": 75,
        "duration_seconds": 30,
        "moment_summary": "A concrete operator take on replacing manual research.",
        "why_post": "Clear mechanism with strong B2B relevance.",
        "suggested_caption": "What changes when AI agents handle the first pass?",
        "blacklist_flags": [],
        "human_decision": "pending",
    }
    clip.update(overrides)
    return clip


def test_save_and_retrieve_clip(tmp_path):
    db_path = tmp_path / "clips.db"

    clip_id = save_clip(sample_clip(), db_path)
    stored = get_clip(clip_id, db_path)

    assert stored is not None
    assert stored["clip_id"] == clip_id
    assert stored["source_video_id"] == "dQw4w9WgXcQ"
    assert stored["duration_seconds"] == 30
    assert stored["status"] == "pending_review"


def test_check_duplicate_by_video_and_time_window(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(sample_clip(start_sec=45, end_sec=75), db_path)

    duplicates = check_duplicate(
        "https://www.youtube.com/shorts/dQw4w9WgXcQ", 70, 100, db_path=db_path
    )

    assert [clip["clip_id"] for clip in duplicates] == [clip_id]


def test_update_status(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(sample_clip(), db_path)

    assert update_status(clip_id, "approved", human_decision="approve", db_path=db_path)
    stored = get_clip(clip_id, db_path)

    assert stored["status"] == "approved"
    assert stored["human_decision"] == "approve"


def test_find_clips_by_status(tmp_path):
    db_path = tmp_path / "clips.db"
    approved_id = save_clip(sample_clip(status="approved", start_sec=45, end_sec=75), db_path)
    save_clip(sample_clip(status="shelved", start_sec=120, end_sec=150), db_path)

    approved = find_clips(status="approved", db_path=db_path)


    assert [clip["clip_id"] for clip in approved] == [approved_id]


def test_find_clips_by_query(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(sample_clip(moment_summary="A retention spike around agent demos."), db_path)

    matches = find_clips(query="retention spike", db_path=db_path)

    assert [clip["clip_id"] for clip in matches] == [clip_id]


def test_find_clips_searches_caption_and_why_post(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(
        sample_clip(
            why_post="This gives operators a concrete retention hook.",
            suggested_caption="The first pass belongs to agents now.",
        ),
        db_path,
    )

    matches = find_clips(query="first pass", db_path=db_path)

    assert [clip["clip_id"] for clip in matches] == [clip_id]


def test_render_clip_brief_has_retrieval_links(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(sample_clip(status="approved"), db_path)
    clip = get_clip(clip_id, db_path)

    brief = render_clip_brief(clip)

    assert "## Source Access" in brief
    assert "https://www.youtube.com/watch?si=abc&v=dQw4w9WgXcQ&t=45" in brief
    assert "https://www.youtube.com/embed/dQw4w9WgXcQ?start=45&end=75" in brief
    assert f"Clip ID: {clip_id}" in brief


def test_check_novelty_flags_near_duplicate_approved_clip(tmp_path):
    db_path = tmp_path / "clips.db"
    save_clip(
        sample_clip(
            status="approved",
            moment_summary="AI agents replace manual SDR research workflows with automated first pass qualification",
        ),
        db_path,
    )

    novelty = check_novelty(
        "AI agents replace manual SDR research workflows with automated first pass qualification",
        threshold=0.8,
        db_path=db_path,
    )

    assert novelty["novelty_status"] == "near_duplicate"
    assert novelty["similarity_score"] >= 0.8
    assert novelty["similar_clips"]


def test_check_novelty_allows_distinct_clip_summary(tmp_path):
    db_path = tmp_path / "clips.db"
    save_clip(
        sample_clip(
            status="approved",
            moment_summary="AI agents replace manual SDR research workflows with automated qualification",
        ),
        db_path,
    )

    novelty = check_novelty(
        "A founder explains why meditation retreats changed her leadership style",
        threshold=0.8,
        db_path=db_path,
    )

    assert novelty["novelty_status"] == "novel"
    assert novelty["similar_clips"] == []
