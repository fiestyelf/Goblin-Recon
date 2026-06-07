# Goblin Recon — Session Log

> Every change tracked. Every decision recorded. No guessing what happened when.

---

## Session 1 — June 6, 2026
**Agent:** Hermes assistant
**What we did:** Full end-to-end test of all 3 layers. Restructured trend pipeline.

### Changes Made

| File | Change | Reason |
|------|--------|--------|
| `config/sources.yaml` | Restructured: Instagram → TikTok → X/Reddit → News | Instagram/TikTok content is 10x more engaging than tech news for faceless reels |
| `config/sources.yaml` | Added Instagram creator accounts as primary sources | @therundownai (491K), @rowancheung (418K), @inflecta.ai, @ankitgupta.ai drive AI conversation |
| `config/sources.yaml` | Added TikTok trend tags + creator handles | TikTok is the #2 platform for viral AI content |
| `config/content-sources.yaml` | Fixed truncated Lex Fridman channel ID | Was: `UCSHZKJJfhK61IS3MnH`, Now: `UCSHZKyawb77ixDdsGog4iWA` |
| `config/content-sources.yaml` | Added TikTok creator list + search queries | For Layer 2 source hunting on TikTok |
| `config/scoring.yaml` | Added `social_velocity` dimension to Trend Radar (max 25) | Replaces generic velocity with platform-specific IG/TikTok metrics |
| `config/scoring.yaml` | Added `scroll_stop` dimension to Moment Finder (max 15) | Does this make someone stop scrolling? Critical for faceless reels |
| `AGENTS.md` | Updated Trend Radar priority: IG first, TikTok second, then social, then news | Reflects where actual engagement lives |
| `AGENTS.md` | Added Instagram/TikTok scraping rules | Public profiles only, no login bypass, respect rate limits |
| `AGENTS.md` | Added reel format analysis to trend reports | Not just what's trending, but HOW it's being presented |
| `SESSION_LOG.md` | Created this file | Track all changes per session |

### Test Results

| Test | Result |
|------|--------|
| Layer 1: Trend Radar (news sites) | ✅ 5 stories found, all scored >60 |
| Layer 1: Instagram creator scan | ✅ 8 trending topics identified from @therundownai + @rowancheung |
| Layer 2: Source Hunter (YouTube) | ✅ 15+ videos found across 3 stories |
| Layer 3: Moment Finder | ✅ 43-second clip extracted from Wes Roth video (5:08→5:51) |
| Python scripts (7 tests) | ✅ All passing |
| Brand gate | ✅ Blacklist check, alignment scoring working |
| Hermes profile | ✅ `goblin-recon` profile created |

### Key Finding
Instagram creator content (@therundownai, @rowancheung) produces **significantly more engaging** material for faceless reels than traditional tech news. Stories like "Claude vs Grok virtual towns" and "Student makes $238K with Claude" are viral-ready in a way that "Google pays SpaceX $920M" is not (despite scoring 96 on the news-based rubric).

### Open Items
- [ ] Competitor list still empty in `competitors.yaml`
- [ ] YouTube Data API not yet enabled (using transcript extraction only)
- [ ] Meta/Instagram API not connected (using public browser scraping)
- [ ] No TikTok API integration (using browser scraping)
- [ ] Content tracker (Notion/Sheets) not connected
- [ ] Desktop Schedules not yet created

### Next Session
- Fill competitor list
- Test TikTok trend scraping
- Build Desktop cron schedules
- Run another full scan with new IG-first pipeline

---

## Session 2 — June 6, 2026
**Agent:** Hermes assistant
**What we did:** Bifurcated Goblin Recon into two pipelines. Created SOUL.md and specialized profile.

### Changes Made

| File | Change | Reason |
|------|--------|--------|
| `AGENTS.md` | Added "Two Pipelines" section | Social Pulse (ideas) and Clip Mine (video clips) serve completely different purposes |
| `AGENTS.md` | Restructured commands into Pipeline A/B sections | User now says "run social pulse" or "run clip mine" — clear separation |
| `AGENTS.md` | Added category tags (Latest AI News / Controversial / Upgrade / Analytical) | Every output tagged so editors know what content type they're handling |
| `templates/social-pulse-report.md` | ✅ Created | Template for Pipeline A: ideas, blogs, carousels, strategy |
| `templates/clip-mine-brief.md` | ✅ Created | Template for Pipeline B: timestamped clips for faceless IG page |
| `.hermes/profiles/goblin-recon/SOUL.md` | ✅ Created full persona | Agent now knows it's Goblin Recon, not a generic assistant. GenX brand DNA embedded |
| `.hermes/profiles/goblin-recon/skills/genx-marketing/goblin-recon/SKILL.md` | ✅ Created operational skill | Auto-loads on profile start. Pipeline stages, scoring, formats |
| `.hermes/profiles/goblin-recon/config.yaml` | ✅ Configured | Auto-load goblin-recon skill, model=deepseek-v4-flash, terminal timeout=300s |
| `.hermes/profiles/goblin-recon/skills/desktop/` | ✅ Installed 5 skills | competitor-profiling, social-content, copywriting, content-strategy, marketing-psychology |
| `goblin-recon skill` | ✅ Added Two Pipelines section | Skill reflects the bifurcation for any agent loading it |

