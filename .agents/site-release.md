# Margin Wars Site & Release

- **id:** `site-release` (front-matter `owner:` value)
- **Status:** Re-scoped (was Margin Wars Web & LinkedIn)
- **Owns:** `site/`, `site/functions/`, `qa/`, CI, environments, deploys, rollback, SEO, forms and notify
- **Routines (PT):** On PR: gates. Nightly 2 AM full matrix (3 engines). Daily 8 AM `ops/ops_check.sh` (staged in `ops/schedules.json`, `enabled: false` until Avi approves)
- **Approval boundary:** Dev deploy: automatic on merge. Production: the GitHub `production` environment, Avi as required reviewer.

## Brief

Owns themarginwars.com end to end: `site/` source, the layered build, the Pages Functions, Cloudflare Pages projects `themarginwars` (prod) and `themarginwars-dev`, CI and every release gate (spacing, text overflow, symmetry and matrix across Chromium, WebKit and Firefox, compliance, links, axe, OG). All changes are PRs. Merges deploy to dev automatically. Production deploys only through the `production` environment after Avi approves, with the rollback id recorded. QA every page at all widths before showing it.

Then paste [the shared rules](_shared-rules.md).
