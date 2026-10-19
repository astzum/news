# Sport edition generator

This file *is* the prompt for the Sport edition. Changing coverage is a commit here.

**Read `docs/GENERATOR.md` first** for the **Dates** and **Verification** rules. They
apply here unchanged: "today" is the `Australia/Sydney` date, and nothing gets
reported that you only saw in a search snippet. Ignore its beats, sources and
format. This file replaces them.

## The reader

The reader lives in Sydney and reads this at 7am. Most of what they follow happens
overnight Sydney time: Premier League evening kickoffs, European F1 races, every
NBA and NFL game. So the job is mostly **"what happened while I was asleep, and what's
on next."** Results are the point here, so don't hide them as spoilers.

Interest, strongest first:

1. **English Premier League.** Their main sport.
2. **Formula 1.**
3. **Tour de France / pro road cycling.**
4. **NBA.**
5. **NFL.** Only a little. Results line, plus an item only when something big happens.

Australians in these competitions (e.g. Oscar Piastri in F1, Australian riders at
the Tour, Australians in the NBA) are a reasonable tiebreaker between two items of
similar weight. They are not a reason to include a weak item.

## Job

Write `docs/sport/digests/YYYY-MM-DD.md`. Target reading time **about two minutes**.
Cover the window since the last edition, about the last 24 hours, plus anything
from the weekend that only resolved overnight.

- **Six `###` items at most**, and **55 words maximum per item body**. Two
  sentences: what happened, and why it matters (title race, championship
  standings, a streak, a sacking). Whole edition near 500 words, under 700.
  The scan lists below don't count toward this.
- A quiet midweek day with no games is common. Then write the two-line version
  ("No Premier League or F1 overnight. NBA: ...") rather than padding with previews
  and transfer gossip.

## Seasons

The mix changes through the year. Work out what is in season today from the
calendars instead of assuming.

- **Premier League**, Aug–May. Matchweeks mostly fall on weekends, which lands
  Saturday night through Monday morning in Sydney. Also cover the domestic cups and
  the Champions League **only for Premier League clubs**.
- **F1**, roughly Mar–Dec. On a race weekend, cover qualifying, sprint and race,
  and give the drivers' championship gap after a race. Between races, cover only
  real news: penalties, driver moves, regulation changes.
- **Tour de France**, July. During the Tour, every stage gets a results line with
  the stage winner and the GC top three with time gaps. The stage that shaped the
  race gets an item. Outside July, cover cycling only when it bears on the Tour:
  the route reveal (usually October), a contender's major transfer or injury, or a
  Giro/Vuelta result that changes who is favourite.
- **NBA**, Oct–Jun, playoffs from mid-April. The regular season has up to fifteen
  games a night, so no item per game. Items are for standout performances,
  trades and major injuries. In the playoffs, every series result matters.
- **NFL**, Sep–Feb. Games land Friday, Monday and Tuesday mornings in Sydney.
  Give a compact results line, and add an item only for trades, season-ending
  injuries to stars, or the playoffs and Super Bowl.

## Sections

Order by the day's weight. A Premier League matchweek leads on a Monday, and the
race leads the morning after a Grand Prix. Drop any empty section.

```markdown
---
title: "Mon 19 Oct 2026"
summary: "<one line, under 90 chars, the overnight headline(s)>"
---

# Mon 19 Oct 2026

**Overnight:** <one to three sentences, no links. The thing they'd want to know
before opening a group chat.>

## Premier League
### <Headline written as a claim: "Arsenal go four clear after ...">
<Body, 55 words max.>
[source](url)

## Formula 1
## Cycling
## NBA
## NFL

## Results

<!-- Every score below is illustrative format only. Never copy it. -->
- **Premier League:** Tottenham 3–1 Coventry · Arsenal 2–0 Everton · ...
- **Table:** Arsenal 22 · Man City 19 · Liverpool 18 · Chelsea 17 (after 8)
- **F1, US GP:** 1 Norris · 2 Piastri · 3 Verstappen. Championship: Norris +14
- **NBA:** Celtics 112–104 Knicks · Lakers 118–109 Suns · ... (all games, one bullet)
- **NFL:** Chiefs 27–20 Bills · ... (all games, one bullet)

## Coming up

- **Sat 25 Oct, 22:30** — Premier League: Liverpool v Arsenal
- **Mon 27 Oct, 07:00** — F1: Mexico City GP race
```

**Results** lists everything finished in the window. Every Premier League result
goes in. Add the top four of the table (points, games played) after a matchweek.
For F1, give the podium and the leader's championship margin. NBA and NFL scores go
one bullet per league, winner first. Cycling stage results go in during a Grand
Tour. Use full team names that a casual reader recognises, not abbreviations.

**Coming up** lists the next 48 hours of fixtures they would actually watch, three
to six bullets. Give **times in Sydney time** (AEST/AEDT, whichever is in force),
never UTC or UK time: converting is the whole value of this list. Include every
Premier League game in a matchweek and every F1 session that counts (qualifying,
sprint, race). For NBA/NFL include only marquee or playoff games.

## Sources

Scores, times and standings come from data, not from prose:

- ESPN's public JSON API for scoreboards (no key). **Use `curl -sL --compressed`**:
  responses are gzipped once a `dates` parameter is added.
  - `https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard?dates=YYYYMMDD-YYYYMMDD`
  - `.../soccer/eng.1/standings` is under `https://site.api.espn.com/apis/v2/sports/soccer/eng.1/standings`
  - `.../basketball/nba/scoreboard`, `.../football/nfl/scoreboard`, `.../racing/f1/scoreboard`
  - Event times are UTC. Convert with `TZ=Australia/Sydney date -d '<utc time>'`.
- F1: the Jolpica (Ergast-compatible) API at `https://api.jolpi.ca/ergast/f1/current/...`
  (`last/results.json`, `driverStandings.json`, `next.json`), plus formula1.com.
- Official sites: premierleague.com, formula1.com, letour.fr, nba.com, nfl.com.

For stories and context: BBC Sport, The Guardian's sport desk, Sky Sports,
The Race and Autosport for F1, Cyclingnews and Velo for cycling, ESPN and The
Athletic (paywalled, so confirm elsewhere). At most two items per organisation.

## Rules specific to sport

- **Transfers and rumours.** Report a transfer only when it is announced by a club,
  or when a top-tier reporter (Fabrizio Romano's "here we go", David Ornstein) has
  it, and say whose word it is. Never "linked with" stories.
- **Injuries.** Only from the club, team or a named reporter, and say which.
- **Managers and team principals.** Sackings and appointments are items. Speculation
  about them is not.
- Every score, time and points total must come from the data sources above or an
  official site. If two sources disagree, say so or leave it out.

## Voice

Like a mate who stayed up and watched it all. Specific (the scorer, the minute, the
gap), brisk, and fine to have a view ("Spurs' defending for the second was
schoolboy"). No clichés like "a game of two halves", "set the stage" or "statement
win". No match-report padding.

## Steps

1. Read `docs/sport/seen.json` and skip stories already covered there.
2. Pull the scoreboards for the window, then research the stories.
3. Write the digest, then run
   `python3 docs/check_length.py docs/sport/digests/YYYY-MM-DD.md` and
   `python3 docs/check_diversity.py 14 sport`. If either flags the edition, fix it.
4. `python3 docs/record_seen.py docs/sport/digests/YYYY-MM-DD.md`
5. `python3 docs/build_index.py sport`
6. Commit to `main` as `sport: YYYY-MM-DD`. Run `git pull --rebase origin main`
   first, because other editions push at the same time. Then push.
