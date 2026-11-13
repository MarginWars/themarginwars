# Consulting-fee funnel review (11 Nov 2026, PT). DRAFT, nothing changed

Read from the site source in site_calm/ (same build as production), channels/linkedin_page_draft.md, MARKETING.md and the X profile state as reported on 11 Nov.

## How a visitor reaches paid work today

1. **Site entry points.** Every page has a "Start a conversation" button (to /contact) and footer links to "Get the Briefing" (private Substack), "Book a talk" (to /speaking) and Contact.
2. **Advisory (/advisory).** Four offers with the prices already live on production:
   - Margin Teardown, 2 days: $17,500
   - Campaign Sprint, 6–8 days: $30,000–$40,000
   - Board sessions and workshops: "$500 per person per day"
   - Retained advisory: at least 16 hours a month, by proposal
   The page's only call to action is "Start a conversation" to /contact. No package has its own button.
3. **Speaking (/speaking).** Four signature talks, past stages and two videos, with "Fees on request". The call to action is "Enquire about a session" to /contact.
4. **Contact (/contact).** A form (/api/contact, Turnstile, stored in D1, with email and Slack alerts) with six topics: the four offers, a Briefing invitation and something else. It also shows a mailto to Avi's personal Gmail and his personal LinkedIn. There is no booking link and no stated reply time.
5. **Measurement.** cta_contact, form_contact and form_briefing events, plus UTM capture, via /api/mk/report.
6. **LinkedIn company page.** Filled in. The draft planned a "Visit website" (or "Contact us") button; the live button setting is not confirmed in files. No posts (soft launch).
7. **X @marginwars.** The bio links plainly to themarginwars.com (X's 100-character limit stopped the tagged link). 0 posts; the pinned intro is unposted.
8. **Games.** Spot the Leak carries a Teardown CTA at $17,500 (REVIEW_QUEUE item 16). The share flow is in preview.

## Existing rate references (no new prices proposed)

- Live on the site: the advisory prices above.
- Draft, not public: 09_Speaker_Kit.md §4 fee sheet, anchored on Avi's $5,000/day with a $3,500 floor: keynote $12,500, half-day workshop $12,500, full day $20,000, virtual $5,000. 03_Commercial_Model.xlsx A16 has the same anchor.
- Expert networks: $750 per 60 minutes, Avi's decision on 22 Oct 2026 (expert-networks/master-profile.md §6). Profiles are drafted, not submitted.
- **Inconsistency to resolve:** the site prices Board sessions and workshops at "$500 per person per day", but the speaker-kit fee sheet prices a half-day workshop at $12,500. Avi decides which is right. Nothing has been changed.

## Prioritised fixes

| # | Fix | Why | Approval? |
|---|---|---|---|
| 1 | Add a **booking link** ("Book a 20-minute scoping call") on /advisory, /speaking and /contact, using a Google Calendar appointment schedule on Avi's calendar | Every route today ends in a form or a mailto. A booked call is the shortest step to a fee | **Yes**: Avi's calendar, the tool, and a production change |
| 2 | **One button per package** on /advisory, linking to /contact?topic=teardown (sprint, board, retained), each with its own cta_ event | Shows which offer pulls; removes the topic-picking step | Build on preview: no. Production: **yes** |
| 3 | **Reconcile board/workshop pricing** (fix 2 above, the $500 vs $12,500 inconsistency) | Mixed price signals put serious buyers off | **Yes**: Avi sets prices |
| 4 | **A business inbox** (e.g. hello@ or <avi@themarginwars.com>) in place of the personal Gmail on /contact; also use it for press and Guest Pass forms that require a business email (Seamless) | Credibility, and some pass forms require it | **Yes** |
| 5 | **LinkedIn page button** set to "Contact us" → <https://themarginwars.com/contact?utm_source=linkedin&utm_medium=company-page&utm_campaign=always-on> | The page's main conversion slot | **Yes** (LinkedIn change) |
| 6 | **Pinned offer post** on LinkedIn and X ("Bring one bleeding number…", with a link to /advisory) | The first thing a profile visitor reads | **Yes**: public post, ends soft launch |
| 7 | **Talk-to-client bridge:** every talk deck ends on a tactic card with a QR code to `/contact?topic=teardown&utm_campaign=<event-slug>` | Turns each stage into tracked leads; the kit already promises a tactic card | No for drafting; **yes** for use |
| 8 | **Proof on /advisory:** an anonymised sample of the Teardown deliverable (ranked 90-day list) | Buyers want to see the output before paying $17,500 | **Yes** (content and confidentiality) |
| 9 | **Reply-time promise** on /contact (e.g. "We reply within 2 business days") plus the notify routing already built | Sets expectations; makes the form feel staffed | **Yes** (copy commitment) |
| 10 | **Game results to advisory:** a "Found a leak in your own statement?" link to /advisory on result cards | Uses game traffic | Preview: no. Production: **yes**. Bundle with the share-flow approval |
| 11 | **Expert-network profiles** (GLG, Third Bridge, AlphaSights, Guidepoint, Tegus) at the decided $750/hr | Paid work while the site funnel matures | **Yes**: submission is external |
| 12 | **Per-event UTM campaigns** (`utm_campaign=2027-<event>`) on every speaker bio link and press form | Attributes leads to events | No |

Nothing above has been changed on the site, LinkedIn or X.
