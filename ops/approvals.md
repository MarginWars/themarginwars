# Approvals queue

Written approvals that a gate or an agent can cite. Ids are permanent. Only Avi changes `status` (by merging a PR
that edits this file; CODEOWNERS applies). Status vocabulary: `proposed`, `approved`, `declined`, `expired`.
Items cite a row with front-matter `approvals: {<gated id>: A-###}`; the compliance gate accepts only `approved` rows.

| id | gated id / topic | What is approved (exact scope) | Approved by, when (PT) | status | expires |
|---|---|---|---|---|---|
| A-001 | paypal | Present-tense mentions on the live site copy (`site/**`) exactly as deployed to production in deploy 6d796b8f (10 Nov 2026) and its predecessors. Not content, speaker forms or pitches. | Avi, 12 Nov 2026, 5:51 PM PT | approved | none |
| A-002 | global_payments | Nothing yet. Any mention needs a new row. | | proposed | |
| A-DEPLOY | production deploys | Each production deploy is approved in the GitHub `production` environment by Avi (required reviewer). | Avi, plan approval 12 Nov 2026, 4:30 PM PT | approved | none |
| A-003 | production deploy, 12 Nov 2026 | Deploy the current test-site build of `main` (hello@ contact address) to themarginwars.com, and redeploy the contact-form mail service with the `MAIL_TO` code. Avi approved in chat; AviShip-Type0 approves the GitHub `production` environment on his behalf. Rollback target: Pages deployment 6d796b8f. Only once the nightly gate is green. Done 12 Nov 2026, 8:31 PM PT: nightly run 43363477188 green; deploy run 43365870666 put commit da2c4ae on production as Pages deployment 93316394. Live QA at 390/768/1280: text overflow 270, spacing 270, Chromium matrix 546 cases, 0 failing. | Avi, 12 Nov 2026, 7:01 PM PT | approved | after this deploy |
| A-REPO | public repo | `MarginWars/themarginwars` is public on the free plan; branch protection and rulesets enforced. | Avi, 12 Nov 2026, 4:30 PM PT | approved | none |
| A-BOT | bot account | Agents author PRs as a separate bot GitHub account; Avi approves. | Avi, 12 Nov 2026, 4:30 PM PT | approved | none |
| A-TOKEN | Cloudflare token | A Pages-Edit-only API token for this account, created and held by Passwords & Vaults, stored as the `CLOUDFLARE_API_TOKEN` environment secret. | Avi, 12 Nov 2026, 4:30 PM PT | approved | rotate every 90 days |
| A-GITHUB | source of truth | GitHub drives all digital content and interactions (ADR-0001). | Avi, 12 Nov 2026, 4:21 PM PT | approved | none |
