# Goblin Recon — Implementation Suggestions
## Diagnosis + MCP-Powered Source Strategy + News Sector Framework

**Generated:** June 15, 2026
**Status:** Recommendations — not yet implemented

---

## 1. DIAGNOSIS: What's Blocking Goblin Recon

### Root Cause

The architecture is sound. The problem is a **platform access mismatch:**

```
Architecture says:  Instagram → TikTok → X → Reddit → News
Reality says:       BLOCKED    BLOCKED   Partial  BLOCKED  Works
```

The system is designed around IG/TikTok as primary trend detection surfaces, but both are walled off at the public-access level and no official APIs are configured.

### What Works (Solid Foundation)

| Component | Status |
|-----------|--------|
| Exa MCP (semantic search) | ✅ Live — 4 keys set |
| Tavily MCP (research search) | ✅ Live |
| Firecrawl MCP (page extraction) | ✅ Live |
| ScrapeGraph MCP (structured extraction) | ✅ Live |
| YouTube transcript MCP | ✅ Live (no key needed) |
| Python tool suite (13 tools) | ✅ All functional |
| Brand gate | ✅ Operational |
| Clip extraction + scoring | ✅ Operational |
| Vault/clip store | ✅ Operational |
| Orchestrator/router | ✅ Sound design |

### What's Missing

| Component | Priority | Difficulty |
|-----------|----------|------------|
| YouTube Data API key | High | Easy — standard Google Cloud Console |
| X/Twitter Bearer Token | Medium | Medium — developer account needed |
| Reddit API credentials | Medium | Medium — app registration needed |
| Instagram Meta API | Low | Hard — business verification required |
| TikTok Research API | Low | Hard — restricted access |
| Real competitors in `config/competitors.yaml` | Medium | Easy — just needs names/URLs |

---

## 2. MCP-POWERED SOURCE STRATEGY

### The New Pipeline

Replace browser-based news scanning with MCP-first discovery:

```
                    MCP-POWERED SOCIAL PULSE
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      LAYER 1:         LAYER 2:       LAYER 3:
      DISCOVERY       EXTRACTION      DEEP RESEARCH
            │              │              │
      Exa MCP        Firecrawl       Tavily MCP
      (semantic       MCP            (research-grade
       search)        (clean          synthesis)
            │         markdown)            │
            │              │              │
      Find stories    Pull full      When a story
      by meaning,     article text   needs multi-
      not keywords.   from URLs      source context
      Date-filtered.  Exa found.     and analysis.
            │              │              │
            └──────────────┼──────────────┘
                           │
                    LAYER 4: STRUCTURING
                           │
                    ScrapeGraph MCP
                    (structured extraction)
                           │
                    Normalize into:
                    headline, author, date,
                    key_claims[], angle,
                    category, source_type
                           │
                           ▼
                    social_intake schema
                           │
                           ▼
                    Trend Radar scoring
```

### Each MCP's Specific Job

| MCP | Job | Query Type | What It Replaces |
|-----|-----|------------|------------------|
| **Exa** | Story discovery | Semantic — search by meaning, not keywords | Instagram/TikTok scanning, TechCrunch browsing |
| **Firecrawl** | Content extraction | URL → clean markdown from any page | Browser navigation + manual copy-paste |
| **ScrapeGraph** | Structured normalization | URL + prompt → JSON with schema | Manual data entry into social_intake fields |
| **Tavily** | Deep research | Multi-source synthesis on one topic | Manual cross-referencing across multiple tabs |

### Query Strategy: Content-Type-Specific Prompts

Each content category gets a dedicated Exa query strategy:

#### CONTRARIAN / ANALYTICAL
```
Query: "AI story with contrarian or critical perspective from practitioner or researcher,
       not press release, published this week"
Query: "under-reported angle on major AI development, from analyst or independent source"
Query: "AI industry critique or strategic analysis from credible non-journalist source"
```

#### UPGRADE / DEMOCRATIZATION
```
Query: "new AI tool or technique that lets non-experts do something previously impossible,
       published this week"
Query: "AI workflow or automation that collapsed a barrier for small business owners or
       independent creators"
Query: "story about someone using AI to achieve result they couldn't before, with specific numbers"
```

#### LATEST AI NEWS (Differentiated)
```
Query: "AI development or launch this week not yet covered by TechCrunch or The Verge"
Query: "AI company strategic decision with operational implications, from internal memo,
       leak, or analyst report"
Query: "new AI model or capability released this week with unexpected capability or restriction"
```

