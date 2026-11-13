# Changelog

All notable changes. Format: Keep a Changelog; dates in Pacific Time.

## [Unreleased]

### Added
- Repository created from the box migration (12 Nov 2026): site history rebuilt from dated backups
  (31 Oct to 12 Nov 2026), layered build, Pages Functions, release gates, governance, CI, deploy workflows,
  publish pipeline scaffold, agent roster, ADR-0001 to ADR-0003 and the Monday 16 Nov launch runbook.

### Changed
- The assistant function's output denylist and confidential prompt rules moved out of source into the
  `MW_GUARD` Pages secret; without it the assistant fails closed.
- Build-time term checks in the feed layers use the hashed compliance list.
