---
name: competitor-scout
description: >
  Monitor competitor pricing, features, and marketing activity for GenX Academy.
  v2.0 — Semantic diffing, content-hash dedup, source-type routing, priority scoring,
  sitemap auto-discovery, executive digest, competitor discovery, "all clear" noise filter.
  Triggers on "run competitor scan", "check competitors", "competitor deep scan",
  "competitor gap analysis", "competitor gap reverse [name]", "compare SEO",
  "discover competitors", "competitor summary", "add source [competitor] [url] [kind]".
  Sources: competitor websites, sitemaps, Atom/RSS feeds, pricing pages, blog, jobs.
  Output: competitor intelligence report with priority-scored change detection.
category: genx-marketing
version: 2.0.0
---

# Competitor Scout v2.0 — Personal Agent

> **"You trigger. It hunts."** — Now with semantic diffing, content-hash dedup, and priority-scored intelligence.

## Purpose

Monitor competitor pricing, features, positioning, and marketing activity. Competitor Scout runs standalone — not chained into Social Pulse or Clip Mine. Its output is a competitor intelligence report with change detection, gap analysis, and ranked action items.

## Triggers

| Command | Description | Depth |
|---------|------------|-------|
| `run competitor scan` | Standard change detection against last saved snapshot | Homepage + key pages |
| `check competitors` | Quick pulse — surface-level changes only, light report | Homepage only |
| `competitor deep scan` | Full-site scrape of all sub-pages + sitemap auto-discovery | All pages (events, blog, press, podcast, pricing, about) |
| `competitor gap analysis` | Side-by-side comparison of competitor vs GenX Academy | Both sites, all 13 dimensions |
| `competitor gap reverse [name]` | What GenX is missing compared to a specific competitor | GenX site audit |
| `compare SEO` | Indexable page count, backlinks, blog volume, meta tags | Both sites |
| `discover competitors` | AI-powered search for new competitors in GenX's space | Exa semantic search |
| `competitor summary` | Executive digest only — 15-second read, no full report | Synthesis from last scan |
| `add source [competitor] [url] [kind]` | Add a new tracked URL to a competitor | Single source addition |

## Architecture

```
config/competitors.yaml (source-typed entries)
    │
    ▼
Step 1 — Sitemap Discovery (deep scans only)
    mcp_firecrawl_firecrawl_map → auto-discover all indexable URLs
    Also check: robots.txt, Atom/RSS feeds
    │
    ▼
Step 2 — Parallel Scrape
    mcp_firecrawl_firecrawl_scrape on every source URL
    Formats: ["markdown"], onlyMainContent: true
    │
    ▼
Step 3 — Content-Hash Dedup
    SHA256 hash each scraped page
    Compare against previous hash from memory/competitor-snapshots.md
    Skip any page where hash matches — zero content change
    │
    ▼
Step 4 — LLM Semantic Diff
    Feed current + previous content to the agent with instructions:
    "Ignore: typo fixes, date updates, rotating testimonials, 
     footer changes, minor wording tweaks.
     Only flag: pricing model changes, new product announcements,
     positioning pivots, feature launches, target market shifts."
    │
    ▼
Step 5 — Priority Classification
    Tag each change: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
    With one-line impact analysis and recommended action
    │
    ▼
Step 6 — Report Generation
    Executive Digest (15-second read) → 13-dimension table → Gap Analysis → Action Items → Cell-Ready Moves
    │
    ▼
Step 6.5 — Security Rail
    Run skills/security-rail/SKILL.md before user delivery.
    Decide APPROVE / REVISE / SHELVE / NEEDS HUMAN REVIEW.
    │
    ▼
Step 7 — Auto-Save + Deliver
    vault/reports/YYYY-MM-DD-competitor-scan.md
    memory/competitor-snapshots.md (updated hashes)
    If zero changes: "[SILENT]" or "Weekly scan: all clear — no competitor movement detected."
```

## Extraction Strategy (Firecrawl-First)

**Firecrawl MCP is the primary scraper.** It handles Shopify, GoHighLevel, and JS-heavy pages reliably. Use markdown extraction for every page.

