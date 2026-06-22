# Carousel Agent — Professional Agent Specification

> **Parent:** Goblin Recon (Hermes agent umbrella)
> **Type:** Production sub-agent — "the hands"
> **Version:** 1.0.0-draft
> **Status:** Plan mode — no code until approved
> **Memory log:** `docs/plans/carousel-agent-memory.md`

---

## 1. Agent Identity

### 1.1 What It Is

The Carousel Agent is a **production sub-agent** under the Goblin Recon umbrella. It takes a structured carousel brief and outputs Instagram-ready slide images. It does not decide what to post. It does not write copy from scratch. It *renders*.

```
Goblin Recon (brain)              Carousel Agent (hands)
├── Finds trends                  ├── Generates slide visuals
├── Selects carousel style        ├── Overlays brand typography
├── Writes copy                   ├── Assembles numbered slides
├── Runs brand gate               └── Outputs production-ready PNGs
└── Produces Carousel Brief ──────▶
```

### 1.2 Trigger Conditions

The agent fires when any of these are true:

| Trigger | Example |
|---------|---------|
| User explicitly requests a carousel | "Make me a carousel about AI agents" |
| Goblin Recon workflow outputs a carousel brief | Social Pulse → "this story works as a hook-slide carousel" |
| User provides a pre-written brief | "Build this brief for my brand" |
| User asks to explore carousel formats | "What carousel styles can you make?" |

### 1.3 What It Does NOT Do

| NOT Responsible For | Who Handles It |
|---------------------|----------------|
| Deciding what to post | Goblin Recon / Human |
| Writing copy from scratch | Goblin Recon (for GenX) or User (for custom brands) |
| Selecting carousel style | Goblin Recon maps topic → best style |
| Brand voice enforcement | Goblin Recon's Brand Gate (GenX mode only) |
| Posting to Instagram | Human / Scheduler |
| Adding trending audio | Human (out of scope for Replicate) |
| Video clip extraction | Goblin Recon's Clip Mine workflow |

---

## 2. Architecture

### 2.1 System Diagram

```
                          USER REQUEST
                               │
                               ▼
                    ┌─────────────────────┐
                    │   GOBLIN RECON       │
                    │   (Parent Agent)     │
                    │                      │
                    │  1. Route intent     │
                    │  2. Pre-flight brand │
                    │     check            │
                    │  3. Style selection  │
                    │  4. Copy generation  │
                    │  5. Brand gate       │
                    │     (GenX only)      │
                    │  6. Produce brief    │
                    └──────────┬──────────┘
                               │ Carousel Brief (dict/YAML)
                               ▼
                    ┌─────────────────────┐
                    │   CAROUSEL AGENT     │
                    │   (This Agent)       │
                    │                      │
                    │  ┌─────────────────┐ │
                    │  │ Stage 1: VALIDATE│ │
                    │  │ Brief + Brand    │ │
                    │  │ Config check     │ │
                    │  └────────┬────────┘ │
                    │           ▼          │
                    │  ┌─────────────────┐ │
                    │  │ Stage 2: GENERATE│ │
                    │  │ Replicate MCP    │ │
                    │  │ Flux Schnell/Pro │ │
                    │  │ 1 image per slide│ │
                    │  └────────┬────────┘ │
                    │           ▼          │
                    │  ┌─────────────────┐ │
                    │  │ Stage 3: COMPOSE │ │
                    │  │ Pillow text      │ │
                    │  │ overlay + brand  │ │
                    │  │ typography       │ │
                    │  └────────┬────────┘ │
                    │           ▼          │
                    │  ┌─────────────────┐ │
                    │  │ Stage 4: ASSEMBLE│ │
                    │  │ Number slides    │ │
                    │  │ Add dots/watermark│ │
                    │  │ Export PNGs      │ │
                    │  └────────┬────────┘ │
                    │           ▼          │
                    │  ┌─────────────────┐ │
                    │  │ Stage 5: VERIFY  │ │
                    │  │ Dimension check  │ │
                    │  │ Text readability │ │
                    │  │ File integrity   │ │
                    │  └────────┬────────┘ │
                    └────────────┼─────────┘
                                 ▼
                    ┌─────────────────────┐
                    │      OUTPUT          │
                    │  slide-01.png        │
                    │  slide-02.png        │
                    │  ...                 │
                    │  manifest.json       │
                    └─────────────────────┘
```

