# Carousel Agent — Planning Memory

> **Started:** Jun 17, 2026
> **Purpose:** Running log of all carousel agent discussions. Decisions, ideas, tradeoffs. Referenced before coding begins.
> **Rule:** Plan mode only. No code until the user says go.

---

## Session 1 — Jun 17, 2026 (Initial Research)

### Source Material
- Scraped Brock Johnson / Build Your Tribe video (238K views, Jul 2025)
- Extracted 8 carousel styles → saved to `memory/instagram-carousel-styles.md`

### The 8 Styles (Reference)
1. Hook Slide (2 slides: headline → value)
2. Freeze Frame (comic-book, captioned stills from video)
3. Photo Dump + Text (visual-first, text overlay)
4. Collage Style (ultra-wide canvas, split into slides)
5. Same Meme, Different Meaning (one meme, multiple audience labels)
6. Curated Collection (standalone quotes/visuals under one theme)
7. Interactive (swipe = action, pick-a-path)
8. Flip Book (stop-motion via rapid swipe)

### Architecture Evolution
- v1: Internal-only (hardcoded GenX) → rejected
- v2: Standalone PyPI package → rejected (user wants it under Goblin Recon)
- v3: Goblin Recon native, multi-brand pre-flight → ACCEPTED

---

## Session 2 — Jun 17, 2026 (Professional Agent Spec)

### What We Built
- Full professional agent specification (`docs/plans/carousel-agent-plan.md`)
- Covers: identity, triggers, input/output contracts, 5-stage pipeline, failure modes, brand config schema, pre-flight gate, testing protocol, implementation phases

### Key Architecture Decisions
- ✅ Carousel Agent = sub-agent under Goblin Recon umbrella
- ✅ Goblin Recon = brain (style selection, copy, brand gate). Carousel Agent = hands (render, compose, assemble)
- ✅ Pre-flight brand gate: "GenX or custom?" before every build
- ✅ GenX mode: full blacklist + nuance word check. Custom mode: raw pipeline, no rules
- ✅ 5-stage pipeline: Validate → Generate → Compose → Assemble → Verify
- ✅ Replicate MCP for image gen (Flux Schnell default, Pro override)
- ✅ Pillow for text overlay (Replicate can't do typography)
- ✅ 3 built-in brand configs: genx-b2b, genx-b2c, neutral-demo
- ✅ Custom brands: 3 minimum fields (name, primary color, tone)
- ✅ Two non-image-gen styles (collage, same-meme) ship as manual

### Documents Created/Updated
- `memory/instagram-carousel-styles.md` — 8 style reference bank
- `docs/plans/carousel-agent-plan.md` — Full professional agent spec (22K+)
- `docs/plans/carousel-agent-memory.md` — This file

### Open Decisions (Still Pending)
- [ ] Default model: Flux Schnell vs Flux Pro
- [ ] Font strategy: bundle in `brands/fonts/` or user provides paths
- [ ] Custom brand minimum: 3 fields good? Or require full YAML?
- [ ] Collage + meme styles: ship as manual or drop from MVP?
- [ ] Build order: P0→P7 sequence confirmed?
- [ ] Replicate API key: ready in .env?

---

## Session 3 — [Date TBD]

### Discussion Points
-

### Decisions Made
-

### Documents Updated
-
