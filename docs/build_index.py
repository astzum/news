#!/usr/bin/env python3
"""Regenerate docs/index.md and docs/archive.md from digest frontmatter.

Run after writing a new digest. Keeping this as a script rather than asking the
model to rewrite the index by hand means it can't silently drift.

The landing page shows only the most recent RECENT_DAYS digests. Listing every
digest forever would put a year of entries on the page you open each morning;
everything older lives in archive.md, grouped by month.
"""
import datetime
import pathlib
import re

DOCS = pathlib.Path(__file__).parent
DIGESTS = DOCS / "digests"

# Enough to catch up after a holiday, short enough to thumb through on a phone.
RECENT_DAYS = 14


def frontmatter(path):
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fields = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip().strip('"')
    return fields


def rows_for(entries):
    return [
        f"- [{title}](digests/{stem}.md)" + (f" — {summary}" if summary else "")
        for stem, title, summary in entries
    ]


def main():
    entries = []
    for path in sorted(DIGESTS.glob("*.md"), reverse=True):
        stem = path.stem
        try:
            date = datetime.date.fromisoformat(stem)
        except ValueError:
            continue
        fields = frontmatter(path)
        entries.append((stem, date,
                        fields.get("title") or date.strftime("%a %d %b %Y"),
                        fields.get("summary", "")))

    recent = [(s, t_, su) for s, d, t_, su in entries[:RECENT_DAYS]]
    older = entries[RECENT_DAYS:]

    body = [
        "---",
        'title: "Daily Digest"',
        "---",
        "",
        "# Daily Digest",
        "",
        "AI, dev, and homelab news — one page a day. Newest first.",
        "",
    ]
    body.extend(rows_for(recent) or ["*No digests yet.*"])
    if older:
        body += ["", f"[Archive →](archive.md) · {len(older)} older"]
    body.append("")
    (DOCS / "index.md").write_text("\n".join(body))

    arch = ["---", 'title: "Archive"', "---", "", "# Archive", ""]
    if older:
        month = None
        for stem, date, title, summary in older:
            label = date.strftime("%B %Y")
            if label != month:
                # Blank line only between groups: a blank line between entries
                # makes Markdown treat it as a loose list and adds paragraph
                # spacing the front page doesn't have.
                if month is not None:
                    arch.append("")
                month = label
                arch += [f"## {label}", ""]
            arch.extend(rows_for([(stem, title, summary)]))
        arch.append("")
    else:
        arch.append("*Nothing archived yet — everything is on the [front page](index.md).*")
        arch.append("")
    (DOCS / "archive.md").write_text("\n".join(arch))

    print(f"index.md: {len(recent)} recent, archive.md: {len(older)} older")


if __name__ == "__main__":
    main()
