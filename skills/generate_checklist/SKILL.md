# Skill: generate-checklist

## When This Skill Activates
- User wants to generate or regenerate the SEO checklist
- User says "generate checklist", "run stage 3", "make the checklist", or "update the checklist"
- `outputs/raw_synthesis.md` has been updated with new tips

---

## What This Skill Does
Takes `outputs/raw_synthesis.md` and produces a final, plain-English, site-specific SEO checklist for [SITE_URL], saved to `outputs/seo_checklist.md`.

---

## Pre-flight Checks

Before running anything:

- [ ] `outputs/raw_synthesis.md` exists and has content
- [ ] `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
- [ ] The site config constants at the top of `scripts/generate_checklist.py` have been filled in (no `[PLACEHOLDER]` values remain)
- [ ] If `outputs/seo_checklist.md` already exists — warn the user and ask if they want to regenerate it

---

## Steps

1. **Show the user** the current state: how many tips are in `raw_synthesis.md`, whether a checklist already exists
2. **Wait for confirmation** before running
3. **Run the script:**
   ```bash
   python3 scripts/generate_checklist.py
   ```
   This writes a preview file first (`seo_checklist_preview.md`), then renames it on approval.
4. **Show the user a summary** of the checklist:
   - Total number of action items
   - Number of "quick wins" (under 1 hour)
   - Themes covered
5. **Ask the user to review** `outputs/seo_checklist_preview.md` before it is saved as final
6. **On approval**, confirm the file has been renamed to `seo_checklist.md`
7. **Git commit:**
   ```bash
   git add outputs/seo_checklist.md
   git commit -m "feat: generate SEO checklist — [N] actions, [N] quick wins"
   ```

---

## Checklist Requirements

The output file must:
- Be written in plain English — no jargon without explanation
- Be actionable — every item says exactly what to do
- Be specific to the target site (e.g. "Add LocalBusiness schema with your [LOCATION] address")
- Group items by theme: `[technical]` `[content]` `[backlinks]` `[local]` `[ux]`
- Include a **Quick Wins** section at the top (tasks under 1 hour)
- Show a priority score for each item

---

## Rules

- Never overwrite `seo_checklist.md` directly — always write preview first
- Model to use: `claude-sonnet-4-6`
- Never hardcode API key
- If the script uses `input()` to wait for approval, it will block — use the preview/rename pattern instead

---

## Done When

- `outputs/seo_checklist.md` exists and is approved by user
- Git commit made
- User knows the checklist is ready to act on
