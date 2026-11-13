# The Margin Wars

Source of truth for The Margin Wars (themarginwars.com): the website, every outbound post, issue, pitch and
speaker pack, and the governance that decides when any of it goes live. Run by Avi and Anitha, Pacific Time.

**GitHub drives every channel** ([ADR-0001](docs/adr/0001-github-source-of-truth.md)). An item is a file with
front-matter; it changes only by pull request; **a merge approved by the code owner is the approval of record**.
Agents prepare. People sign.

## Layout

| Path | What lives there |
|---|---|
| `site/src/` | The site source of record (generated pages committed as source) |
| `site/layers/` | The ordered build layers that produced `site/src` (copy, UI, route briefs, about, feeds, normalize, buildout, marketing, brand assets) |
| `site/build.sh` | `dist` (default): `site/src` → `site/dist` (the only deploy artifact). `full`: rerun every layer. `check`: prove `site/src` is a fixed point of the layers |
| `site/functions/` | Cloudflare Pages Functions (contact, escalations, measurement, assistant). Runtime secrets are Pages project secrets, never here |
| `site/workers/` | The rate-limit and contact-mailer Workers (config templates only) |
| `qa/` | Release gates: compliance, claims, character limits, links, spacing, text overflow, symmetry, cross-engine matrix |
| `content/{linkedin,x,substack}/` | Channel posts, threads and profile copy; `content/calendar/` holds the weekly calendar (the approval unit) |
| `publications/` | The Briefing (invite-only monthly letter), essays, route briefs |
| `speaking/` | `register.yml` (the single CFP register), one pack per event, the speaker kit |
| `media/` | Press-pass and media pitches, media kit |
| `pipeline/` | Lead-generation **schema and playbooks only**. No personal records, ever |
| `research/` | Source library and research notes |
| `facts/` | `approved.yml` and `assumptions.yml`: every number in outbound copy maps here |
| `brand/` | Brand docs, logo and channel assets |
| `ops/` | Approvals, standing permissions, agent schedules, runbooks, environments, publish spec |
| `docs/adr/` | Architecture decision records |
| `schemas/` | JSON Schemas for front-matter, the calendar and the publish ledger |

## Everyday commands

```bash
pip install -r requirements.txt && python3 -m playwright install --with-deps chromium
bash site/build.sh            # build site/dist + qa-out/dist.md5
bash site/build.sh check      # layers fixed-point check
qa/run_gates.sh static        # compliance, front-matter/limits, claims, links, standards lock, functions
qa/run_gates.sh browser       # text overflow, spacing, symmetry (Chromium core) on the built site
```

## Flow

1. An agent (bot account) opens a PR from a short-lived branch (`feat/ fix/ content/ speaking/ pub/ chore/ ops/`).
2. CI runs every gate. Avi (code owner) reviews; **merge = approval** for exactly what is in the PR.
3. Merge to `main` deploys the site to **dev** (`themarginwars-dev`). Production waits on the `production`
   environment, which Avi approves.
4. Channels publishes merged items at their scheduled PT time and writes the live URL to the `ledger` branch.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [ops/approvals.md](ops/approvals.md),
[ops/runbooks/launch-2026-11-16.md](ops/runbooks/launch-2026-11-16.md) and [ops/publish/scheduler-spec.md](ops/publish/scheduler-spec.md).

## Licence

Copyright © 2026 The Margin Wars. All rights reserved; see [LICENSE](LICENSE). Public so the work is open to read,
not open to reuse.
