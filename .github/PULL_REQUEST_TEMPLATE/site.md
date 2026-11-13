<!-- Title: a Conventional Commit, at most 72 characters. It becomes the squash commit. Link the issue below. -->

## Summary

<!-- Site: pages, functions, workers or gates. What changed on which pages, and why. Closes #… -->

## Evidence

- [ ] `bash site/build.sh` and `bash site/build.sh check` pass (layers fixed point)
- [ ] `qa/run_gates.sh browser` green: text overflow (360–1440), spacing (320–1920), symmetry, contrast and targets (Chromium core)
- [ ] Nightly cross-engine matrix (Chromium, WebKit, Firefox) green before the production deploy
- [ ] Links, OG cards and axe checked for touched pages
- [ ] Functions: `node qa/functions/test_soldier.mjs` and any contract tests pass; no new runtime secret without a SECURITY.md row
- [ ] Rollback target recorded in the deploy PR comment

## Approval

Merge deploys to dev automatically. Production runs only when the deploy workflow is started by hand, and Avi
approves it in the `production` environment.

- Standing permission: <!-- SP-n or none -->
- Approvals rows: <!-- A-### or none -->
