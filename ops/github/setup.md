# GitHub setup for MarginWars/themarginwars

Run once, in this order, by Avi (org owner) or by Site & Release with Avi's OK. `ops/github/setup.sh` does steps 3–7.

1. **Bot account.** Create the machine user (for example `marginwars-bot`) with its own email and 2FA; invite it to
   the `MarginWars` org; create team `marginwars-bots` containing only the bot; give the team **Write** on the repo.
   Agents commit and open PRs as the bot; Avi approves (GitHub blocks approving your own PR).
2. **Push.** From the box: `git remote add origin https://github.com/MarginWars/themarginwars.git`,
   `git push -u origin main`, then `git push origin fix/restore-buildout-css` and open its PR.
   Push `main` **before** applying rulesets (step 6), or the first push needs a temporary bypass.
3. **Repo settings.** Squash merge only (title = PR title), delete head branches, no auto-merge, no wiki;
   Actions: default token read-only, Actions may not approve PRs; require approval for first-time contributors.
4. **Security.** Secret scanning and push protection on; Dependabot alerts and security updates on;
   private vulnerability reporting on (`SECURITY.md`).
5. **Environments.**
   - `dev`: deployment branches `main` only. Secret `CLOUDFLARE_API_TOKEN`.
   - `production`: required reviewer `@AviShip-Type0`, prevent self-review, deployment branches `main` only.
     Secret `CLOUDFLARE_API_TOKEN` (may be the same token or a separate production-only one).
   - Repository variable `CLOUDFLARE_ACCOUNT_ID` (not secret, but kept out of files).
6. **Rulesets** (`ops/github/ruleset-*.json`):
   - `main-protected` on the default branch: PR required, 1 approval, code-owner review, dismiss stale approvals,
     approval of the last push, conversations resolved, squash only, linear history, no force-push, no deletion,
     required checks `compliance`, `frontmatter-limits`, `claims`, `links-docs`, `secrets`, `standards-lock`,
     `functions`, `site-build`, `site-gates` (strict). **No bypass actors**, so the bot cannot bypass.
   - `ledger-bot-only` on `refs/heads/ledger`: no deletion, no force-push, updates restricted; bypass only for the
     `marginwars-bots` team (set `BOTS_TEAM_ID`).
   - `release-tags` on `prod-*` and `v*` tags: no update or deletion.
7. **Labels** from `.github/labels.yml` (the `labels` workflow keeps them in sync after that).
8. **Repository secrets for CI** (all optional; checks degrade to the public-safe subset without them):
   - `COMPLIANCE_EXTRA_TERMS`: the clear-text restricted names list, one per line (adds to the hashed list).
   - `MW_GUARD`, `MW_GUARD_TESTS`: the site assistant's guard JSON and its test cases (the `functions` job runs the
     full 19 tests when present, the fail-closed test otherwise).
   - `QA_TOKEN`: the contact-form QA bypass token for live form checks (nightly, later).
   - `MK_REPORT_TOKEN`: read token for `/api/mk/report` metrics (Channels, later).
9. **Cloudflare Pages secrets** on both `themarginwars-dev` and `themarginwars`: `MW_GUARD` (required before the
   first deploy from this repo; without it the assistant answers 503).
10. **Projects board** (Launch Command): fields Status, Workstream, Channel, Schedule, Live URL; views Launch,
    Calendar, Speaking, Waiting on Avi, Board.
11. Optional: Anitha as a second code owner on `content/**` and `speaking/**` (decision D5), via CODEOWNERS PR.

Note: the first runs of `site-build` and `site-gates` on `main` are expected to fail until the
`fix/restore-buildout-css` PR merges (see its description). Merge that PR first.