```bash
# ✅ Firecrawl (primary — works on all page types)
mcp_firecrawl_firecrawl_scrape with formats=["markdown"], onlyMainContent=true

# ✅ Firecrawl Map (deep scans — auto-discover pages)
mcp_firecrawl_firecrawl_map with search="" to discover all URLs

# ✅ ScrapeGraph (structured JSON fallback — only when markdown is insufficient)
mcp_scrapegraph_extract with output_schema for features/pricing arrays
```

### Deep Scan Workflow

1. **Discover:** `mcp_firecrawl_firecrawl_map` on competitor domain → get all indexed URLs
2. **Filter:** Keep URLs matching source kinds: blog, pricing, docs, changelog, about, events
3. **Batch scrape:** All filtered URLs in parallel via Firecrawl
4. **Hash + diff:** Only process pages with changed content (SHA256 mismatch)
5. **Repeat for GenX Academy** for gap analysis baseline

### GenX Academy Baseline URLs

Always scrape GenX as the comparison baseline:
- `https://www.genxleadershipacademy.com/home`
- `https://www.genxleadershipacademy.com/drsarahegy`
- `https://www.genxleadershipacademy.com/coaching`
- `https://www.genxleadershipacademy.com/consulting-`
- `https://www.genxleadershipacademy.com/blog/category/leadership-skills`

---

## Source Types (NEW in v2.0)

Each competitor tracks multiple source URLs by type. The type tells the agent *what* to expect before scraping, and determines priority:

| Kind | What It Tracks | Priority | Example URL |
|------|---------------|----------|-------------|
| `homepage` | Main landing page — positioning, narrative, hero copy | 🔴 Critical | `https://competitor.com` |
| `pricing` | Pricing page — plan changes, tier restructuring | 🔴 Critical | `https://competitor.com/pricing` |
| `blog` | Blog index — content velocity, topic shifts, launches | 🟡 High | `https://competitor.com/blog` |
| `changelog` | Product changelog — feature releases, deprecations | 🟡 High | `https://competitor.com/changelog` |
| `jobs` | Careers page — hiring signals, growth direction | 🟢 Signal | `https://competitor.com/careers` |
| `docs` | Documentation — API changes, new capabilities | 🟢 Signal | `https://competitor.com/docs` |
| `about` | About page — team growth, mission shifts | 🟢 Signal | `https://competitor.com/about` |
| `events` | Events page — webinars, conferences, launches | 🟢 Signal | `https://competitor.com/events` |
| `press` | Press/media page — credibility moves, announcements | 🟢 Signal | `https://competitor.com/press` |
| `podcast` | Podcast page — thought leadership, audience building | 🟢 Signal | `https://competitor.com/podcast` |
| `other` | Custom page — specify with label | 🟢 Signal | Any URL |

**Config format** (`config/competitors.yaml`):
```yaml
competitors:
  - name: "CrewAI"
    domain: "crewai.com"
    category: "agent-platform"
    sources:
      - url: "https://www.crewai.com"
        kind: homepage
      - url: "https://www.crewai.com/pricing"
        kind: pricing
      - url: "https://www.crewai.com/blog"
        kind: blog
      - url: "https://www.crewai.com/careers"
        kind: jobs
      - url: "https://docs.crewai.com"
        kind: docs
    rss_feed: ""  # optional Atom/RSS feed URL
```

---

## Content-Hash Dedup (NEW in v2.0)

Every scraped page gets a SHA256 hash. Only pages with hash mismatches are processed further.

**Process:**
1. Scrape page → raw markdown content
2. Compute `SHA256(raw_content)`
3. Look up previous hash from `memory/competitor-snapshots.md`
4. If hash matches → skip (zero content change)
5. If hash differs → flag for semantic diffing

**Storage format** (in `memory/competitor-snapshots.md`):
```
### 2026-06-15 — CrewAI
**Content hashes:**
- homepage: a1b2c3d4...
- pricing: e5f6g7h8...
- blog: i9j0k1l2...

**Changes detected:**
- homepage: 🔴 pricing model restructure
- blog: 🟡 2 new posts
- pricing: ✅ no change
- jobs: ✅ no change
```

