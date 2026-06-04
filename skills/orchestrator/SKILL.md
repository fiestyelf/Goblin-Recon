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
2. Verify scripts are available
3. Prepare memory/trend-history.md for dedup
4. Report: "Starting full scan..."
```

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

### Step 4: Run Layer 3 — Moment Finder
```
1. For each source with transcript:
   a. Execute moment-finder skill
   b. Find hot zones in transcript
   c. Score and rank moments
   d. Generate clip briefs
2. Collect all clip briefs
3. Rank by score (highest first)
```

**Output:** 2-3 clip briefs per source with timestamps

### Step 5: Human Gate — Present Results

**Format: One message per clip brief**

```
CLIP BRIEF: "[headline]"

Trend Score: [X]/100 | Source: [video title]
URL: youtube.com/watch?v=XXX&t=[START] → t=[END]
Duration: [X] seconds

THE MOMENT:
"[transcript of the clip]"

WHY POST:
[1-2 sentences: why this will get engagement]

CAPTION:
"[suggested caption]"

FORMAT: [faceless reel type]
#[tag1] #[tag2] #[tag3]

Reply: approve / shelve / modify
```

**User Options:**
- `approve` → Save to vault/briefs/, record in trend-history
- `shelve` → Skip, record in trend-history for dedup
- `modify [instructions]` → Revise and re-propose

### Step 6: Handle User Responses

**For each "approve":**
```
1. Save clip brief to vault/briefs/[date]-[headline].md
2. Record in memory/trend-history.md
3. Report: "Approved and saved"
```

**For each "shelve":**
```
1. Record in memory/trend-history.md with reason
2. Report: "Shelved"
```

**For each "modify [instructions]":**
```
1. Apply modifications to clip brief
2. Re-propose modified version
3. Wait for new response
```

### Step 7: Summary Report

After all clips processed:

```
SCAN COMPLETE

TODAY'S RESULTS:
- Stories scanned: [count]
- Sources found: [count]
- Clips extracted: [count]
- Approved: [count]
- Shelved: [count]

APPROVED CLIPS:
1. [headline] — [duration] seconds
2. [headline] — [duration] seconds

NEXT STEPS:
- Create faceless reels from approved clips
- Schedule posting for optimal times
- Run next scan in [X] hours/days
```

### Step 8: Save Memory
- Update memory/trend-history.md with all today's data
- Format: date, story, source, clip, status (approved/shelved)
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
- [ ] All clips are 15-60 seconds
- [ ] All clips have working URLs
- [ ] Human gate presented for every clip
- [ ] User responses handled correctly
- [ ] Memory updated with all data
- [ ] No secrets, cookies, or API keys included in outputs
- [ ] No restricted or private sources used without approval
