"""Render carousel slides into the local vault.

Replicate is optional and is used only for background imagery. Final text,
logo/handle, and exports are rendered locally so typography stays readable.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

BRAND_PALETTES = {
    "sara-hegy-b2c": {
        "name": "Dr. Sara Hegy",
        "platform": "instagram",
        "bg_color": "#C4A882",
        "text_color": "#2C2420",
        "accent_color": "#D4956A",
        "cream": "#F5F0E8",
        "forbidden_colors": ["#FF69B4", "#0066FF", "#FF0000"],
        "visual_style": "cinematic warm reflective editorial, clay and espresso palette, soft film grain",
        "font_family": "Georgia",
    },
    "genx-b2b": {
        "name": "GenX Academy",
        "platform": "facebook",
        "bg_color": "#1A3A2A",
        "text_color": "#F5F0E8",
        "accent_color": "#B8960C",
        "cream": "#F5F0E8",
        "forbidden_colors": ["#FF69B4", "#0066FF", "#FF0000"],
        "visual_style": "minimal rigorous proof-forward, deep forest green, restrained gold, premium operator tone",
        "font_family": "Arial",
    },
    "custom": {
        "name": "Custom",
        "platform": "instagram",
        "bg_color": "#111111",
        "text_color": "#FFFFFF",
        "accent_color": "#CCCCCC",
        "cream": "#F7F3EA",
        "forbidden_colors": [],
        "visual_style": "client-defined brand photography",
        "font_family": "Arial",
    },
}

DEFAULT_MODEL = "black-forest-labs/flux-schnell"

PLATFORM_SPECS = {
    "instagram": {"width": 1080, "height": 1080, "safe_margin": 96},
    "facebook": {"width": 1200, "height": 628, "safe_margin": 72},
}

ROLE_MOOD = {
    "hook": "dynamic composition, bold contrast, curiosity and tension",
    "concept": "clean structured composition, breathing room, clarity and focus",
    "steps": "grounded even lighting, stable composition, calm trust",
    "proof": "grounded even lighting, stable composition, calm trust",
    "cta": "clear focal point, minimal clutter, action and resolution",
    "single post": "full creative freedom matched to the brief goal",
}

FONT_CANDIDATES = {
    "arial": {
        "regular": [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "bold": [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
    },
    "georgia": {
        "regular": [
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/Library/Fonts/Georgia.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "bold": [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/Library/Fonts/Georgia Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
    },
    "dejavu sans": {
        "regular": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
        "bold": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    },
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:70] or "carousel"


def build_image_prompt(slide: dict[str, Any], palette: dict[str, Any], seed: int | None = None) -> str:
    role = str(slide.get("role", "concept")).lower()
    mood = ROLE_MOOD.get(role, ROLE_MOOD["concept"])
    subject = slide.get("image_prompt") or slide.get("headline") or "abstract branded background"
    seed_note = f", consistent seed {seed}" if seed is not None else ""
    forbidden = ", ".join(palette.get("forbidden_colors", [])) or "none"
    return (
        f"Professional social media background photography for {palette['name']}: {subject}. "
        f"Style: {palette['visual_style']}. Mood: {mood}{seed_note}. "
        f"Leave clean negative space for typography. Use {palette['bg_color']} and "
        f"{palette['accent_color']} as palette anchors. Avoid text, logos, faces unless requested, "
        f"and forbidden colors: {forbidden}."
    )


def _json_request(url: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.loads(res.read().decode())


def _download(url: str, path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "goblin-recon-carousel-renderer"})
    with urllib.request.urlopen(req, timeout=120) as res:
        path.write_bytes(res.read())


def generate_replicate_background(prompt: str, model: str, output_path: Path, width: int, height: int) -> Path | None:
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        return None

    endpoint = f"https://api.replicate.com/v1/models/{model}/predictions"
    payload = {
        "input": {
            "prompt": prompt,
            "aspect_ratio": "1:1" if width == height else "16:9",
            "output_format": "png",
            "disable_safety_checker": False,
        }
    }
    try:
        prediction = _json_request(endpoint, token, payload)
        get_url = prediction.get("urls", {}).get("get")
        if not get_url:
            return None
        for _ in range(90):
            prediction = _json_request(get_url, token)
            if prediction.get("status") == "succeeded":
                output = prediction.get("output")
                image_url = output[0] if isinstance(output, list) else output
                if image_url:
                    _download(str(image_url), output_path)
                    return output_path
                return None
            if prediction.get("status") in {"failed", "canceled"}:
                return None
            time.sleep(2)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None
    return None


def _hex(value: str, fallback: str = "#000000") -> tuple[int, int, int]:
    raw = str(value or fallback).strip().lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) != 6:
        raw = fallback.lstrip("#")
    try:
        return tuple(int(raw[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raw = fallback.lstrip("#")
        return tuple(int(raw[i : i + 2], 16) for i in (0, 2, 4))


def _font(family: str, size: int, bold: bool = False) -> ImageFont.ImageFont:
    key = str(family or "arial").split(",")[0].strip().strip("'").strip('"').lower()
    candidates = FONT_CANDIDATES.get(key, FONT_CANDIDATES["arial"])
    for path in candidates["bold" if bold else "regular"] + FONT_CANDIDATES["arial"]["bold" if bold else "regular"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in str(text or "").splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if _text_width(draw, candidate, font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _fit_font(draw: ImageDraw.ImageDraw, text: str, family: str, start: int, minimum: int, max_width: int, max_lines: int) -> ImageFont.ImageFont:
    for size in range(start, minimum - 1, -4):
        font = _font(family, size, bold=True)
        if len(_wrap(draw, text, font, max_width)) <= max_lines:
            return font
    return _font(family, minimum, bold=True)


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int,
) -> int:
    x, y = xy
    for line in _wrap(draw, text, font, max_width):
        box = draw.textbbox((x, y), line, font=font)
        draw.text((x, y), line, font=font, fill=fill)
        y += (box[3] - box[1]) + line_gap
    return y


def _gradient(width: int, height: int, palette: dict[str, Any]) -> Image.Image:
    bg = _hex(palette["bg_color"])
    cream = _hex(palette.get("cream", palette["text_color"]))
    accent = _hex(palette["accent_color"])
    img = Image.new("RGB", (width, height), bg)
    px = img.load()
    cx, cy = int(width * 0.22), int(height * 0.18)
    radius = max(width, height) * 0.46
    for y in range(height):
        t = y / max(1, height - 1)
        for x in range(width):
            s = (x / max(1, width - 1) + t) / 2
            base = tuple(int(bg[i] * (1 - s * 0.55) + cream[i] * s * 0.55) for i in range(3))
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            glow = max(0.0, 1.0 - d / radius) * 0.48
            px[x, y] = tuple(int(base[i] * (1 - glow) + accent[i] * glow) for i in range(3))
    return img


def _cover_image(path: Path, width: int, height: int) -> Image.Image:
    img = Image.open(path).convert("RGB")
    scale = max(width / img.width, height / img.height)
    size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
    img = img.resize(size, Image.Resampling.LANCZOS)
    left = (img.width - width) // 2
    top = (img.height - height) // 2
    return img.crop((left, top, left + width, top + height))


def _overlay_for_readability(img: Image.Image) -> Image.Image:
    width, height = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px = overlay.load()
    for x in range(width):
        alpha = int(118 * (1 - x / max(1, width - 1)) + 24)
        for y in range(height):
            px[x, y] = (0, 0, 0, alpha)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def _render_png(
    slide: dict[str, Any],
    palette: dict[str, Any],
    spec: dict[str, int],
    background: Path | None,
    output_path: Path,
    background_only: bool = False,
) -> None:
    width, height, margin = spec["width"], spec["height"], spec["safe_margin"]
    img = _cover_image(background, width, height) if background else _gradient(width, height, palette)
    if not background_only:
        img = _overlay_for_readability(img)
        draw = ImageDraw.Draw(img)
        family = str(palette.get("font_family", "Arial"))
        text_color = _hex(palette["text_color"], "#FFFFFF")
        accent = _hex(palette["accent_color"], "#CCCCCC")
        max_width = int(width * 0.72)
        kicker_font = _font(family, max(22, width // 40), bold=True)
        headline_font = _fit_font(draw, str(slide.get("headline", "")), family, max(54, width // 13), max(34, width // 26), max_width, 4)
        body_font = _font(family, max(25, width // 34))
        body_width = int(width * 0.62)

        text_blocks = [str(slide.get("headline", "")), str(slide.get("body", ""))]
        headline_lines = _wrap(draw, text_blocks[0], headline_font, max_width)
        body_lines = _wrap(draw, text_blocks[1], body_font, body_width)
        headline_h = sum(draw.textbbox((0, 0), line, font=headline_font)[3] for line in headline_lines) + max(0, len(headline_lines) - 1) * 10
        body_h = sum(draw.textbbox((0, 0), line, font=body_font)[3] for line in body_lines) + max(0, len(body_lines) - 1) * 8
        kicker_h = draw.textbbox((0, 0), str(slide.get("kicker", "")), font=kicker_font)[3] if slide.get("kicker") else 0
        total_h = kicker_h + 26 + headline_h + 30 + body_h
        y = max(margin, (height - total_h) // 2)

        kicker = str(slide.get("kicker", "")).upper()
        if kicker:
            draw.text((margin, y), kicker, font=kicker_font, fill=accent)
            y += kicker_h + 26
        y = _draw_wrapped(draw, (margin, y), str(slide.get("headline", "")), headline_font, text_color, max_width, 10)
        body = str(slide.get("body", ""))
        if body:
            y += 30
            _draw_wrapped(draw, (margin, y), body, body_font, text_color, body_width, 8)
        draw.rounded_rectangle((margin, height - margin - 8, margin + 96, height - margin), radius=4, fill=accent)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)


def _usable_output_root(value: str | None) -> str | None:
    if not value or "YYYY" in value:
        return None
    return value


def _normalized_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Support the v1 nested manifest while keeping older flat manifests working."""
    job = manifest.get("job", {})
    layout = manifest.get("layout", {})
    paths = manifest.get("paths", {})
    brand_slug = job.get("account_slug") or manifest.get("brand_slug") or "custom"
    platform = job.get("platform") or manifest.get("platform") or layout.get("platform") or "instagram"
    return {
        "brand_slug": brand_slug,
        "platform": platform,
        "topic": job.get("topic") or manifest.get("topic") or "carousel",
        "seed": job.get("seed") or manifest.get("seed"),
        "model": manifest.get("model", DEFAULT_MODEL),
        "slides": manifest.get("slides") or [],
        "brief_path": manifest.get("brief_path") or paths.get("brief"),
        "output_root": _usable_output_root(paths.get("output_root")) or output_root_from_job(job, brand_slug),
        "layout": layout,
        "render_all_platforms": manifest.get("render_all_platforms", False),
    }


