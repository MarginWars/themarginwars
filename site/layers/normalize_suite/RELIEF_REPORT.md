# White/grey refinement — calm preview handoff

## Direction retained
Technicolor is still an action system, not section paint: sky secondary hover, mint selection/correct answers, gold focus/expanded states, coral correction/reset/near-deadline keylines. Conversion magenta remains restrained. Existing spacing, 44px effective targets, control behavior and game-width fixes are retained.

## Surface decisions
- **Home Wire:** soft grey research workspace, dark ink, outlined actions; white saved-preference panel. The dark Home hero remains the orientation anchor.
- **Research suite:** soft grey page canvas, white reading cards and controls, dark title anchor. Applied to Wire, Calendar, Basis-Point Watch, route updates, Feeds and Digest, including every item route. Timeline labels/counts and previously pale fine print have light-context ink colors.
- **Route Brief:** grey workspace around a white working document; pale neutral radio faces, white evidence/source areas, original mint selection and gold keyboard focus.
- **About:** portrait hero retained; principles now white, field-record cards on soft grey, archive grey. No saturated section fields.
- **Games:** existing white panels on the shared soft-grey canvas; no mechanic or content changes. Other already-light core pages remain light rather than receiving artificial alternating stripes.

Tokens: white `#FFFFFF`, paper `#F4F6F7`, grey `#E9EDEF`, ink `#111417`, muted ink `#4A555B`, rule `#C2CBD0`. Dark anchors `#101315`. Action tokens unchanged: sky `#8FB0E0`, mint `#3FBF85`, gold `#D2A63A`, coral `#EA6259`.

## Sole copy change
Anitha terrain: **Australia & NZ · Singapore · Malaysia · Hong Kong · US · UK / EU · Global**.
Verified in `about_rethink_1108/ppl_section.html`, rebuilt `site_calm/about.html`, and public-only `review_deploy/functions/api/_knowledge.js`. The public About text diff is exactly one added `UK / EU` chip. No other facts or copy changed. No private facts file is deployed.

## Authoritative source / rebuild
Existing order retained: copy_weekend → ui → rb → tighten → about → feeds → normalize.
`normalize_suite/relief.css` is composed into the existing `/assets/suite.css` by the final normalization step. `SUITE_RELIEF=0` omits this surface refinement as a reversible local fallback; it does not remove the approved terrain correction. No repo checkout or git operations.

Compared with the previous release, the only changed publish/bundle files are `about.html`, `assets/suite.css`, and the derived public assistant knowledge. Feed datasets, links, game scripts, forms and server submission/send handlers are unchanged.

## QA and release
Final coverage/results and deployment URL are recorded below. Full artifacts are under `/workspace/deliverables/brand/site_qa/relief_1108/`. Route inventory remains `ROUTES.md`; per-route coverage is `COVERAGE.md`.

Representative captures: `home_wire_375.png` / `home_wire_1440.png`, `wire_first_375.png` / `wire_first_1440.png`, `wire_reading_375.png` / `wire_reading_1440.png`, `about_first_375.png` / `about_first_1440.png`, `about_full_375.png` / `about_full_1440.png`, `anitha_375.png` / `anitha_1440.png`. Captures prefixed `live_` are from the final unique deployment. Component-only captures hide the sticky global header to avoid screenshot stitching artifacts; full-page and first-fold captures include the real header.

## Limits
Chromium/Linux, not a real iPhone/Safari or an accessibility certification. No external sends/submissions, live paid AI calls or third-party video playback. No-JS static content remains available; JS-only games/search and existing coming-soon restrictions are unchanged. Mobile navigation retains its intentional local horizontal scrolling; document-level overflow is checked separately.

## Completed local release gates
- All 89 HTML routes: 375/768/1280/1440, default and expanded; 712 cases with zero final symmetry, document-overflow, effective-target, text-contrast or page-error findings.
- Home/About/Advisory/Deal/Wire/Calendar/Feeds/Digest also at 320/390/430/1024, both states: 64 additional render cases, clean.
- All 89 static routes visible without JS; 3 actual search/preferences flows; 19 existing keyboard/motion checks PASS; 12 actual selected/focused/search/calculated/answered states contrast-clean at 375/1440.
- Numerical checks plus visual inspection of all 18 final route atlases, both extra-width atlases and full-size representative captures. Light-context pale text on research controls, timeline summaries, status labels and fine print was found and fixed before acceptance. No layout blockers remain.
- Two full ordered rebuilds are byte-identical across 365 static/function files. Privacy scan covers 360 publish files and the derived public assistant payload; 18 local output-guard tests pass.

## Calm deployment
Unique preview: https://75f68cb3.themarginwars.pages.dev
About: https://75f68cb3.themarginwars.pages.dev/about
Wire: https://75f68cb3.themarginwars.pages.dev/wire/
Deployment `75f68cb3`, branch `calm`; Functions compiled/uploaded. No main/production or LinkedIn changes. All 89 live routes returned 200 with normalization; deployed CSS matches local bytes. Live About includes Anitha UK / EU and preserves Global/all other markets. Assistant GET returns expected 405; no live POST/AI call sent. Preview URLs are public unless separately protected.

Live mobile/desktop screenshots were also visually inspected after deployment: Home Wire, About first-fold/full-page, Wire reading view and Route Brief. No deployment-only differences found.
