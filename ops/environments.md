# The Margin Wars: environments, promote and rollback

Last updated 10 Nov 2026, 5:35 PM PT. Secrets are never written here; names only.

## One build, two places

- `buildout/apply_buildout.py` — 404, contact form, Briefing links, next blocks, SEO, sitemap, robots, `_headers` (in place on `site_calm/`, idempotent)
- `marketing/apply_marketing.py` — first-party measurement script, attribution on the assistant escalation form, registry-minted UTM tags on every outbound LinkedIn/Substack link (see MARKETING.md)
- `buildout/make_dist.py` — copies `site_calm/` to **`site_dist/`**, self-hosts fonts, writes per-route CSS bundles

**`site_dist/` is the only deploy artifact.** Functions come from `review_deploy/functions/` (run wrangler from `review_deploy/`). Rebuilds are byte-identical (check md5 of every file across two builds).

| | Production | Dev |
|---|---|---|
| Pages project | `themarginwars` (branch `main`) | `themarginwars-dev` (branch `main`) |
| URLs | <https://themarginwars.com> (www → 301 apex); themarginwars.pages.dev | <https://themarginwars-dev.pages.dev> (+ per-deploy hash URLs) |
| Indexing | indexable; robots.txt allows + sitemap | `X-Robots-Tag: noindex` on every host (`_headers`), robots.txt `Disallow: /` (Function `functions/robots.txt.js` disallows every non-production host) |
| Contact store (D1 `CONTACT_DB`) | `themarginwars-contact` <D1_ID> | `themarginwars-dev-contact` <D1_ID> |
| KV `ESC_KV` / `SOLDIER_KV` | <KV_ID> / <KV_ID> (titles say "-review" but these ARE production) | `themarginwars-dev-escalations` <KV_ID> / `themarginwars-dev-soldier` <KV_ID> |
| Turnstile | widget `themarginwars-contact` sitekey 0x4AAAAAAF7re4tqJBnuPWrR | widget `themarginwars-dev-contact` sitekey 0x4AAAAAAF7sH18lHsCygRFq (assets/contact.js picks the key by hostname) |
| Secrets (names) | RL_SECRET, ESCALATIONS_TOKEN, TURNSTILE_SECRET, NOTIFY_EMAILS, QA_TOKEN, MK_REPORT_TOKEN, MW_ALERT_URL, MW_ALERT_SECRET (SLACK_WEBHOOK_URL deleted 10 Nov 5:32 PM PT) | RL_SECRET, ESCALATIONS_TOKEN, TURNSTILE_SECRET, QA_TOKEN, MK_REPORT_TOKEN (all dev-only values), NOTIFY_EMAILS (SLACK_WEBHOOK_URL deleted 10 Nov 5:31 PM PT), MW_ALERT_URL, MW_ALERT_SECRET (same alert route and signing secret as prod) |
| Plain vars | — | SITE_ENV=dev (every notification subject/post prefixed **[DEV]**) |
| Mailer | service binding `MAILER` → Worker `themarginwars-contact-mailer` | same Worker (stateless), subjects tagged [DEV] |
| Rate limit | `themarginwars-soldier-rl` Durable Object (needs prod RL_SECRET) + D1 cap 5/hour/IP | dev RL_SECRET is not accepted by the shared limiter, so dev falls back to the in-memory limiter + the dev D1 cap; never touches prod counters |

## Notifications (form)

- `{ok:true}` → done; the old webhook and MAILER are skipped (no double post). Row/record notify field = `harness:ok`.
- Non-2xx, timeout (25 s) or `ok:false` → logged (`harness-fail:<reason>` in `notify_error` / KV `notify`) and the MAILER email fallback runs if the route did not report mail delivered. **There is no Slack fallback** (recorded as `slack-fail:no-fallback`); `notified=1` means the email reached the team.
- Timeout is 25 s, not 5 s: the route replies after sending (measured 7–10 s), notify runs in `waitUntil` so visitors never wait, and aborting early makes the route drop its dedupe record (seen on dev: 5 s abort → double post).
- The old "Margin Wars Alerts" Slack webhook was **retired 10 Nov 2026, 5:32 PM PT per Avi (5:27 PM PT)**: code path removed, `SLACK_WEBHOOK_URL` deleted from both Pages projects, local file renamed `.retired`. The Slack app (<SLACK_APP>) is still installed but unused: no sanctioned connector or API here can revoke its webhook, so revoke it in Slack app settings (Incoming Webhooks) when convenient. The MAILER email binding stays as the fallback.

