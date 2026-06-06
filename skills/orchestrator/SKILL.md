# Orchestrator — Driver Skill

## Purpose
Run the full pipeline: Layer 1 → Layer 2 → Layer 3 → Human Gate

## Triggers
- "run full scan"
- "goblin recon go"
- "find me content"

## Tools Required
- Loads and chains: trend-radar → source-hunter → moment-finder
- All config files
- All templates
- memory/brand-rules.md
- config/brand-voice.yaml

## Optional Helpers
- MCP Memory: store approved/shelved examples after human decision
- Ghost Browser: help inspect approved public social or JavaScript-heavy pages when normal extraction fails
- Firecrawl: help extract approved public web pages after the API key is configured through environment variables
- config/content-tracker.yaml: create Notion/Sheets tracking entries after approval when enabled
- GPT Researcher, TrendRadar, Scrapling, and FunASR remain optional helpers only; they do not replace the core pipeline

## Execution Flow

### Step 0: Security Preflight
```
1. Load config/security.yaml
2. Confirm no API keys or tokens are requested in chat
3. Confirm sources are public or explicitly approved
4. Stop if a source requires bypassing login, paywall, captcha, or access restrictions
5. Remind user that human review is required before publishing
```

### Step 1: Initialize
```
1. Load all configuration files
2. Load memory/brand-rules.md and config/brand-voice.yaml
3. Load config/content-tracker.yaml if present
4. Verify scripts are available
5. Prepare memory/trend-history.md for dedup
6. Report: "Starting full scan..."
```

### Step 1.5: Brand Calibration
Before running the layers, calibrate the scan against the brand rules:
- B2C filter: successful-on-paper, lost spark, wants real science plus real soul, no woo or preciousness.
- B2B filter: burnt-out SME operator, wants implementation/results, no advice-merchant or consultant theater.
- Voice filter: direct, precise, grounded, emotionally true; no blacklisted phrases in GenX-written copy.
- Open decisions: do not guess B2C brand name, Sara visibility level, or domain mapping.

### Step 2: Run Layer 1 — Trend Radar
```
1. Execute trend-radar skill
2. Wait for trend report
3. If no stories found: report and stop
4. If stories found: proceed to Layer 2
```

**Output:** Top 5 trending stories with scores

### Step 3: Run Layer 2 — Source Hunter
```
1. For each story from Layer 1:
   a. Execute source-hunter skill
   b. Find YouTube and Instagram sources
   c. Pull transcripts for YouTube videos
2. Collect all sources
3. If no sources found for a story: note and continue
```

**Output:** 3-5 sources per story with transcripts

### Step 3.1: Vault Dedup Check
```
1. Before running Moment Finder, check memory/trend-history.md and vault/briefs/ for similar:
   a. Trend/topic
   b. Hook or claim
   c. Audience tension
   d. Competitor gap
   e. Source or speaker
2. If no overlap exists: mark Vault check as "no overlap" and continue
3. If overlap exists but the angle is meaningfully different: mark "needs differentiation" and state the difference
4. If overlap exists and the angle is not meaningfully different: shelve before clip extraction
5. Record the dedup decision in the final brief
```

**Output:** Dedup decision for each story/source before clip extraction

### Step 4: Run Layer 3 — Moment Finder
```
1. For each source with transcript:
   a. Execute moment-finder skill
   b. Find hot zones in transcript
   c. Score and rank moments
   d. Generate clip briefs
2. Collect all clip briefs
3. Rank by score (highest first)
4. Each clip brief must include Decision, Effort, Confidence, Vault check, Fallback, AI Overview potential, and Platform Variants
```

**Output:** 2-3 clip briefs per source with timestamps

### Step 5: Brand Gate

Before human approval, filter every trend, source, and clip brief:

```
For each clip brief:
  1. Confirm Brand Angle: B2C, B2B, or Both
  2. Confirm brand alignment >= 8/15
  3. Scan GenX-written hook, caption, explanation, and next steps against config/brand-voice.yaml blacklist
  4. If transcript contains blacklisted words, flag as quoted source material and do not reuse in GenX copy
  5. Check B2C: science+soul, truly seen, depth plus play, no woo
  6. Check B2B: results not advice, implementation, proof, no advice-merchant tone
  7. Check first-touch feeling: recognized, challenged, relieved, provoked, or weak/generic
  8. If any check fails: auto-shelve and record reason
```

