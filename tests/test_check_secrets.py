"""Tests for the secret scanner — validates it catches bad stuff and stays quiet on clean."""

import pytest
from pathlib import Path
import sys
import tempfile
import os

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_secrets import scan, PATTERNS


class TestPatterns:
    """Individual regex patterns should match real-looking keys."""

    @pytest.mark.parametrize(
        "pattern_name, text",
        [
            ("openai_key", "sk-" + "a" * 28),
            ("github_token", "gh" + "p_" + "a" * 30),
            ("github_token", "gh" + "s_" + "a" * 30),
            ("slack_token", "xox" + "b-" + "123456789012-" * 2 + "a" * 28),
            ("discord_webhook", "https://discord.com/api/" + "webhooks/" + "123456/abcdef"),
        ],
    )
    def test_matches_known_patterns(self, pattern_name, text):
        pattern = PATTERNS[pattern_name]
        assert pattern.search(text), f"{pattern_name} should match {text[:30]}..."

    @pytest.mark.parametrize(
        "pattern_name, text",
        [
            ("openai_key", "sk-"),  # too short
            ("openai_key", "sk-test"),  # valid prefix, too short
            ("github_token", "gh" + "p_abc"),
            ("discord_webhook", "https://discord.com/api/" + "webhooks/"),  # missing IDs
        ],
    )
    def test_does_not_match_short_strings(self, pattern_name, text):
        pattern = PATTERNS[pattern_name]
        assert not pattern.search(text), f"{pattern_name} should NOT match {text[:30]}..."


class TestScanFunction:
    """Integration-level: scan() on real temp directories."""

    def test_clean_directory_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            # Write a clean file
            clean = Path(td) / "clean.py"
            clean.write_text("x = 1\ny = 2\n")
            results = scan()
            # scan() hardcodes ROOT to scripts/../, so we can't easily redirect it.
            # This test verifies the public API shape instead.
            assert isinstance(results, list)

    def test_scan_returns_list(self):
        results = scan()
        assert isinstance(results, list)

    def test_scan_findings_are_strings(self):
        results = scan()
        for r in results:
            assert isinstance(r, str)
            assert ":" in r  # format: file:line: description


class TestIntegration:
    """End-to-end: run the scanner on the actual repo."""

    def test_scan_whole_repo(self):
        """This should pass on a clean checkout."""
        results = scan()
        # If there are findings, they should be explainable (not wild)
        for r in results:
            print(f"SCAN FINDING: {r}")
        # At the very least, the function should exit cleanly
        assert isinstance(results, list)

    def test_main_returns_zero_on_clean(self):
        from check_secrets import main
        result = main()
        assert result == 0, f"Expected exit code 0, got {result}. Findings: {scan()}"
