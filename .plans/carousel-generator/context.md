# Reconciled Context — Carousel Generator

## Two Planning Documents Reconciled

| Source | Role |
|--------|------|
| `.plans/carousel-generator/PLAN.md` | Submitted plan — drives task tracking |
| `docs/plans/carousel-agent-plan.md` | Detailed spec — 5-stage pipeline, brand configs, style bank |
| `docs/plans/carousel-agent-memory.md` | Session log — decisions, tradeoffs, open issues |

## Key Merged Decisions

1. **5-stage pipeline** (from spec): Validate → Generate → Compose → Assemble → Verify
2. **Replicate MCP** for visuals, **Pillow** for text overlay
3. **Brand config system**: 3 built-in (genx-b2b, genx-b2c, neutral-demo) + custom min 3 fields
4. **8 carousel styles** from Brock Johnson research
5. **Pre-flight brand gate**: "GenX or custom?" before every build
6. **GenX mode**: full brand_gate. **Custom mode**: raw pipeline, no gate

## Task to Spec Mapping

| Task | Maps To | Extra Detail from Spec |
|------|---------|----------------------|
| t-001 (MCP config) | P0 | mcp.json + hermes-mcp.yaml + integrations.yaml |
| t-002 (skill) | P4 | Pre-flight brand gate flow in SKILL.md |
| t-003 (templates) | P5 | carousel-brief.md + manifest.json schema |
| t-004 (memory) | P1, P2 | carousel-styles.yaml + brands/*.yaml + memory dirs |
| t-005 (renderer) | P3 | carousel_builder.py (Stages 1-5) with Pillow |
| t-006 (output) | — | vault/carousels/YYYY-MM-DD-style-brand/ |
| t-007 (QA/docs) | P6, P7 | Tests + Goblin Recon workflow integration |

## Open Decisions (Still Pending)

- [ ] Default model: Flux Schnell vs Flux Pro
- [ ] Font strategy: bundle fonts or user provides paths
- [ ] Custom brand minimum: 3 fields confirmed
- [ ] Collage + meme styles: manual or drop from MVP
- [ ] REPLICATE_API_TOKEN status in .env