#### CONTROVERSIAL / POLARIZING
```
Query: "AI ethics or safety controversy with whistleblower, internal criticism, or
       legal action angle this month"
Query: "AI company accused of deceptive, anti-competitive, or harmful behavior by
       credible source"
Query: "AI policy or regulation story with genuine operational impact on companies"
```

### Fallback Chain (When MCP Fails)

```
Exa MCP failed → Firecrawl search (mcp_firecrawl_firecrawl_search)
  → Tavily search (mcp_tavily_tavily_search)
    → Hermes built-in web_search (final fallback)
```

Same for extraction:
```
Firecrawl scrape failed → ScrapeGraph extract
  → Tavily extract
    → Hermes built-in web_extract (final fallback)
```

---

## 3. NEWS QUALITY FILTER

### Hard Skip Criteria (Auto-Reject)

Stories matching ANY of these are automatically skipped:

- Funding round announcement without structural insight (e.g., "Company X raises $Y million")
- Feature launch unless it genuinely changes the product category
- Press release as the sole or primary source
- Story already on 3+ mainstream outlets without a new angle offered
- Generic "AI is transforming [industry]" thought piece with no data
- "Company X partners with Company Y" announcement (unless strategic implications are clear)
- Story older than 7 days without a fresh development

### Prioritize Criteria (Boost Score)

Stories matching these get priority:

- Broke on X, Hacker News, GitHub, or a niche newsletter before mainstream coverage
- Contrarian position available from a credible practitioner or analyst
- Direct operational impact on founders/SME operators (not just enterprise)
- Under-reported angle on a mainstream story
- Research paper with clear product or workflow implications
- Internal memo, leak, or court filing (primary source, not journalist interpretation)
- Specific numbers: "X% of Y," "$Z in savings," "N companies affected"

### Minimum Score Thresholds

| Criterion | Minimum | Weight |
|-----------|---------|--------|
| Novelty (not on every AI page) | 6/10 | High |
| Angle potential (can we take a position?) | 5/10 | High |
| Format adaptability (maps to reel/carousel/blog) | Required | Gate |
| Audience relevance (matters to founders/SMEs) | 4/10 | Medium |
| Velocity (accelerating or holding?) | 3/10 | Medium |
| Source uniqueness (non-mainstream origin) | Bonus | Bonus |

---

## 4. NEWS BY TECH SECTOR

Organize news discovery by sector so each scan can pull from specific domains.
This prevents the "same 5 stories" problem and enables sector-specific content.

### Sector 1: Frontier AI Models & Labs

**What it covers:** New model releases, capability jumps, safety incidents, lab strategy

**Sources:**
- Anthropic research blog (anthropic.com/research)
- OpenAI blog (openai.com/blog)
- Google DeepMind (deepmind.google/blog)
- Meta AI (ai.meta.com/blog)
- Mistral AI blog
- arXiv — cs.AI, cs.CL, cs.LG categories
- Simon Willison's blog (simonwillison.net)
- Nathan Lambert / Interconnects (interconnects.ai)

**Query strategy:**
```
Exa: "frontier AI model release or capability change this week, from lab blog
     or researcher analysis, not generic news roundup"
Exa: "AI safety incident or model restriction story this month, from researcher
     or internal source"
```

### Sector 2: AI Agents & Automation

**What it covers:** Agent platforms, workflow automation, agent-to-agent systems, enterprise deployment

**Sources:**
- LangChain blog (blog.langchain.dev)
- CrewAI blog
- Anthropic — agent-related research
- GitHub Trending — agent frameworks
- Hacker News — agent discussions
- Substack writers focused on agents

**Query strategy:**
```
Exa: "AI agent deployment or failure story from real company, with specific outcomes,
     published this month"
Exa: "AI agent platform comparison or critique from practitioner who built with them"
```

### Sector 3: AI + Business / Enterprise

**What it covers:** ROI data, adoption statistics, organizational change, job market impact

**Sources:**
- Bain / McKinsey / Deloitte AI reports
- Bloomberg — AI economy coverage
- WSJ tech section
- Harvard Business Review — AI articles
- Company earnings calls mentioning AI spend
- Apollo / Goldman Sachs AI research

**Query strategy:**
```
Exa: "AI adoption or ROI data from company earnings call or consulting report,
     with specific percentages, this quarter"
Exa: "AI replacing or changing job roles story with before/after data, not speculation"
```

### Sector 4: AI Policy & Regulation

