#!/usr/bin/env python3
"""Regenerate docs/index.md from the frontmatter of every digest.

Run after writing a new digest. Keeping this as a script rather than asking the
model to rewrite index.md by hand means the index can't silently drift.
"""
import datetime
import pathlib
import re

DOCS = pathlib.Path(__file__).parent
DIGESTS = DOCS / "digests"


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


def main():
    rows = []
    for path in sorted(DIGESTS.glob("*.md"), reverse=True):
        stem = path.stem
        try:
            date = datetime.date.fromisoformat(stem)
        except ValueError:
            continue
        fields = frontmatter(path)
        title = fields.get("title") or date.strftime("%a %d %b %Y")
        summary = fields.get("summary", "")
        row = f"- [{title}](digests/{stem}.md)"
        if summary:
            row += f" — {summary}"
        rows.append(row)

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
    body.extend(rows or ["*No digests yet.*"])
    body.append("")
    (DOCS / "index.md").write_text("\n".join(body))
    print(f"index.md: {len(rows)} digest(s)")


if __name__ == "__main__":
    main()
