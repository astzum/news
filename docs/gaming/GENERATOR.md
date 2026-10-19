# Gaming edition generator

This file *is* the prompt for the Gaming edition. Changing coverage is a commit here.

**Read `docs/GENERATOR.md` first** for the **Dates**, **Voice** and **Verification**
rules. They apply here unchanged. Ignore its beats, sources and format. This file
replaces them.

## Job

Write `docs/gaming/digests/YYYY-MM-DD.md`. This is the **short** edition: about
ninety seconds to read.

- **Five `###` items at most**, and **60 words maximum per item body**. Whole
  edition near 400 words, under 600. On a slow day, two items is fine.
- GPUs and PC hardware belong to the Tech edition. Cover them here only when the
  story is about games: a console, a handheld, a store or a platform.

## Beats

- **Releases and reviews.** Notable launches and how they actually landed. Cite
  the OpenCritic or Metacritic aggregate rather than one outlet's score, and say
  when the launch is troubled (performance, servers, pricing).
- **Announcements.** Reveals, release dates and delays from showcases and
  publishers. A trailer alone is not an item unless the game is a genuinely big deal.
- **Industry.** Studio closures, layoffs, acquisitions, unionisation, and earnings
  that change what gets made.
- **Platforms.** PlayStation, Xbox, Nintendo, Steam and PC storefronts, and
  handhelds: hardware, pricing, subscriptions, policy changes.

## Sections

```markdown
---
title: "Mon 19 Oct 2026"
summary: "<one line, under 90 chars>"
---

# Mon 19 Oct 2026

### <Headline written as a claim>
<Body, 60 words max.>
[source](url)

## Out this week

- **Game title** — what it is, under 10 words. `PC · PS5 · Switch 2` · Thu 23 Oct
```

There are no beat headings: with five items they are noise. Put the strongest item
first.

**Out this week** lists notable releases in the next seven days, three to six
bullets. Give the platforms and the Australian release date. Include it on
Mondays and Thursdays only, and on other days only when a major game launches
that day.

## Sources

Eurogamer, PC Gamer, Rock Paper Shotgun, GamesIndustry.biz (industry), The Verge
games, Digital Foundry (performance), Polygon, Kotaku, VGC, OpenCritic, and the
official PlayStation Blog, Xbox Wire, Nintendo and Steam news posts. At most two
items per organisation.

**Leaks and rumours:** leave them out unless the publisher has confirmed. The one
exception is a rumour so widely covered that the reader will have seen it already.
Then include it labelled as unconfirmed, with the source of the claim.

## Steps

1. Read `docs/gaming/seen.json` and skip stories already covered there.
2. Research and write the digest.
3. Run `python3 docs/check_length.py docs/gaming/digests/YYYY-MM-DD.md` and
   `python3 docs/check_diversity.py 14 gaming`. If either flags the edition, fix it.
4. `python3 docs/record_seen.py docs/gaming/digests/YYYY-MM-DD.md`
5. `python3 docs/build_index.py gaming`
6. Commit to `main` as `gaming: YYYY-MM-DD`. Run `git pull --rebase origin main`
   first, because other editions push at the same time. Then push.