Pre-cutover paths (email still wired as fallback; the Slack item is historical):

Storage is always on: every valid submission is written to D1 first. Notifiers then run in the background and the result is recorded per row (`notified`, `notify_error`).

1. Email: Pages → `MAILER` service binding → Worker `send_email` (Cloudflare Email Routing on themarginwars.com). Sender `contact-form@themarginwars.com` ("The Margin Wars site"); Reply-To is the visitor so the team can answer by hand. Recipients come from the `NOTIFY_EMAILS` secret and must be (a) on the Worker allow-list (`contact_mailer/wrangler.toml`) and (b) **verified Email Routing destination addresses**. Visitors never receive anything automatically.
2. Slack (RETIRED 10 Nov 2026, 5:32 PM PT, historical): `SLACK_WEBHOOK_URL` posts to the **private** #margin-wars (<SLACK_CHANNEL>): kind, topic, name, company and record id. Never the email address or the message. Dev posts carry [DEV].
3. Every form uses the same notifier (`functions/api/_notify.js`): Contact and Briefing invitation (`/api/contact`, D1) and the assistant's "ask the team" escalation (`/api/escalate`, KV `ESC_KV`, notify result written back to the record).

Email status (10 Nov, 11:35 AM PT): {{contact.email}} and {{profile.anitha.email}} are both verified Email Routing destinations; production test 30ed0923 recorded `mail:ok` (2/2 sent) and arrived in {{contact.email}}. The sender needs nothing further: `send_email` from `contact-form@themarginwars.com` works because Email Routing is enabled on the zone.

Spam protection: Contact/Briefing and the assistant escalation both require Cloudflare Turnstile (server-side `functions/api/_ts.js`), plus honeypot and rate limits.

### Test submissions and the QA hook

```bash
npx wrangler d1 execute themarginwars-contact --remote --command "DELETE FROM submissions WHERE is_test=1"
```

## Ops check (daily routine)

`ops/ops_check.sh` (read-only, stores nothing, no visitor data): prod and dev uptime, every sitemap page = 200 on both hosts, 404 for unknown URLs, form endpoint health (GET 405, empty POST validation 422/400, nothing stored), sitemap, RSS/Atom/iCal 200 and production links with no preview labels, prod indexable / dev noindex, www → apex 301, SSL days left, live deployment ids (when wrangler is logged in). Prints a summary; exit 1 on any failure.

```bash
OPS_SLACK_WEBHOOK_URL=… bash ops/ops_check.sh --slack          # also post the summary (no PII) to public #margin-wars-ops
```

`OPS_SLACK_WEBHOOK_URL` is **not set yet**: #margin-wars-ops (<SLACK_CHANNEL>) needs its own incoming webhook (the existing webhook is bound to the private channel and must not be reused for ops). The surfaces register is refreshed with `python3 marketing/make_surfaces.py`.

## Promote dev → production (same artifact)

```bash
bash build.sh                         # once; record md5 manifest of site_dist
cd review_deploy
export WRANGLER_CACHE_DIR=/tmp/wrcache CLOUDFLARE_ACCOUNT_ID=<CLOUDFLARE_ACCOUNT_ID>
npx wrangler pages deploy ../site_dist --project-name themarginwars-dev --branch main --commit-dirty=true   # dev
# … QA on https://themarginwars-dev.pages.dev …
npx wrangler pages deploy ../site_dist --project-name themarginwars --branch main --commit-dirty=true       # production (needs Avi's OK)
```

Do not rebuild between the two deploys. Verify by comparing md5 of served files on both hosts against the local manifest (fetch `/x` not `/x.html`; Pages 308s `.html`).

## Rollback

Dashboard: Pages → themarginwars → Deployments → previous production deployment → "Rollback to this deployment". API:

```http
POST /accounts/<CLOUDFLARE_ACCOUNT_ID>/pages/projects/themarginwars/deployments/<DEPLOYMENT_ID>/rollback
```

Rollback restores static files and Functions of that deployment; bindings/secrets are project settings and are not rolled back (the previous builds ignore the new bindings).

## Deploy log

