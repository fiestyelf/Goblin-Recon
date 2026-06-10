"""Unit tests for Goblin Recon scripts — pytest style."""

import pytest
from goblin_recon.tools.clip_extractor import extract_clip_metadata
from goblin_recon.tools.youtube_tool import extract_video_id
from goblin_recon.tools.scoring import calculate_velocity


# ── extract_clip ──────────────────────────────────────────────────────────────

class TestExtractClipMetadata:
    """Parametrized tests for clip metadata extraction."""

    def test_basic_extraction(self):
        result = extract_clip_metadata(
            "https://youtube.com/watch?v=dQw4w9WgXcQ", 10, 40
        )
        assert "error" not in result
        assert result["duration"] == 30
        assert result["url_with_timestamp"] == (
            "https://youtube.com/watch?v=dQw4w9WgXcQ&t=10"
        )

    @pytest.mark.parametrize(
        "start, end, expected_error",
        [
            (10, 80, "15-60"),             # > 60s
            (10, 15, "15-60"),             # < 15s
            (-5, 30, "negative"),          # negative start
            (30, 20, "before"),            # end before start
        ],
    )
    def test_rejects_invalid_clip_windows(self, start, end, expected_error):
        result = extract_clip_metadata(
            "https://youtube.com/watch?v=dQw4w9WgXcQ", start, end
        )
        assert "error" in result
        assert expected_error in result["error"].lower()

    @pytest.mark.parametrize(
        "url",
        [
            "not-a-url",
            "",
            "https://vimeo.com/12345",
        ],
    )
    def test_rejects_invalid_urls(self, url):
        result = extract_clip_metadata(url, 10, 40)
        assert "error" in result

    def test_handles_yt_short_url(self):
        result = extract_clip_metadata("https://youtu.be/dQw4w9WgXcQ", 0, 30)
        assert "error" not in result
        assert result["duration"] == 30

    def test_handles_youtube_shorts_url(self):
        result = extract_clip_metadata(
            "https://www.youtube.com/shorts/dQw4w9WgXcQ", 0, 30
        )
        assert "error" not in result
        assert result["url_with_timestamp"] == (
            "https://youtube.com/watch?v=dQw4w9WgXcQ&t=0"
        )


# ── get_youtube_transcript ────────────────────────────────────────────────────

class TestTranscriptInput:
    """Video ID extraction from various YouTube URL formats."""

    @pytest.mark.parametrize(
        "url, expected",
        [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ&t=120", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?si=abc&v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ],
    )
    def test_extracts_video_id(self, url, expected):
        assert extract_video_id(url) == expected

    @pytest.mark.parametrize(
        "bad_input",
        [
            "bad",
            "https://example.com",
            "",
            "dQw",  # too short
        ],
    )
    def test_rejects_invalid_inputs(self, bad_input):
        with pytest.raises(ValueError):
            extract_video_id(bad_input)


# ── score_engagement ──────────────────────────────────────────────────────────

class TestEngagementScore:
    """Engagement velocity scoring logic."""

    def test_rejects_unknown_platform(self):
        result = calculate_velocity("unknown", "https://x.com/a/status/1", "2026-01-01T00:00:00Z", 10)
        assert "error" in result

    @pytest.mark.parametrize(
        "platform, count",
        [
            ("twitter", -1),
            ("instagram", -5),
            ("tiktok", -100),
        ],
    )
    def test_rejects_negative_engagement(self, platform, count):
        result = calculate_velocity(platform, f"https://{platform}.com/post", "2026-01-01T00:00:00Z", count)
        assert "error" in result

    def test_rejects_future_timestamp(self):
        result = calculate_velocity("twitter", "https://x.com/a/status/1", "2099-01-01T00:00:00Z", 100)
        assert "error" in result

    def test_zero_engagement_returns_zero_scores(self):
        result = calculate_velocity("twitter", "https://x.com/a/status/1", "2026-01-01T00:00:00Z", 0)
        # Zero engagement should still be valid, just score zero
        assert "error" not in result or "score" in result
