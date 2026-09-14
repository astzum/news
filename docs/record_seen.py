#!/usr/bin/env python3
"""Record every URL in a digest to seen.json, then prune entries older than 21 days.

Usage: python3 docs/record_seen.py docs/digests/2026-09-14.md
"""
import datetime
import json
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).parent
LEDGER = DOCS / "seen.json"
WINDOW_DAYS = 21


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: record_seen.py <digest.md>")
    digest = pathlib.Path(sys.argv[1])
    date = digest.stem

    urls = sorted(set(re.findall(r"\]\((https?://[^)\s]+)\)", digest.read_text())))

    data = json.loads(LEDGER.read_text())
    entries = data.get("entries", [])
    known = {e["url"] for e in entries}
    added = 0
    for url in urls:
        if url not in known:
            entries.append({"url": url, "date": date})
            added += 1

    cutoff = datetime.date.fromisoformat(date) - datetime.timedelta(days=WINDOW_DAYS)
    kept = [e for e in entries if datetime.date.fromisoformat(e["date"]) >= cutoff]
    dropped = len(entries) - len(kept)

    data["entries"] = sorted(kept, key=lambda e: (e["date"], e["url"]))
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")
    print(f"seen.json: +{added} new, -{dropped} aged out, {len(kept)} tracked")


if __name__ == "__main__":
    main()