### 2.2 Tool Dependencies

| Tool | Provider | Purpose | Fallback |
|------|----------|---------|----------|
| Replicate MCP | `replicate-mcp` (npm) | Image generation (Flux Schnell/Pro) | Direct Replicate SDK if MCP unavailable |
| Pillow | Python `Pillow` | Text overlay, compositing, export | None — required |
| Brand Config | `brands/*.yaml` (local) | Colors, fonts, typography rules | `neutral-demo.yaml` |
| Style Bank | `config/carousel-styles.yaml` | 8 styles → Replicate prompts | Built-in defaults |
| Brand Gate | `goblin_recon.tools.brand_gate` | Blacklist + nuance word check | Skipped in custom mode |

### 2.3 File Map

```
goblin-recon/
│
├── goblin_recon/tools/
│   └── carousel_builder.py          ← Stage 3-5: compose + assemble + verify
│
├── skills/carousel-agent/
│   └── SKILL.md                     ← Agent operational instructions
│
├── config/
│   ├── carousel-styles.yaml         ← 8 styles → prompt strategies
│   └── mcp.json                     ← Replicate MCP server entry
│
├── brands/
│   ├── genx-b2b.yaml                ← GenX B2B brand config
│   ├── genx-b2c.yaml                ← GenX B2C brand config
│   └── neutral-demo.yaml            ← Fallback config
│
├── templates/
│   └── carousel-brief.md            ← Brief format spec
│
└── output/carousels/                ← Generated slides land here
    └── YYYY-MM-DD-<style>-<brand>/
```

---

## 3. Input Contract — The Carousel Brief

### 3.1 Required Fields

```yaml
# carousel-brief.yaml
style: hook-slide              # from config/carousel-styles.yaml
brand: genx-b2b                # references brands/<name>.yaml
slides:
  - text: "Slide 1 copy here"
    visual_direction: "Natural language description of desired visual"
  - text: "Slide 2 copy here"
    visual_direction: "Natural language description of desired visual"
```

### 3.2 Optional Fields

```yaml
model: flux-pro                 # default: flux-schnell
dimensions: [1080, 1440]        # default: [1080, 1440] (3:4 IG)
output_dir: ./output/carousels/ # default: output/carousels/YYYY-MM-DD-<style>-<brand>/
slide_numbering: true           # default: true
watermark: "© BrandName"       # default: none
```

### 3.3 Validation Rules

| Field | Rule | Error If |
|-------|------|----------|
| `style` | Must exist in `config/carousel-styles.yaml` | Unknown style name |
| `brand` | Must resolve to a `.yaml` in `brands/` | Brand config not found |
| `slides` | 2-20 slides. Each has `text` field. | Empty or over 20 |
| `visual_direction` | Optional per slide. Falls back to style default if missing. | — |
| `model` | Must be a valid Replicate model ID | Unknown model |

### 3.4 Who Produces the Brief?

| Scenario | Brief Writer | Brand Gate Applied? |
|----------|-------------|---------------------|
| GenX Academy content | Goblin Recon writes brief, applies GenX voice + blacklist | YES |
| Custom brand content | Goblin Recon writes brief, user's voice, no GenX rules | NO |
| User provides pre-written brief | User writes it. Agent validates and builds. | Only if brand=genx-* |

---

## 4. Output Contract

### 4.1 File Output

```
output/carousels/2026-06-17-hook-slide-genx-b2b/
├── slide-01.png
├── slide-02.png
├── slide-03.png
├── ...
└── manifest.json
```

### 4.2 Manifest

```json
{
  "brief": "carousel-brief.yaml",
  "brand": "genx-b2b",
  "style": "hook-slide",
  "model": "flux-schnell",
  "slides": 2,
  "dimensions": [1080, 1440],
  "generated_at": "2026-06-17T14:30:00Z",
  "replicate_predictions": ["pred_abc123", "pred_def456"],
  "total_credits_used": 0.006
}
```

### 4.3 Image Specs

| Property | Value |
|----------|-------|
| Format | PNG |
| Dimensions | 1080 × 1440 px (3:4 IG) |
| Resolution | 72 DPI (screen-optimized) |
| Color space | RGB |
| Max file size per slide | 2 MB |

---

## 5. The 5-Stage Pipeline

### Stage 1: VALIDATE

