#!/usr/bin/env bash
# One-time GitHub setup for MarginWars/themarginwars. Run by Avi (org owner) or Site & Release with Avi's OK.
# Not run by CI. Idempotent where the API allows. Requires: gh authenticated as an org owner.
set -euo pipefail
R=MarginWars/themarginwars
AVI_ID=$(gh api users/AviShip-Type0 --jq .id)
# Repo settings: squash only, PR title as the commit, delete branches, no auto-merge, no wiki/projects-classic
gh api -X PATCH repos/$R -f allow_squash_merge=true -f allow_merge_commit=false -f allow_rebase_merge=false \
  -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY -f delete_branch_on_merge=true \
  -f allow_auto_merge=false -f has_wiki=false -f web_commit_signoff_required=false
# Secret scanning + push protection (free on public repos)
gh api -X PATCH repos/$R --input - <<'J'
{"security_and_analysis":{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}}
J
gh api -X PUT repos/$R/vulnerability-alerts || true
gh api -X PUT repos/$R/automated-security-fixes || true
# Actions: read-only GITHUB_TOKEN by default; Actions cannot approve PRs
gh api -X PUT repos/$R/actions/permissions/workflow -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false
# Environments
gh api -X PUT repos/$R/environments/dev --input - <<'J'
{"deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}
J
gh api -X POST repos/$R/environments/dev/deployment-branch-policies -f name=main -f type=branch || true
gh api -X PUT repos/$R/environments/production --input - <<J
{"wait_timer":0,"prevent_self_review":true,"reviewers":[{"type":"User","id":$AVI_ID}],
 "deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}
J
gh api -X POST repos/$R/environments/production/deployment-branch-policies -f name=main -f type=branch || true
# Rulesets (ledger needs the bots team id: gh api orgs/MarginWars/teams/marginwars-bots --jq .id)
gh api -X POST repos/$R/rulesets --input ops/github/ruleset-main.json
gh api -X POST repos/$R/rulesets --input ops/github/ruleset-tags.json
if [ -n "${BOTS_TEAM_ID:-}" ]; then sed "s/\"<BOTS_TEAM_ID>\"/$BOTS_TEAM_ID/" ops/github/ruleset-ledger.json | gh api -X POST repos/$R/rulesets --input -; fi
# Labels
python3 - <<'P'
import subprocess, yaml
for l in yaml.safe_load(open('.github/labels.yml')):
    subprocess.run(['gh','label','create',l['name'],'--repo','MarginWars/themarginwars','--color',l['color'],'--description',l['description'],'--force'],check=False)
P
echo "Now set secrets (values from Passwords & Vaults, never typed into chat):"
echo "  gh secret set CLOUDFLARE_API_TOKEN --env dev --repo $R ; same for --env production"
echo "  gh variable set CLOUDFLARE_ACCOUNT_ID --repo $R   (not secret)"
