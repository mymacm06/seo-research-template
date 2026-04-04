# Skill: add-videos

## When This Skill Activates
- User wants to add new YouTube videos to the research
- User pastes new YouTube URLs
- User says "add these videos", "process more videos", or "add to the pipeline"

---

## What This Skill Does
Adds new YouTube URLs to the pipeline, fetches their transcripts, re-runs synthesis to merge new tips, and regenerates the checklist.

---

## Pre-flight Checks

Before running anything:

- [ ] User has provided at least one new YouTube URL
- [ ] Check `/transcripts/` — confirm the videos haven't already been fetched
- [ ] `ANTHROPIC_API_KEY` is set
- [ ] Confirm the user wants to regenerate the full checklist after adding (not just the transcripts)

---

## Steps

1. **List the new URLs** the user has provided
2. **Check for duplicates** — show any that are already in the transcripts folder
3. **Add the new URLs** to `scripts/fetch_transcripts.py`
4. **Show the plan:**
   - N new videos to fetch
   - Will re-run synthesis to merge new tips
   - Will regenerate checklist
5. **Wait for confirmation**
6. **Fetch new transcripts:**
   ```bash
   python3 scripts/fetch_transcripts.py
   ```
7. **Re-run synthesis** (load and follow `skills/synthesise/SKILL.md`)
8. **Regenerate checklist** (load and follow `skills/generate_checklist/SKILL.md`)
9. **Git commit:**
   ```bash
   git add transcripts/ outputs/
   git commit -m "feat: add [N] new videos — re-synthesised and updated checklist"
   ```

---

## Rules

- Never re-fetch a transcript that already exists in `/transcripts/`
- Always re-run synthesis after adding videos — never just append transcripts without updating `raw_synthesis.md`
- Always regenerate the checklist after synthesis — keep the outputs in sync

---

## Done When

- New transcripts saved in `/transcripts/`
- `outputs/raw_synthesis.md` updated with new tips merged in
- `outputs/seo_checklist.md` regenerated and approved
- Git commit made
