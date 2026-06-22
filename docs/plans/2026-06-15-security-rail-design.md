# Security Rail Design

## Purpose

Add a mandatory final review gate for Goblin Recon before any user-facing output is delivered. The rail adapts Constitutional AI's critique/revision pattern to Goblin Recon's business use case: checking whether gathered information is good enough, safe enough, and sourced enough to share.

## Scope

The Security Rail applies to final answers, internal briefs, reports, clip recommendations, competitor claims, publish/shelve decisions, and any output that may influence business decisions.

It does not replace human judgment, legal review, or platform-policy review. It decides whether the draft is safe to present, needs revision, should be shelved, or requires human review.

## Constitution

The rail checks every draft against these principles:

1. Use only public, allowed sources.
2. Do not bypass paywalls, captchas, private accounts, restricted communities, or platform rules.
3. Never invent quotes, timestamps, citations, URLs, dates, metrics, or creator names.
4. Every material claim must include a source URL or be clearly marked unverified.
5. Prefer shelving when copyright, legality, factuality, source quality, or context is unclear.
6. Require human review before publishing, competitor claims, serious claims, new third-party API use, or company social automation.
7. Do not misrepresent speakers, competitors, creators, customers, or private individuals.
8. Keep the final output useful, specific, concise, and decision-ready.

## Decision Labels

- `APPROVE` — Safe and useful enough to show.
- `REVISE` — Has fixable issues; produce a safer version.
- `SHELVE` — Not good enough or too risky to recommend.
- `NEEDS HUMAN REVIEW` — Can be shown with a clear approval requirement, but should not be treated as publish-ready.

## Integration

1. Add `goblin-recon/skills/security-rail/SKILL.md`.
2. Update the Goblin Recon operational skill to require Security Rail before final output.
3. Update the Orchestrator skill to run Security Rail as the final gate.

## Success Criteria

- Final outputs explicitly pass through a source/safety/usefulness check.
- Unsupported or unclear information is marked unverified, revised, or shelved.
- Human-review requirements are surfaced clearly.
- The agent remains helpful and does not over-refuse when safe revision is possible.
