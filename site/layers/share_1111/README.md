# Game share flow (11 Nov 2026), staged, not deployed

- `share.js`, `share.css`: result card (six-colour band, M mark, score, band-colour grid, date or game number), Share on X (x.com/intent/post, text + tagged link, X-weighted length kept <= 280), Share on LinkedIn (share-offsite with tagged URL; copies the result text first and says "Text copied, paste it into your post."), Copy result, native share sheet on touch devices, Download card (1200x630 brand canvas).
- `apply_share.py TARGET`: patches a built copy (games.js, tracewire.js, 15 pages' meta, Arcade hub row), writes `assets/brand/og/<game>.png`. Idempotent; refuses `site_calm`.
- `deploy/functions`: copy of review_deploy/functions with share_* events added to CLIENT_EVENTS.
- `deploy_preview.sh`: rebuild dist from site_dist, run checks, deploy to themarginwars-dev branch `game-share` (preview). Refuses production. Needs wrangler auth.
- QA: `qa/` (screenshots, layout_chromium.json, layout_firefox.json, spacing_vs_prod.json, flow.json, axe.json, og.json, surfaces.json, curl_results.txt, curl_roundtrip.txt, privacy.json).
- `qa_unparked/` is a local-only QA copy with Tracewire and Episodes 2-3 un-parked to test their share flow; never deploy it.
