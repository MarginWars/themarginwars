# Feed UX — calm preview

Built and verified Nov 08, 2026, 07:01 AM PST.

Preview: https://f537a984.themarginwars.pages.dev (alias https://calm.themarginwars.pages.dev).
Deployment: `f537a984-97f1-465b-89ab-c11bb78f545c`; environment Preview; branch calm. No production deployment, external post, email, newsletter or new routine.

## Six upgrades
1. Impact first: merchant-action lead, reviewed tag, native collapsible details. Source-backed cost-down tags only; no fabricated savings ranges. Includes Route Brief context updates, which explicitly leave recommendations unchanged.
2. My markets: market + rail/controls preferences persist locally across Wire, calendar, BP Watch, subscription hub and Home. No-JS shows all. Preferences do not alter the contents of downloaded RSS subscriptions.
3. Calendar: Pacific-calendar-day countdowns, next-90-day highlights, per-market timelines. The summary recomputes the nearest matching future event after rail changes or clock changes. Actual source dates remain the no-JS fallback.
4. Share: 61 dedicated OG item pages and 1200×630 branded PNGs, LinkedIn/email copy snippets including the primary source, selectable-text fallback when clipboard permission is unavailable. Nothing sends or posts.
5. Digest: latest complete Sunday-ending week at `/digest/`, dated archive, print CSS and Save as PDF. Both 375 and 1440 tests produce one A4 page with clickable sources.
6. Search: full client-side index, `/`, arrows, Enter and Escape, native dialog focus containment/restoration, My markets integration, and session-stable since-last-visit counts.

## Pages and feeds
- https://f537a984.themarginwars.pages.dev/wire/ — 31 Wire records.
- https://f537a984.themarginwars.pages.dev/bp-watch/ — 3 weekly moves.
- https://f537a984.themarginwars.pages.dev/calendar/ — 23 dated milestones: 12 upcoming and 11 historical in this edition.
- https://f537a984.themarginwars.pages.dev/feeds/ — hub + 4 Route Brief context updates.
- https://f537a984.themarginwars.pages.dev/digest/ and https://f537a984.themarginwars.pages.dev/digest/2026-11-08/.
- https://f537a984.themarginwars.pages.dev/ — corrected shared-edge, unclipped Home strip.
- RSS: `/feeds/wire.xml`, `/feeds/wire-{us,ukeu,br,ca-latam,anz,global}.xml`, `/feeds/bp-watch.xml`, `/feeds/calendar.xml`, `/feeds/route-briefs.xml`. Each also has Atom `.atom` and JSON Feed `.json`: 30 collections total.
- Calendar subscription: https://f537a984.themarginwars.pages.dev/feeds/dates.ics.
- Example OG item: https://f537a984.themarginwars.pages.dev/wire/items/nz-commercial-cards/.
- Example Route Brief update: https://f537a984.themarginwars.pages.dev/route-briefs/items/us-bank-context-20261108/.
- Example card: https://f537a984.themarginwars.pages.dev/assets/feeds/cards/wire-nz-commercial-cards.png.

All generated surfaces are labelled Preview, pending Avi’s review. Feed autodiscovery remains in all page heads. New styles are feed-owned; no wk.css/global tokens changed.

## Daily append
Read `feeds/README.md` for schemas. Append official-source-backed records under `site_calm/assets/feeds/`: `wire.json`, optional `calendar.json`, weekly `bp-watch.json`, and genuine context changes in `route-briefs.json`. Add/review the matching `ux.json` annotation: concise `so_what`, sourced impact tag, relevant rails and matching official URL. New unreviewed annotations default neutral, not savings. Verify official URLs and the source text/status; do not turn drafts into mandates or unknown dates into calendar events.

From the build workspace, run:
```sh
python3 copy_weekend/apply_copy_weekend.py
python3 copy_tighten/apply_tighten.py
python3 ui_weekend/apply_ui.py
python3 route_brief/apply_rb.py
python3 copy_tighten/apply_tighten.py
python3 feeds/apply_feeds.py
feeds/.venv/bin/python feeds/validate.py
python3 feeds/qa_feed_ux.py
python3 feeds/qa_feed_ux_extra.py
```
`apply_feeds.py` invokes `apply_feed_ux.py`. Consecutive runs produce no changed site files. Review first; deploy only the approved calm preview using the exact README command. No automated publishing configured.

## QA and caveats
- Seven widths: 375 / 390 / 430 / 768 / 1024 / 1280 / 1440, default + expanded, JavaScript + no-JS + reduced motion: 252 render checks.
- No feed-owned overflow, asymmetric rows or browser script errors. Native keyboard controls, persisted preferences across five surfaces, clock changes, filtered timeline summaries, clipboard fallback, all 61 OG pages/images and mobile >=44px targets passed.
- Separate Home strip check: 14 passes for shared edge, 64/96/120 rhythm, preview-label/bottom clearance, no-JS and Chrome iPhone emulation.
- Live immutable preview: 24 desktop/mobile render checks, functional controls, PDFs and 15 endpoint/MIME checks passed. W3C independently accepted final live Wire RSS and Atom; Atom has non-failing namespace/timestamp recommendations. All 30 feed formats and 23 ICS events passed local structural/parsing validation.
- Outstanding UI-owner issue: pre-existing Home market switchboard `.tm-lane` / `.tm-s` no-JS horizontal overflow at 1024 and 1280, in both expanded/default checks (four flags). Not caused by the new strip; no unrelated UI was clipped or overwritten. Handoff in `UI_COORDINATION.md`.
- Feed-owned entity audit passes. `entity-audit.json` notes an unrelated About job-title phrase for the copy owner, plus Fed URL substring false positives.
- No physical iPhone/WebKit claim. NZ Commerce Commission material was readable with WebFetch but curl returns 403: retained as a documented source-access exception. All other source-check details are in `source-checks.json`.
- Excluded unsupported final PSD3/PSR application dates, a final Reg II rate/deadline, a universal 3DS migration mandate, unverified current scheme implementation dates and a Pix refund change incorrectly attributed to October 2026. Older implementation context is labelled, not presented as breaking news.

## Requested screenshots (live preview)
- Screenshots (375 and 1440 for each surface: wire-mymarkets, wire-expanded, share-card, calendar-countdown, digest-print, search, home and more) are QA artefacts kept off the repo.

QA artifacts: `qa-ux/results.json`, `qa-ux/additional-results.json`, `qa-ux/idempotence.json`, `qa-ux/live/results.json`, `qa-ux/live-checks.json`, `qa-ux/w3c-wire-xml.html`, `qa-ux/w3c-wire-atom.html`, `final-deploy.json`.