### Profile State

```
Profile:   goblin-recon
Model:     deepseek-v4-flash (deepseek)
Skills:    96 (90 base + goblin-recon + 5 cherry-picked)
SOUL.md:   ✅ 151 lines, GenX brand DNA
Auto-load: ✅ goblin-recon skill on startup
```

### What This Means for the User

**Before:** "find trending AI stories" → got mixed bag of everything

**Now:**
- `run social pulse` → gets blog ideas, carousel topics, content strategy angles
- `run clip mine` → gets timestamped podcast clips for editors to cut
- Every item tagged: Latest AI News / Controversial / Upgrade / Analytical
- Clean separation: ideas for strategy team, clips for video editors

### Open Items
- [ ] Competitor list still empty in `competitors.yaml`
- [ ] YouTube Data API not yet enabled
- [ ] Meta/Instagram API not connected
- [ ] TikTok API not connected
- [ ] Content tracker (Notion/Sheets) not connected
- [ ] Desktop Schedules not yet created

### Next Session
- Fill competitor list
- Test live Social Pulse scan
- Test live Clip Mine scan
- Verify profile launches with new persona

---

## Session 3 — June 6, 2026
**Agent:** Hermes assistant
**What we did:** Pre-push audit. Fixed scoring inconsistency, updated layer skills for two pipelines, refreshed user-facing docs.

### Changes Made

| File | Change | Reason |
|------|--------|--------|
| `README.md` | Updated commands table + description | Old commands referenced single pipeline |
| `INSTRUCTIONS.md` | Updated "What You Get" + commands table | Users need to know about Social Pulse vs Clip Mine |
| `skills/trend-radar/SKILL.md` | Updated scoring table + source scan order + triggers | Scoring was inconsistent with config/scoring.yaml; no IG/TikTok priority |
| `skills/source-hunter/SKILL.md` | Updated triggers + scoring table | Added format_reusability, updated commands |
| `skills/moment-finder/SKILL.md` | Updated scoring table + category tags + template reference | Added scroll_stop, category assignment, correct template path |
| `templates/clip-brief.md` | Added deprecation note | clip-mine-brief.md is the new template; avoid confusion |
| `AGENTS.md` | Updated template references | Point to correct templates (social-pulse-report.md, clip-mine-brief.md) |

### Verification
- [x] 7/7 Python tests pass
- [x] All YAML configs structurally valid
- [x] Two pipelines documented in AGENTS.md, SOUL.md, and skill
- [x] Profile goblin-recon ready for anyone to launch

### Ready to Push
- [x] All files consistent
- [x] No broken references
- [x] User docs match actual commands

---

## Session 2 — June 7, 2026
**Agent:** Hermes assistant
**What we did:** Created pre-made SOUL.md for goblin-recon profile. Updated skill docs.

### Changes Made
| File | Change | Reason |
|------|--------|--------|
| `SOUL.md` | ✅ Created comprehensive identity file (197 lines) | New users get full GenX brand context without configuration |
| `.hermes/profiles/goblin-recon/SOUL.md` | ✅ Copied to profile | Agent now loads GenX identity on start |
| `genx-marketing/goblin-recon/SKILL.md` | 🔄 Updated profile setup section | Points to project-root SOUL.md instead of example |

### Key Decisions
- **Blacklist: referenced, not inline.** SOUL.md has the spirit (with examples) but `brand-voice.yaml` is the authoritative dictionary. Revisit if token budget becomes an issue.
- **Maintenance section included.** SOUL.md has explicit "what to edit when" guide.
- **Setup instructions in the file.** New users can copy-paste setup commands from SOUL.md itself.

### Open Items
- [ ] Test with a clean goblin-recon profile to verify onboarding flow
- [ ] If new users need the blacklist baked in (not referenced), can inline it later

---

## Session 3 — June 7, 2026
**Agent:** Hermes assistant
**What we did:** Removed machine-specific paths for portable company use. SOUL.md and SKILL.md are now portable — any user can clone the repo and run setup without editing paths.

