"""Tests for Competitor Scout v2 configuration and templates."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_competitors_config_uses_source_typed_entries():
    config = yaml.safe_load((ROOT / "config" / "competitors.yaml").read_text())
    competitors = config["competitors"]

    assert competitors
    for competitor in competitors:
        assert competitor["name"]
        assert competitor["domain"]
        assert competitor["website"].startswith("https://")
        assert competitor["pricing_page"].startswith("https://")
        assert competitor["sources"]
        kinds = {source["kind"] for source in competitor["sources"]}
        assert "homepage" in kinds
        assert "pricing" in kinds
        for source in competitor["sources"]:
            assert source["url"].startswith("https://")
            assert source["kind"] in {
                "homepage",
                "pricing",
                "blog",
                "changelog",
                "jobs",
                "docs",
                "about",
                "events",
                "press",
                "podcast",
                "other",
            }


def test_competitor_report_template_has_cells_and_security_rail():
    template = (ROOT / "templates" / "competitor-report.md").read_text()

    assert "## Cell-Ready Moves" in template
    assert "Content Cell" in template
    assert "Sales Cell" in template
    assert "Product/Offer Cell" in template
    assert "## Security Rail Result" in template


def test_competitor_skill_mentions_security_rail_and_cells():
    skill = (ROOT / "skills" / "competitor-scout" / "SKILL.md").read_text()

    assert "Step 6.5 — Security Rail" in skill
    assert "Cell-Ready Moves" in skill
    assert "Security Rail is mandatory before delivery" in skill
