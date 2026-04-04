# Skill: fetch-transcripts

## When This Skill Activates
- User wants to download transcripts from YouTube
- User provides new YouTube URLs to process
- User says "fetch", "download transcripts", or "run stage 1"

---

## What This Skill Does
Downloads transcripts from YouTube videos using `youtube-transcript-api` and saves them as clean `.txt` files in the `/transcripts` folder.

---

## Pre-flight Checks

Before running anything:

- [ ] Confirm the user has provided YouTube URLs (or check `scripts/fetch_transcripts.py` for the existing URL list)
- [ ] Check `/transcripts/` to see which videos have already been fetched — do not re-fetch
- [ ] Confirm `youtube-transcript-api` is installed: `pip3 show youtube-transcript-api`
- [ ] Confirm `.env` exists with `ANTHROPIC_API_KEY` (not needed for this stage but good habit)

---

## Steps

1. **Show the user the URLs to be fetched** and which transcripts already exist in `/transcripts/`
2. **Wait for confirmation** before running
3. **Run the script:**
   ```bash
   python3 scripts/fetch_transcripts.py
   ```
4. **Report results:**
   - How many transcripts were fetched successfully
   - Which (if any) failed and why
   - Full list of files now in `/transcripts/`
5. **Git commit:**
   ```bash
   git add transcripts/
   git commit -m "feat: fetch transcripts from [N] YouTube videos"
   ```

---

## Rules

- NEVER use `yt-dlp` for transcript downloads — it is blocked by YouTube's PO token requirement
- NEVER overwrite an existing transcript file without asking
- If a video has no transcript available, skip it and note it — do not block progress
- Name files clearly: e.g. `seo-topic-slug.txt`

---

## API Notes

`youtube-transcript-api` v1.2.4:
```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch(video_id)  # NOT get_transcript()
```

---

## Done When

- All available transcripts are saved as `.txt` files in `/transcripts/`
- Failed videos are noted
- Git commit made
- User told the next step is to run the `synthesise` skill
