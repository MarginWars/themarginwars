# Changelog

All notable changes. Format: Keep a Changelog; dates in Pacific Time.

## [Unreleased]

### Added

- Contact and Briefing forms emit cookieless `form_view`, `form_start`, `form_error` and `form_submit`
  events through `/api/ev` (once per browser session per page; no IP, visitor id or form values).
  `/api/mk/report` adds a `funnel` rollup and `form_submit_rate` (`form_submit / form_view`).
  The visible form is shorter: email is required, the one-line message is optional, and a Briefing
  link no longer opens the "More details" topic list. Turnstile still runs; it now loads when the
  form comes on screen so the human check is ready before send.

- Season 1 episodes emit cookieless `game_start`, `game_complete` and `game_rank` events through `/api/ev` into
  `mk_daily` / `mk_daily_content` (once per browser session per page; no IP, visitor id or score is stored).
  `/api/mk/report` adds a `games` rollup and `game_completion_rate` so the daily metrics file can include them.
  The Episode 2 "Go to Episode 1" lock link is a 44px tap target, matching the existing "opens soon" Daily link,
  which unblocks the Chromium core site-gates failure at 390px.

- Home page: a compact Briefing-invite strip above the hero (existing invitation copy and form flow), with distinct
  `utm_content` / `data-mk-content` labels (`index-top-briefing` vs the existing hero button `index-hero-briefing`)
  so the two placements can be compared in `/api/mk/report` `by_content`. Dev only until reviewed.

- Repository created from the box migration (12 Nov 2026): site history rebuilt from dated backups
  (31 Oct to 12 Nov 2026), layered build, Pages Functions, release gates, governance, CI, deploy workflows,
  publish pipeline scaffold, agent roster, ADR-0001 to ADR-0003 and the Monday 16 Nov launch runbook.

### Changed

- Season 1 rebased to launch on Monday 16 Nov 2026 (`site/layers/season_rebase`): the Arcade and game pages sit
  behind a "Season 1 starts Monday, Nov 16" lock (server and client, shipped locked until a one-line config
  change), episodes open on Mondays at 9:00 AM PT, Tracewire boards re-dated from 16 Nov with a "next board is
  coming" state after the last board.
- Repo presentation brought into the site brand: README front door with light and dark banners, the six-colour
  band divider and check badges; brand quick reference in `brand/README.md`; social preview and organisation
  avatar in `.github/assets/`; pull request and issue templates on one structure; labels in the brand palette;
  Markdown style pass with `markdownlint-cli2` and a `markdown` check.
- The assistant function's output denylist and confidential prompt rules moved out of source into the
  `MW_GUARD` Pages secret; without it the assistant fails closed.
- Build-time term checks in the feed layers use the hashed compliance list.
