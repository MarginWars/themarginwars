# Changelog

All notable changes. Format: Keep a Changelog; dates in Pacific Time.

## [Unreleased]

### Added

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
