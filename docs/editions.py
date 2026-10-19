"""The site's editions, and the per-edition settings the helper scripts share.

Each edition is a directory under docs/ holding its own GENERATOR.md, digests/,
seen.json, index.md and archive.md. Tech predates the others and lives at the docs/
root so its URLs never moved.

`list_sections` are scan lists (bullets, not ### items): exempt from the word budget
and from the per-organisation diversity count.
"""
import pathlib

DOCS = pathlib.Path(__file__).parent

EDITIONS = {
    "tech": {
        "dir": "",
        "title": "Daily Digest",
        "blurb": "AI, dev, homelab, hardware, and science news — one page a day. Newest first.",
        "max_item_words": 65, "target_words": 700, "max_words": 900,
        "list_sections": ["Trending on GitHub"],
    },
    "world": {
        "dir": "world",
        "title": "World + Sydney",
        "blurb": "The world, then home — one page a day. Newest first.",
        "max_item_words": 60, "target_words": 650, "max_words": 850,
        "list_sections": [],
    },
    "sport": {
        "dir": "sport",
        "title": "Sport",
        "blurb": "Premier League, F1, NBA, NFL and the Tour — what happened overnight. Newest first.",
        "max_item_words": 55, "target_words": 500, "max_words": 700,
        "list_sections": ["Results", "Coming up"],
    },
    "gaming": {
        "dir": "gaming",
        "title": "Gaming",
        "blurb": "Releases, reviews and the industry — short on purpose. Newest first.",
        "max_item_words": 60, "target_words": 400, "max_words": 600,
        "list_sections": ["Out this week"],
    },
}


def root(name):
    return DOCS / EDITIONS[name]["dir"]


def for_digest(path):
    """Which edition a docs/<dir>/digests/YYYY-MM-DD.md file belongs to."""
    edition_dir = pathlib.Path(path).resolve().parent.parent
    for name in EDITIONS:
        if root(name).resolve() == edition_dir:
            return name
    raise SystemExit(f"{path}: not inside any edition's digests/ directory")


def strip_list_sections(text, name):
    """Cut every scan-list section (up to the next ## heading) out of a digest."""
    import re
    for heading in EDITIONS[name]["list_sections"]:
        text = re.sub(rf"\n## {re.escape(heading)}\n.*?(?=\n## |\Z)", "\n", text, flags=re.S)
    return text
