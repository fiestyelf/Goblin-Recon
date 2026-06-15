"""Tests for Goblin Recon's shared template structure."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TEMPLATES = [
    "templates/README.md",
    "templates/social-pulse-report.md",
    "templates/news-brief.md",
    "templates/clip-mine-brief.md",
    "templates/caption-pack.md",
    "templates/competitor-report.md",
    "templates/content-brief.md",
]


def test_core_templates_exist():
    for rel in REQUIRED_TEMPLATES:
        assert (ROOT / rel).is_file(), rel


def test_core_templates_have_common_handoff_sections():
    for rel in REQUIRED_TEMPLATES[1:]:
        text = (ROOT / rel).read_text()
        assert "## Decision" in text, rel
        assert "Evidence Ledger" in text, rel
        assert "Security Rail" in text, rel
        assert "Review status" in text or "Review Status" in text, rel


def test_full_autonomous_scan_command_is_documented():
    commands = (ROOT / "COMMANDS.md").read_text()
    readme = (ROOT / "README.md").read_text()
    orchestrator = (ROOT / "skills" / "orchestrator" / "SKILL.md").read_text()
    goblin = (ROOT / "skills" / "goblin-recon" / "SKILL.md").read_text()

    for text in (commands, readme, orchestrator, goblin):
        assert "run full autonomous scan" in text


def test_caption_skill_uses_caption_pack_and_security_rail():
    skill = (ROOT / "skills" / "caption-tone" / "SKILL.md").read_text()

    assert "templates/caption-pack.md" in skill
    assert "skills/security-rail/SKILL.md" in skill
