# Carousel Generator — Design Plan

**Date:** 2026-06-21
**Status:** Ready to build
**Runs in:** Hermes
**Brands:** Dr. Sara Hegy (B2C / Instagram) + GenX Academy (B2B / Facebook)

---

## What We're Building

A carousel and social image generator skill. User fills a brief → agent asks 3 questions → generates slides with AI backgrounds + clean text → exports editable layers.

---

## Key Decisions

| Decision | Choice | Why |
|---|---|---|
| Image renderer | Pillow PNG renderer | Fewer moving parts than browser screenshots; deterministic local typography |
| AI backgrounds | Replicate API | Generates background visuals per slide |
| Fallback (no Replicate token) | CSS gradient from brand palette | No crash, still works |
| Brand selection | Optional gate | Works for any client, not just Sara/GenX |
| Output format | 3 layers per slide + JSON spec | Editable without regenerating |
| Style/model mapping | Dict inside renderer | No separate YAML file needed |
| Folder creation | Inline in renderer | No separate file needed |

---

## How It Works (Plain English)

```
User fills carousel-brief.md template
         ↓
Agent asks 3 questions:
  Q1. Which brand? (Sara / GenX / Custom / Quick Test)
  Q2. Carousel or single post?
  Q3. What type? (Educational / Promotional / Repurposing / Trend)
         ↓
Agent builds image prompt per slide
         ↓
Replicate generates background image per slide
(fallback: color gradient if no token)
         ↓
Pillow composites background, overlay, and local text
Pillow exports each slide as PNG
         ↓
3 files saved per slide:
  bg_1.png        ← just the background
  final_1.png     ← background + text combined
  slide_spec.json ← all text/colors/fonts (re-renderable)
         ↓
QA check: blacklist + brand voice + dimensions
         ↓
Human approves → files saved to vault/carousels/
```

---

## Brand Options

```
Q1 options:
→ Dr. Sara Hegy (B2C / Instagram)
   Palette: Clay #C4A882 / Espresso #2C2420 / Gold #D4956A
   Style: Cinematic, warm, reflective

→ GenX Academy (B2B / Facebook or LinkedIn)
   Palette: Forest Green #1A3A2A / Cream #F5F0E8 / Gold #B8960C
   Style: Minimal, rigorous, proof-forward

→ Custom
   Agent asks: brand name + platform + colors

→ Quick Test
   Black and white, no brand rules
```

---

## Carousel Types

```
Educational:   hook → concept → steps → proof → CTA
Promotional:   problem → offer → proof → urgency → CTA
Repurposing:   original source → key moments → context → CTA
Trend:         what happened → why it matters → our take → CTA
```

---

## Output Folder Structure

```
vault/carousels/
  2026-06-21-ai-tools-101-genx-b2b/
    slide_spec.json          ← edit this to change text, re-render
    assets/
      bg_1.png               ← background only (Replicate output)
      bg_2.png
      final_1.png            ← ready-to-post slide
      final_2.png
    exports/
      instagram/             ← 1080x1080 versions
      facebook/              ← 1200x628 versions
    brief.md                 ← the brief you submitted
    generation-log.md        ← what was generated and when
```

---

## Files to Create/Edit — Full List

### Step 1 — Commit existing doc changes (7 files already done, just saving)
- `AGENTS.md`
- `COMMANDS.md`
- `GETTING_STARTED.md`
- `INSTRUCTIONS.md`
- `README.md`
- `skills/goblin-recon/SKILL.md`
- `updates/hermes/goblin-recon-command-reference.md`

---

### Step 2 — Clean up existing file
**File:** `design-image-prompt-engineer.md` (exists, untracked)

**Delete:**
- Line ~13: fake "Experience" backstory
- Lines ~172-180: "Success Metrics" section
- "Communication Style" section — merge into "Prompt Engineering Standards"

**Add 3 new sections:**

