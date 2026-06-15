# Orchestrator Skill — Complete Fix Plan

> Audit date: June 15, 2026
> Current version: 1.0.0 (file) / 1.0.1 (memory — version was never bumped)
> Proposed version after all fixes: **1.1.0**

---

## Problem Summary

The orchestrator routes 6 intents (Social Pulse, Clip Mine, Clip Vault, Competitor Scout, Email Hook, Brand Gate) but only has execution steps for one: Clip Mine. Steps 4–11 assume the answer is always "run the 3-layer clip chain." The other 5 paths have no defined behavior — the agent would either fall through into Clip Mine steps or improvise.

---

## Fix 1: Add Workflow Branching (Step 3.5)

**The core structural fix.** Insert a new step between Social Extraction Policy (Step 3) and Layer 1 (Step 4).

### New Step 3.5: Workflow Branch

After social extraction policy is applied, branch based on the intent selected in Step 0:

```text
IF Social Pulse:
  → Run Trend Radar (same as Step 4, but stop after scoring)
  → Present ranked trend report with Decision, scores, category tags, format analysis
  → Auto-save to vault/reports/YYYY-MM-DD-social-pulse.md
  → Ask user: "Clip Mine the top 2-3? Or done for now?"
  → STOP. Do not proceed to Source Hunter unless user asks.

IF Clip Mine:
  → Continue to Step 4 (Layer 1 → Layer 2 → Layer 3 → Brand Gate → Human Gate)
  → This is the existing path — steps 4-11 remain unchanged.

IF Clip Vault:
  → Query vault/clips.db and vault/briefs/ directly
  → Present results: "X approved clips, Y shelved, Z in production"
  → If user asks for a specific clip, regenerate brief via scripts/query_clips.py
  → STOP. No layers needed.

IF Competitor Scout:
  → Load skill: competitor-scout
  → Execute: scrape competitor sites + GenX Academy baseline
  → Produce competitor intelligence report with side-by-side comparison
  → Auto-save to vault/reports/YYYY-MM-DD-competitor-scan.md
  → Present Priority Action Items table
  → STOP.

IF Email Hook:
  → Ask Output Direction pre-check (if missing): B2C/B2B/Both? Where does it go? What tone?
  → Load config/email-campaigns.yaml
  → Select/infer campaign type (value/trust_building/launch/re_engagement)
  → Generate 5 subject + opener variants
  → Run email_gate on all variants
  → Present ranked results with PASS/FLAGGED/REJECT verdicts
  → STOP.

IF Brand Gate (standalone):
  → Run goblin_recon.tools.brand_gate on user-provided copy
  → Present: alignment score, blacklist violations, first-touch feeling
  → STOP.
```

**Stop condition for each branch:**
| Workflow | Stop When |
|----------|-----------|
| Social Pulse | Trend report delivered + auto-saved + user says "done" |
| Clip Mine | All clips approved/shelved by Human Gate |
| Clip Vault | Results presented; user stops asking |
| Competitor Scout | Report delivered + auto-saved |
| Email Hook | Variants presented + user selects |
| Brand Gate | Verdict delivered |

---

## Fix 2: Add Signal Scan Mode to Step 0.5

Currently Step 0.5 defines Fast Scan, Deep Social Scan, and Manual Assisted Scan. Signal Scan is mentioned in the description line but has no body.

### Add to Step 0.5:

```text
Signal Scan:
  - Use for first-mover discovery when mainstream news is too slow
  - Scan public early-signal surfaces in this order:
    1. X/Twitter (when approved API or public access available)
    2. Hacker News
    3. GitHub Trending
    4. ArXiv
  - Time gate: last 6 hours only
  - If nothing clears the velocity threshold, return "nothing worth posting right now"
  - Do not force weak ideas — a null result is a valid result
  - Reddit only if public access works (often blocked)
```

---

## Fix 3: Add Missing Triggers

The orchestrator should catch all known commands. Add these to the triggers section:

```text
- "run signal scan"
- "run competitor scan"
- "check competitors"
- "what are competitors doing"
- "write email hooks for [offer/audience]"
- "write subject lines for [campaign]"
- "validate this email"
```

The full triggers list becomes:

```text
- "run full scan"
- "goblin recon go"
- "find me content"
- "run fast scan"
- "run deep social scan"
- "run signal scan"                          ← NEW
- "manual scan this [URL/screenshot/caption]"
- "what clips are ready"
- "run competitor scan"                      ← NEW
- "check competitors"                        ← NEW
- "what are competitors doing"               ← NEW
- "write email hooks for [offer/audience]"   ← NEW
- "write subject lines for [campaign]"       ← NEW
- "validate this email"                      ← NEW
```

---

## Fix 4: Move Output Direction Pre-Check Earlier

Currently the 3-question pre-check fires at Step 7 (Brand Gate) — only for Clip Mine. But Social Pulse and Email Hook also produce brand-facing output.

