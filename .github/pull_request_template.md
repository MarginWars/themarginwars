# Pull request

<!-- Title: a Conventional Commit, at most 72 characters. It becomes the squash commit. -->

## Summary

<!-- One paragraph: what this changes and why. Link the issue. -->

## Workstream and channel

- Workstream: <!-- site | channels | content | publications | speaking | media | pipeline | research | launch | ops -->
- Channel(s): <!-- linkedin-personal | linkedin-company | x | substack | briefing | site | speaking-form | email-draft | none -->
- Scheduled times (PT): <!-- every schedule in the PR, or "none" -->

## Rules

- [ ] No secrets, tokens, webhook URLs or personal data (phones, addresses, private emails, lead records, submissions)
- [ ] Nothing on the private denylist; approval-gated names carry an `approvals:` row that is approved in `ops/approvals.md`
- [ ] First names only on site material; no invented facts, stats, quotes or war stories
- [ ] Every number cites `sources:` or is marked `[Assumption]` (claims gate)
- [ ] Channel character limits pass (`qa/limits.yml`)
- [ ] For site changes: built, spacing, text-overflow and symmetry gates pass at every width; screenshots attached as CI artifacts
- [ ] Emails stay draft cards; nothing here sends, posts, deploys or submits by itself

## Approval

<!-- Merging = Avi's approval of record for exactly what is in this PR.
If a standing permission applies, cite it (SP-n from ops/standing-permissions.md).
Fees, spend or new public claims need a row in ops/approvals.md. -->

- Standing permission: <!-- SP-n or none -->
- Approvals rows: <!-- A-### or none -->
