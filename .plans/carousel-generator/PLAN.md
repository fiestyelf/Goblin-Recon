# Carousel Generator Agent Architecture

## What This Is
A multi-purpose carousel generation sub-agent under Goblin Recon. Takes structured carousel briefs and outputs Instagram/Facebook-ready slide images using Replicate MCP for visuals and Pillow for text overlay.

## Architecture
5-stage pipeline: Validate → Generate (Replicate MCP) → Compose (Pillow text) → Assemble → Verify.
Goblin Recon = brain (strategy, copy, brand gate). Carousel Agent = hands (render, compose, assemble).

## Key Decisions
- Replicate MCP for visual generation, Pillow for text overlay (AI can't do typography)
- 8 carousel styles from Brock Johnson research
- 3 built-in brand configs: genx-b2b, genx-b2c, neutral-demo
- Pre-flight brand gate: "GenX or custom?" before every build
- GenX mode: full blacklist + brand gate. Custom mode: raw pipeline, no gate
- Reference-first workflow: ask for template/reference first, then 2-4 missing questions
- Memory-driven: platform/page/brand/style/trend memory files

## Files to Create
- mcp.json, config/hermes-mcp.yaml, config/integrations.yaml (Replicate MCP)
- skills/carousel-agent/SKILL.md
- templates/carousel-brief.md, templates/carousel-manifest.json
- config/carousel-styles.yaml
- brands/genx-b2b.yaml, brands/genx-b2c.yaml, brands/neutral-demo.yaml
- memory/carousel/ (platforms, accounts, trends, styles, performance)
- goblin_recon/tools/carousel_builder.py (5-stage pipeline)
- vault/carousels/ output structure

## Detailed Spec
See docs/plans/carousel-agent-plan.md (full professional agent spec)
See docs/plans/carousel-agent-memory.md (session decision log)

## Open Decisions
- Default model: Flux Schnell vs Flux Pro
- Font strategy: bundle fonts or user provides
- Collage + meme styles: manual or drop from MVP
- REPLICATE_API_TOKEN status