### Changes Made
| File | Change | Reason |
|------|--------|--------|
| `SOUL.md` | Replaced local Desktop paths with relative/project-root references in Setup Instructions | New users clone anywhere — setup must work from project root |
| `SOUL.md` | Added `hermes profile create goblin-recon` step (Step 0) | New users need to create the profile before copying SOUL.md |
| `SOUL.md` | Changed "canonical version" note to say "project root" instead of a local Desktop path | Company-facing, no personal paths |
| `goblin-recon` SKILL.md | Replaced `## Project Location` block — removed local absolute path, added portable directory tree | Any clone location works |
| `goblin-recon` SKILL.md | Profile Setup step 1: `cp SOUL.md ~/.hermes/...` (relative) instead of an absolute local path | Works from any project root |
| `goblin-recon` SKILL.md | Script Usage: `cd goblin-recon` instead of a local absolute path | Portable |
| `goblin-recon` SKILL.md | Pitfalls: Tests path changed to `cd goblin-recon` (relative) | Portable |
| `.hermes/profiles/goblin-recon/SOUL.md` | Synced from project-root SOUL.md | Profile always matches canonical version |

### Key Decision
- **All paths are now relative to project root.** Users `cd` into wherever they cloned `goblin-recon/` and everything works. SOUL.md copy command runs from project root. Script commands run from project root. Tests run from project root.
- **The only absolute path that stays is `~/.hermes/profiles/goblin-recon/`** — that's Hermes' profile location, which is consistent across all macOS Hermes installs.

### Open Items
- [ ] Test setup flow from a clean machine (clone repo → profile create → SOUL.md copy → skill auto-load → verify)
- [ ] Update `references/soul-md-example.md` if it still has hardcoded paths

---

## Session 4 — June 7, 2026
**Agent:** Hermes assistant
**What we did:** Built one-command setup script. Added operational skill to project. Setup now handles full profile creation.

### Changes Made
| File | Change | Reason |
|------|--------|--------|
| `scripts/setup.sh` | ✅ Rewritten — full setup: profile, SOUL.md, skills, config, Python, verification | One command instead of 4+ manual steps |
| `skills/goblin-recon/SKILL.md` | ✅ Added to project (copied from discord-bot profile) | Project needs to be self-contained for public use |
| `skills/goblin-recon/SKILL.md` | Fixed hardcoded local path → relative | Portable for any user |
| `skills/goblin-recon/SKILL.md` | Updated pitfall: "setup.sh Only Handles Python Deps" → "setup.sh Handles Full Setup" | Reflects new reality |

### Setup Flow (New)
```bash
cd goblin-recon && bash scripts/setup.sh
```
Does everything:
1. Checks prerequisites (Hermes, Python, uv, any LLM provider)
2. Creates `goblin-recon` profile
3. Installs SOUL.md
4. Installs skills (goblin-recon + 5 pipeline + 5 cherry-picked marketing)
5. Configures auto-load and agent settings
6. Sets up Python venv and dependencies
7. Verifies installation

### Key Decisions
- **No model forced.** Uses whatever provider the user already has configured.
- **Cherry-picked skills from default profile.** Copies 5 marketing skills if they exist in the user's Hermes install. Warns but continues if missing.
- **Pipeline skills bundled.** orchestrator, trend-radar, source-hunter, moment-finder, competitor-scout ship with the project.

### Open Items
- [ ] Test on a clean machine (clone → setup.sh → verify)
- [ ] Consider adding `hermes profile create` command if supported

---

## Session 5 — June 7, 2026
**Agent:** Hermes assistant
**What we did:** Prepared the repo for company-internal distribution. Cleaned personal references, aligned one-command setup docs, and removed scratch update notes.

### Changes Made
| File | Change | Reason |
|------|--------|--------|
| `scripts/setup.sh` | Added real Hermes profile creation attempt, safer config warnings, and project-root-relative final paths | Setup should explain failures instead of hiding them |
| `README.md` / `GETTING_STARTED.md` / `INSTRUCTIONS.md` / `HERMES_APPROVALS.md` | Aligned first-time setup around `bash scripts/setup.sh` | Team members should follow one consistent onboarding flow |
| `SOUL.md` / `skills/goblin-recon/SKILL.md` | Made model/provider guidance provider-neutral | Company users can use any approved model provider |
| `skills/goblin-recon/SKILL.md` / `FILE_DESCRIPTIONS.md` | Pointed Clip Mine to `templates/clip-mine-brief.md` and marked legacy `clip-brief.md` as deprecated | Avoid deprecated template use |
| `SESSION_LOG.md` | Removed personal-name and machine-path references | Safer company handoff |
| `VSCODE_CHANGES.md` | Removed scratch update doc from tracked repo | Do not distribute personal/update scratch files |

### Verification
| Check | Result |
|------|--------|
| Secret scan | ✅ No obvious secrets found |
| Unit tests | ✅ 43/43 pytest tests passed |
| Diff whitespace check | ✅ No whitespace errors |
| Pre-flight script | ✅ 5 checks passed, 0 failed |

### Open Items
- [ ] Run a clean-machine setup test: clone → `bash scripts/setup.sh` → `hermes -p goblin-recon`
- [ ] Confirm which provider/model the team wants as the default recommendation
