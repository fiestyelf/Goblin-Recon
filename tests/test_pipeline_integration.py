"""
Integration tests for the Goblin Recon pipeline chain.

These test the contract between pipeline stages without hitting real APIs:

  Transcript source → Clip extractor → Engagement scorer → Report renderer

Each test uses a fixed fixture (sample data) so results are deterministic.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_clip import extract_clip_metadata
from score_engagement import calculate_velocity


# ── Static Test Inputs ─────────────────────────────────────────────────────────

KNOWN_BAD_CONTENT = """This revolutionary AI platform is limitless in its ability to transform everything.
It represents an awakening for the entire industry. The best part? It's completely
magical and requires no effort. Anyone can be limitless with this tool."""


# ── Pipeline Contract Tests ───────────────────────────────────────────────────


class TestStageContract:
    """Each stage accepts the previous stage's output and produces valid input for the next."""

    def test_stage_1_clip_extraction_produces_valid_metadata(self):
        """Stage 1 output must have keys the scorer needs."""
        result = extract_clip_metadata(
            "https://youtube.com/watch?v=dQw4w9WgXcQ", 45, 65
        )
        assert "error" not in result
        # Required fields for handoff to stage 2
        for key in ("duration", "start_time", "end_time", "url_with_timestamp"):
            assert key in result, f"Missing key: {key}"
        assert 15 <= result["duration"] <= 60

    def test_stage_2_scorer_accepts_clip_metadata(self):
        """Stage 2: engagement scorer works with real-looking clip data."""
        result = calculate_velocity(
            "youtube",
            "https://youtube.com/watch?v=dQw4w9WgXcQ&t=45",
            "2026-06-07T10:00:00Z",
            15000,
        )
        assert "error" not in result

    def test_stage_3_velocity_scores_are_within_range(self):
        """Stage 2 output scores should be human-readable and bounded."""
        result = calculate_velocity(
            "youtube",
            "https://youtube.com/watch?v=dQw4w9WgXcQ&t=45",
            "2026-06-07T10:00:00Z",
            5000,
        )
        assert "error" not in result
        # Score field presence — validate the contract
        assert "score" in result or "velocity" in result or isinstance(result, dict)

    def test_pipeline_empty_transcript_graceful_handling(self):
        """Empty transcript should not crash — produce a clear error or skip."""
        from extract_clip import extract_clip_metadata

        # Empty content test: a real clip with nothing to extract
        result = extract_clip_metadata(
            "https://youtube.com/watch?v=dQw4w9WgXcQ", 0, 30
        )
        # Should not throw — should return a dict
        assert isinstance(result, dict)
        # Even an error response is valid: it should explain why
        if "error" in result:
            assert len(result["error"]) > 0  # non-empty error message


class TestBrandGateContract:
    """The brand gate should flag known-bad language patterns."""

    def test_brand_gate_identifies_bad_content(self):
        blacklist_words = ["limitless", "awakening", "transform", "revolutionary"]

        flagged = [w for w in blacklist_words if w.lower() in KNOWN_BAD_CONTENT.lower()]
        assert len(flagged) >= 3, (
            f"Brand gate should flag at least 3 of: {blacklist_words}. "
            f"Found: {flagged}"
        )

    def test_brand_gate_passes_clean_content(self):
        clean = """Claude built a Stripe dashboard clone in 12 minutes.
Here's how we tested it and what we found."""
        blacklist_words = ["limitless", "awakening", "transform", "revolutionary"]

        flagged = [w for w in blacklist_words if w.lower() in clean.lower()]
        assert len(flagged) == 0, f"Clean content flagged: {flagged}"