```
Input: Carousel Brief (dict)
Action:
  1. Validate style exists in carousel-styles.yaml
  2. Load brand config from brands/<name>.yaml
  3. Validate slide count (2-20)
  4. If brand_config.blacklist == true: run brand_gate on all slide text
  5. Resolve dimensions (brief override or default 1080×1440)
Output: ValidatedBrief + BrandConfig
Failure: Return validation errors, do not proceed
```

### Stage 2: GENERATE

```
Input: ValidatedBrief + BrandConfig
Action:
  1. For each slide:
     a. Build Replicate prompt from:
        - style.image_prompt_strategy (base aesthetic)
        - slide.visual_direction (specific instruction)
        - brand.tone (mood modifier)
     b. Call Replicate MCP predictions.create
     c. Poll predictions.get until complete
     d. Download generated image
  2. Run slides in parallel (Replicate supports concurrent predictions)
Output: List[Path] — raw generated images
Failure modes:
  - API key invalid → tell user to check REPLICATE_API_TOKEN
  - Model unavailable → fall back to flux-schnell
  - Timeout (>120s) → return partial results, flag incomplete slides
  - Rate limited → wait and retry once, then fail gracefully
```

### Stage 3: COMPOSE

```
Input: List[Path] (raw images) + ValidatedBrief + BrandConfig
Action:
  1. For each slide:
     a. Open raw image with Pillow
     b. Resize to target dimensions
     c. Apply brand typography:
        - Font: BrandConfig.typography.body_font
        - Size: BrandConfig.typography.body_size
        - Color: BrandConfig.colors.text
        - Position: centered with padding
     d. Render slide.text as overlay
  2. Text readability check: contrast ratio ≥ 4.5:1
Output: List[Path] — composed slide images
Failure modes:
  - Font file missing → fall back to system default, warn user
  - Text overflow → truncate with ellipsis, log warning
```

### Stage 4: ASSEMBLE

```
Input: List[Path] (composed slides) + ValidatedBrief + BrandConfig
Action:
  1. Add slide number indicator if slide_numbering == true
  2. Add watermark if configured
  3. Export as numbered PNGs: slide-01.png, slide-02.png, ...
  4. Generate manifest.json
Output: output_dir/ with all files
```

### Stage 5: VERIFY

```
Input: output_dir/
Action:
  1. Confirm all expected PNGs exist
  2. Check dimensions match spec
  3. File size sanity check (not 0 bytes, not >2MB)
  4. Text readability spot-check (first and last slide)
Output: VerificationReport { pass: bool, warnings: [], errors: [] }
```

---

## 6. Brand Configuration Specification

### 6.1 Schema

```yaml
# brands/<name>.yaml
name: string                    # unique brand identifier
source: internal | custom       # internal = ships with Goblin Recon
colors:
  primary: hex                  # main brand color
  background: hex               # slide background
  accent: hex                   # highlight / CTA color
  text: hex                     # body text color
  text_muted: hex               # secondary text (optional)
typography:
  heading_font: string          # TTF filename or system font
  body_font: string             # TTF filename or system font
  heading_size: int             # px (default: 48)
  body_size: int                # px (default: 36)
tone: professional | casual | edgy | warm | bold | minimal
slide_numbering: boolean        # show dot indicators
watermark: string | null        # optional watermark text
blacklist: boolean              # apply brand_gate? (GenX only)
brand_gate: boolean             # run blacklist + nuance-word check
```

### 6.2 Built-in Configs

| Config | Use Case | Tone | Blacklist |
|--------|----------|------|-----------|
| `genx-b2b` | GenX Academy B2B content | rigorous | YES |
| `genx-b2c` | Dr. Sara Hegy B2C content | warm | YES |
| `neutral-demo` | Exploration, demos, testing | professional | NO |

### 6.3 Custom Brand Minimum Fields

When a user creates a custom brand without a full YAML file, these 3 fields are mandatory:
1. **name** — brand identifier
2. **primary color** — hex code
3. **tone** — one of the 6 tone options

All other fields fall back to `neutral-demo` defaults. Missing fields are NOT blockers.

---

## 7. The Pre-Flight Brand Gate (Critical Workflow)

### 7.1 When It Runs

Before the carousel agent fires, Goblin Recon asks exactly once:

> "Is this carousel for GenX Academy, or for another brand? If another brand, tell me the brand name, primary color (hex), and tone."

### 7.2 Decision Tree

