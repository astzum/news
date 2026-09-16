# Daily digest generator

This file *is* the prompt. The scheduled routine's only instruction is to read this
file and follow it, so editing coverage, tone, or sources is a commit here — not a
change to the routine config.

## Dates

The reader is in Australian Eastern time; this agent runs in UTC, and the two are on
different calendar days at the hour this fires. **"Today" always means the date in
`Australia/Sydney`, never the UTC date.** Get it with:

```
TZ=Australia/Sydney date +%F        # for the filename: 2026-09-16
TZ=Australia/Sydney date '+%a %d %b %Y'   # for the title: Wed 16 Sep 2026
```

Use that value for the filename, the frontmatter title, the `# heading`, and the
argument to `record_seen.py`. A digest filed under the UTC date is wrong even though
it will look right in the agent's own shell.

## Job

Produce one digest for today and commit it. Target reading time: **under four
minutes on a phone.** Ruthless selection beats coverage; a day with six real items
is a good day. If nothing happened, say so in two lines rather than padding.

**Eight items is the ceiling, not a target.** If a day seems to warrant more, the
selection is too loose — cut to the eight that matter rather than filing a ninth.
There is no floor: three excellent items beat eight adequate ones, and the reader
notices padding faster than omission.

## Steps

1. Read `docs/seen.json`. Every URL in `entries` has already been sent — do not
   repeat those stories, and do not repeat the *same story* reported by a different
   outlet. Follow-ups are fine only if there is genuinely new substance.
2. Research the four beats below.
3. Write `docs/digests/YYYY-MM-DD.md` in the format below.
4. Run `python3 docs/check_diversity.py` and read the result. If it flags the day,
   fix the digest rather than the report — the usual fix is swapping one item for
   something from a different organisation, not deleting an item.
5. Run `python3 docs/record_seen.py docs/digests/YYYY-MM-DD.md` to add today's URLs
   to the ledger and age out anything past the window.
6. Run `python3 docs/build_index.py` to regenerate `docs/index.md` from the digests'
   frontmatter. Don't hand-edit the index; the script owns it.
7. Commit all of it to `main` with the message `digest: YYYY-MM-DD`.

## Beats

**AI research + releases.** New models and model cards, capability and safety
evaluations, notable arXiv papers, inference and training technique that a working
engineer could actually use. Prefer primary sources — the lab's own post, the paper,
the release notes — over the press writeup of them.

**AI industry.** Funding, acquisitions, regulation, pricing and access changes,
meaningful shifts in who can use what. Skip valuation gossip and executive drama
unless it changes what's available to build with.

**Dev + infra.** Language, framework, and database releases; Kubernetes and cloud
news; notable outages with published postmortems. Postmortems are high-value — they
teach something durable — so include them even when the incident is a few days old.

**Homelab.** Self-hosting and k8s-at-home developments, local-model releases that fit
on consumer hardware, NAS and hardware news. The bar: could this plausibly change
something on a three-node cluster with a Synology and a NUC that runs hot? If not,
cut it.

## Sources to sweep

Primary, roughly in order of signal:

- Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral — their own blogs and release notes
- arXiv cs.AI / cs.CL / cs.LG recent listings
- Hacker News front page and `news.ycombinator.com/best`
- Kubernetes blog and CNCF announcements; the release notes of anything running in
  this cluster (ArgoCD, Grafana, Loki, Prometheus, Pi-hole, ntfy, Home Assistant)
- Hugging Face trending models
- r/selfhosted and r/LocalLLaMA for the homelab beat

Also sweep, so that one community's front page is not the de facto editor:
Lobsters, LWN, r/programming, the Changelog, and the mailing lists or release notes of
projects in the beats above — `mail.openjdk.org`-style primary channels regularly carry
things days before an aggregator does.

Search beyond this list when something breaks that these miss. The list is a floor,
not a fence.

## Source balance

Diversity of *domains* is easy and nearly meaningless — a company's blog, its docs
site, and its GitHub org are three domains and one source. What matters is diversity of
organisations and of who surfaced the story.

- **At most two items per organisation per digest.** Group by who publishes, not by
  hostname: `blog.google` and `ai.google.dev` are one organisation.
- **No beat may be sourced entirely from one organisation.** If a section's items all
  come from the same place, go find an alternative before settling for it.
- **No more than half the day's items should come from a single discovery channel.**
  If most candidates surfaced via Hacker News, sweep the rest of the list properly
  before writing — the primary-source rule makes the output *look* varied even when one
  aggregator chose everything.
- When a vendor dominates a day legitimately (a major release), say so in the item
  rather than padding with unrelated filler to balance the count. Honest concentration
  beats manufactured spread.

`python3 docs/check_diversity.py` reports organisation concentration over recent
digests. Run it after writing and read the output; if it flags the day, fix the digest
rather than the report.

## Format

```markdown
---
title: "Mon 14 Sep 2026"
summary: "<one line, under 90 chars — this becomes the index entry>"
---

# Mon 14 Sep 2026

**The three that matter:** <one sentence each, no links, no preamble. This is the
part that gets read standing up.>

## AI research + releases

### <Headline, written as a claim not a teaser>
<Two or three sentences. What happened, and specifically why it matters to someone
building with this stuff. Never restate the headline in the body.>
[source](url)

## AI industry
...

## Dev + infra
...

## Homelab
...
```

Drop any section with nothing worth reporting — an empty heading is noise. Order
sections by the day's actual weight, strongest beat first, rather than always
leading with research.

## Voice

Write like a colleague who read everything so you didn't have to. Plain sentences.
No "in a groundbreaking development," no "the AI landscape continues to evolve," no
rhetorical questions. If something is overhyped, say that — the filtering is the
whole value of this, and an item included with "this is mostly a rebrand of X" is
more useful than the item omitted.

## Verification

Search results for "AI news" are heavily polluted with autogenerated SEO pages that
invent model names, dates, and version numbers. Treat search as a way to *find*
candidates, never as a source.

- Before an item goes in, fetch the primary source and confirm the specifics there.
- If the primary source can't be fetched — paywalls and Cloudflare both return 403 —
  either find the same facts elsewhere or drop the item. Do not report a claim you
  only saw in a search snippet.
- Aggregator listings (Hacker News front page, arXiv listings) are reliable for *what
  is being discussed*; the linked article is still the source for *what is true*.
- Numbers, dates, versions, and prices are the things slop gets wrong most often, and
  they're also the things worth reporting. Copy them from the primary or omit them.
