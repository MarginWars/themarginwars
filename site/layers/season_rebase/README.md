# Season 1 rebase layer (13 Nov 2026)

Launch day one for the Games is **Monday 16 Nov 2026, 9:00 AM PT**. This layer runs last in `site/build.sh` and
is idempotent. All settings live in [`season.json`](season.json). After any change, run `bash site/build.sh full`
and commit `site/src`, `site/functions` and `site/dist.md5`.

## What it does

- **Season lock.** The Arcade and every game page (`arcade`, `tracewire`, `daily`, `leak`, `deal`, `quiz`,
  `ep1` to `ep9`) carry a "Season 1 starts Monday, Nov 16" panel in a `<template id="s1-lock">`.
  - Server side: `site/functions/_middleware.js` (generated) serves a locked page as the panel only, with
    `Cache-Control: no-store` and `X-Robots-Tag: noindex`. It works without JavaScript.
  - Client side: `/assets/season.js` (generated) applies the same rule when no server is present (local static
    serving) and defers to the server's `data-s1` attribute when it is.
- **Episodes un-parked.** Episodes 2 to 9 and Tracewire get their game sections back. Each episode opens on its own
  date (`data-open`). Before that date the server serves the episode without its game, and `games.js` shows the
  existing countdown lock.
- **Arcade list.** Every episode links to its page and shows its open date (for example "Mon, Nov 23"). The
  server, then the client, switch the label to "Open" once the date has passed.
- **Tracewire.** Boards are re-dated to run daily from 16 Nov. When the last board's date has passed, the page
  shows a "The next board is coming" state instead of repeating the last board.
- **Preview.** `?preview=1` skips the gates on non-production hosts only: `themarginwars-dev.pages.dev`, its
  preview branches, `review.themarginwars.pages.dev` and localhost. It has no effect on themarginwars.com.
- **Sitemap.** Game URLs get `lastmod` 2026-11-13. No feed, digest or calendar entry referred to game dates.

## How the lock lifts

`season.json` ships with `"force": "locked"`. The lock lifts only through one config change plus a deploy:

| `force` | Behaviour |
|---|---|
| `"locked"` | Locked regardless of date (default shipped). Preview hosts with `?preview=1` still see the games. |
| `"auto"` | Locked until `launch` (2026-11-16T17:00:00Z = 9:00 AM PT), then lifts by itself, server and client. |
| `"open"` | Never locked. Episodes still open on their own dates. |

Monday runbook: change `"force": "locked"` to `"auto"` (any time before 9:00 AM PT, it lifts at 9:00) or to
`"open"` (lifts as soon as it is deployed), run `bash site/build.sh full`, open the PR, merge after Avi's OK, then
deploy production through the `deploy` workflow with Avi's approval.

## Calendar

All times 9:00 AM PT (17:00 UTC; Pacific Standard Time throughout).

| Episode | Old date (Tue) | New date (Mon) |
|---|---|---|
| 1 The Muster | 3 Nov | 16 Nov |
| 2 Close Quarters | 10 Nov | 23 Nov |
| 3 The FX Front | 17 Nov | 30 Nov |
| 4 Forced March | 24 Nov | 7 Dec |
| 5 The Loins | 1 Dec | 14 Dec |
| 6 Chest and Horns | 8 Dec | 4 Jan 2027 |
| 7 The Agent Frontier | 15 Dec | 11 Jan 2027 |
| 8 New Currency | 5 Jan 2027 | 18 Jan 2027 |
| 9 The Council | 12 Jan 2027 | 25 Jan 2027 |

The old plan skipped the two holiday weeks (no drop on 22 or 29 Dec). The new plan keeps that skip: no drop on
21 or 28 Dec. This is a proposal for Avi to decide. The strict weekly alternative is Ep6 21 Dec, Ep7 28 Dec, Ep8
4 Jan, Ep9 11 Jan. Change `episodes` in `season.json` to switch. 18 Jan 2027 is a US public holiday (Martin
Luther King Jr. Day).

## Tracewire coverage

The 30 existing boards cover 16 Nov to 15 Dec 2026, one a day. Each episode week now runs Monday to Sunday. The
old weeks ran Tuesday to Monday, so each week's Monday board moved to Tuesday. That keeps the size pattern
(5, 5, 6, 6, 7, 7, 8) and every "Sunday:" board on a Sunday. Board numbers follow the new dates.

New boards are needed from **16 Dec 2026**. That is 5 to finish the Episode 5 week (16 to 20 Dec), 14 if boards
run through the holiday weeks (21 Dec to 3 Jan), and 28 for the Episode 6 to 9 weeks (4 to 31 Jan 2027). The
"next board is coming" state covers any gap.
