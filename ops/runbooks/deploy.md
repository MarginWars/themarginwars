# Deploy

| Environment | Pages project | Trigger | Gate |
|---|---|---|---|
| dev | `themarginwars-dev` (branch `main`) → https://themarginwars-dev.pages.dev | every push to `main` touching `site/**` (= merged PR) | required checks on the PR; `site/dist.md5` must match the build |
| production | `themarginwars` → https://themarginwars.com | manual only: Actions → deploy → Run workflow → `production` (never on push) | `production` environment: Avi approves; latest nightly on `main` green |

Both run `npx wrangler@4 pages deploy dist` from `site/`, so `site/functions` deploy with the static build.
Secrets: `CLOUDFLARE_API_TOKEN` in each environment (Pages:Edit for this account only); variable `CLOUDFLARE_ACCOUNT_ID`.

Before the first deploy from this repo, set the Pages secret `MW_GUARD` on **both** projects
(`wrangler pages secret put MW_GUARD --project-name <project>`, value from Passwords & Vaults). The site assistant's
guard list lives there, not in git; without it `/api/soldier` answers 503 by design.

Manual deploy: Actions → deploy → Run workflow → `dev` or `production` (main only).

Every production deploy writes the new deployment id and the previous one (the rollback target) to the job summary;
Site & Release copies both to `ledger/deploys.jsonl`.
