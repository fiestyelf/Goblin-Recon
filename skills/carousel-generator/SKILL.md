---
name: carousel-generator
description: |
  Build Instagram and Facebook carousel assets from a reference-first workflow.
  Use when the user asks to make a carousel, generate carousel slides, create a social image, or build editable carousel layers.
category: goblin-recon-content
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Carousel Generator

Generate Instagram/Facebook carousel assets while keeping strategy, page memory, text, layout, QA, and export controlled by Goblin Recon.

## Purpose

Turn an approved idea, source, or user brief into a finished editable carousel package.

This is not Social Pulse. Social Pulse finds ideas and formats. Carousel Generator creates the carousel asset package.

## Non-Goals

- No auto-posting.
- No direct publishing.
- No database or queue system.
- No LinkedIn/TikTok in MVP.
- No AI-generated final typography.

## Required Files

| File | Purpose |
|---|---|
| `templates/carousel-brief.md` | Human-readable carousel plan. |
| `templates/carousel-manifest.json` | Machine-readable render manifest. |
| `goblin_recon/tools/carousel_renderer.py` | Local renderer for final text/layout/export. |
| `memory/carousel/platforms/instagram.md` | Instagram carousel rules. |
| `memory/carousel/platforms/facebook.md` | Facebook carousel/page image rules. |
| `memory/carousel/accounts/*.md` | Page/account-specific memory. |
| `memory/carousel/trends/*.md` | Platform trend notes. |
| `memory/carousel/styles/*.md` | Reusable visual style rules. |
| `memory/carousel/performance/*.md` | Winning/weak format notes. |
| `config/brand-voice.yaml` | Voice, blacklist, and claim guardrails. |

## Trigger Phrases

Use this workflow for requests like:

- make an Instagram carousel
- create a carousel for this topic
- generate a Facebook carousel
- turn this idea into carousel slides
- create social image
- build editable carousel layers

## Workflow

### Step 1: Ask for Reference First

If no reference/template is provided, ask only this first:

```text
Please provide the carousel template or reference you want this generation to follow.
```

Accepted references:
- Existing carousel screenshot or image set
- Canva design
- Instagram/Facebook post link
- PDF
- Brand sample
- Manual template/style notes

Do not start by asking 10-15 intake questions.

### Step 2: Analyze Reference

Extract structure and visual style only:

- Slide count
- Aspect ratio
- Visual style
- Color palette
- Typography style
- Headline placement
- Body text density
- CTA pattern
- Logo/handle placement
- Slide-to-slide pacing

Do not copy third-party content or claims from the reference.

### Step 3: Load Memory

Load memory in this order:

```text
Page/account memory > Brand/client memory > Platform memory > Trend memory > Style memory > Performance memory
```

Safety and accuracy override all memory.

Use likely paths:

```text
memory/carousel/accounts/<account>.md
memory/carousel/platforms/instagram.md
memory/carousel/platforms/facebook.md
memory/carousel/trends/*.md
memory/carousel/styles/*.md
memory/carousel/performance/*.md
config/brand-voice.yaml
```

### Step 4: Ask Only Missing Questions

After reference + memory, ask only 2-4 missing questions.

Good questions:
- Which page/account is this for?
- What topic or source should this carousel cover?
- What CTA should the final slide use?
- Should the tone be educational, promotional, repurposed, or trend-based?

Do not ask for details already obvious from the user request, reference, or memory.

### Step 5: Create Carousel Plan

Before image generation, produce a plan with:

```text
Carousel title:
Platform:
Account/page:
Slide count:
Target audience:
Goal:
Style reference summary:
Memory rules applied:
Slide-by-slide outline:
Visual generation plan:
Assets needed:
```

Human approval is required before calling Replicate or spending credits.

### Step 6: Generate Visual Layers

Replicate rule:

```text
Replicate = visual generation only.
Goblin Recon = strategy, memory, text, layout, QA, and export.
```

Replicate may generate:
- Backgrounds
- Abstract visuals
- Product mockups
- Scenes
- Textures
- Illustrations

Replicate must not generate:
- Final slide text
- Logos
- Handles
- CTA text
- Final typography

If `REPLICATE_API_TOKEN` is missing or Replicate fails, use the renderer fallback backgrounds and continue if quality is acceptable. The Replicate MCP is for agent/tool generation; `goblin_recon.tools.carousel_renderer` uses `REPLICATE_API_TOKEN` directly when run locally.

### Step 7: Render Locally

Use the Pillow renderer to add real text and layout:

- Headline
- Body text
- Logo
- Handle
- CTA
- Page/account name
- Safe margins
- Slide numbers if needed

Text changes should be manifest edits + re-render, not background regeneration.

### Step 8: QA Gate

Before final output, check:

- Text is readable on mobile.
- No AI-garbled text appears in final exports.
- Platform dimensions are correct.
- Brand/page voice matches memory.
- Claims are safe and sourced.
- CTA is clear when needed.
- Slides are visually consistent.
- Export files exist.
- Human approval is recorded.

If QA fails, recommend `revise` or `shelve`, not approve.

### Step 9: Save Output Package

Save every job under:

```text
vault/carousels/<date-topic-page>/
  manifest.json
  brief.md
  generation-log.md
  assets/
  exports/
    instagram/
    facebook/
```

## Output Format

```markdown
## Decision

Recommend: approve for human review / revise / shelve
Platform: [instagram/facebook]
Account: [account_slug]
Saved: [vault path]

## Files

| File | Purpose |
|---|---|
| manifest.json | Editable carousel source of truth |
| brief.md | Human-readable carousel plan |
| generation-log.md | Generation and revision log |
| assets/bg-slide-01.png | Visual/background layer |
| exports/[platform]/slide-01.png | Final rendered slide |

## QA

- Readability: pass / needs edits
- Dimensions: pass / fail
- Brand/page fit: pass / needs edits
- Claims: safe / needs source / shelve
- Replicate: used / fallback
- Human gate: required before final use

## Next Step

[Approve, revise copy/layout, regenerate backgrounds, or shelve]
```