**Benefit:** After 6 months of weekly scans, you'll have ~26 unique snapshots per source, not 52 duplicates. The database stays lean and diffing stays fast.

---

## Semantic Diffing (NEW in v2.0)

Instead of text-level diffing (which flags every typo and footer update), Competitor Scout uses LLM-powered semantic diffing.

**The prompt pattern:**
> "Compare the current [homepage/pricing/blog] content against the previous snapshot. 
> 
> **IGNORE these noise categories:**
> - Typo fixes and grammar corrections
> - Date updates (copyright year, 'last updated' timestamps)
> - Rotating testimonials or customer logo carousels
> - Footer/navigation/menu changes
> - Minor wording tweaks that don't change meaning
> - CSS/design-only changes
> 
> **ONLY FLAG these strategic signals:**
> - Pricing model changes (new tiers, price adjustments, billing period changes)
> - New product announcements or feature launches
> - Positioning pivots (new taglines, target market shifts, value prop changes)
> - Deprecations or feature removals
> - New partnerships, integrations, or certifications
> - Hiring pattern shifts (engineering → sales = go-to-market phase)
> - Rebranding signals (name changes, visual identity overhauls)
> - New customer logos or case studies (especially Fortune 500 / enterprise)
> - Event or product launch announcements
> 
> **For each detected change, provide:**
> 1. What changed (specific before/after)
> 2. Priority: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
> 3. One-line impact analysis
> 4. Recommended GenX response (if any)
> 
> If no strategic signals are detected, respond: 'NO_STRATEGIC_CHANGE'."

**Thresholds:**
- 🔴 **HIGH** — Pricing change, new product, major repositioning, Fortune 500 win
- 🟡 **MEDIUM** — New feature, new blog series, new customer logo, partnership
- 🟢 **LOW** — Minor copy update, new blog post (routine), updated testimonial

---

## Change Priority Scoring (NEW in v2.0)

Every detected change gets classified and prioritized. The report displays them in a scannable format:

| Change | Detail | Priority | Impact | GenX Response |
|--------|--------|----------|--------|---------------|
| New product launch | "Interrupt" event shipped | 🔴 HIGH | Expands platform — new competitive dimension | Monitor for 2 weeks, review blog post |
| New customer logos | 5 Fortune 500 logos added | 🟡 MEDIUM | Credibility floor raised | Note in positioning docs |
| Blog post frequency | Now publishing 3x/week (was 1x) | 🟢 LOW | Content velocity up | No action needed |
| Pricing page | No change | ✅ STABLE | — | — |

---

## "All Clear" — Noise Suppression (NEW in v2.0)

When zero strategic changes are detected across all competitors:

**For cron jobs:**
Respond with exactly `[SILENT]` — nothing is delivered to the user. No report is generated. No tokens wasted.

**For ad-hoc scans:**
Respond with:
> "Weekly competitor scan: all clear. No strategic movement detected across [N] competitors since [last scan date]. Next scan: [next Monday's date]."

**Rule:** If total hash mismatches = 0 OR all hash mismatches are classified as LOW/noise, treat as "all clear."

---

## Competitor Auto-Discovery (NEW in v2.0)

The `discover competitors` command uses Exa semantic search to find new competitors in GenX's space.

**Prompt pattern:**
> "Find B2B SaaS companies offering AI team platforms, AI agent orchestration, or AI implementation services for founders and SMEs (50-200 employees). Similar to CrewAI and LangChain but focused on implementation outcomes rather than developer tooling. Exclude: enterprise-only platforms, pure developer tools, AI coding assistants."

**Output:**
- Top 5 candidates with: name, website, one-line description, why they're relevant
- User selects which to add → appended to `config/competitors.yaml`
- Deep discovery frequency: monthly (to avoid noise)

---

## Output — Full Report Structure

Every report follows this structure:

