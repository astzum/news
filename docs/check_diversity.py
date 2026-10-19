#!/usr/bin/env python3
"""Report organisation concentration across recent digests.

Counting distinct domains flatters the digest: a company's blog, its docs site and
its GitHub org are three domains and one source. This groups by organisation instead
and flags the two failure modes worth catching -- one org dominating a single digest,
and one org quietly recurring across the window.

Usage: python3 docs/check_diversity.py [days] [edition]   (default 14 tech)
"""
import collections
import datetime
import pathlib
import re
import sys
import urllib.parse

from editions import EDITIONS, root, strip_list_sections

# Domains that belong to the same publisher. Anything unlisted falls back to its
# registrable-looking domain, which is right often enough.
ALIASES = {
    "blog.google": "Google", "ai.google.dev": "Google", "deepmind.google": "Google",
    "developers.googleblog.com": "Google", "research.google": "Google",
    "openai.com": "OpenAI", "anthropic.com": "Anthropic", "darioamodei.com": "Anthropic",
    "ai.meta.com": "Meta", "mistral.ai": "Mistral",
    "openjdk.org": "OpenJDK", "mail.openjdk.org": "OpenJDK",
    "kubernetes.io": "CNCF", "cncf.io": "CNCF",
    "amazon.science": "Amazon", "aws.amazon.com": "Amazon",
    "blog.cloudflare.com": "Cloudflare",
    "huggingface.co": "Hugging Face", "arxiv.org": "arXiv",
    "github.com": "GitHub (various)",
}
MAX_PER_DIGEST = 2


def org(url):
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    if host in ALIASES:
        return ALIASES[host]
    parts = host.split(".")
    # blog.example.com -> example.com; example.co.uk stays whole
    if len(parts) > 2 and parts[-2] not in ("co", "com", "org", "net", "ac"):
        host = ".".join(parts[-2:])
    return host


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    name = sys.argv[2] if len(sys.argv) > 2 else "tech"
    if name not in EDITIONS:
        sys.exit(f"unknown edition {name!r}; one of {', '.join(EDITIONS)}")
    DIGESTS = root(name) / "digests"
    cutoff = datetime.date.today() - datetime.timedelta(days=days)

    per_digest, window = {}, collections.Counter()
    for path in sorted(DIGESTS.glob("*.md"), reverse=True):
        try:
            date = datetime.date.fromisoformat(path.stem)
        except ValueError:
            continue
        if date < cutoff:
            continue
        # Scan lists (GitHub trending, results tables) are listings, not sourced
        # reporting. Counting their links would trip the per-org cap every day.
        body = strip_list_sections(path.read_text(), name)
        orgs = [org(u) for u in re.findall(r"\]\((https?://[^)\s]+)\)", body)]
        per_digest[path.stem] = collections.Counter(orgs)
        window.update(orgs)

    if not per_digest:
        print("no digests in window")
        return 0

    problems = []
    print(f"organisations over the last {days} days ({len(per_digest)} digests, "
          f"{sum(window.values())} links, {len(window)} orgs)\n")
    for name, count in window.most_common():
        share = count / sum(window.values()) * 100
        print(f"  {count:3}  {share:4.0f}%  {name}")
    print()

    for date, counts in sorted(per_digest.items(), reverse=True):
        over = [f"{o} x{n}" for o, n in counts.items() if n > MAX_PER_DIGEST]
        if over:
            problems.append(f"{date}: over the {MAX_PER_DIGEST}-per-org cap -- {', '.join(over)}")

    top, top_n = window.most_common(1)[0]
    if len(per_digest) > 1 and top_n / sum(window.values()) > 0.25:
        problems.append(f"{top} is {top_n/sum(window.values()):.0%} of the window "
                        f"-- check it is not becoming the default source")

    if problems:
        print("FLAGGED")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK: no organisation over the per-digest cap or dominating the window")
    return 0


if __name__ == "__main__":
    sys.exit(main())
