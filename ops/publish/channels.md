# How each channel publishes

| Channel | Route at launch (Mon 16 Nov 2026) | Longer-term route | Notes |
|---|---|---|---|
| Site (themarginwars.com) | GitHub Actions `deploy.yml`: merge to `main` → dev (`themarginwars-dev`); `production` environment (Avi approves) → prod (`themarginwars`), wrangler with `CLOUDFLARE_API_TOKEN` | Same | Same artifact promoted dev → prod (md5 manifest compared) |
| LinkedIn personal (Avi) | Computer-use in Avi's signed-in LinkedIn: paste the merged text, use LinkedIn's native **Schedule post** or post at the time | "Share on LinkedIn" (`w_member_social`) via a developer app with Avi's one-time OAuth; tokens expire and need re-auth [verify TTL] | Every LinkedIn change needs Avi's explicit OK = the merge (plus SP-1 for calendars) |
| LinkedIn company page | Computer-use with the page's native scheduler (Avi is admin) | Community Management API (`w_organization_social`) needs LinkedIn vetting; not achievable by Monday | Anitha as admin is Avi's call |
| X @marginwars | Computer-use in the box Chrome profile "Margin Wars (clean)" at the scheduled time | Connect @marginwars to the X connector, or an X API app with an @marginwars user token for `publish-x.yml` (paid tier [verify]) | Assert the handle before posting; the X connector is currently signed in to a different personal account |
| Substack | Computer-use: paste the merged issue, use Substack's native schedule | Same (no public publishing API) | Sign-in via Passwords & Vaults; public vs private at launch is decision D8 |
| Briefing (invite-only) | As Substack (private publication) | Same | The invite list lives in the CRM store, never in git |
| Speaker forms | Computer-use form filling after the pack merges (SP-4) | Same | Confirmation summary (no personal values) goes in `speaking/events/<event>/confirmation.md` |
| Speaker and media emails | Draft cards from merged text | Same | Never sent by an agent |
| Slack #margin-wars-ops digests | Slack connector post (needs Avi's OK for the channel) or `OPS_SLACK_WEBHOOK_URL` once created | Webhook | Totals only; no personal data |

X @marginwars computer-use uses only the box Chrome profile "Margin Wars (clean)". Never sign in to x.com in the default shared Chrome profile, because other workflows use it.
