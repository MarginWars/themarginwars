# Rollback

1. Find the rollback target: the previous production deployment id in the last deploy job summary or
   `ledger/deploys.jsonl`.
2. Roll back (Avi's OK, or Site & Release under SP-5 if granted): Cloudflare dashboard → Pages → `themarginwars` →
   Deployments → the target → **Rollback to this deployment**, or the API
   `POST /accounts/<CLOUDFLARE_ACCOUNT_ID>/pages/projects/themarginwars/deployments/<id>/rollback`.
3. `bash ops/ops_check.sh` must exit 0.
4. Record `{at, env: production, deployment_id: <target>, action: rollback, reason}` in `ledger/deploys.jsonl`.
5. Fix forward with a `fix:` PR. `main` is never force-pushed or reverted outside a PR.
