# GitHub Distribution Guide

Use this guide when Goblin Recon is stored in GitHub and team members copy or clone it to their own machines.

---

## Recommended Workflow

1. Keep Goblin Recon in the company GitHub repository.
2. Commit only safe project files, docs, configs, scripts, skills, and templates.
3. Do not commit local environments, API keys, outputs, logs, or private briefs.
4. Each team member clones the repo locally.
5. Each team member creates their own Hermes profile.
6. Each team member adds approved API keys locally using `.env` or Hermes secrets.
7. Each team member runs Goblin Recon from their own machine or approved company environment.

---

## What Should Be Committed

Commit these:

- `AGENTS.md`
- `README.md`
- `INSTRUCTIONS.md`
- `SECURITY.md`
- `API_KEYS.md`
- `SOCIAL_API_SETUP.md`
- `LEGAL_GUARDRAILS.md`
- `PRE_LAUNCH_CHECKLIST.md`
- `GITHUB_DISTRIBUTION.md`
- `config/*.yaml`
- `skills/**/SKILL.md`
- `scripts/*.py`
- `scripts/setup.sh`
- `templates/*.md`
- `memory/*.md` if they contain only placeholders or approved non-sensitive history
- `requirements.txt`
- `pyproject.toml`
- `.env.example`
- `.gitignore`
- `tests/*.py`
- `vault/**/.gitkeep`

---

## What Must Not Be Committed

Never commit these:

- `.env`
- `.env.*` except `.env.example`
- `.venv/`
- API keys
- Access tokens
- Cookies
- Browser sessions
- Hermes private session data
- Personal account credentials
- Downloaded videos
- Raw unpublished content briefs unless approved
- Logs containing private data
- Screenshots showing keys or private dashboards

The `.gitignore` file already blocks the most common unsafe files, but the team should still run the secret scanner before pushing.

---

## Owner Setup Before Publishing to GitHub

Run these from inside `goblin-recon`:

```bash
python3 scripts/check_secrets.py
```

Expected result:

```text
No obvious secrets found.
```

Then verify local tests:

```bash
source .venv/bin/activate
python3 -m unittest discover -s tests
```

Expected result:

```text
OK
```

Only push after both checks pass.

---

## Team Member Setup After Cloning

Each team member should run:

```bash
git clone <company-github-repo-url>
cd goblin-recon
bash scripts/setup.sh
source .venv/bin/activate
python3 scripts/check_secrets.py
```

Then create their own Hermes profile:

```bash
hermes profile create goblin-recon
hermes -p goblin-recon
```

If the company uses a different model/provider, follow the team lead's Hermes setup instructions.

---

## API Keys for Team Members

Team members should not receive API keys through GitHub.

Use one of these methods:

1. Hermes profile secrets, if available.
2. Local `.env` file copied from `.env.example`.
3. Company secret manager for shared/scheduled deployment.

Simple local `.env` setup:

```bash
cp .env.example .env
```

Then the team member adds only approved keys to `.env`.

Do not commit `.env`.

---

## Enabling Social APIs

Social APIs are disabled by default in `config/integrations.yaml`.

To enable one:

1. Get company/admin approval.
2. Add the approved key locally through `.env` or Hermes secrets.
3. Change only that integration to `enabled: true`.
4. Run a low-risk read-only test.
5. Keep human review before publishing.

Do not enable every API at once.

---

## Recommended GitHub Repository Settings

For business use, enable these in GitHub:

- Private repository unless the company explicitly wants public release.
- Branch protection on `main`.
- Pull requests required before merging.
- Secret scanning enabled.
- Dependabot enabled for dependency alerts.
- Code owners or required reviewer for security files.
- No direct commits to `main` by marketing users.

---

## Suggested Repository Layout

If Goblin Bureau contains multiple tools:

```text
goblin-bureau/
├── goblin-recon/
├── other-goblin-tool/
└── README.md
```

If Goblin Recon is its own repository:

```text
goblin-recon/
├── AGENTS.md
├── README.md
├── config/
├── scripts/
├── skills/
└── templates/
```

Both are fine. For multiple internal agents, `goblin-bureau/goblin-recon` is cleaner.

---

## Copy vs Clone

Prefer cloning:

```bash
git clone <company-github-repo-url>
```

Cloning is better because team members can pull updates later:

```bash
git pull
```

Copying a ZIP is okay for non-technical users, but they will not receive updates automatically.

---

## Update Workflow

When the owner updates Goblin Recon:

1. Make changes locally.
2. Run tests.
3. Run secret scan.
4. Push to GitHub.
5. Tell team members to run:

```bash
git pull
bash scripts/setup.sh
```

They should keep their own `.env` file. Git will not overwrite it.

---

## Quick Team Instructions

Send this to the team:

```text
1. Clone the Goblin Recon repo.
2. Run: bash scripts/setup.sh
3. Run: source .venv/bin/activate
4. Run: python3 scripts/check_secrets.py
5. Create your Hermes profile: hermes profile create goblin-recon
6. Launch: hermes -p goblin-recon
7. Read HERMES_APPROVALS.md before approving tool permissions.
8. Type: run full scan

Do not paste API keys into chat. Use .env or Hermes secrets only.
```