**What it covers:** Laws, executive orders, court cases, export controls, liability frameworks

**Sources:**
- Law firm AI practice blogs (Mishcon, Wilson Sonsini, etc.)
- EU AI Act enforcement updates
- FTC/DOJ actions involving AI
- Court filings (PACER, CourtListener)
- Congressional bills (congress.gov)
- State-level AI bills

**Query strategy:**
```
Exa: "AI regulation or court ruling this month with direct compliance impact on
     companies building or using AI"
Exa: "AI export control or national security restriction story, from legal or
     policy analyst, this week"
```

### Sector 5: Open Source AI

**What it covers:** Open model releases, community projects, license changes, open vs closed debates

**Sources:**
- Hugging Face blog
- GitHub Trending
- EleutherAI blog
- Allen AI (AI2) blog
- Mistral releases
- Reddit — r/LocalLLaMA
- Hacker News

**Query strategy:**
```
Exa: "open source AI model release or license change this week with significant
     capability jump"
Exa: "open source vs closed AI debate or comparison from practitioner who uses both"
```

### Sector 6: AI Tools & Developer Ecosystem

**What it covers:** New dev tools, IDE features, API changes, developer experience, MCP ecosystem

**Sources:**
- Product Hunt — AI category
- GitHub Trending
- Hacker News
- Dev tool company blogs (Vercel, Replit, Codeium, Cursor, Windsurf)
- Hermes/Claude Code/Copilot updates

**Query strategy:**
```
Exa: "AI developer tool launch or update this week with significant new capability"
Exa: "AI coding tool benchmark or comparison from developer who tested multiple tools"
```

### Sector 7: AI + Specific Industries

**What it covers:** Healthcare AI, legal AI, fintech AI, education AI, creative AI

**Sources:**
- Industry-specific publications
- FDA AI/ML approvals
- Legal tech publications
- Education technology blogs
- Creative tool updates

**Query strategy:**
```
Exa: "AI deployment in [healthcare/law/finance/education] with measured outcomes,
     not pilot announcement, this quarter"
```

### Sector Scan Priority (Per Run)

Not all sectors every time. Rotate based on velocity:

| Frequency | Sectors |
|-----------|---------|
| **Every scan** | Frontier Models, AI Agents |
| **2x/week** | Business/Enterprise, Policy/Regulation |
| **1x/week** | Open Source, Dev Tools |
| **As relevant** | Industry-specific (healthcare, legal, fintech) |

---

## 5. SOURCE REBALANCING

### Current Source Pyramid (Broken)

```
Priority 1: Instagram ── BLOCKED
Priority 2: TikTok    ── BLOCKED
Priority 3: X/Twitter ── Partial
Priority 4: Reddit    ── BLOCKED
Priority 5: Tech News ── Working but generic
Priority 6: Product Hunt ── Working
```

### Proposed Source Pyramid (Reality-Based)

```
TRACK A: Early Signal (first-mover — daily)
  1. Exa semantic search     — differentiated story discovery
  2. Hacker News             — builder sentiment
  3. GitHub Trending         — repo velocity
  4. X/Twitter (when token)  — real-time velocity check
  5. ArXiv                   — research-to-product leads

TRACK B: Validation (confirm + enrich)
  1. Firecrawl scrape        — full article text
  2. TechCrunch / Verge      — confirm dates, URLs, facts
  3. Tavily research         — multi-source context
  4. YouTube podcasts        — expert commentary, clip source

FEED: Sector-specific queries
  (Frontier Models, Agents, Business, Policy, Open Source, Dev Tools, Industry)
```

### Fast Scan Becomes Default

Fast Scan already uses YouTube, Reddit, Tech News, Product Hunt, X. It should be renamed
from "the exception" to "the default scan mode." Deep Social Scan gets gated behind
actual social API connectivity (Meta/TikTok API approval).

---

## 6. BETTER NEWS SOURCES (Beyond Mainstream)

### Current Sources (Generic — Keep for Validation Only)

- TechCrunch
- The Verge
- VentureBeat
- Ars Technica

**Role:** Validation. Confirm dates, URLs, facts. Do NOT let these drive story selection.

### New Sources (Differentiated — Drive Discovery)