### Section 1: Executive Digest (NEW — top of every report)
```
## Executive Digest

**This week's signal:** [2-3 sentence synthesis of what moved]
**Urgency:** 🔴 HIGH / 🟡 MODERATE / 🟢 LOW — [one-line reason]
**Key change:** [single most important competitive move this week]
**Recommended action:** [one concrete thing GenX should do]
**Competitors scanned:** [N] | **Changes detected:** [N] | **Strategic shifts:** [N]
```

### Section 2: Decision
```
## Decision
**Recommended action:** [respond / monitor / ignore]
**Priority competitor:** [name]
**Confidence:** [High / Medium / Low] — [reason]
**Fallback:** If rejected, monitor [signal] for [timeframe].
```

### Section 3: Competitor Profiles (per competitor)
```
### [COMPETITOR NAME]

**Website:** [URL] | **Last scanned:** [date] | **Threat level:** [H/M/L]

#### What Changed
| Change | Detail | Priority | Impact | GenX Response |
|--------|--------|----------|--------|---------------|
| [what] | [detail] | 🔴🟡🟢 | [impact] | [response] |

**Pages with no change:** pricing, jobs (hash match — skipped)

#### Current Positioning
- **Messaging:** "[tagline]"
- **Positioning:** [description]
- **Blacklist signals:** [none / hype / woo / corporate filler]

#### Brand Gap Mapping
- **B2C gap:** [science+soul opportunity]
- **B2B gap:** [results-not-advice opportunity]
- **What GenX can own:** [one clear angle]
- **What NOT to copy:** [specific competitor tactics that conflict with GenX brand]
```

### Section 4: Side-by-Side Comparison (13 dimensions)
```
| Dimension | Competitor A | Competitor B | GenX | Gap |
|-----------|-------------|-------------|------|-----|
| Platform | ... | ... | ... | 🔴🟡✅ |
| Products | ... | ... | ... | ... |
| Blog | ... | ... | ... | ... |
| Podcast | ... | ... | ... | ... |
| Events | ... | ... | ... | ... |
| Press/Media | ... | ... | ... | ... |
| Newsletter | ... | ... | ... | ... |
| Testimonials | ... | ... | ... | ... |
| Founder Story | ... | ... | ... | ... |
| Methodology | ... | ... | ... | ... |
| Credibility | ... | ... | ... | ... |
| Pricing Visible | ... | ... | ... | ... |
| SEO surface area | ... | ... | ... | ... |
```

### Section 5: Positioning Gap Analysis
- B2B gap — "Results not advice" opportunity
- B2C gap — "Science + soul" opportunity
- GenX's unfair advantage — what competitors structurally cannot copy

### Section 6: Priority Action Items
```
| # | Gap | What to Build | Effort | Impact | Severity |
|---|-----|--------------|--------|--------|----------|
| 1 | [gap] | [action] | Low/Med/High | 🟢 revenue, SEO, conversions | 🔴 Critical |
| 2 | [gap] | [action] | Low/Med/High | 🟢 ... | 🟡 High-Value |
```

### Section 7: Cell-Ready Moves

Translate competitive intelligence into small operating cells the team can use immediately:

```text
| Cell | Use | Move | Evidence Required | Owner |
|------|-----|------|-------------------|-------|
| Content Cell | Post/blog/reel idea | [angle] | [source URL/proof] | [team/person] |
| Sales Cell | Sales objection or positioning note | [talk track] | [source URL/proof] | [team/person] |
| Product/Offer Cell | Offer, page, or proof gap | [build/fix] | [source URL/proof] | [team/person] |
```

Rules:
- Do not invent proof for a cell.
- Mark cells `NEEDS HUMAN REVIEW` when they contain competitor, legal, pricing, or performance claims.
- Keep cells short enough to paste into a planning board or CRM note.

### Section 8: Next Scan
```
**Next scan:** Monday, [date]
**Focus areas:** [specific things to watch]
**Add or remove competitors** in `config/competitors.yaml`.
```

---

## Light Report (Quick Pulse)

When the user says `check competitors` (quick pulse), skip sections 4-6. Output only:

```
## Executive Digest
[2-3 sentence synthesis]

## Quick Pulse — [Date]
| Competitor | Status | Key Change | Priority |
|------------|--------|------------|----------|
| CrewAI | 🟢 stable | No changes | — |
| LangChain | 🔴 changed | New product launch | HIGH |

**Scan time:** [X] seconds | **Pages checked:** [N] | **Hash matches:** [N]
**Next full scan:** [next Monday]
```

---

## Weekly Automation

1. Competitor list lives in `config/competitors.yaml` (source-typed entries)
2. Cron job `Weekly Competitor Scan` runs Mondays at 9am
3. Pipeline: Firecrawl scrape → hash dedup → semantic diff → priority score → report
4. If zero strategic changes → `[SILENT]`
5. Saves report to `vault/reports/YYYY-MM-DD-competitor-scan.md`
6. Updates hashes in `memory/competitor-snapshots.md`
7. Delivers summary to user (via cron origin delivery)

## Delivery

Before delivery, run `skills/security-rail/SKILL.md`. Deliver only the approved or revised safe version. If Security Rail returns `SHELVE`, do not recommend the competitive move. If it returns `NEEDS HUMAN REVIEW`, label the report/cell clearly.

Reports are delivered to the user's conversation. For future multi-channel delivery (Slack, email), configure in the cron job settings.

When the `send_message` tool is available, post-scan delivery can route to:
- Telegram (default — origin channel)
- Slack (configure webhook URL)
- Email (via Resend, needs `RESEND_API_KEY`)

**Delivery rules:**
- `[SILENT]` → nothing delivered
- Quick pulse → executive digest only
- Full scan → complete report with all 7 sections
- Deep scan → full report + sitemap discovery notes

---

## MCP-Only Fallback Mode (Cron / Backend Outage)

When the Python CLI is unreachable (Hermes backend errors, sandbox restrictions):

1. **Read config:** Recover `competitors.yaml` from session history or browser `file://` navigation
2. **Scrape:** Use `mcp_firecrawl_firecrawl_scrape` with `formats=["markdown"]` for each source URL
3. **Hash:** Compute SHA256 manually or track page content fingerprints
4. **Diff:** Semantic diff via LLM prompting in the agent's context
5. **Report:** Produce report directly in response — this is the canonical record
6. **Snapshots:** Update `memory/competitor-snapshots.md` when `write_file` is available

**Key limitations in MCP-only mode:**
- Cannot run `api_extract.py` (requires terminal)
- Cannot write files (requires `write_file` or `terminal`)
- Must diff features manually in context
- JSON snapshots to `vault/competitor-data/` may be blocked

---

## Rules

- Public sources only — no login/paywall bypass
- Cite dates for all changes
- Flag unverified claims
- Store snapshots to `memory/competitor-snapshots.md`
- **Firecrawl first, ScrapeGraph only as structured-data fallback**
- **Always scrape GenX Academy as the comparison baseline**
- **Never skip the positioning gap** — raw feature lists without GenX gap analysis waste the scan
- **Always include "What NOT to copy"** — competitor tactics that conflict with GenX brand voice
- **Scrape ALL source-typed sub-pages on deep dives** — homepage alone misses 80% of the picture
- **Use parallel Firecrawl calls** for sub-pages — faster, avoids sequential bottlenecks
- **Hash before diffing** — skip unchanged pages to save tokens and time
- **Semantic diff, not text diff** — ignore noise, surface strategic signals only
- **Prioritize every change** — 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW with impact analysis
- **Silence on no change** — `[SILENT]` for cron, "all clear" for ad-hoc
- **Competitor discovery is monthly** — don't spam search APIs
- **Security Rail is mandatory before delivery** — competitor claims and action cells must be sourced, caveated, or shelved

---

## Reference Files

- `updates/hermes/competitor-report-template-v2.md` — Full report structure and section guidance.
- `updates/hermes/competitor-landscape-research-jun-2026.md` — Open-source competitive intelligence landscape: repos analyzed, techniques compared, adaptation plan.
- `updates/hermes/competitors-v2.yaml` — Source-typed competitor config reference.