```
#### Seed & Consistency Layer (carousel only)
- seed: integer — lock same value across all slides for visual coherence
- carousel_position: "hook" | "body" | "cta" — informs mood per slide

#### Slide Role → Mood Map
| Role        | Mood              | Visual Energy | Prompt modifier                             |
|-------------|-------------------|---------------|---------------------------------------------|
| hook        | Curiosity/tension | High          | Dynamic composition, bold contrast          |
| concept     | Clarity/focus     | Medium        | Clean, structured, breathing room           |
| steps/proof | Trust/calm        | Low-medium    | Grounded, even lighting, stable composition |
| CTA         | Action/resolution | Medium-high   | Clear focal point, minimal clutter          |
| single post | Depends on goal   | Any           | No constraint — full creative freedom       |

#### Brand Palette Injection (fill per client)
- bg_color: ""
- text_color: ""
- accent_color: ""
- forbidden_colors: []
- visual_style: ""
```

**Update frontmatter description:** "Multi-client photography prompt engineer. Works for any brand or project."

---

### Step 3 — Main renderer (new Python file)
**File:** `goblin_recon/tools/carousel_renderer.py`

Contains everything in one file:
- `BRAND_PALETTES` dict — colors for all 4 brand options
- `DEFAULT_MODEL` constant — one Replicate model unless a manifest overrides it
- `PLATFORM_SPECS` dict — Instagram + Facebook dimensions
- Replicate API call → background image (try/except → gradient fallback)
- Pillow background composer
- Pillow text/layout renderer
- Layer export: bg_{n}.png + final_{n}.png
- Vault folder creation (os.makedirs inline)
- Self-check:
  ```python
  if __name__ == "__main__":
      assert "sara-hegy-b2c" in BRAND_PALETTES
      assert "genx-b2b" in BRAND_PALETTES
      print("carousel_renderer: palette check passed")
  ```

---

### Step 4 — Memory files (4 files only, no placeholders)
```
memory/carousel/
  platforms/
    instagram.md    ← specs, safe zones, caption rules
    facebook.md     ← specs, aspect ratios, caption rules
  accounts/
    sara-hegy-b2c.md  ← palette, tone, blacklist, slide preferences
    genx-b2b.md       ← palette, tone, blacklist, slide preferences
```
Voice rules + blacklist pulled from existing `config/brand-voice.yaml`

---

### Step 5 — Main skill file (new)
**File:** `skills/carousel-generator/SKILL.md`

Full workflow: brand gate → post type → carousel type → prompt build → Replicate → Pillow → QA → human gate → vault export.

---

### Step 6 — Templates (2 new files)
**`templates/carousel-brief.md`**
Fields: topic, reference (URL/image/text), slide copy ideas, target audience, tone/mood, brand_slug, carousel_type

**`templates/carousel-manifest.json`**
Schema: brand_slug, carousel_type, slide_count, per-slide spec, generation date, file paths

---

### Step 7 — Replicate token note (1 file edit)
- `.env.example` — keep `REPLICATE_API_TOKEN=` note for the direct renderer API path only. No Replicate MCP wiring.

---

### Step 8 — Docs update (2 file edits)
**`AGENTS.md`** — add to commands table:
```
| run carousel generator | Build a multi-slide carousel for Instagram or Facebook |
| generate single post   | Make one social image for a topic                     |
```
**`COMMANDS.md`** — add matching entries in plain English style

---

## What We Decided NOT to Build

| Skipped | Reason |
|---|---|
| `carousel_assets.py` | Merged into renderer — just 3 lines |
| `config/carousel-models.yaml` | Dict inside renderer |
| `config/carousel-platforms.yaml` | Dict inside renderer |
| `memory/carousel/styles/` (3 files) | Info already in account files |
| `memory/carousel/performance/` (2 files) | No real data yet |
| `memory/carousel/trends/` (2 files) | No real data yet |

---

## Build Order

1. Commit 7 existing doc changes
2. Clean up `design-image-prompt-engineer.md` + commit
3. Build `carousel_renderer.py` + run self-check
4. Build 4 memory files
5. Build `skills/carousel-generator/SKILL.md`
6. Build 2 templates
7. Wire MCP config (4 files)
8. Update `AGENTS.md` + `COMMANDS.md`
9. Run `python -m pytest tests/` — all existing tests must pass
10. Final commit

---

## How to Test After Build

1. `python goblin_recon/tools/carousel_renderer.py` → prints "palette check passed"
2. `python -m pytest tests/` → all green
3. In Hermes: sara-hegy-b2c → educational → confirm palette + layers exported
4. In Hermes: genx-b2b → promotional → confirm green/gold palette
5. Check `vault/carousels/` folder has brand slug in name
6. Remove `REPLICATE_API_TOKEN` → re-run → gradient fallback works
