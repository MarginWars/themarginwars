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
- `qa_text_overflow.py` → every route at 360, 390, 768, 1024, 1280 and 1440. Fails if any text element's scrollWidth exceeds its clientWidth, or if text ink spills horizontally outside its element or card border box. Shared probe: `text_overflow_check.js` (also injected into `qa_spacing.py`). Page-level `documentElement.scrollWidth > innerWidth` is not enough: titles can collide inside the layout without widening the document.
- `make_sheets.py` / screenshot inspection → numerical results are never the sole visual acceptance gate.

## White/grey refinement
The final layer composes `relief.css` into `assets/suite.css` by default. It uses neutral reading surfaces, preserving the existing action hierarchy. `SUITE_RELIEF=0` is the prior-surface fallback. Latest rationale/release: `RELIEF_REPORT.md`; artifacts: `site_qa/relief_1108`. QA scripts accept `QA_OUT` for separate release evidence.

## Accent roles (Nov 10)
`roles.css` is appended last (`SUITE_ROLES=0` gives the fallback). Per-page-family accents (`--nm-fam`) are removed. On every page: sky for links, hover, keylines, eyebrow ticks and open disclosures; mint for selected, current, success and live; gold for focus (and `.nm-featured`); coral for deadlines, alerts and new; magenta only for CTAs to Contact. Census: `qa_accents.py`. Report: `site_qa/roles_1110/REPORT.md`.

## Spectrum band (Nov 10)
`band.css` is appended after `roles.css` (`SUITE_BAND=0` gives the fallback). It adds a six-segment band (sky, mint, gold, coral, grey #B7C1C9, violet #A08FE6), pinned to the top of every page at 6px, or 4px under 768px. The band also appears on eyebrow ticks, section keylines, hero edges, footers, the current nav item and selected controls (which now use an ink fill instead of mint). Repeated items take the six colours in turn. Research items are coloured by market. Report: `site_qa/band_1110/REPORT.md`.

## Polish (10 Nov 2026)

Layer order in `assets/suite.css`: suite, relief, balance, spacing, roles, band, **polish_cycle, polish**. Turn the layer off with `SUITE_POLISH=0`, which also skips `polish.js` and the polish HTML attributes.

- `polish_cycle.css`: the role-colour cycle (sky, violet, mint, grey, gold, coral) with an offset per group. Coral comes last. The old cycle lines in band.css were removed.
- `polish.css`, by section:
  - 0 cross-engine normalize (text-size-adjust, color-scheme light, scroll-padding, text-wrap, form controls 16px, focus-visible)
  - 1 card anatomy (index | heading | chevron)
  - 2 hover only on fine pointers, with `:active` on touch
  - 3 one heading and rule system, quiet notes
  - 4 mobile nav strip
  - 5 stacked tables under 640px
  - 6 next-step block
  - 7 images
  - 8 footer
  - 9 dvh
  - 10 forced colors
  - 11 print (reveal sections forced visible)
  - 12 radii (containers 12px, controls 6px, top keylines)
  - 13 Tracewire h1 on phones
  - 14 research preview-strip CLS
  - 15 one primary CTA per screen
  - 16 in-sentence link tap height
- `polish.js`: keeps the current nav item in view and toggles the edge fades (`nm-start` / `nm-mid` / `nm-end`).
- `apply_normalize.py` (polish block, idempotent):
  - landmark on `.f-preview`
  - `article[role=tabpanel]` becomes `section`
  - `aria-level=2` on an h3 that comes before the first h2
  - `tabindex=-1` on `main` (for the skip link)
  - `meta color-scheme` and `theme-color`
- QA:
  - `qa_matrix.py ENGINE core|devices PART PARTS`: Chromium, WebKit or Firefox. Core is every route at 375/390/768/1440. Devices is the named phones and tablets, plus landscape, 1280/1920/2560, dark, reduced motion, forced colors and 200% text, on 12 key templates.
  - `qa_diff.py SHOTS OUT [pct]`: the cross-engine pixel-diff gate.
  - `qa_journeys.py ENGINE WIDTH`: usability journeys.
  - `qa_spacing.py`: now ignores visually-hidden (1px clipped) blocks.

- Added after the first QA pass:
  - 17: two-row header at 768–1099px; non-sticky header when the screen is 500px or less tall in landscape
  - 18: reserved height for game panels until they mount (CLS)
  - in-text link detection (`a.nm-intext`), set in `apply_normalize.py`
  - `aria-level=2` on game-panel h3s in `assets/games.js`
  - Tracewire hidden hero uses id-level specificity, to beat wk.css `:not(#\#)`
- Final calm deployment: 345476f1.
