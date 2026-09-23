#!/usr/bin/env python3
"""Report item and digest length against the budget in GENERATOR.md.

The word limits are the rules most prone to quiet drift -- bodies grew from the
intended two or three sentences to ~180 words over ten days without anything
noticing. This makes that visible.

Usage: python3 docs/check_length.py [digest.md ...]   (default: newest)
"""
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).parent
DIGESTS = DOCS / "digests"

MAX_ITEM_WORDS = 65
TARGET_TOTAL = 700
MAX_TOTAL = 900
WPM = 220  # unhurried phone reading


def words(text):
    return len(text.split())


def check(path):
    raw = path.read_text()
    body = re.split(r"\n## Trending on GitHub", raw)[0]
    # Drop frontmatter, headings, and bare source links; what's left is prose.
    prose = re.sub(r"^---\n.*?\n---\n", "", body, flags=re.S)

    items, over = [], []
    for chunk in re.split(r"\n### ", prose)[1:]:
        headline = chunk.split("\n")[0].strip()
        text = "\n".join(chunk.split("\n")[1:])
        text = re.sub(r"^\[.*?\]\(.*?\)\s*(·\s*\[.*?\]\(.*?\)\s*)*$", "", text,
                      flags=re.M)
        n = words(text)
        items.append((headline, n))
        if n > MAX_ITEM_WORDS:
            over.append((headline, n))

    total = words(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", prose))
    print(f"{path.stem}: {len(items)} items, {total} words, "
          f"~{total / WPM:.1f} min read")
    if items:
        longest = max(items, key=lambda x: x[1])
        print(f"  longest item: {longest[1]}w — {longest[0][:56]}")
        print(f"  mean item:    {sum(n for _, n in items) // len(items)}w "
              f"(limit {MAX_ITEM_WORDS})")

    problems = []
    if over:
        problems += [f"{n}w over the {MAX_ITEM_WORDS}w item limit — {h[:50]}"
                     for h, n in over]
    if total > MAX_TOTAL:
        problems.append(f"{total}w total, over the {MAX_TOTAL}w ceiling "
                        f"(target {TARGET_TOTAL})")
    return problems


def main():
    paths = [pathlib.Path(a) for a in sys.argv[1:]]
    if not paths:
        paths = sorted(DIGESTS.glob("*.md"))[-1:]
    problems = []
    for path in paths:
        problems += check(path)
    print()
    if problems:
        print("FLAGGED")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK: within the length budget")
    return 0


if __name__ == "__main__":
    sys.exit(main())
