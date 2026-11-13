# The Margin Wars — preview research desk

Preview only. Every surface is marked **Preview, pending Avi’s review**. No production publish, social post, automatic newsletter or recurring publishing routine has been created.

## Surfaces
- `/wire/`: market + type filters; static accessible content without JavaScript; item anchors.
- `/bp-watch/`: weekly top three; sourced direction + explicit method; no made-up basis-point savings.
- `/calendar/`: upcoming dates, then implementation history. `.ics` is a subscription URL, not just a one-off import.
- `/feeds/`: subscription hub, market feeds and Route Brief context-link changelog.
- Home: three-item Wire strip, automatically selecting the newest batch across distinct markets. Home + Advisory: dated context badges on four Route Briefs. These link to rule context; underlying recommendations are not silently rewritten.
- Autodiscovery in all HTML heads.

## Files and daily append procedure
Source of truth is `site_calm/assets/feeds/`:
1. Research only official sources. Confirm the source text and its status (proposal, draft, milestone or effective rule). Keep an official working URL; record access issues honestly. Never turn a draft, expectation or consultation into an effective rule.
2. Append a unique, stable ID to `wire.json`. Required: `id`, `date` (briefing date, YYYY-MM-DD), `market` (`us`, `ukeu`, `br`, `ca-latam`, `anz`, `global`), `type` (`network rule`, `regulation`, `policy`), `title`, `changed`, `hits`, `effective` (ISO date or null), `source`, `source_date` (announcement date if confirmed), `date_kind`. Optional `rank` controls ordering within the same briefing day; lower comes first. Do not reuse IDs. Future research batches use their own `date`; old item publication timestamps stay stable.
3. Append a calendar entry only for a genuinely dated milestone: `id`, `date` (event date), `added` (briefing publication date), `title`, `market`, `kind`, `description`, `source`, `wire_id`. All-day source-jurisdiction dates are intentional. Unconfirmed application dates remain off the calendar. Policy expectations are marked TENTATIVE in iCalendar.
4. For the weekly top three, update `bp-watch.json`: `id`, `date`, `title`, `market`, `impact`, `method`, `move`, `source`, `wire_id`. Preserve past IDs if retaining the archive. A numeric estimate requires a visible method and inputs. Current seed has no numeric savings claims.
5. For a genuine Route Brief change, append to `route-briefs.json`: `id`, `date`, `market`, `route_id` (existing rb.json scenario), `wire_id`, `title`, `description`, `source`. Current four entries explicitly describe context links, not changed recommendations.
6. Obtain Avi’s editorial approval before any production publication. No unattended publish step is configured.
7. Start the local QA server in a separate terminal if needed: `python3 -m http.server 8957 --directory site/dist`. Rebuild in order from the build workspace:
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
8. Review screenshots and `feeds/qa-ux/results.json`. Deploy PREVIEW only, from `review_deploy/`, to include functions:
   ```sh
   WRANGLER_CACHE_DIR=/tmp/wrcache CLOUDFLARE_ACCOUNT_ID=bebd3358c71defc8949c4e92ff14e925 npx wrangler pages deploy ../site_calm --project-name themarginwars --branch calm
   ```
   Never deploy `main` without fresh explicit approval.

Generator is re-runnable, preserves other workers’ layers and only replaces its own marked blocks. No missing original build pipeline is assumed. Seed helpers are historical bootstrap tools; daily research edits JSON, not seed.py. Do not run seed.py as a reset.

## Formats
All ten collections have RSS 2.0 `.xml`, Atom `.atom`, JSON Feed 1.1 `.json`: Wire global + six markets, BP Watch, calendar, Route Briefs. Calendar also has RFC 5545 `/feeds/dates.ics` with stable UIDs, CRLF and UTF-8-safe line folding. Cloudflare MIME rules are appended without replacing existing headers.

Feed URLs deliberately point to `https://calm.themarginwars.pages.dev` so preview subscriptions stay off production. Do not flip the base URL as a substitute for a separately approved production release.

## Source review / exclusions
- Curl checks are in `source-checks.json`; fetched primary material is private under `sources/`.
- EU PSR and PSD3 Council records were read directly. No guessed Parliament final-adoption, Official Journal or application dates.
- The Bank of England deferred the November 2026 RTGS release. No replacement date is invented.
- The Fed docket is a watch only: no asserted final Reg II cap, litigation conclusion or effective date.
- Omitted a claimed universal 3DS migration mandate: EMVCo’s v2.4 material is a draft, not a network-wide compliance deadline.
- Omitted Mastercard enhanced-data/AAV implementation dates because this run did not establish a current primary public scheme notice.
- Dropped the search claim that a Pix Automático refund reason was newly added in October 2026: the BCB changelog places that addition in August 2024. The actual October MonitorAccount default change is used instead.
- Visa Secure’s 2019 processing-reminder PDF is not treated as 2026 news. The public digest archive checked was largely 2024; no fabricated current mandate was added.
- NZ Commerce Commission’s current page was successfully read via WebFetch, confirming the 22 October decision and 22 April 2027 implementation. Curl receives 403 on that host (including PDFs); this is a source-access exception, not a dead-link claim. The authentic official URL is retained and flagged for review.
- Older implementation context is labelled rather than passed off as breaking news. Market labels are broad buckets, not claims of exhaustive jurisdictional coverage.