```
User Response
├── "GenX B2B"
│   → Load brands/genx-b2b.yaml
│   → Apply full brand gate (blacklist + nuance words)
│   → GenX voice: rigorous, no-BS, results-not-advice
│
├── "GenX B2C"
│   → Load brands/genx-b2c.yaml
│   → Apply full brand gate
│   → GenX voice: warm, alive, depth-plus-play
│
├── "Custom: Peak Fitness, #ff6b35, edgy"
│   → Scaffold brands/peak-fitness.yaml from 3 minimum fields
│   → NO brand gate, NO GenX voice rules
│   → User's voice, user's risk
│
├── "Custom: here's my brand.yaml at ~/brands/peak.yaml"
│   → Validate and load the provided file
│   → NO brand gate unless file sets blacklist: true
│
└── No answer / skip
    → Load brands/neutral-demo.yaml
    → State explicitly: "Using neutral demo config. No brand rules applied."
```

### 7.3 GenX Mode — Full Machinery

When `brand: genx-b2b` or `genx-b2c`:
- All slide text runs through `goblin_recon.tools.brand_gate`
- Blacklisted words → flagged, alternative suggested
- Nuance words (`limitless`, `alive`, etc.) → require before/after proof or flagged
- Tone must match B2B (rigorous) or B2C (warm)
- Fails hard: revise before generation, do not proceed with violations

### 7.4 Custom Mode — Raw Pipeline

When `brand: custom-*`:
- NO brand gate
- NO blacklist
- NO voice enforcement
- User's copy is rendered as-is
- Goblin Recon may offer suggestions but does not block

---

## 8. Style Bank Specification

### 8.1 The 8 Styles (from Brock Johnson, validated)

| ID | Name | GenX B2B | GenX B2C | Image Gen? | Slide Count |
|----|------|----------|----------|------------|-------------|
| `hook-slide` | Hook Slide | ★★★★★ | ★★★★ | YES | 2 |
| `freeze-frame` | Freeze Frame | ★★★★★ | ★★★★ | YES | 4–7 |
| `photo-dump-text` | Photo Dump + Text | ★★ | ★★★★ | YES | 3–8 |
| `collage` | Collage Style | ★ | ★★★ | NO — manual photos | 3–10 |
| `same-meme` | Same Meme, Different Meaning | ★★★★★ | ★★★ | NO — manual meme | 2–6 |
| `curated-collection` | Curated Collection | ★★★ | ★★★★★ | YES | 3–10 |
| `interactive` | Interactive | ★★ | ★★★ | YES | 2–5 |
| `flip-book` | Flip Book | ★ | ★★ | YES | 5–20 |

### 8.2 Prompt Strategy per Style

Each style has a `image_prompt_strategy` field in `config/carousel-styles.yaml` that maps to a Replicate prompt template:

```yaml
hook-slide:
  image_prompt_strategy: >
    Bold, high-contrast background. Dark mode. Clean, minimal composition.
    Large empty area in center for text overlay. No text in the generated image.
    News-alert or editorial aesthetic. No people. No clutter.
    {visual_direction}
    {tone_modifier}
```

The `{visual_direction}` comes from the brief. The `{tone_modifier}` comes from the brand config (e.g., "edgy, raw" or "warm, inviting").

---

## 9. Failure Modes & Recovery

| Failure | Detection | Recovery | User Sees |
|---------|-----------|----------|-----------|
| Replicate API key missing | `predictions.create` returns 401 | Stop. Do not proceed. | "Replicate API key not set. Add REPLICATE_API_TOKEN to your .env." |
| Model unavailable | `predictions.create` returns 404 | Fall back to flux-schnell | "Flux Pro unavailable. Used Flux Schnell instead." |
| Prediction timeout (>120s) | Stage 2 poll exceeds deadline | Return partial results | "Slide 3 of 5 timed out. 2 slides generated. Retry or reduce slide count?" |
| Rate limited | 429 response | Wait 10s, retry once. Then fail. | "Replicate rate limit hit. Try again in a minute." |
| Font file missing | Brand config references non-existent TTF | Fall back to system default | Warning: "Font X not found. Using system default." |
| Text overflow | Text renders beyond slide bounds | Truncate + log warning | Warning: "Slide 3 text truncated. Consider shorter copy." |
| Brand config not found | `brands/<name>.yaml` missing | Fall back to neutral-demo | "Brand 'X' not found. Using neutral demo. Create it with `carousel init-brand X`." |
| Style not found | Style not in carousel-styles.yaml | Stop. List available styles. | "Style 'X' not found. Available: hook-slide, freeze-frame, ..." |
| Image gen produces NSFW | Content filter check (optional) | Regenerate with modified prompt | "Generated image flagged. Regenerating with adjusted prompt." |

