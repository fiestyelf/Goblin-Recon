import json
from pathlib import Path

from PIL import Image

from goblin_recon.tools.carousel_renderer import render_carousel

ROOT = Path(__file__).resolve().parents[1]


def test_carousel_renderer_fallback_creates_output_package(monkeypatch, tmp_path):
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    manifest = json.loads((ROOT / "templates" / "carousel-manifest.json").read_text())
    manifest["job"].update(
        {
            "id": "pytest-carousel-smoke",
            "topic": "pytest carousel smoke",
            "platform": "instagram",
            "account_slug": "genx-b2b",
        }
    )
    manifest["paths"]["output_root"] = str(tmp_path / "pytest-carousel-smoke")
    manifest["slides"] = [
        {
            "number": 1,
            "role": "hook",
            "kicker": "AUDIT",
            "headline": "Readable local text",
            "body": "This renders without Replicate or a browser.",
            "cta": "Review before posting.",
            "image_prompt": "clean branded abstract background",
            "background_asset": "assets/bg-slide-01.png",
            "export_path": "exports/instagram/slide-01.png",
            "revision_notes": [],
        }
    ]

    out = render_carousel(manifest)

    for rel in [
        "manifest.json",
        "brief.md",
        "generation-log.md",
        "assets/bg-slide-01.png",
        "assets/final-slide-01.png",
        "exports/instagram/slide-01.png",
    ]:
        assert (out / rel).is_file(), rel

    with Image.open(out / "exports/instagram/slide-01.png") as img:
        assert img.size == (1080, 1080)

    rendered = json.loads((out / "manifest.json").read_text())
    assert rendered["qa"]["exports_exist"] == "pass"
    assert rendered["qa"]["no_ai_garbled_text"].startswith("pass")
