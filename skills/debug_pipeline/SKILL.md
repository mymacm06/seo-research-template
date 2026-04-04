# Skill: debug-pipeline

## When This Skill Activates
- A script throws an error
- A transcript fails to download
- The Claude API call fails
- The checklist is empty or malformed
- User says "it's broken", "something failed", or "I'm getting an error"

---

## What This Skill Does
Walks through a systematic process to identify and fix the problem without guessing.

---

## Step 1 — Get the Full Error

Ask the user to share the full error message if they haven't already.
Look for:
- The exact line that failed
- The exception type (e.g. `TranscriptsDisabled`, `AuthenticationError`, `JSONDecodeError`)
- Which script was running

---

## Step 2 — Check the Most Common Causes

Work through this list in order. Stop at the first match.

### Transcript fetch failures
| Symptom | Likely cause | Fix |
|---|---|---|
| `TranscriptsDisabled` | Video has no captions | Skip this video |
| `VideoUnavailable` | Video is private or deleted | Remove URL from list |
| `NoTranscriptFound` | No English transcript | Try `languages=['en', 'en-GB']` |
| `get_transcript` not found | Wrong API version | Use `api = YouTubeTranscriptApi(); api.fetch(video_id)` |
| Import error | Package not installed | `pip3 install youtube-transcript-api` |

### Claude API failures
| Symptom | Likely cause | Fix |
|---|---|---|
| `AuthenticationError` | API key missing or wrong | Check `echo $ANTHROPIC_API_KEY` |
| `RateLimitError` | Too many requests | Add `time.sleep(2)` between calls |
| `JSONDecodeError` | Model returned non-JSON | Add JSON extraction with fallback |
| Empty `raw_synthesis.md` | Script exited early | Check for silent exceptions in the loop |

### Checklist failures
| Symptom | Likely cause | Fix |
|---|---|---|
| Empty checklist | `raw_synthesis.md` is empty | Re-run synthesis first |
| Preview file not renamed | `input()` blocking | Script should use preview/rename pattern, not `input()` |
| Placeholder warning on startup | Site config not filled in | Edit the constants at the top of `generate_checklist.py` |
| Jargon or non-specific output | Prompt too generic | Tighten the system prompt to reference your specific site |

---

## Step 3 — Apply the Fix

- Show the user exactly what line to change and what to change it to
- Do not rewrite the whole script unless necessary
- Test the fix on one item before re-running the full pipeline

---

## Step 4 — Confirm Fixed

- Run the failing step again
- Show the user the output confirming it worked
- Git commit the fix:
  ```bash
  git commit -m "fix: [short description of what was broken and how it was fixed]"
  ```

---

## Rules

- Never guess — always read the actual error before suggesting a fix
- Never rewrite a whole script to fix a small bug
- If the cause is unclear after checking the list above, ask the user for more info
- Python 3.9 is the system version — use `Optional[str]` not `str | None`
- Always use `python3` and `pip3`, never `python` or `pip`