| Source | Type | What It Surfaces | Why Different |
|--------|------|-----------------|---------------|
| **The Rundown AI** (therundown.ai) | Newsletter | Curated daily AI news, not republished | Signal-to-noise filter built in |
| **TLDR AI** (tldr.tech/ai) | Newsletter | Daily curated AI with practitioner focus | No fluff, no press releases |
| **Import AI** (Jack Clark, importai.substack.com) | Newsletter | Anthropic co-founder perspective | Insider lens, policy + technical depth |
| **Simon Willison's Blog** (simonwillison.net) | Blog | Practitioner deep-dives | Technical truth vs PR narrative |
| **Interconnects** (Nathan Lambert, interconnects.ai) | Substack | AI governance + lab strategy | Independent analyst at Allen AI |
| **Stratechery** (Ben Thompson, stratechery.com) | Substack | Tech strategy analysis | Structural, not news-cycle driven |
| **AI Snake Oil** (aisnakeoil.com) | Blog | AI hype debunking, empirical critique | Contrarian by design |
| **One Useful Thing** (Ethan Mollick, oneusefulthing.org) | Substack | AI in practice, experiments | Practitioner with data, not opinion |
| **Latent Space** (latent.space) | Newsletter | AI engineering + research | Technical depth from builders |
| **Hacker News** (news.ycombinator.com) | Aggregator | What builders care about | Practitioner signal, not journalist narrative |
| **Company Engineering Blogs** | Primary | Technical truth from source | OpenAI, Anthropic, DeepMind, Meta all publish directly |

---

## 7. COMPETITOR CONFIG FIX

### Current State
`config/competitors.yaml` has two placeholder entries (CrewAI, LangChain). Neither is a direct GenX Academy competitor.

### Suggested Competitors

GenX Academy operates in "AI team platform for founders" — helping founders build AI-powered teams. Real competitors to add:

```yaml
competitors:
  - name: "Taskade"
    website: "https://www.taskade.com"
    pricing_page: "https://www.taskade.com/pricing"
    category: "ai-team-platform"
    notes: "AI agents for teams. Direct feature overlap."

  - name: "Relevance AI"
    website: "https://relevanceai.com"
    pricing_page: "https://relevanceai.com/pricing"
    category: "ai-team-platform"
    notes: "AI workforce platform. B2B focus."

  - name: "Agent.ai"
    website: "https://agent.ai"
    pricing_page: ""
    category: "agent-marketplace"
    notes: "AI agent marketplace. Adjacent competitor."

  - name: "Lindy"
    website: "https://www.lindy.ai"
    pricing_page: "https://www.lindy.ai/pricing"
    category: "ai-team-platform"
    notes: "AI assistants for business teams."

  - name: "CrewAI"
    website: "https://www.crewai.com"
    pricing_page: "https://www.crewai.com/pricing"
    category: "agent-platform"
    notes: "Multi-agent orchestration. Developer-focused."

  - name: "AutoGen (Microsoft)"
    website: "https://microsoft.github.io/autogen/"
    pricing_page: ""
    category: "agent-framework"
    notes: "Microsoft-backed agent framework. Enterprise credibility."
```

---

## 8. IMPLEMENTATION PRIORITY ORDER

### Phase 1: Immediate (This Week) — Zero New Keys Required

1. **Add MCP query strategies to Social Pulse workflow**
   - Replace browser-based news scanning with Exa semantic search
   - Wire Firecrawl for article extraction from Exa-discovered URLs
   - Add ScrapeGraph for structured normalization

2. **Implement news quality filter**
   - Add hard-skip criteria before Trend Radar scoring
   - Gate stories on novelty + angle potential minimums

3. **Organize queries by sector**
   - Create sector-specific query templates in config
   - Rotate sector scans based on frequency table

### Phase 2: Short-Term (Next 1-2 Weeks) — New API Keys Needed

4. **Get YouTube Data API key**
   - Standard Google Cloud Console → enable YouTube Data API v3
   - Enables: search by topic, view counts, engagement metrics without browser

5. **Fill competitor config**
   - Add real GenX competitors from list above
   - Run first real competitor scan

6. **Add differentiated news sources to config**
   - Substack newsletters, blogs, Hacker News, company engineering blogs

### Phase 3: Medium-Term (When Approved)

7. **Get X/Twitter Bearer Token**
   - Enables: real-time velocity validation, breaking story detection

8. **Get Reddit API credentials**
   - Enables: community sentiment analysis, practitioner discussion mining

### Phase 4: Long-Term (When Possible)

9. **Meta API / TikTok Research API**
   - Required: business verification, research application
   - Only pursue if GenX Academy decides social-native discovery is essential

---

## 9. CONFIG CHANGES REQUIRED