## Validation boundaries
`validate.py` uses feedparser + explicit RSS/Atom required-field checks, JSON Feed required fields and the icalendar RFC parser. The live Wire RSS and Atom were additionally accepted by the W3C Feed Validation Service. Atom has non-failing recommendations about a namespace prefix and shared batch timestamps. Browser QA covers 375 / 390 / 430 / 768 / 1024 / 1280 / 1440, default, no-JS, reduced motion, filters, copy interaction and grid symmetry. No physical iPhone or WebKit claim is made.

Known pre-existing Home no-JS overflow: `.tm-lane` / `.tm-s` market switchboard extends beyond the viewport at 1024 and 1280. The new strip itself has no overflow or asymmetric rows; existing market/UI worker owns that surface. No unrelated layout was overwritten to mask the failure.

## Home strip correction
Mobile-first stacked items at 375/390/430, scaling to three equal columns at 960+. It now inherits the shared `--edge` (1072px content width), uses `--sec` (64/96/120px) on both vertical edges, explicitly clears fixed/max heights and overflow clipping, and gives the preview label its own full-width row with 24px separation. `qa_strip.py` verifies edge equality, section rhythm and bottom-label clearance with and without JS, including Chrome iPhone emulation.

Feed deep-links select the matching Route Brief market and method before scrolling to its dated badge; the plain HTML fallback leaves all briefs readable without JS.

# Six UX upgrades — Nov 8 preview

## Impact first
Every Wire/calendar/BP/Route Brief update record has a merchant-action lead, a reviewed impact tag and native disclosure. Details collapse on listing pages and open on an individual item page. Only two Wire source facts support `cost down` today (Australian domestic interchange caps and NZ commercial-card regulation); other items use `deadline` or `neutral`. No invented cost-up or basis-point range. `assets/feeds/ux.json` holds `so_what`, `impact`, `rails`, and the matching official `source`; future unannotated items default to neutral, never an inferred savings claim. RSS, Atom and JSON descriptions also start with the action lead.

## My markets / rails
Pick markets and rails/controls once; checkbox changes save locally in `mw-feed-prefs-v1`. Empty selection means all. The same preferences apply across Wire, calendar, BP Watch, market subscriptions/route updates in the feed hub, and automatically selected Home highlights. `Show everything` resets the choices. Preferences are not sent to a server and do not silently alter downloaded RSS subscriptions. Without JavaScript all published HTML records remain available, with native details controls; inactive copy/preferences/search controls stay hidden.

## Dates
Countdowns use the current America/Los_Angeles calendar day and all-day source dates (UTC arithmetic avoids DST errors). Today through 90 days is highlighted; past dates are explicitly labelled. The per-market timeline is a compact native disclosure with a nearest-date countdown. Static HTML retains the actual event date rather than a stale hard-coded “in N days”.

## Item sharing
61 item pages have server-rendered OG metadata and 1200×630 PNG cards, generated deterministically in the normal build using the installed brand fonts, grain and magenta. Paths:
- `/wire/items/<id>/`
- `/calendar/items/<id>/`
- `/bp-watch/items/<id>/`
- `/route-briefs/items/<id>/`
- `/assets/feeds/cards/<kind>-<id>.png`
Copy LinkedIn/email text includes the official source, the item URL and the preview warning. Clipboard denial exposes selectable text. Nothing opens a composer, posts or sends a message.

## Weekly digest
`/digest/` is a one-page print edition; `/digest/2026-11-08/` is the initial dated archive. Editions are bucketed by Sunday week ending, rather than creating a new daily “weekly” archive. Later builds retain earlier edition directories. The current edition has three moves, five signals and the next three dates. `Save as PDF` opens the browser print flow; current A4 PDF output was tested as exactly one page. All PDF source links remain clickable. No automated external distribution or production publish is configured.

## Search / return visits
A build-time index (`assets/feeds/search-index.json`, mirrored as a deferred JS data asset) covers 61 rule, date, BP and Route Brief update records: full source-backed item text, titles, leads, markets, rails, dates and source URLs. Search is entirely client-side, respects My markets, uses `/`, ↑/↓, Enter and Escape, and restores focus to the opener. A native modal contains keyboard focus. Return-visit counts use localStorage plus a sessionStorage cutoff so navigating between pages does not reset the same visit’s count. First visits are labelled honestly, not reported as returning visits.

## New required build order
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
`apply_feeds.py` invokes `apply_feed_ux.py` itself; there is no extra publishing step. Feed changes are scoped to feed CSS/JS and generated surfaces. Home replacements are confined to the marked strip, its own assets and its own search dialog. No `wk.css` or shared tokens were edited. Coordination note for the UI worker: `feeds/UI_COORDINATION.md`.
