#!/usr/bin/env python3
"""
fetch_transcripts.py
Downloads transcripts from a manually specified list of YouTube URLs
using youtube-transcript-api. Cleans and saves to /transcripts/.

Usage:
  python3 scripts/fetch_transcripts.py
"""

import re
import sys
import warnings
from pathlib import Path
from typing import Optional

# Suppress urllib3/LibreSSL warning on macOS Python 3.9
warnings.filterwarnings("ignore")

from youtube_transcript_api import YouTubeTranscriptApi

TRANSCRIPTS_DIR = Path(__file__).parent.parent / "transcripts"
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# Add your YouTube URLs here before running.
# Each entry: ("youtube_url_or_video_id", "output-slug")
# The slug becomes the filename: transcripts/<slug>.txt
# ---------------------------------------------------------------
VIDEOS = [
    # ("https://www.youtube.com/watch?v=XXXXXXXXXXX", "seo-topic-name"),
]
# ---------------------------------------------------------------


def extract_video_id(url: str) -> str:
    """Extract the 11-character video ID from a YouTube URL or return as-is."""
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else url


def fetch_transcript(video_id: str) -> Optional[str]:
    """Fetch and clean transcript text for a given video ID."""
    api = YouTubeTranscriptApi()
    try:
        snippets = api.fetch(video_id)
    except Exception:
        # Try fetching any available language
        try:
            transcript_list = api.list(video_id)
            first = next(iter(transcript_list))
            snippets = first.fetch()
        except Exception:
            return None

    lines = [snippet.text.strip() for snippet in snippets if snippet.text.strip()]

    # Deduplicate consecutive identical lines
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    # Strip any residual HTML tags (e.g. <i>, </i>)
    text = " ".join(deduped)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def main():
    if not VIDEOS:
        print("ERROR: No videos configured. Add YouTube URLs to the VIDEOS list in this script.")
        sys.exit(1)

    saved = []
    failed = []

    for url, slug in VIDEOS:
        out_file = TRANSCRIPTS_DIR / f"{slug}.txt"

        if out_file.exists():
            print(f"[SKIP] {slug}.txt already exists")
            saved.append((slug, str(out_file), "cached"))
            continue

        video_id = extract_video_id(url)
        print(f"\n[FETCH] {slug}  (id: {video_id})")

        text = fetch_transcript(video_id)
        if text:
            out_file.write_text(text, encoding="utf-8")
            size = out_file.stat().st_size
            print(f"  SAVED: {out_file}  ({size:,} bytes)")
            saved.append((slug, str(out_file), f"{size:,} bytes"))
        else:
            print(f"  ERROR: no transcript available")
            failed.append((slug, f"no transcript — {url}"))

    # Summary
    print("\n" + "=" * 60)
    print(f"SUMMARY — {len(saved)} saved, {len(failed)} failed")
    print("=" * 60)
    if saved:
        print("\nSaved:")
        for slug, path, note in saved:
            print(f"  ✓  {slug}.txt  ({note})")
    if failed:
        print("\nFailed:")
        for slug, reason in failed:
            print(f"  ✗  {slug}  — {reason}")


if __name__ == "__main__":
    main()