| When (PT) | Project | Deployment | Rollback target | What |
|---|---|---|---|---|
| 10 Nov 2026 17:32 | themarginwars (prod) | 6d796b8f-d678-4d20-834f-ae2f562ece39 | 91271ab7-0b5f-4d0a-9d4c-405cf8d8ba58 | old Slack webhook retired: no Slack fallback, MAILER email fallback kept; SLACK_WEBHOOK_URL deleted. Note: rolling back to 91271ab7 or earlier gives no webhook fallback, as the secret is gone |
| 10 Nov 2026 17:31 | themarginwars-dev | 9a58769f-4884-4a03-a554-e5a3af624668 | d1d1b33a-5319-4d08-9ce8-6690eaab46d9 | same functions, proven first |
| 10 Nov 2026 17:21 | themarginwars (prod) | 91271ab7-0b5f-4d0a-9d4c-405cf8d8ba58 | 6dc34813-cf6a-4659-9667-92f2ed31e82e | form alerts cut over to the signed alert route, old webhook + MAILER kept as fallback; same site_dist artifact |
| 10 Nov 2026 17:20 | themarginwars-dev | d1d1b33a-5319-4d08-9ce8-6690eaab46d9 | 6157baef | same functions, MW_ALERT_URL restored after the fallback test (interim dev deploys 84cb529f, 0fb97f60, 7d41b405 = 5 s timeout build, 25 s build, bad-URL fallback test) |
| 10 Nov 2026 11:39 | themarginwars (prod) | 6dc34813-cf6a-4659-9667-92f2ed31e82e | 7c141e26-f55b-4fa2-becb-4508fe95ec83 | Turnstile on the assistant "Talk to a human" form (QA_TOKEN bypass kept) |
| 10 Nov 2026 11:37 | themarginwars-dev | 6157baef | fca1bc89 | same artifact |
| 10 Nov 2026 11:29 | themarginwars (prod) | 7c141e26-f55b-4fa2-becb-4508fe95ec83 | d1460efb-e6d4-4335-84a7-dbc5a0aa06c8 | mk.js ignores automated browsers (Lighthouse/test runners) unless ?mk_test=1 |
| 10 Nov 2026 11:29 | themarginwars-dev | fca1bc89 | 2bd5ee4d | same artifact |
| 10 Nov 2026 11:22 | themarginwars (prod) | d1460efb-e6d4-4335-84a7-dbc5a0aa06c8 | 10e7366e-22ce-428c-920e-71587edb0960 | shared form notifier, escalation alerts, brand fixes (logo C favicon/OG, band order, wordmark rule, tagline), marketing instrumentation |
| 10 Nov 2026 11:15 | themarginwars-dev | 2bd5ee4d | cde76af0 | same artifact, proven first |

## Retired test surfaces (10 Nov 2026, per Avi 9:47)

- All 90 preview deployments of project `themarginwars` (branch `calm`) deleted; <https://calm.themarginwars.pages.dev> now 404. Production deployments kept as rollback targets.
- Local preview servers stopped: :8817 (site_dist), :8818 (site_calm backup), :8957 (site_calm), :8819 (about_rethink_1108), :8788 (wrangler pages dev).
- Untouched: `themarginwars-soldier-rl` (production rate limiter), other brands' projects and servers.

## Internal launch, Nov 10 2026

10 Nov 2026, 4:45 PM PT. Avi asked to launch The Margin Wars internally. This is an internal launch only. Soft launch stays: no public marketing, PR, LinkedIn posts or campaigns without Avi's explicit go.

- Production remains `6dc34813-cf6a-4659-9667-92f2ed31e82e`, rollback `7c141e26-f55b-4fa2-becb-4508fe95ec83`. Dev remains `6157baef`, rollback `fca1bc89`. No production deploy was made for this launch.
- Internal launch Page and Notion space were opened the same afternoon. The #margin-wars-ops announcement was drafted for Avi to send; it was not posted from this update.
- Forms, Turnstile, email routing (Avi's inbox verified; Anitha's copy sent but not inbox-confirmed), private #margin-wars summaries, first-party analytics and `GET /api/mk/report` were already live.
- Daily ops routine (`ops/ops_check.sh`) remains scheduled for first run 11 Nov 2026 around 8 AM PT, posting a summary to #margin-wars-ops. As of 11:40 AM PT the ops webhook was not yet set; the form-alert webhook must not be reused.
- Still open and Avi's call: Anitha as a LinkedIn admin; the magenta poster on Home; a real-iPhone check of the final build; a LinkedIn re-check against the branding audit.