---

## 10. Integration With Goblin Recon Workflows

### 10.1 Social Pulse → Carousel

```
Social Pulse finds trending topic
  → Recon: "This works as a hook-slide carousel for GenX B2B"
  → Recon produces carousel brief
  → Carousel Agent builds slides
  → Human reviews + posts
```

### 10.2 Clip Mine → Carousel

```
Clip Mine finds strong clip moment
  → Recon: "This clip works as a freeze-frame carousel"
  → Recon extracts 4-6 key frames + transcript quotes
  → Recon produces carousel brief (freeze-frame style)
  → Carousel Agent generates backgrounds + overlays captions
```

### 10.3 Standalone (User Request)

```
User: "Make me a carousel about AI trends for my brand"
  → Pre-flight brand check
  → Recon writes brief
  → Carousel Agent builds
```

---

## 11. Testing Protocol

### 11.1 Unit Tests (per stage)

| Stage | What to Test |
|-------|-------------|
| Validate | Invalid style → error. Missing brand → fallback. Over 20 slides → error. |
| Generate | Mocked Replicate response → images saved. API failure → graceful error. |
| Compose | Text renders at correct position. Brand colors applied. Font fallback works. |
| Assemble | Correct filename pattern. Manifest generated. Watermark applied if set. |
| Verify | Missing file detected. Wrong dimensions flagged. Zero-byte file caught. |

### 11.2 Integration Tests

| Test | Expected |
|------|----------|
| GenX B2B + hook-slide | Blacklist applied. No violations in output. GenX tone. |
| Custom brand + curated-collection | No brand gate. User's colors applied. |
| Neutral demo + any style | No errors. Generic output. |
| 20-slide flip-book | All 20 slides generated. No timeout. |
| Missing API key | Clean error, no partial output. |

### 11.3 Test Command

```bash
cd goblin-recon
.venv/bin/pytest tests/test_carousel_agent.py -v
```

---

## 12. Implementation Phases

| Phase | What | Time Est. | Depends On |
|-------|------|-----------|------------|
| **P0** | Replicate MCP in `mcp.json` + API key test | 30 min | REPLICATE_API_TOKEN in .env |
| **P1** | `config/carousel-styles.yaml` + prompt strategies | 1 hr | — |
| **P2** | `brands/` directory + 3 built-in configs | 1 hr | — |
| **P3** | `goblin_recon/tools/carousel_builder.py` (Stages 1-5) | 3-4 hrs | P0, P1, P2 |
| **P4** | `skills/carousel-agent/SKILL.md` + pre-flight flow | 1-2 hrs | P3 |
| **P5** | `templates/carousel-brief.md` | 30 min | — |
| **P6** | End-to-end tests (GenX B2B, custom, neutral) | 1-2 hrs | P3, P4 |
| **P7** | Goblin Recon skill update (carousel as workflow option) | 1 hr | P4 |

---

## 13. Open Decisions

| # | Decision | Options | Impact |
|---|----------|---------|--------|
| 1 | **Default model** | Flux Schnell (fast, $0.003/img) vs Flux Pro (quality, $0.05/img) | Cost + speed |
| 2 | **Font strategy** | Bundle Inter + Playfair in `brands/fonts/` | User setup complexity |
| 3 | **Custom brand minimum** | 3 fields (name, color, tone) or require full YAML | Onboarding friction |
| 4 | **Collage + meme styles** | Ship as manual (user provides images), or drop from MVP | Scope |
| 5 | **Build order** | P0→P1→P2→P3→P4→P5→P6→P7 — any changes? | Sequencing |

---

## 14. References

- `memory/instagram-carousel-styles.md` — 8 styles from Brock Johnson video
- `docs/plans/carousel-agent-memory.md` — Running discussion log
- `config/brand-voice.yaml` — GenX voice rules (blacklist, nuance words)
- `goblin_recon/tools/brand_gate.py` — Brand gate implementation
- Replicate MCP docs: https://replicate.com/docs/reference/mcp
