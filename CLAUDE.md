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

- **JSON-LD schema on homepage** — LocalBusiness + DrivingSchool + WebSite structured data added (`priority 8/10` checklist item ticked in both Quick Wins and Technical SEO sections)
- **Keyword-optimised URL structure** — all 15 location pages and service pages use exact-match keyword slugs e.g. `/driving-lessons-richmond`, `/automatic-driving-lessons` (`priority 8/10` Technical SEO item ticked)
- **FAQ page published** — `/faq` exists on idrive-auto.co.uk (`priority 10/10` Content item ticked)
- **15 dedicated location pages built** — `/driving-lessons-richmond`, `/driving-lessons-twickenham`, `/driving-lessons-hounslow`, `/driving-lessons-barnes`, `/driving-lessons-chiswick`, `/driving-lessons-kew`, `/driving-lessons-surbiton`, `/driving-lessons-teddington`, `/driving-lessons-isleworth`, `/driving-lessons-hampton`, `/driving-lessons-roehampton`, `/driving-lessons-sheen`, `/driving-lessons-whitton`, `/driving-lessons-east-molesey`, `/driving-lessons-kingston` (`priority 7/10` Content item ticked)
- **Service category pages built** — `/automatic-driving-lessons`, `/intensive-driving-lessons`, `/pass-plus`
- **Supporting pages built** — `/booking`, `/contact`, `/resources`, `/terms`
- **Metadata on all pages** — title, meta description, OpenGraph, Twitter Card tags added to every page
- **sitemap.xml and robots.txt** — both generated and live at idrive-auto.co.uk
- **Website deployed to Vercel** — project `idrive-auto`, production deployment `dpl_C9BdTunjTzZrYcY8ZhnAhpduEwv5`, aliased to `www.idrive-auto.co.uk`

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

### 2026-06-09
- Image alt text: updated 5 alt attributes across Nav.tsx, Footer.tsx, PassesCarousel.tsx, PassGrid.tsx
  - Logos: "iDrive Auto" → "iDrive Auto School of Motoring logo"
  - Pass photos: generic numbering → "iDrive Auto student driving test pass ${n}"
  - Committed f3fc2a5, pushed to GitHub
- Internal links: nearbyAreas already built and rendering in LocationPage.tsx — no code needed
  - Fixed 6 broken nearbyAreas links (Sunbury, Brentford x4, Putney → real area slugs)
  - Committed 905ffe2, pushed to GitHub
- Google Maps embed: already present in MapEmbed.tsx, used on homepage and all 15 location pages — no code needed

### 2026-06-09 (session 2)
- Google Search Console: sitemap already submitted (Apr 6), showing Success, 24 pages discovered
- Fixed www vs non-www redirect issue in Vercel:
  - idrive-auto.co.uk set as Production (was redirecting to www)
  - www.idrive-auto.co.uk set to 301 redirect to idrive-auto.co.uk
- Updated Hostinger DNS records to Vercel's new IP range:
  - A record @ updated from 76.76.21.21 → 216.198.79.1
  - CNAME www updated from cname.vercel-dns.com → 02f8b283b5f88ba0.vercel-dns-017.com
- ALIAS record @ was already set to 02f8b283b5f88ba0.vercel-dns-017.com

### 2026-06-10
- NAP consistency fixes in Footer.tsx:
  - Phone number display text: "07867 866 868" → "07867 866868" (matches tel: href format)
  - Removed Brentford from Areas Covered list (no location page exists for it)
  - Build: 31 pages, zero errors
  - Committed dcf2cca, pushed to main
- GBP audit completed:
  - Business description updated — keyword-rich, 748 chars, all service areas mentioned
  - Services expanded from 7 to 20+ including all 15 location-specific services
  - Logo (square steering wheel PNG) and cover photo uploaded — pending verification
  - Phone number NAP mismatch fixed — site footer updated from "07867 866 868" → "07867 866868"
  - Brentford removed from footer Areas Covered list (no location page exists)
  - Opening hours confirmed on GBP — added matching openingHoursSpecification to homepage JSON-LD schema
  - GBP verification pending — video verification required (client to record tomorrow)
  - Social profiles not yet added to GBP — need Instagram/Facebook URLs from client
- Phone number CTA added to all 15 location pages — "Call us on 07867 866868" after bullets in Section 2
- Areas We Cover page created at /areas-we-cover — 15 location cards, linked from footer
- /areas-we-cover added to sitemap.ts
- GOV.UK outbound link added to all 15 location pages — "Book your practical driving test on GOV.UK" linking to gov.uk/book-driving-test, sits between FAQ and nearby areas sections
- Resources page already had 7 authoritative GOV.UK/DVSA outbound links — no changes needed
- Google Analytics 4: already installed — measurement ID G-BS0R29LHFV, loaded via Next.js Script in layout.tsx with afterInteractive strategy (added in a previous session)
- GA4 linked to Search Console — keyword and landing page data now available in GA4
- Search Console baseline metrics (3 month view, last updated 2026-06-10):
  - Total clicks: 19
  - Total impressions: 1,580
  - Average CTR: 1.2%
  - Average position: 51.6
  - Top queries by impressions: molesey driving lessons (54), driving lessons richmond (51), driving lessons hampton (47), driving lessons twickenham (43), driving lessons surbiton (36), driving lessons hounslow (34), driving lessons hampton hill (33), driving lessons isleworth (29)
  - Only branded queries converting to clicks — position improvements expected as site gains authority and GBP gets verified
  - 175 total queries indexed — keyword targeting working, authority is the limiting factor
  - Next check: week of 2026-06-17 — look for any queries moving from position 40–60 into 10–20
