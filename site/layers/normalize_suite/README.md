# Preview normalization layer
Authoritative step: `python3 normalize_suite/apply_normalize.py` AFTER feeds. `build.sh` is the full ordered build.

## Action hierarchy
- Magenta: primary conversion (existing solid CTAs only). Not category/body prose.
- Sky #8FB0E0: actionable secondary hover / link underline cue. Link text stays readable monochrome on light surfaces.
- Mint #3FBF85: selected filters/tabs, checked saved preferences, correct game answers. Black text, no arbitrary per-item colors.
- Gold #D2A63A: keyboard focus and genuinely expanded disclosure keylines.
- Coral #EA6259: incorrect game answers and existing near-deadline cues only; no new urgency claims.
- Disabled/coming-soon: neutral, no hover glow or fake link.

Neutral reading surfaces break up dark anchors. The About trial's colored section fields are removed. The Wire's three-control bar stays neutral until acted on. All facts, data, hrefs, handlers and form destinations are preserved.

## Coverage
`ROUTES.md` / `routes.json` inventory every emitted HTML route. Core, research indexes, every generated research detail, digest and games all receive the same final stylesheet. No template sampling is substituted for per-route render checks.
`site_qa/suite_1108` contains route/width/state screenshots, JSON findings and logs. Any remaining exclusions or blockers must be documented in REPORT.md before deploy.

## Rebuild
copy_weekend → ui → rb → tighten → about → feeds → normalize.
Removing the final stylesheet link/body `nm` class and rebuilding without this final step restores upstream rendering; content is never rewritten by this layer.

## Assistant confidentiality
The final step also rebuilds `review_deploy/functions/api/_knowledge.js` from the current public main content on six core pages. The old server snapshot contained the removed CV and disallowed colleague names. No private facts document is read. The output denylist in `soldier.js` now covers the full existing confidentiality rules; routing, rate limits, bindings and external send/submission handlers are unchanged. Local mocked-response tests are in `qa_function.mjs`.

## Release gates
- `qa_suite.py` (four shards) → 712 route/width/state cases.
- `qa_interactions.py` → 64 extra-width render cases, 3 actual search/preferences checks, 89 static no-JS route checks.
- `qa_actions.py`, `qa_keys.py` → actual action/answer/focus and keyboard/reduced-motion regressions.
- `qa_privacy.py` and `qa_function.mjs` → static/payload privacy and local output-guard tests.
- `make_sheets.py` / screenshot inspection → numerical results are never the sole visual acceptance gate.

## White/grey refinement
The final layer composes `relief.css` into `assets/suite.css` by default. It uses neutral reading surfaces, preserving the existing action hierarchy. `SUITE_RELIEF=0` is the prior-surface fallback. Latest rationale/release: `RELIEF_REPORT.md`; artifacts: `site_qa/relief_1108`. QA scripts accept `QA_OUT` for separate release evidence.

## Accent roles (Nov 10)
`roles.css` is appended last (`SUITE_ROLES=0` gives the fallback). Per-page-family accents (`--nm-fam`) are removed. On every page: sky for links, hover, keylines, eyebrow ticks and open disclosures; mint for selected, current, success and live; gold for focus (and `.nm-featured`); coral for deadlines, alerts and new; magenta only for CTAs to Contact. Census: `qa_accents.py`. Report: `site_qa/roles_1110/REPORT.md`.
