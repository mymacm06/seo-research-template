# CLAUDE.md — driving school / driving instructor SEO Research Tool

## What This Project Does
Fetches YouTube transcripts from top SEO educators, synthesises them via the Claude API, and produces a prioritised SEO checklist tailored to idrive-auto.co.uk.

---

## Setup — Fill In These Placeholders Before Starting

Search and replace the following in this file **and** in `scripts/generate_checklist.py`:

| Placeholder | What to replace it with |
|---|---|
| `[SITE_URL]` | Your website URL e.g. `example.co.uk` |
| `[BUSINESS_NAME]` | Your business name e.g. `Acme Plumbing` |
| `[NICHE]` | Your business type e.g. `plumber` or `driving instructor` |
| `[LOCATION]` | Your primary location e.g. `Manchester` |
| `[TARGET_AREAS]` | Comma-separated areas you serve e.g. `Manchester, Salford, Stockport` |
| `[TECH_STACK]` | Your site's tech stack e.g. `WordPress`, `Next.js`, `Shopify` |

---

## Critical Rules

1. Read this file once at session start. Do not re-read mid-session.
2. Never overwrite this file. Append session notes at the bottom only.
3. One task at a time. Never combine tasks in a single prompt.
4. Never install packages without asking first.
5. Never delete or rename files without explicit permission.
6. After every completed task, do a git commit with a clear message.
7. Always check files exist before creating new ones.
8. If anything is unclear, ask before starting.
9. No code before the user approves the plan.

---

## How to Respond

Plain English always. Every response must include:
- **What I just did**
- **What you need to do** (step by step)
- **Why** (one sentence)
- **Next step** (one clear action)

Be concise. Do not ramble.

---

## Skills

Before taking any action, check whether a skill applies. If it does, load and follow it exactly.

| Situation | Skill to load |
|---|---|
| User wants to fetch transcripts from YouTube | `skills/fetch_transcripts/SKILL.md` |
| User wants to run synthesis / extract SEO tips | `skills/synthesise/SKILL.md` |
| User wants to generate or update the checklist | `skills/generate_checklist/SKILL.md` |
| User wants to add new YouTube videos | `skills/add_videos/SKILL.md` |
| Something is broken or a script is failing | `skills/debug_pipeline/SKILL.md` |

Load the skill file. Follow it exactly. Do not improvise.

---

## About the Target Site

- **URL:** idrive-auto.co.uk
- **Business:** iDrive Auto School of Motoring — driving school / driving instructor
- **Primary location:** London, UK
- **Service areas:** Richmond, Twickenham, Barnes, Teddington, Surbiton, Brentford, Isleworth, Whitton, Hounslow, Hampton, Roehampton, Kew, Sheen, East Molesey, Chiswick
- **Tech stack:** Next.js 15, Tailwind CSS v3, Vercel
- **Goal:** Rank for "driving school London, UK" and related local queries

## SEO Already Done
_(Fill this in as you work through the checklist)_

## SEO Gaps to Fix
_(Fill this in after reviewing the generated checklist)_

---

## Folder Structure

```
seo-research-template/
├── CLAUDE.md
├── requirements.txt
├── .env                        # ANTHROPIC_API_KEY — never commit
├── transcripts/                # Raw .txt transcript files
├── outputs/
│   ├── raw_synthesis.md
│   └── seo_checklist.md
├── scripts/
│   ├── fetch_transcripts.py
│   ├── synthesise.py
│   └── generate_checklist.py
└── skills/
    ├── fetch_transcripts/SKILL.md
    ├── synthesise/SKILL.md
    ├── generate_checklist/SKILL.md
    ├── add_videos/SKILL.md
    └── debug_pipeline/SKILL.md
```

---

## Tech Notes

- Python 3.9 — use `Optional[str]` not `str | None`
- Use `python3` and `pip3`, not `python` or `pip`
- Transcript tool: `youtube-transcript-api` v1.2.4
  - Use `api = YouTubeTranscriptApi(); api.fetch(video_id)` — no class method
- Claude API model: `claude-sonnet-4-6`
- Do NOT use `yt-dlp` for subtitles — blocked by YouTube PO token requirement
- `generate_checklist.py` writes a preview file first, then renames on approval

---

## Session Notes

_(Append notes here after each session. Never delete previous entries.)_

### 2026-04-05
- Cloned seo-research-template into `/Users/sb/idrive-auto/idrive-seo/` alongside the website folder
- Filled in constants in `scripts/generate_checklist.py`: SITE_URL, BUSINESS_NAME, NICHE, LOCATION, TARGET_AREAS (TECH_STACK not a constant in that file; PRIMARY_KEYWORDS left as placeholder)
- Updated all placeholders in `CLAUDE.md` with iDrive Auto details
- Fixed `.env` format issue (missing `=` sign) so python-dotenv could parse ANTHROPIC_API_KEY
- Ran `generate_checklist.py` — loaded 156 tips from `outputs/raw_synthesis.md`, rewrote all 8 batches as site-specific actions, generated `outputs/seo_checklist.md`
- Committed 3 files: `CLAUDE.md`, `scripts/generate_checklist.py`, `outputs/seo_checklist.md` (commit c7dbe09)
- `.env` not committed — keep it off GitHub
