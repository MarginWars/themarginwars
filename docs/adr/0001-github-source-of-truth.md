# ADR-0001: GitHub drives every channel

- Status: accepted (Avi, 12 Nov 2026)
- Deciders: Avi (owner); proposed by the Margin Wars agents

## Context

The Margin Wars publishes on its site, LinkedIn (Avi's profile and the company page), X (@marginwars), Substack and
the invite-only Briefing, and runs speaking and media pipelines. Until now the source of each was a folder on an
agent box: dated backups instead of history, approvals in chat, no enforced gates, and no single place to see what
was approved, scheduled or live.

## Decision

1. `MarginWars/themarginwars` is the source of truth for all public digital content and interactions: the site, every
   post, issue, profile change, speaker pack and pitch.
2. A change is a PR. Avi is the required code owner, so **a merge is Avi's approval** of exactly the merged text.
   Agents commit as a separate bot account so Avi can review their PRs (GitHub blocks approving your own PR).
3. Gates run on every PR: compliance (restricted names, personal data, secrets), front-matter schema and per-channel
   character limits, claims against `facts/`, links, the site build (byte-for-byte manifest), and browser gates
   for spacing, text overflow and symmetry. A nightly run covers three engines and named devices.
4. The site deploys from `main`: dev automatically, production through an approval-gated environment.
5. Post-approval state (scheduled, published, failed, metrics) lives on the `ledger` branch, written by the bot only.
6. Personal data never enters git: lead and contact records stay in the CRM stores; the repo holds schemas and
   placeholders.

## Consequences

- Every public word has an author, a review, a timestamp and a diff. Rollback is a Pages rollback or a revert PR.
- Weekend and launch approvals depend on Avi merging; standing permissions (`ops/standing-permissions.md`) cover
  routine cases only once granted.
- Channels without a publishing API (Substack, LinkedIn company page) still publish by computer-use, but only from
  merged text, with the result recorded in the ledger.
- The repo is public (free plan, so rulesets and environments are enforced). Sensitive name lists are stored as
  salted hashes and the clear lists stay off-repo; this is obscurity for a lint list, not a secret.
