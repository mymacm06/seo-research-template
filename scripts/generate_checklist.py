#!/usr/bin/env python3
"""
generate_checklist.py
Reads aggregated tips from /outputs/raw_synthesis.md, rewrites each tip as a
specific action for your site using Claude, then writes a prioritised
/outputs/seo_checklist.md grouped by theme.

Requires: ANTHROPIC_API_KEY in environment or .env file
"""

import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

OUTPUTS_DIR    = Path(__file__).parent.parent / "outputs"
RAW_SYNTHESIS  = OUTPUTS_DIR / "raw_synthesis.md"
CHECKLIST_FILE = OUTPUTS_DIR / "seo_checklist.md"
PREVIEW_FILE   = OUTPUTS_DIR / "seo_checklist_preview.md"

MODEL      = "claude-sonnet-4-6"
MAX_TOKENS = 8096

# ---------------------------------------------------------------
# CONFIGURE FOR YOUR SITE — fill in these values before running
# ---------------------------------------------------------------
SITE_URL        = "[SITE_URL]"           # e.g. "example.co.uk"
BUSINESS_NAME   = "[BUSINESS_NAME]"      # e.g. "Acme Plumbing"
NICHE           = "[NICHE]"              # e.g. "plumber"
LOCATION        = "[LOCATION]"           # e.g. "Manchester"
TARGET_AREAS    = "[TARGET_AREAS]"       # e.g. "Manchester, Salford, Stockport"
PRIMARY_KEYWORDS = "[PRIMARY_KEYWORDS]"  # e.g. '"plumber Manchester", "emergency plumber Manchester"'
# ---------------------------------------------------------------

SITE_CONTEXT = f"""
Site: {SITE_URL}
Business: {BUSINESS_NAME} — {NICHE}
Primary location: {LOCATION}
Service areas: {TARGET_AREAS}
Main keywords to rank for: {PRIMARY_KEYWORDS}
""".strip()

REWRITE_SYSTEM = f"""You are an SEO consultant working on a specific website.

{SITE_CONTEXT}

You will receive a JSON array of generic SEO tips. For each tip, rewrite the recommendation as a concrete, specific action for THIS site.

Rules:
- Name specific pages, real keywords, or real locations where relevant
- Do NOT say "add schema" — say "add LocalBusiness schema to your homepage with your {LOCATION} address and phone number"
- Do NOT say "write blog content" — say 'write a blog post titled "How to find a {NICHE} in {LOCATION}"'
- Keep each recommendation to 1–2 sentences
- Add a field "quick_win": true if the task can realistically be done in under 1 hour, false otherwise
- Keep all other fields (theme, importance, frequency) exactly as provided
- Return a JSON array only, no other text
"""


def load_tips_from_synthesis() -> list[dict]:
    """Extract the JSON data block from raw_synthesis.md."""
    text = RAW_SYNTHESIS.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
    if not match:
        print("ERROR: could not find JSON block in raw_synthesis.md")
        sys.exit(1)
    return json.loads(match.group(1))


def rewrite_tips_in_batches(client: anthropic.Anthropic, tips: list[dict]) -> list[dict]:
    """Send tips to Claude in batches of 20 for site-specific rewriting."""
    batch_size = 20
    rewritten = []

    for i in range(0, len(tips), batch_size):
        batch = tips[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tips) + batch_size - 1) // batch_size
        print(f"  Rewriting batch {batch_num}/{total_batches} ({len(batch)} tips) ...")

        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=REWRITE_SYSTEM,
                messages=[
                    {
                        "role": "user",
                        "content": json.dumps(batch, indent=2)
                    }
                ]
            )
            raw = message.content[0].text.strip()

            # Strip markdown code fences if present
            if raw.startswith("```"):
                raw = "\n".join(raw.splitlines()[1:])
            if raw.endswith("```"):
                raw = "\n".join(raw.splitlines()[:-1])

            batch_result = json.loads(raw)
            if isinstance(batch_result, list):
                rewritten.extend(batch_result)
            else:
                print(f"  WARNING: unexpected format in batch {batch_num}, using originals")
                rewritten.extend(batch)

        except (json.JSONDecodeError, anthropic.APIError) as e:
            print(f"  ERROR in batch {batch_num}: {e} — using originals")
            rewritten.extend(batch)

        time.sleep(1)

    return rewritten


THEME_ORDER = ["technical", "content", "backlinks", "local", "ux"]
THEME_LABELS = {
    "technical": "Technical SEO",
    "content":   "Content",
    "backlinks": "Backlinks",
    "local":     "Local SEO",
    "ux":        "UX",
}