Only briefs that pass the brand gate reach the Human Gate.

### Step 6: Human Gate — Present Results

**Format: One message per clip brief**

```
CLIP BRIEF: "[headline]"

DECISION:
Action: [approve / modify / shelve]
Effort: [X] hours
Confidence: [High / Medium / Low] — [reason]
Vault check: [no overlap / similar exists / needs differentiation]
Fallback: [alternative angle if rejected]
AI Overview potential: [Strong / Medium / Weak] — [reason]

Trend Score: [X]/100 | Source: [video title]
URL: youtube.com/watch?v=XXX&t=[START] → t=[END]
Duration: [X] seconds
Brand Angle: [B2C/B2B/Both] | Brand Alignment: [X]/15
First-Touch Feeling: [recognized/challenged/relieved/provoked/weak]
Blacklist Flags: [none/list]

THE MOMENT:
"[transcript of the clip]"

WHY POST:
[1-2 sentences: why this will get engagement]

CAPTION:
"[suggested caption]"

FORMAT: [faceless reel type]
PLATFORM VARIANTS: [Instagram / LinkedIn / YouTube Shorts]
#[tag1] #[tag2] #[tag3]

Reply: approve / shelve / modify
```

**User Options:**
- `approve` → Save to vault/briefs/, record in trend-history
- `shelve` → Skip, record in trend-history for dedup
- `modify [instructions]` → Revise and re-propose

### Step 7: Handle User Responses

**For each "approve":**
```
1. Save clip brief to vault/briefs/[date]-[headline].md
2. Record in memory/trend-history.md
3. If config/content-tracker.yaml tracking.enabled is true, create/update the Notion or Sheets tracker entry using approved integration only
4. If MCP Memory is enabled, store a short approved-example summary without full raw transcript
5. Report: "Approved and saved"
```

**For each "shelve":**
```
1. Record in memory/trend-history.md with reason
2. If MCP Memory is enabled, store a short shelved-example summary and reason without full raw transcript
3. Report: "Shelved"
```

**For each "modify [instructions]":**
```
1. Apply modifications to clip brief
2. Re-propose modified version
3. Wait for new response
```

### Step 8: Summary Report

After all clips processed:

```
SCAN COMPLETE

TODAY'S RESULTS:
- Stories scanned: [count]
- Sources found: [count]
- Clips extracted: [count]
- Approved: [count]
- Shelved: [count]
- B2C opportunities: [count]
- B2B opportunities: [count]
- Brand-gate shelved: [count]
- Tracker entries created: [count, if enabled]

APPROVED CLIPS:
1. [headline] — [duration] seconds
2. [headline] — [duration] seconds

NEXT STEPS:
- Create faceless reels from approved clips
- Schedule posting for optimal times
- Run next scan in [X] hours/days
```

### Step 9: Save Memory
- Update memory/trend-history.md with all today's data
- Format: date, story, source, clip, brand angle, brand score, status (approved/shelved)
- Used for dedup in future runs

## Output
- Full pipeline execution report
- All clip briefs presented for human approval
- Approved clips saved to vault
- Memory updated for future runs

## Error Handling
- If Layer 1 fails: report error and stop
- If Layer 2 fails for one story: continue with other stories
- If Layer 3 fails for one video: continue with other videos
- If user doesn't respond: wait and prompt again
- If access is denied or a source appears restricted: stop that source and mark as shelved
- If a prompt or page exposes a secret: stop and tell the user to rotate the secret

## Quality Checks
- [ ] Security preflight completed
- [ ] All layers executed in order
- [ ] All stories have sources (or noted as "no sources found")
- [ ] All sources have transcripts (or noted as "no transcript")
- [ ] Vault dedup completed before Moment Finder
- [ ] All clips are 15-60 seconds
- [ ] All clips have working URLs
- [ ] Brand calibration completed before Layer 1
- [ ] Brand gate completed before human gate
- [ ] Brand Angle and brand alignment score included for every presented clip
- [ ] First-touch feeling included for every presented clip
- [ ] Effort, confidence, vault check, fallback, AI Overview potential, and platform variants included for every presented clip
- [ ] Blacklist scan completed for every presented clip
- [ ] Human gate presented for every clip
- [ ] User responses handled correctly
- [ ] Memory updated with all data
- [ ] Content tracker updated only if enabled and approved
- [ ] No secrets, cookies, or API keys included in outputs
- [ ] No restricted or private sources used without approval
