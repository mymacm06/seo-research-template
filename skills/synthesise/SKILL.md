# Skill: synthesise

## When This Skill Activates
- User wants to extract SEO tips from transcripts
- User says "synthesise", "run synthesis", "run stage 2", or "extract tips"
- New transcripts have been added and need processing

---

## What This Skill Does
Sends each transcript to the Claude API (`claude-sonnet-4-6`), extracts structured SEO tips as JSON, aggregates them, deduplicates, scores by frequency, and saves to `outputs/raw_synthesis.md`.

---

## Pre-flight Checks

Before running anything:

- [ ] At least one `.txt` file exists in `/transcripts/`
- [ ] `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
- [ ] `anthropic` Python package is installed: `pip3 show anthropic`
- [ ] Check if `outputs/raw_synthesis.md` already exists — ask user if they want to overwrite or append

---

## Steps

1. **Show the user** how many transcripts will be processed and the current state of `outputs/raw_synthesis.md`
2. **Wait for confirmation** before running
3. **Run the script:**
   ```bash
   python3 scripts/synthesise.py
   ```
4. **Report results:**
   - How many transcripts were processed
   - How many tips were extracted in total
   - Top 5 most frequent tips (by frequency score)
   - Any transcripts that failed
5. **Git commit:**
   ```bash
   git add outputs/raw_synthesis.md
   git commit -m "feat: synthesise [N] transcripts → [N] SEO tips extracted"
   ```

---

## Output Format

Each extracted tip must include:
```json
{
  "recommendation": "...",
  "theme": "technical | content | backlinks | local | ux",
  "importance": 1-10,
  "frequency": 1-10
}
```

Tips are aggregated across all transcripts, deduplicated, and sorted by frequency (highest first), then by importance.

---

## Rules

- Model to use: `claude-sonnet-4-6`
- Never hardcode the API key — always read from environment variable
- If a transcript is too long for one API call, chunk it and merge results
- If the API call fails for a transcript, skip and note it — do not block progress
- Always append to `raw_synthesis.md`, never silently overwrite

---

## Done When

- `outputs/raw_synthesis.md` contains all extracted tips
- Tips are grouped by theme and sorted by frequency
- Git commit made
- User told the next step is to run the `generate-checklist` skill
