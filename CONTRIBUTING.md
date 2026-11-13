# Contributing

These rules apply to people and to automated agents. Adapted from the group standard (predicated / instip CONTRIBUTING).

## Branching

Branch from `main`: `feat/<short-name>`, `fix/…`, `docs/…`, `chore/…`, `ci/…`, and for channel work
`content/…`, `speaking/…`, `pub/…`, `media/…`, `ops/…`. Keep branches short-lived. Everything lands through a pull request.
Nobody pushes to `main` directly; the ruleset blocks it.

## Commits

Conventional Commits: `<type>(<scope>): <summary>`, imperative, at most 72 characters.
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, plus
`content`, `speaking`, `pub`, `media` for channel items. Scopes: `site`, `functions`, `qa`, `linkedin`, `x`,
`substack`, `briefing`, `speaking`, `media`, `pipeline`, `research`, `facts`, `brand`, `ops`, `ci`.

## Pull requests

1. Open the PR with the matching template (`?template=content.md`, `site.md`, `speaking.md`, `outreach.md`) and link the issue.
2. Every required check must pass: `compliance`, `frontmatter-limits`, `claims`, `links-docs`, `secrets`,
   `standards-lock`, `functions`, and for site changes `site-build`, `site-gates`.
3. The code owner (Avi, `@AviShip-Type0`) approves. **The merge is the approval of record** for exactly the text,
   times and lists in the PR. A change after merge needs a new PR.
4. **Squash-merge only.** The PR title becomes the commit, so it must be a Conventional Commit. The branch is deleted on merge.
5. Agents open PRs as the bot account and never approve, merge or bypass. People sign.

## Outbound items

Every outbound item (post, thread, issue, pitch, speaker pack, profile change) is one file with front-matter that
validates against `schemas/content-item.schema.json`:

```yaml
---
id: li-company-2026-11-16-launch
channel: linkedin-company   # linkedin-personal | linkedin-company | x | substack | briefing | site | speaking-form | email-draft | media-pitch
kind: post                  # post | thread | issue | profile | pack | pitch | proposal
schedule: 2026-11-16T08:30:00-08:00   # Pacific Time with an explicit offset
status: draft               # draft -> in-review -> approved (merge) ; scheduled/published/failed live on the ledger branch
owner: channels             # agent id from .agents/
approvals: {}               # e.g. {<gated id>: A-001}; required when an approval-gated name appears (ids in qa/compliance/banned.yml)
sources: [facts/approved.yml#turnaround]   # every number maps to a fact, a source file, or an [Assumption]
links: []                   # link ids from site/layers/marketing/links.csv (UTM registry)
standing_permission: SP-1   # optional, from ops/standing-permissions.md
---
```

- Character limits per channel live in `qa/limits.yml` and are enforced in CI.
- Numbers must cite `sources:` (see `qa/check_claims.py`). Never invent facts, stats, quotes or war stories.
- Approval-gated company names need an `approvals:` entry pointing at an **approved** row in `ops/approvals.md`.
- Private names and terms are blocked by hash (see `qa/compliance/banned.yml`). If the gate fires, remove the
  text; do not try to reword around it.

## Secrets and data

No secrets, tokens, webhook URLs, personal data, lead records or form submissions in git. See [SECURITY.md](SECURITY.md).
