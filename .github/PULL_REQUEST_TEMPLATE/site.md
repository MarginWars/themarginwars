# Site PR (site/, functions, workers, gates)

## Change

<!-- What changed on which pages, and why. -->

## Evidence

- [ ] `bash site/build.sh` and `bash site/build.sh check` pass (layers fixed point)
- [ ] `qa/run_gates.sh browser` green: text overflow (360–1440), spacing (320–1920), symmetry/contrast/targets (Chromium core)
- [ ] Nightly cross-engine matrix (Chromium, WebKit, Firefox) green before the production deploy
- [ ] Links, OG cards and axe checked for touched pages
- [ ] Functions: `node qa/functions/test_soldier.mjs` and any contract tests pass; no new runtime secret without a SECURITY.md row
- [ ] Rollback target recorded in the deploy PR comment

Deploy: merge → dev automatically. Production only through the `production` environment, approved by Avi.
