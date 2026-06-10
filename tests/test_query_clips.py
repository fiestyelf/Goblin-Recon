"""Tests for the Clip Mine query CLI."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
from goblin_recon.tools.clip_store import save_clip


def sample_clip(**overrides):
    clip = {
        "status": "approved",
        "brand_angle": "B2B",
        "brand_alignment_score": 12,
        "trend_headline": "AI agents replace manual SDR workflows",
        "source_title": "AI Sales Debate",
        "source_channel_or_account": "Example Channel",
        "source_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "start_timestamp": "0:45",
        "end_timestamp": "1:15",
        "start_sec": 45,
        "end_sec": 75,
        "duration_seconds": 30,
        "moment_summary": "A concrete operator take on replacing manual research.",
        "why_post": "Clear mechanism with strong B2B relevance.",
        "suggested_caption": "What changes when AI agents handle the first pass?",
    }
    clip.update(overrides)
    return clip


def run_cli(db_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "query_clips.py"), "--db", str(db_path), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_lists_clips_as_json(tmp_path):
    db_path = tmp_path / "clips.db"
    clip_id = save_clip(sample_clip(), db_path)

    result = run_cli(db_path, "list", "--status", "approved", "--query", "agents", "--json")

    assert result.returncode == 0
    records = json.loads(result.stdout)
    assert [record["clip_id"] for record in records] == [clip_id]


def test_cli_exports_brief_to_file(tmp_path):
    db_path = tmp_path / "clips.db"
    output_path = tmp_path / "brief.md"
    clip_id = save_clip(sample_clip(), db_path)

    result = run_cli(db_path, "brief", clip_id, "--output", str(output_path))

    assert result.returncode == 0
    assert "Brief written:" in result.stdout
    brief = output_path.read_text(encoding="utf-8")
    assert "# Clip Mine Brief" in brief
    assert f"Clip ID: {clip_id}" in brief
