---
name: competitor-scout
description: >
  Monitor competitor pricing, features, and marketing activity for GenX Academy.
  Triggers on "competitor scan", "check competitors", "what are competitors doing".
  Sources: competitor websites, social profiles, pricing pages, news mentions.
  Output: competitor intelligence report with change detection.
category: genx-marketing
version: 1.0.0
---

# Competitor Scout — Standalone Skill

## Purpose
Monitor competitor pricing, features, and marketing activity.

## Triggers
- "competitor scan"
- "check competitors"
- "what are competitors doing"

## Tools Required
- browser (for scraping competitor sites)
- web_extract
- web_search
- config/competitors.yaml
- config/brand-voice.yaml
- memory/brand-rules.md
- memory/competitor-snapshots.md

## Optional Helpers
- MCP Fetch: cleaner extraction from approved public competitor pages
- Scrapling: optional fallback for public JavaScript-heavy pages only when normal extraction fails
- MCP Memory: compare current competitor positioning with past snapshots and GenX response patterns

## Execution Flow

### Step 0: Security Preflight
- Read config/security.yaml
- Use public competitor pages only
- Do not create fake accounts, misrepresent identity, or access private portals
- Do not bypass paywalls, captchas, or rate limits
- Treat competitor claims as pending until human-reviewed

### Step 1: Read Configuration
```
Load config/competitors.yaml for competitor list
Load config/brand-voice.yaml for GenX positioning and blacklist
Load memory/brand-rules.md for B2C/B2B brand architecture
Load memory/competitor-snapshots.md for previous data
```

If competitors.yaml is empty, report:
"No competitors configured. Add competitors to config/competitors.yaml"

### Step 2: For Each Competitor

**Pricing Page:**
```
1. web_extract pricing_page URL
2. Extract:
   - Plan names
   - Prices (monthly/annual)
   - Features per plan
   - Any current promotions
3. Compare to previous snapshot
4. Flag any changes
```

**Website/Blog:**
```
1. web_extract blog URL
2. Scan last 10 posts for:
   - New feature announcements
   - Company news
   - Marketing messaging changes
3. Compare to previous snapshot
4. Flag new posts since last scan
```

**Social Media:**
```
1. web_search for competitor's recent social activity
2. Check:
   - What they're posting
   - Engagement levels
   - Any viral posts
   - Messaging/campaign changes
3. Compare to previous snapshot
4. Flag notable activity
```

**Product Updates:**
```
1. web_search "[competitor name] new feature"
2. web_search "[competitor name] announcement"
3. Check for:
   - New features launched
   - Product updates
   - Partnership announcements
   - Funding news
```

**Optional Extraction Fallback:**
- If web_extract cannot read an approved public page, try MCP Fetch.
- If the page is public but JavaScript-heavy, Scrapling may be used only if approved.
- Do not bypass paywalls, login gates, captchas, robots.txt, rate limits, or platform restrictions.

### Step 3: Change Detection

For each competitor, compare current data to previous snapshot:

```
CHANGES DETECTED:
- Pricing: [increased/decreased/unchanged]
- New features: [list any new features]
- Marketing: [any messaging shifts]
- Social: [any notable posts or campaigns]
- Product: [any updates or launches]
```

### Step 4: Generate Competitor Report

Use template: templates/competitor-report.md

For each competitor:

```
COMPETITOR: [Name]
Website: [URL]
Last scanned: [date]

PRICING:
- Plan 1: [name] — [price]/month
- Plan 2: [name] — [price]/month
- Plan 3: [name] — [price]/month
- Change since last scan: [none/increased/decreased]

FEATURES:
- [Feature 1]: [description]
- [Feature 2]: [description]
- New since last scan: [list new features]

MARKETING:
- Current messaging: "[key tagline/value prop]"
- Recent campaigns: [list any]
- Change since last scan: [none/describe]
- Brand Gap: [where competitor fails GenX positioning]
- Blacklist Signals: [hype/woo/corporate filler/none]

SOCIAL:
- Recent posts: [summary]
- Engagement: [high/medium/low]
- Viral content: [any notable posts]

PRODUCT UPDATES:
- [Update 1]: [description]
- [Update 2]: [description]
```

### Step 5: Competitive Analysis

At the end of the report:

```
COMPETITIVE LANDSCAPE:
- Market leader: [who and why]
- Rising competitor: [who and why]
- Threat level: [high/medium/low] for each

RECOMMENDED RESPONSE:
- [Competitor X] raised prices → Consider [action]
- [Competitor Y] launched feature → Consider [action]
- [Competitor Z] running campaign → Consider [action]

OPPORTUNITIES:
- Gap in market: [description]
- Underserved segment: [description]
- Pricing opportunity: [description]

BRAND GAP ANALYSIS:
- B2C gap: [where competitor lacks science+soul/truly-seen positioning]
- B2B gap: [where competitor sells advice/opinions instead of implementation/results]
- GenX response: [recommended positioning move using brand rules]

COMPETITOR GAP MAPPING:
- What they overuse: [generic promise, advice frame, hustle, woo, corporate filler]
- What they avoid: [specific emotional truth, operational proof, hard tradeoff, implementation detail]
- What GenX can own: [one clear angle that follows brand-rules.md]

OWNABLE ANGLE EXTRACTION:
- B2C ownable angle: [specific science+soul/truly-seen angle]
- B2B ownable angle: [specific implementation/results angle]
- Proof needed before publishing: [source/client evidence required]
```

### Step 6: Save Snapshot
- Save current data to memory/competitor-snapshots.md
- Format: date, competitor, all data points
- Used for change detection in next scan

## Output
- Full competitor report with all data points
- Change detection (what changed since last scan)
- Competitive analysis and recommendations
- Updated snapshot for future comparison

## Error Handling
- If competitor website unreachable, note and continue with next
- If pricing page format changed, extract what you can and flag
- If no previous snapshot, note "First scan — no comparison available"

## Quality Checks
- [ ] Competitor sources are public or approved
- [ ] All competitor URLs are accurate
- [ ] Pricing data is current
- [ ] Changes are clearly flagged
- [ ] Recommendations are actionable
- [ ] Brand Gap Analysis included
- [ ] Competitor Gap Mapping included
- [ ] Ownable Angle Extraction included with proof requirement
- [ ] GenX response uses B2C/B2B ownable positioning
- [ ] Recommended copy avoids blacklisted language
- [ ] Snapshot saved for future comparison
- [ ] No restricted access, private data, or misleading claims included