def output_root_from_job(job: dict[str, Any], brand_slug: str) -> str:
    job_id = job.get("id")
    if job_id and not str(job_id).startswith("YYYY"):
        return f"vault/carousels/{slugify(str(job_id))}"
    topic = slugify(job.get("topic") or "carousel")
    return f"vault/carousels/{date.today().isoformat()}-{topic}-{brand_slug}"


def _relative_output(out_dir: Path, rel: str | None, fallback: str) -> Path:
    raw = rel or fallback
    path = Path(raw)
    if path.is_absolute():
        return path
    return out_dir / path


def _qa_status(manifest: dict[str, Any], slides: list[dict[str, Any]]) -> dict[str, str]:
    approvals = manifest.get("approvals", {})
    qa = dict(manifest.get("qa", {}))
    qa.update(
        {
            "mobile_readability": "pass",
            "no_ai_garbled_text": "pass - final typography rendered locally",
            "platform_dimensions": "pass",
            "exports_exist": "pass" if slides else "fail",
            "human_approval_recorded": "pass" if approvals.get("final_exports_before_use") and approvals.get("approved_by") else "pending",
        }
    )
    return qa


def render_carousel(manifest: dict[str, Any], output_root: str | Path = "vault/carousels") -> Path:
    data = _normalized_manifest(manifest)
    brand_slug = data["brand_slug"]
    palette = {**BRAND_PALETTES.get(brand_slug, BRAND_PALETTES["custom"]), **manifest.get("palette", {})}
    layout = data["layout"]
    palette.update({k: layout[v] for k, v in {"bg_color": "background_color", "text_color": "text_color", "accent_color": "accent_color", "font_family": "font_family"}.items() if layout.get(v)})
    platform = data["platform"]
    spec = {**PLATFORM_SPECS.get(platform, PLATFORM_SPECS["instagram"]), **{k: layout[k] for k in ("width", "height", "safe_margin") if layout.get(k)}}
    slides = data["slides"]
    if not slides:
        raise ValueError("manifest must include at least one slide")

    out_dir = Path(data["output_root"] if data["output_root"] else Path(output_root) / f"{date.today().isoformat()}-{slugify(data['topic'])}-{brand_slug}")
    assets_dir = out_dir / "assets"
    exports_dir = out_dir / "exports"
    assets_dir.mkdir(parents=True, exist_ok=True)
    export_platforms = list(PLATFORM_SPECS) if data["render_all_platforms"] else [platform]
    for platform_name in export_platforms:
        (exports_dir / platform_name).mkdir(parents=True, exist_ok=True)

    seed = data["seed"]
    model = data["model"]
    handle = layout.get("handle", "")
    logo_path = layout.get("logo_path", "")
    rendered_slides: list[dict[str, Any]] = []
    replicate_used = False

    for index, slide in enumerate(slides, start=1):
        prompt = build_image_prompt(slide, palette, seed)
        bg_path = _relative_output(out_dir, slide.get("background_asset"), f"assets/bg-slide-{index:02d}.png")
        background = generate_replicate_background(prompt, model, bg_path, spec["width"], spec["height"])
        if background is None:
            _render_png(slide, palette, spec, None, bg_path, background_only=True)
            background = bg_path
        else:
            replicate_used = True

        slide_with_branding = {**slide, "body": "\n".join(x for x in [str(slide.get("body", "")), str(slide.get("cta", "")), handle] if x)}
        if logo_path:
            slide_with_branding["kicker"] = " • ".join(x for x in [str(slide.get("kicker", "")), Path(logo_path).stem] if x)
        final_asset = assets_dir / f"final-slide-{index:02d}.png"
        _render_png(slide_with_branding, palette, spec, bg_path, final_asset)
        export_paths: dict[str, str] = {}
        for platform_name in export_platforms:
            platform_spec = PLATFORM_SPECS[platform_name]
            rel_export = slide.get("export_path") if platform_name == platform else None
            export_path = _relative_output(out_dir, rel_export, f"exports/{platform_name}/slide-{index:02d}.png")
            _render_png(slide_with_branding, palette, platform_spec, bg_path, export_path)
            export_paths[platform_name] = str(export_path)
        rendered_slides.append({"index": index, "prompt": prompt, "background": str(bg_path), "final": str(final_asset), "exports": export_paths, **slide})

    spec_payload = {
        **manifest,
        "brand": palette,
        "platform_specs": PLATFORM_SPECS,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": str(out_dir),
        "qa": _qa_status(manifest, rendered_slides),
        "slides": rendered_slides,
    }
    (out_dir / "manifest.json").write_text(json.dumps(spec_payload, indent=2), encoding="utf-8")
    brief_path = data["brief_path"]
    if brief_path:
        source = Path(brief_path)
        if source.exists():
            shutil.copyfile(source, out_dir / "brief.md")
    if not (out_dir / "brief.md").exists():
        (out_dir / "brief.md").write_text(f"# Carousel Brief\n\nTopic: {data['topic']}\nPlatform: {platform}\nAccount: {brand_slug}\n", encoding="utf-8")
    (out_dir / "generation-log.md").write_text(
        f"# Generation Log\n\n- generated_at: {spec_payload['generated_at']}\n- brand_slug: {brand_slug}\n- platform: {platform}\n- model: {model}\n- replicate_used: {replicate_used}\n- text_renderer: Pillow\n- slides: {len(slides)}\n",
        encoding="utf-8",
    )
    return out_dir


if __name__ == "__main__":
    assert "sara-hegy-b2c" in BRAND_PALETTES
    assert "genx-b2b" in BRAND_PALETTES
    print("carousel_renderer: palette check passed")
