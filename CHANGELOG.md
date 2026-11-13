# Changelog

All notable changes. Format: Keep a Changelog; dates in Pacific Time.

## [Unreleased]

### Added

- Repository created from the box migration (12 Nov 2026): site history rebuilt from dated backups
  (31 Oct to 12 Nov 2026), layered build, Pages Functions, release gates, governance, CI, deploy workflows,
  publish pipeline scaffold, agent roster, ADR-0001 to ADR-0003 and the Monday 16 Nov launch runbook.

### Changed

- Repo presentation brought into the site brand: README front door with light and dark banners, the six-colour
  band divider and check badges; brand quick reference in `brand/README.md`; social preview and organisation
  avatar in `.github/assets/`; pull request and issue templates on one structure; labels in the brand palette;
  Markdown style pass with `markdownlint-cli2` and a `markdown` check.
- The assistant function's output denylist and confidential prompt rules moved out of source into the
  `MW_GUARD` Pages secret; without it the assistant fails closed.
- Build-time term checks in the feed layers use the hashed compliance list.
