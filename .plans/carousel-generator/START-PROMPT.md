[EXECUTING PLAN — FOLLOW THE PLAN EXACTLY]

You are executing a structured plan. Your ONLY job is to implement the plan tasks below, one at a time.

Rules:
- Work on ONE task at a time, starting with t-001
- After completing each task, IMMEDIATELY call update_task to mark it done with notes
- Do NOT run diagnostics, linters, test suites, or skills unless a task explicitly asks for it
- Do NOT explore the codebase beyond what the current task requires
- Do NOT deviate from the plan — if something seems wrong, call update_task with status "blocked"
- If you notice worthwhile work OUTSIDE the plan, call add_task to capture it, then keep going

## Current task
t-001: Add Replicate MCP config
Details: Add Replicate MCP server entry to mcp.json, config/hermes-mcp.yaml, config/integrations.yaml. Use npx -y replicate-mcp@latest. Token from env only.

## Handoff
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

## All remaining tasks
t-001. Add Replicate MCP config
   Details: Add Replicate MCP server entry to mcp.json, config/hermes-mcp.yaml, config/integrations.yaml. Use npx -y replicate-mcp@latest. Token from env only.

t-002. Create carousel agent SKILL.md
   Details: Create skills/carousel-agent/SKILL.md. 5-stage pipeline, pre-flight brand gate, reference-first workflow, memory loading order, Replicate+Pillow rules, QA gate.

t-003. Add templates: brief and manifest
   Details: templates/carousel-brief.md (input contract) and templates/carousel-manifest.json (output spec).

t-004. Create styles YAML + 3 brand configs + memory dirs
   Details: config/carousel-styles.yaml with 8 styles. brands/genx-b2b.yaml, genx-b2c.yaml, neutral-demo.yaml. memory/carousel/ directory tree with seed files.

t-005. Build carousel_builder.py pipeline
   Details: goblin_recon/tools/carousel_builder.py. Stages: Validate, Generate (Replicate), Compose (Pillow), Assemble, Verify. 1080×1440 PNG.

t-006. Add vault/carousels/ output structure
   Details: Save slide-NN.png, manifest.json, brief.md, generation-log.md under vault/carousels/YYYY-MM-DD-style-brand/.

t-007. Wire QA checks and workflow docs
   Details: QA readability/platform/safety checks. Add carousel as recognized workflow in Goblin Recon commands.

Start with t-001 NOW.