def build_checklist(tips: list[dict]) -> str:
    """Format the final markdown checklist."""
    # Sort all tips: frequency desc, then importance desc
    tips = sorted(tips, key=lambda t: (-t.get("frequency", 1), -t.get("importance", 5)))

    # Separate quick wins
    quick_wins = [t for t in tips if t.get("quick_win")]
    the_rest   = [t for t in tips if not t.get("quick_win")]

    lines = []
    lines.append(f"# SEO Checklist — {SITE_URL}\n")
    lines.append(
        "_Generated from YouTube transcripts by SEO research tool. "
        "Tips sorted by frequency (how many sources mentioned it) then importance._\n"
    )
    lines.append(f"\n**{len(tips)} total actions** across {len(THEME_ORDER)} themes\n")

    # --- Quick wins ---
    lines.append("\n---\n")
    lines.append("## Quick Wins (under 1 hour)\n")
    if quick_wins:
        for tip in quick_wins:
            freq  = tip.get("frequency", 1)
            imp   = tip.get("importance", 5)
            theme = tip.get("theme", "").strip("[]")
            rec   = tip.get("recommendation", "")
            lines.append(f"- [ ] **[{theme}]** `priority {imp}/10` _(mentioned in {freq} source{'s' if freq != 1 else ''})_  \n")
            lines.append(f"  {rec}\n")
    else:
        lines.append("_No quick wins identified._\n")

    # --- Per-theme sections ---
    lines.append("\n---\n")

    # Group tips by theme
    grouped: dict[str, list[dict]] = {t: [] for t in THEME_ORDER}
    other = []
    for tip in tips:
        theme = tip.get("theme", "").strip("[]").lower()
        if theme in grouped:
            grouped[theme].append(tip)
        else:
            other.append(tip)

    for theme_key in THEME_ORDER:
        theme_tips = grouped[theme_key]
        label = THEME_LABELS[theme_key]
        lines.append(f"\n## {label}  ({len(theme_tips)} actions)\n")

        if not theme_tips:
            lines.append("_No tips in this category._\n")
            continue

        for tip in theme_tips:
            freq     = tip.get("frequency", 1)
            imp      = tip.get("importance", 5)
            rec      = tip.get("recommendation", "")
            is_quick = " (quick win)" if tip.get("quick_win") else ""
            lines.append(
                f"- [ ] `priority {imp}/10`{is_quick} _(mentioned in {freq} source{'s' if freq != 1 else ''})_  \n"
            )
            lines.append(f"  {rec}\n")

    if other:
        lines.append("\n## Other\n")
        for tip in other:
            freq = tip.get("frequency", 1)
            imp  = tip.get("importance", 5)
            rec  = tip.get("recommendation", "")
            lines.append(f"- [ ] `priority {imp}/10` _(mentioned in {freq} source{'s' if freq != 1 else ''})_  \n")
            lines.append(f"  {rec}\n")

    return "".join(lines)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    if not RAW_SYNTHESIS.exists():
        print(f"ERROR: {RAW_SYNTHESIS} not found. Run synthesise.py first.")
        sys.exit(1)

    # Warn if placeholders haven't been filled in
    if "[SITE_URL]" in SITE_URL:
        print("WARNING: Site config placeholders not filled in. Edit the constants at the top of this script first.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Loading tips from {RAW_SYNTHESIS.name} ...")
    tips = load_tips_from_synthesis()
    print(f"  {len(tips)} tips loaded\n")

    print(f"Rewriting tips as site-specific actions for {SITE_URL} ...")
    rewritten = rewrite_tips_in_batches(client, tips)
    print(f"  {len(rewritten)} tips rewritten\n")

    print("Building checklist ...\n")
    checklist = build_checklist(rewritten)

    # Always save to preview file first
    PREVIEW_FILE.write_text(checklist, encoding="utf-8")

    # Print first 80 lines as preview
    preview_lines = checklist.splitlines()[:80]
    print("=" * 60)
    print("PREVIEW (first 80 lines)")
    print("=" * 60)
    print("\n".join(preview_lines))
    print(f"\n... ({len(checklist.splitlines())} total lines)")
    print("=" * 60)
    print(f"\nFull preview saved to: {PREVIEW_FILE}")
    print("Run: mv outputs/seo_checklist_preview.md outputs/seo_checklist.md  to finalise.")


if __name__ == "__main__":
    main()
