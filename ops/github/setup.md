# GitHub setup for MarginWars/themarginwars

State as applied on 12 Nov 2026 (PT), and what changes later. `ops/github/setup.sh` is the original one-shot
script; the JSON files in this folder are the source of truth for the rulesets.

## Applied now

| Area | Setting |
|---|---|
| Repo | Public. Squash merge only (title = PR title, message = PR body), delete head branches on merge, no auto-merge, no wiki |
| Actions | Default `GITHUB_TOKEN` read-only; Actions cannot approve PRs |
| Security | Secret scanning and push protection on; Dependabot alerts and security updates on; private vulnerability reporting on |
| Environment `dev` | Deployment branches: `main` only. Secret `CLOUDFLARE_API_TOKEN` |
| Environment `production` | Required reviewer `@AviShip-Type0`; **prevent self-review off** (see below); deployment branches `main` only. Secret `CLOUDFLARE_API_TOKEN`. Deploys only by manual dispatch of `deploy.yml` |
| Variable | `CLOUDFLARE_ACCOUNT_ID` (repository variable) |
| Ruleset `main-protected` (`ruleset-main.json`) | PR required, **0 approvals, no code-owner review** (see below), stale approvals dismissed, conversations resolved, squash only, linear history, no force-push, no deletion, no bypass actors. Required checks (strict): `compliance`, `frontmatter-limits`, `claims`, `links-docs`, `secrets`, `standards-lock`, `functions`, `site-build`, `site-gates` |
| Ruleset `ledger-bot-only` (`ruleset-ledger.json`) | `refs/heads/ledger`: no deletion, no force-push, updates restricted; bypass only for team `marginwars-bots` (members: `marginwars-bot` only) |
| Ruleset `release-tags` (`ruleset-tags.json`) | `prod-*` and `v*` tags cannot be updated or deleted |
| Labels | From `.github/labels.yml`; the `labels` workflow keeps them in sync |
| Cloudflare Pages secrets | `MW_GUARD` on `themarginwars-dev` and `themarginwars` |
| Contact mailer Worker | `themarginwars-contact-mailer` is deployed separately (wrangler, not CI); secret `MAIL_TO` set |

## Why two protections are relaxed today

Until now every PR is authored by `AviShip-Type0`, and Avi is the only human reviewer. GitHub blocks approving
your own PR and, with prevent self-review, approving your own deployment. With the target settings nothing could
merge or deploy. So, temporarily:

- `main-protected` requires 0 approvals and no code-owner review (the required checks still gate every merge).
- `production` allows the person who started the deploy to approve it.

## Re-tighten plan (waits for a working bot login)

`marginwars-bot` is in the org and the `marginwars-bots` team, but its password is being fixed at Avi's next
Touch ID session. Re-tighten only after the bot can sign in and has opened and pushed at least one PR, so Avi is
never locked out:

1. Agents commit and open PRs as `marginwars-bot` (its own credentials; never Avi's session).
2. Apply `ruleset-main.target.json` to ruleset `main-protected`: 1 approval, code-owner review, approval of the
   last push. `gh api -X PUT repos/MarginWars/themarginwars/rulesets/<id> --input ops/github/ruleset-main.target.json`
3. Turn on prevent self-review for `production` once deploys are dispatched by the bot (or a second reviewer exists).
4. Copy the target file over `ruleset-main.json` in the same PR, so the repo keeps describing what is applied.

Optional later: Anitha as a second code owner on `content/**` and `speaking/**` (decision D5).

## Secrets reference (values live in Passwords & Vaults; never in git)

- Environments `dev`, `production`: `CLOUDFLARE_API_TOKEN` (Pages edit only; it cannot manage Workers).
- Optional repository secrets: `COMPLIANCE_EXTRA_TERMS`, `MW_GUARD`, `MW_GUARD_TESTS`, `QA_TOKEN`, `MK_REPORT_TOKEN`.
- Pages projects: `MW_GUARD` (required; without it `/api/soldier` answers 503).
- Worker `themarginwars-contact-mailer`: `MAIL_TO` (a verified Email Routing destination). Redeploying the Worker
  from `site/workers/contact_mailer/worker.js` needs a token with Workers Scripts edit and the private
  `wrangler.toml` (send_email allow-list), and Avi's OK.
