import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_clip import extract_clip_metadata
from get_youtube_transcript import extract_video_id
from score_engagement import calculate_velocity


class ExtractClipTests(unittest.TestCase):
    def test_extracts_youtube_clip_metadata(self):
        result = extract_clip_metadata("https://youtube.com/watch?v=dQw4w9WgXcQ", 10, 40)
        self.assertNotIn("error", result)
        self.assertEqual(result["duration"], 30)
        self.assertEqual(result["url_with_timestamp"], "https://youtube.com/watch?v=dQw4w9WgXcQ&t=10")

    def test_rejects_invalid_duration(self):
        result = extract_clip_metadata("https://youtube.com/watch?v=dQw4w9WgXcQ", 10, 80)
        self.assertIn("error", result)

    def test_rejects_invalid_url(self):
        result = extract_clip_metadata("not-a-url", 10, 40)
        self.assertIn("error", result)


class TranscriptInputTests(unittest.TestCase):
    def test_extracts_video_id_from_watch_url(self):
        self.assertEqual(
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
            "dQw4w9WgXcQ",
        )

    def test_rejects_invalid_video_id(self):
        with self.assertRaises(ValueError):
            extract_video_id("bad")


class EngagementScoreTests(unittest.TestCase):
    def test_rejects_unknown_platform(self):
        result = calculate_velocity("unknown", "https://example.com/post", "2026-01-01T00:00:00Z", 10)
        self.assertIn("error", result)

    def test_rejects_negative_engagement(self):
        result = calculate_velocity("twitter", "https://x.com/a/status/1", "2026-01-01T00:00:00Z", -1)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