### Change: Add to Step 0 (Intent Router)

After classifying the intent but before stating the workflow, ask:

```
If this request will produce brand-facing output (Social Pulse, Clip Mine, Email Hook,
or Competitor Scout with positioning recommendations):
  Ask the Output Direction 3 questions:
  1. Who is this for? B2C, B2B, or Both?
  2. Where does it go? Faceless Instagram, personal brand, client work, internal,
     email/outbound, or other?
  3. What tone? Professional, casual, edgy, warm, wry, reflective, analytical/data-driven,
     bold, or platform-native?

Skip this only for: Clip Vault queries, Manual Assisted Scan where direction is already
provided, and standalone Brand Gate checks on user-provided copy.

If the user skips direction, default to: Both / Faceless Instagram / Professional.
State that default before generating.
```

Then remove the Output Direction check from Step 7 (it's no longer needed there).

---

## Fix 5: Add Auto-Save to All Workflow Branches

The goblin-recon skill mandates: *"After every Social Pulse report, Fast Scan, Deep Social Scan, Signal Scan, Competitor report, or Clip Brief: Write the full output to `vault/reports/YYYY-MM-DD-{type}.md`."*

Currently only Clip Mine briefs get saved (Step 9 → `vault/briefs/`). Social Pulse and Competitor Scout have no save step.

### Add to each branch in new Step 3.5:

| Workflow | Auto-Save Path |
|----------|---------------|
| Social Pulse | `vault/reports/YYYY-MM-DD-social-pulse.md` |
| Competitor Scout | `vault/reports/YYYY-MM-DD-competitor-scan.md` |
| Clip Mine | `vault/briefs/[date]-[headline].md` (existing) |
| Email Hook | Not auto-saved (tactical, not report-format) |
| Clip Vault | Not auto-saved (retrieval, not new content) |
| Brand Gate | Not auto-saved (one-off check) |

After each save, tell the user: `Saved -> vault/reports/<filename>`

---

## Fix 6: Add Delegation Policy

The goblin-recon skill has a hard rule against using subagents for data collection. The orchestrator — as the driver that decides *how* to execute — should own this rule.

### Add new section after Step 1 (Security Preflight):

```text
### Delegate Task Policy

NEVER use delegate_task/subagents for:
  - Fast Scan, Deep Social Scan, Signal Scan (data collection)
  - Single-source lookups
  - Brand gate checks
  - Transcript extraction
  - Browser-based social scraping

ONLY use delegate_task after data is already collected, and only for:
  - Scoring candidate rows
  - Cross-referencing source dates
  - Formatting reports
  - Counter-reviewing recommendations

If you delegate, pass explicitly:
  - Source URLs, query limits, blocked-source rules
  - Brand rules (B2C/B2B filters, blacklist, voice traits)
  - Expected output fields and format
```

---

## Fix 7: Clarify content-tracker.yaml Reference

Step 2 says *"Load config/content-tracker.yaml if present"* and Step 9 references it. This file may not exist.

### Change Step 2:

```text
3. Load config/content-tracker.yaml if present (optional — not yet created; tracker
   integration is future work. Skip silently if absent.)
```

### Change Step 9:

```text
5. If config/content-tracker.yaml exists AND tracking.enabled is true, create/update
   the Notion or Sheets tracker entry using approved integration only.
   (Note: this file is optional and not part of the current pipeline.)
```

---

## Fix 8: Expand Quality Checklist for Non-Clip Mine Workflows

Add these items after the existing 23:

```text
- [ ] Output Direction pre-check completed before brand-facing output (moved from Step 7)
- [ ] Social Pulse report auto-saved to vault/reports/ (if Social Pulse)
- [ ] Competitor report auto-saved to vault/reports/ (if Competitor Scout)
- [ ] Competitor report includes side-by-side comparison table (if Competitor Scout)
- [ ] Competitor report includes "What NOT to copy" section (if Competitor Scout)
- [ ] Email Hook variants all passed email_gate before delivery (if Email Hook)
- [ ] Email Hook variants ranked with PASS/FLAGGED/REJECT verdicts (if Email Hook)
- [ ] Clip Vault results deduplicated before presentation (if Clip Vault)
- [ ] Delegation policy followed — no subagents used for data collection
- [ ] Stop condition respected for non-Clip Mine workflows
```

---

## Fix 9: Bump Version Number

Current: `version: 1.0.0` (file) / implied `1.0.1` (memory — sensitivity auto-shelve was added but version wasn't bumped).

With all 9 fixes applied, this is a significant structural change — new branching logic, new scan mode, new triggers, relocated pre-check.

**Proposed: `version: 1.1.0`**

---

## Fix 10: Update "Tools Required" Section

Currently says: *"Loads and chains: trend-radar → source-hunter → moment-finder"* — but the orchestrator now also drives competitor-scout, email-hook, and caption-tone.

### Change:

```text
## Tools Required
- Loads and chains based on intent:
  - Social Pulse: trend-radar
  - Clip Mine: trend-radar → source-hunter → moment-finder
  - Clip Vault: scripts/query_clips.py + vault/clips.db
  - Competitor Scout: competitor-scout skill + mcp_firecrawl_firecrawl_scrape
  - Email Hook: email-hook skill + goblin_recon.tools.email_gate
  - Brand Gate: goblin_recon.tools.brand_gate
- All config files (config/*.yaml)
- All templates (templates/*.md)
- memory/brand-rules.md
- config/brand-voice.yaml
```

---

## Fix 11: Remove Step 7 Output Direction Check (Redundant After Fix 4)

Step 7 currently says:

> 1. Use Output Direction from session start (brand angle, destination, and tone). If missing, ask the 3-question Output Direction Pre-Check before judging the brief.

Since Fix 4 moves this to Step 0, Step 7 should assume direction is already captured:

```text
1. Confirm Output Direction from Step 0 (brand angle, destination, tone). If somehow
   missing (should not happen), default to Both / Faceless Instagram / professional.
```

---

## Fix 12: Add Error Handling for Non-Clip Mine Paths

The current error handling only references Layer 1/2/3 failures. Add:

```text
- If Social Pulse returns zero trends: report "nothing worth posting right now" and stop
- If Competitor Scout cannot reach any sites: report which sites failed, deliver partial
  report with available data
- If Email Hook email_gate rejects all 5 variants: regenerate with different campaign type
  or broader psychological triggers, re-submit
- If Clip Vault returns zero results for a search: tell user "no clips match" and suggest
  running Clip Mine instead
- If the workflow branch cannot determine the path: ask one short clarifying question
```

---

## Complete Before/After Structure

### Before (Current — v1.0.0)

```
Step 0:    Intent Router (routes 6 intents)
Step 0.5:  Scan Mode Selection (3 modes — Signal Scan missing)
Step 1:    Security Preflight
Step 2:    Initialize
Step 2.5:  Brand Calibration
Step 3:    Social Extraction Policy
Step 4:    Layer 1 — Trend Radar          ← assumes Clip Mine
Step 5:    Layer 2 — Source Hunter         ← assumes Clip Mine
Step 5.1:  Vault Dedup Check
Step 6:    Layer 3 — Moment Finder         ← assumes Clip Mine
Step 7:    Brand Gate (asks Output Direction here)
Step 8:    Human Gate
Step 9:    Handle User Responses
Step 10:   Summary Report
Step 11:   Save Memory
```

### After (Proposed — v1.1.0)

```
Step 0:    Intent Router + Output Direction Pre-Check   ← MOVED UP from Step 7
Step 0.5:  Scan Mode Selection (4 modes — Signal Scan added)
Step 1:    Security Preflight + Delegation Policy        ← DELEGATION POLICY ADDED
Step 2:    Initialize (content-tracker.yaml clarified)
Step 2.5:  Brand Calibration
Step 3:    Social Extraction Policy
Step 3.5:  WORKFLOW BRANCH ← THE BIG FIX
  ├─ Social Pulse      → Trend Radar → Report → Auto-save → STOP
  ├─ Clip Mine         → Continue to Steps 4-11 (unchanged)
  ├─ Clip Vault        → Query → Present → STOP
  ├─ Competitor Scout  → Load skill → Execute → Auto-save → STOP
  ├─ Email Hook        → Direction → Campaign → Generate → Gate → Present → STOP
  └─ Brand Gate        → Run tool → Present → STOP
Step 4:    Layer 1 — Trend Radar
Step 5:    Layer 2 — Source Hunter
Step 5.1:  Vault Dedup Check
Step 6:    Layer 3 — Moment Finder
Step 7:    Brand Gate (direction already captured from Step 0)
Step 8:    Human Gate
Step 9:    Handle User Responses
Step 10:   Summary Report
Step 11:   Save Memory

Quality Checks: expanded from 23 to 33 items
Error Handling: expanded to cover non-Clip Mine paths
Triggers: expanded from 7 to 14
```

---

## Implementation Order

| Batch | Fixes | Impact |
|-------|-------|--------|
| **Batch 1** (Critical) | Fix 1 (Workflow Branch), Fix 2 (Signal Scan mode), Fix 3 (Missing triggers), Fix 4 (Move Output Direction) | Structural — changes how the agent routes |
| **Batch 2** (High) | Fix 5 (Auto-save all reports), Fix 6 (Delegation policy), Fix 11 (Remove redundant Step 7 check) | Operational — ensures consistency |
| **Batch 3** (Medium) | Fix 7 (content-tracker clarification), Fix 8 (Quality checklist expansion), Fix 10 (Tools Required update), Fix 12 (Error handling expansion) | Polish — no behavioral change |
| **Batch 4** (Low) | Fix 9 (Version bump to 1.1.0) | Bookkeeping |