### `config/sources.yaml` — Add news quality filter section

```yaml
news_quality_filter:
  hard_skip:
    - "funding round announcement without structural insight"
    - "feature launch unless genuinely category-changing"
    - "press release as sole source"
    - "story already on 3+ mainstream outlets without new angle"
    - "generic AI industry thought piece with no data"
    - "partnership announcement without clear strategic implications"
    - "story older than 7 days without fresh development"

  prioritize:
    - "broke on X, HN, GitHub, or niche newsletter before mainstream coverage"
    - "contrarian position available from credible practitioner"
    - "direct operational impact on founders/SME operators"
    - "under-reported angle on mainstream story"
    - "research paper with clear product/workflow implications"
    - "internal memo, leak, or court filing as primary source"
    - "specific numbers: percentages, dollar amounts, affected counts"

  minimum_scores:
    novelty: 6
    angle_potential: 5
    format_adaptability: "required"
    audience_relevance: 4
    velocity: 3
```

### `config/sources.yaml` — Add sector-based source configuration

```yaml
news_sectors:
  frontier_models:
    frequency: daily
    sources:
      - type: company_blog
        names: [Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral]
      - type: researcher
        names: [Simon Willison, Nathan Lambert, Jack Clark]
      - type: arxiv
        categories: [cs.AI, cs.CL, cs.LG]
    exa_queries:
      - "frontier AI model release or capability change this week, from lab blog or researcher analysis"
      - "AI safety incident or model restriction story this month, from researcher or internal source"

  ai_agents:
    frequency: daily
    sources:
      - type: company_blog
        names: [LangChain, CrewAI]
      - type: github_trending
        filter: "agent"
      - type: hacker_news
        search_terms: [agent, multi-agent, automation]
    exa_queries:
      - "AI agent deployment or failure story from real company with specific outcomes this month"
      - "AI agent platform comparison or critique from practitioner who built with them"

  ai_business:
    frequency: twice_weekly
    sources:
      - type: consulting_report
        sources: [Bain, McKinsey, Deloitte, Goldman Sachs, Apollo]
      - type: news
        sources: [Bloomberg, WSJ, HBR]
    exa_queries:
      - "AI adoption or ROI data from company earnings call or consulting report with percentages this quarter"
      - "AI replacing or changing job roles story with before/after data not speculation"

  ai_policy:
    frequency: twice_weekly
    sources:
      - type: legal_blog
        sources: [Mishcon, Wilson Sonsini, IAPP]
      - type: government
        sources: [congress.gov, FTC, EU AI Office]
    exa_queries:
      - "AI regulation or court ruling this month with direct compliance impact on companies"
      - "AI export control or national security restriction from legal or policy analyst this week"

  open_source_ai:
    frequency: weekly
    sources:
      - type: blog
        sources: [Hugging Face, EleutherAI, Allen AI]
      - type: github_trending
      - type: reddit
        subreddits: [LocalLLaMA]
    exa_queries:
      - "open source AI model release or license change this week with significant capability jump"

  ai_dev_tools:
    frequency: weekly
    sources:
      - type: product_hunt
        topic: artificial-intelligence
      - type: github_trending
      - type: company_blog
        sources: [Vercel, Replit, Cursor, Windsurf]
    exa_queries:
      - "AI developer tool launch or update this week with significant new capability"

  ai_industry_specific:
    frequency: as_relevant
    sectors: [healthcare, legal, fintech, education, creative]
    exa_queries:
      - "AI deployment in {sector} with measured outcomes not pilot announcement this quarter"
```

---

## 10. SUMMARY

### What Changes

| Before | After |
|--------|-------|
| Instagram/TikTok primary discovery | Exa semantic search primary discovery |
| Browser-based news scanning | MCP-first extraction (Exa → Firecrawl → ScrapeGraph) |
| Generic "what's trending" queries | Sector-specific semantic queries |
| No quality filter on news | Hard-skip + minimum score gates |
| TechCrunch/Verge drive story selection | They validate only — niche sources drive discovery |
| All sectors every scan | Rotated sector priority per frequency table |
| Placeholder competitors | Real GenX Academy competitors |

### What Stays the Same

- Router → Workflow → Tools → Score → Brand Gate → Human Gate → Memory
- 7-dimension clip scoring system
- Brand gate (blacklist + alignment ≥ 8/15)
- Output standards (Decision-first, platform variants, phone-scannable)
- Clip Vault + dedup system
- All 13 Python tools
