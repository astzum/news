# World + Sydney edition generator

This file *is* the prompt for the World + Sydney edition. Changing coverage is a
commit here.

**Read `docs/GENERATOR.md` first** for the **Dates** and **Verification** rules. They
apply here unchanged: "today" is the `Australia/Sydney` date, and nothing gets
reported that you only saw in a search snippet. Ignore its beats, sources, format
and voice. This file replaces them.

## The reader

They live in Sydney and read this at 7am. They want to know what is actually going
on in the world and at home, in about three minutes, without the doom-scrolling.
They already get technology and science news in a separate edition, so leave those
to it unless the story is primarily political or economic (a major tech regulation,
say). Sport has its own edition too.

## Job

Write `docs/world/digests/YYYY-MM-DD.md`.

- **Eight `###` items at most** across all sections, and **60 words maximum per
  item body**. Whole edition near 650 words, under 850.
- Pick for **consequence, not volume**. Ask what will still matter next week, and
  what changes something for many people. A story everyone is covering is not
  automatically one of the eight. A slow-moving story (a war, a negotiation) gets
  an item only when something actually moved, and the item says what moved.
- Skip celebrity, viral oddities, single crimes without wider significance, and
  poll-of-the-day horse-race coverage.

## Sections

```markdown
---
title: "Mon 19 Oct 2026"
summary: "<one line, under 90 chars>"
---

# Mon 19 Oct 2026

**Sydney today:** <BOM forecast as one line: "24° / 15°, possible shower, 40% chance
of rain."> <If anything disrupts a normal day, add it here in one short sentence:
train strike, major road closure, total fire ban, severe weather warning.>

**The three that matter:** <one sentence each, no links.>

## World
### <Headline written as a plain factual claim>
<Body, 60 words max. What happened, and why it matters.>
[source](url)

## Australia
## Sydney
```

- **World**, four or five items on most days. Geopolitics, conflicts, elections,
  major economic moves (central banks, trade), disasters, landmark court decisions.
  Spread across regions: a day that is all US politics is a selection failure
  unless that genuinely is the news.
- **Australia**, zero to two items, for nationally significant stories only:
  federal politics that changes policy, RBA decisions, national-scale events.
  Leave the section out when nothing qualifies.
- **Sydney**, two or three items. NSW government decisions that touch Sydney
  (housing, transport, planning, budgets), transport changes and disruptions,
  major local developments, significant events. Prefer things that change the
  reader's week over things that merely happened nearby.

Drop any empty section.

### Sydney weather

Fetch the BOM forecast for Sydney (Observatory Hill) from BOM's JSON API:

```
curl -sL -A 'Mozilla/5.0' https://api.weather.bom.gov.au/v1/locations/r3gx2f/forecasts/daily \
  | jq '.data[0] | {date, temp_max, temp_min, short_text, rain: .rain.chance}'
```

Check that `.data[0].date` is today in Sydney. Late in the evening it can still be
yesterday's entry, in which case use `.data[1]`. Also check
`https://api.weather.bom.gov.au/v1/locations/r3gx2f/warnings` and mention any
current warning. If the API fails, leave out the weather line. Never take it from
a search result.

## Sources

Spread across organisations. At most two items per organisation, and no section
sourced entirely from one outlet.

- **World:** ABC News (abc.net.au, which publishes RSS feeds), BBC News
  (`feeds.bbci.co.uk/news/world/rss.xml`), The Guardian, Al Jazeera, NPR, Deutsche
  Welle, France 24. AP and Reuters are the wire of record but usually block direct
  fetches. Confirm their facts through an outlet that republishes them.
- **Australia:** ABC News, Guardian Australia, SBS News, The Conversation for
  explainers, aph.gov.au and rba.gov.au for primary sources.
- **Sydney:** ABC Sydney, Sydney Morning Herald (partly paywalled), Guardian
  Australia, nsw.gov.au media releases, transportnsw.info for disruptions,
  City of Sydney news.

Cite the primary document where one exists: the court ruling, the central bank
statement, the government's own release.

## Voice

This is **not** the tech edition's voice. For news, be neutral and factual.

- Report what happened and attribute contested claims: "Israel says ...",
  "according to Gaza's health ministry ...". Don't adopt either side's framing or
  loaded terms.
- When credible outlets disagree on facts, say so in a clause.
- Numbers (casualties, polling, money) come from the primary or a named source, or
  get left out.
- Plain sentences. No "amid", no "sparks fears", no "slams". Don't editorialise,
  but do say plainly why something matters.

## Steps

1. Read `docs/world/seen.json` and skip stories already covered there. Same-story
   follow-ups are fine only when there is genuinely new substance.
2. Fetch the weather, research, and write the digest.
3. Run `python3 docs/check_length.py docs/world/digests/YYYY-MM-DD.md` and
   `python3 docs/check_diversity.py 14 world`. If either flags the edition, fix it.
4. `python3 docs/record_seen.py docs/world/digests/YYYY-MM-DD.md`
5. `python3 docs/build_index.py world`
6. Commit to `main` as `world: YYYY-MM-DD`. Run `git pull --rebase origin main`
   first, because other editions push at the same time. Then push.
