# The `ledger` branch convention

`ledger` is an orphan data branch (no site or content code) that records what was actually published and how it
performed. It is **not** reviewed like `main`: only the bot account may push to it (ruleset `ledger-bot-only`),
force-pushes and deletion are blocked, and every line validates against `schemas/ledger-entry.schema.json`.

```
ledger/
  published.jsonl          # append-only, one entry per publish attempt (scheduled / published / failed / withdrawn)
  metrics/YYYY-MM-DD.jsonl # daily totals per item and campaign (no personal data)
  deploys.jsonl            # site deploys: {at, env, deployment_id, rollback_id, sha, manifest_md5, approved_by}
```

Create it once (bot account, after the first push of `main`):

```bash
git switch --orphan ledger
mkdir -p ledger/metrics && touch ledger/published.jsonl ledger/deploys.jsonl ledger/metrics/.keep
git add ledger && git commit -m "chore(ledger): start the publish ledger"
git push origin ledger
```

Commit messages on `ledger`: `chore(ledger): <id> <status>` or `chore(metrics): YYYY-MM-DD`.
