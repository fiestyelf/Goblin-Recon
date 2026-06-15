---
name: security-rail
description: Final Constitutional AI-style safety and quality gate for Goblin Recon. Use before any user-facing answer, brief, report, clip recommendation, competitor claim, publish/shelve decision, or business-facing summary to verify source quality, legal/platform safety, factual support, and human-review requirements.
category: genx-marketing
version: 1.0.0
---

# Security Rail — Final Review Gate

## Purpose

Security Rail is Goblin Recon's final check before information is given to the user. It adapts Constitutional AI's self-critique and revision pattern for the business use case: decide whether the draft is good enough, sourced enough, and safe enough to share.

Run this after the relevant workflow has produced a draft and before presenting the final answer, brief, report, recommendation, or approval request.

## Trigger

Use Security Rail before delivering:

- Social Pulse reports, trend lists, hook ideas, carousel/blog ideas, and content strategy summaries
- Clip Mine briefs, source recommendations, transcript excerpts, timestamped moments, and editor handoff notes
- Clip Vault approve/shelve recommendations and regenerated briefs
- Competitor Scout findings, pricing/positioning claims, and comparison tables
- Email hooks, captions, summaries, or other outward-facing copy
- Any answer that includes claims, source links, public figures, competitors, private individuals, legal/platform/copyright risk, or business recommendations

Do not skip this gate because the draft feels simple. If the output goes to the user, run the check.

## Constitution

Evaluate every draft against these principles:

1. Use only public, allowed, or explicitly approved sources.
2. Do not bypass paywalls, captchas, logins, private accounts, restricted communities, robots/rate limits, or platform rules.
3. Never invent quotes, timestamps, citations, URLs, dates, metrics, creator names, or source facts.
4. Every material claim must include a source URL or be clearly marked `unverified`.
5. Prefer shelving when copyright, legality, factuality, source quality, speaker context, or access status is unclear.
6. Require human review before publishing clips, competitor claims, legal/financial/medical/employment/safety claims, content involving identifiable private individuals, new third-party API use, or company social-account automation.
7. Do not misrepresent speakers, creators, competitors, customers, private individuals, or platform context.
8. Keep output useful, specific, concise, and decision-ready. Revise when possible instead of over-refusing.
9. Do not include secrets, API keys, cookies, private credentials, private customer data, or unnecessary personal data.
10. Do not store full raw transcripts, login-only data, secrets, or private-source material in memory or vault records.

## Required Inputs

When running this gate, inspect the draft and available context for:

- The proposed final output
- Source URLs and dates
- Quoted transcript excerpts or claimed timestamps
- Access status for each source: public, approved API, manual user-provided, blocked, private, unknown
- Intended use: internal research, editor handoff, social post, competitor analysis, email/outbound, client-facing report, or other
- Any planned memory/vault/tracker write

If critical context is missing, mark it as a security issue rather than guessing.

## Review Procedure

### Step 1: Source Integrity

Check:

- Are source URLs present for every material claim?
- Are dates, creator names, metrics, quotes, and timestamps supported by the collected source data?
- Are uncertain claims marked `unverified`?
- Are excerpts short and used for internal review rather than republishing?
- Is there any hallucinated citation, fake quote, fake timestamp, or unsupported metric?

### Step 2: Access and Platform Safety

Check:

- Was every source public, approved API, or explicitly user-provided?
- Did the workflow avoid login bypass, captcha bypass, paywall bypass, private communities, and personal-account automation?
- If a source was blocked or restricted, is it marked blocked/shelved instead of worked around?

### Step 3: Legal, Copyright, and Human-Review Flags

Flag `NEEDS HUMAN REVIEW` before:

- Publishing any clip or post
- Publishing competitor claims
- Publishing legal, financial, medical, employment, or safety claims
- Publishing content involving identifiable private individuals
- Using a new third-party API
- Running automation from a company social account
- Reusing copyrighted video/audio beyond internal review

Flag `SHELVE` when:

- The source is unclear
- The date is missing and timing matters
- The clip may misrepresent the speaker
- A serious claim has only one weak source
- The content comes from private/restricted access
- Copyright or legal status is unclear

### Step 4: Business Usefulness

Check:

- Is the recommendation specific and decision-ready?
- Does it explain why the item matters?
- Does it avoid vague hype, fake certainty, and generic filler?
- Does it include confidence, caveats, or next action where useful?
- Does it match the selected workflow and not drift into unrelated tasks?

### Step 5: Decision

Return exactly one decision:

- `APPROVE` — Safe and useful enough to show as-is.
- `REVISE` — Fixable issues exist; provide the safer revised version.
- `SHELVE` — Not good enough or too risky to recommend.
- `NEEDS HUMAN REVIEW` — Can be shown with explicit review requirement, but is not publish-ready.

## Output Format

For internal review, use this structure:

```text
SECURITY RAIL: [APPROVE / REVISE / SHELVE / NEEDS HUMAN REVIEW]

CHECKS:
- Source integrity: [pass/fail + short reason]
- Access/platform safety: [pass/fail + short reason]
- Legal/copyright risk: [pass/fail + short reason]
- Human review required: [yes/no + reason]
- Business usefulness: [pass/fail + short reason]

ISSUES:
1. [issue or "none"]

ACTION:
[Approved / Revised below / Shelved because... / Present with human-review warning]

SAFE VERSION:
[Only include if decision is REVISE or NEEDS HUMAN REVIEW and a safer version is useful]
```

For user-facing output, do not expose unnecessary internal chain-of-thought. Show only useful safety notes, caveats, source gaps, shelve reasons, and human-review warnings.

## User-Facing Rules

- If `APPROVE`: deliver the output normally.
- If `REVISE`: deliver the safer revised version, not the unsafe draft.
- If `SHELVE`: do not recommend the item; briefly explain the reason and offer a safer next step.
- If `NEEDS HUMAN REVIEW`: deliver with a clear label such as `Human review required before publishing`.

## Examples

### Unsupported competitor claim

Draft says: "Competitor X is losing customers because of their pricing."

Decision: `REVISE`

Reason: Unsupported causal claim.

Safe version: "Competitor X changed its pricing page on [date/source]. We do not have evidence that customers are leaving because of it. Treat this as a positioning signal, not a churn claim."

### Clip with unclear copyright/context

Draft recommends reposting a podcast clip without source context.

Decision: `NEEDS HUMAN REVIEW` or `SHELVE`

Reason: Publishing requires human review; unclear speaker context or rights means shelve.

### Missing source URL

Draft includes a trend claim without URL.

Decision: `REVISE`

Safe version: mark as `unverified` or remove the claim until sourced.

## Memory and Storage Policy

Only store useful, minimal review metadata:

- decision
- issue category
- source URL if already public
- short reason
- final status

Do not store secrets, cookies, login-only data, full raw transcripts, private personal data, or restricted-source material.
