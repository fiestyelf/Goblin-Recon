# Goblin Recon Template System

Goblin Recon templates use one shared information structure so every handoff is clear, source-backed, and action-ready.

## Universal Output Order

Every report or brief should follow this order unless a workflow-specific template says otherwise:

1. **Metadata** — what this is, when it was generated, who it is for, and how it will be used.
2. **Decision** — the recommended action in the first few seconds.
3. **Evidence Ledger** — source URLs, dates, what each source proves, and confidence.
4. **Analysis** — interpretation, scoring, risks, and brand fit.
5. **Action Cells** — clear next moves for the right team/person.
6. **Security Rail** — approve/revise/shelve/human-review decision.
7. **Next Step** — exact owner/action/timing.

## Required Status Labels

Use only these labels for user-facing work:

- `APPROVE` — safe and useful enough to use.
- `REVISE` — useful, but must be corrected first.
- `SHELVE` — do not use this recommendation or asset.
- `NEEDS HUMAN REVIEW` — keep, but do not publish or act until reviewed.

## Core Templates

| Template | Use |
|---|---|
| `social-pulse-report.md` | News, trend, and social signal reports. |
| `clip-mine-brief.md` | Editor-ready clip handoff. |
| `competitor-report.md` | Competitor intelligence, gap analysis, and cells. |
| `caption-pack.md` | Platform-specific captions and post copy. |
| `news-brief.md` | Single-story or multi-story news brief. |
| `content-brief.md` | Standalone planning brief when requested. |
| `carousel-brief.md` | Human-readable carousel plan, approval, QA, and revision record. |
| `carousel-manifest.json` | Machine-readable carousel render source of truth. |

## Anti-Mismatch Rules

- Do not present unsupported claims as facts.
- Every material claim needs a source URL or `unverified` label.
- Separate facts, interpretation, and recommended action.
- Keep the Decision section short enough to skim.
- Keep Action Cells concrete enough to assign.
- Run Security Rail before delivery.
- For carousel exports, confirm readability, dimensions, page fit, safe claims, visual consistency, output files, and human approval.
