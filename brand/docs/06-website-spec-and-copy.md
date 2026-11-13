# Website Build Spec and Draft Copy - The Margin Wars / Avi Reddy Advisory


## 1. Purpose and tone

- **Job of the site:** make it easy for a payments or finance leader, or an event organiser, to see in 30 seconds that Avi offers specific margin tactics (not trend commentary), trust that he has done this at scale, and get in touch.
- **Positioning line:** "The operator's playbook for winning back payment margin, one tactic at a time, in every market you sell in."
- **Public footprint is deliberately light:** the site is the only public home of The Margin Wars apart from one quarterly LinkedIn excerpt. No subscribe box, no follower counts, no blog feed.
- **Tone:** operator-credible, understated, problem-led. No "thought leader" language, no follower counts, no logo walls until clients have agreed.
- **Primary call to action:** "Discuss a margin problem" (contact). Secondary: "Request an invitation" to The Margin Wars Briefing (invite-only; Avi approves each request).

## 2. Sitemap

| Page | File | Purpose | Primary CTA |
|---|---|---|---|
| Home | index.html | Positioning line, four ways in, tactic-card format, the 12 Playbook tactics, recent stages | Discuss a margin problem; Request an invitation |
| About / war stories | about.html | Background (naming rule applied), stages, war-story slots, confidentiality note | - |
| Advisory | advisory.html | Offer ladder: Margin Teardown ($17.5K), Cross-Market Expansion or Stablecoin Cost Sprint ($30-40K), board sessions and workshops, retained advisory (by proposal) | Start a conversation |
| Speaking | speaking.html | Four signature talks (flagship: "Payment tactics for margin wars"), formats, past stages table (from 08), organiser info; fees on request (fee sheet in 09) | Enquire about a session |
| Briefing | writing.html (nav label "Briefing") | The Margin Wars Briefing: who it is for, format, what it excludes, one public tactic-card excerpt | Request an invitation |
| Contact | contact.html | Email, LinkedIn, X, what to include | Email |

Later (not in the draft): speaker kit PDF (from 09), privacy notice. No essay archive: issues stay private, with one public excerpt a quarter.

## 3. Technical spec

| Item | Specification |
|---|---|
| Build | Plain static HTML + one CSS file; no JavaScript, no cookies, no third-party trackers |
| Hosting (Avi to choose at G3) | Any static host with free TLS (for example Cloudflare Pages, Netlify or GitHub Pages); no server to maintain |
| Domain | Avi buys it himself at Gate G3 (shortlist in Section 5); point the apex and `www` to the host |
| Email | Professional address on the chosen domain |
| Briefing | Private: Substack in Private mode or Ghost with "Only people I invite" (07 Section 3). The site links only to "Request an invitation" (contact) |
| Accessibility | WCAG 2.2 AA: semantic headings, colour contrast, alt text on headshots, keyboard-navigable |
| Performance | Under 200 KB per page; system fonts; optimised headshot images |
| SEO | Unique title and meta description per page (in the copy below); schema.org `Person` and `ProfessionalService` markup at launch; sitemap.xml and robots.txt at launch; remove `noindex` only at go-live |
| Analytics | Optional privacy-friendly, cookieless analytics; decide at G3 |
| Legal | Footer disclaimer ("Views are my own and do not represent any employer or client"); privacy notice if a contact form or analytics is added |
| Compliance gate | Nothing goes live until Gate G0 (employer outside-activity approval; client consent for naming) is cleared |

## 4. Page copy (as built in the draft site, revised 21 Oct 2026)

Generated from the built pages (`build/build_site.py`), so the copy here and the HTML match. Naming rule: the employer is "a large payments network" and the anchor client "a large merchant acquirer" until written approval.

### Home (index.html)

- **Title tag:** The Margin Wars - payment tactics for winning back margin | Avi Reddy
- **Meta description:** Avi Reddy shows payments and finance leaders specific moves to win back payment margin - routing, network tokens, retries, interchange++, chargebacks, FX, PayFac economics and stablecoin settlement - across the US, UK/EU, Africa and APAC.

**H1:** The operator's playbook for winning back payment margin, one tactic at a time, in every market you sell in.

I am Avi Reddy, a payments product executive at a large payments network. Through The Margin Wars I show payments and finance leaders specific moves, not trends: routing, network tokens, retries, interchange++, chargebacks, FX, PayFac economics and stablecoin settlement, and how each one plays in the US, UK/EU, Africa and APAC.

**Button/link:** Discuss a margin problem | **Button/link:** Request an invitation to the Briefing

#### Four ways in

**The Margin Wars Briefing**

Invite-only and monthly. One tactic per issue, for about 150 senior payments operators.

**Working Sessions**

Closed-door sessions for 8-12 peers, each on one lever, held around major conferences in different regions.

**Margin Teardown**

Two days on your own data, ending in a prioritised 90-day list of moves.

**Advisory**

Sprints and retained advice for cross-market expansion and stablecoin cost decisions.

#### Every tactic, the same way

- **The move** and how it works, step by step
- **Prerequisites**: contracts, data, systems, people
- **Metrics and impact range**, sourced or labelled as an assumption
- **Failure modes**, early warnings and rollback
- **Owner**: who decides, who builds, who watches the number
- **Cross-market column**: US, UK/EU, Africa, APAC

#### The Margin Wars Playbook: first 12 tactics

1. Re-route an under-performing BIN range to a second acquirer
2. Turn on network tokens for card-on-file
3. Set a retry schedule for soft declines
4. Renegotiate interchange++ pass-through
5. Build a chargeback representment workflow
6. Pass Level 2/3 data on commercial cards
7. Decide where the FX markup sits, and when to acquire locally
8. Re-price sub-merchants as a PayFac
9. Set marketplace payouts and reserves by seller risk tier
10. Steer one high-cost segment to pay-by-bank or a local APM
11. Exit-proof your orchestration before you sign
12. Run stablecoin settlement on one corridor as a cost line

#### Recent stages

Snowflake Summit 2025 (keynote), Money20/20 USA 2024, Fiserv Forum 2024 and MRC Las Vegas 2024 (host).  | **Button/link:** Speaking

### About (about.html)

- **Title tag:** About Avi Reddy - The Margin Wars
- **Meta description:** About Avi Reddy: payments product executive at a large payments network, with payments experience in the US, the UK and South Africa, and the operator behind The Margin Wars.

**H1:** About Avi

I have spent my career on the parts of payments where margin is won or lost: how a transaction is routed, approved, priced, disputed, converted and settled, at a scale where a few basis points add up to real money.

#### Background

Avi Reddy is a payments product executive at a large payments network, where he works on enterprise platforms and merchant experience.

He has worked in payments in the US, the UK and South Africa, and co-founded the South African companies Rentoza and Effectus Capital.

He advises payments companies on stablecoin strategy, including a current engagement with a large merchant acquirer.

#### Where I have spoken

- Snowflake Summit 2025, San Francisco: keynote co-presenter with Fiserv
- Money20/20 USA 2024, Las Vegas: merchant cloud data sharing, with Snowflake
- Fiserv Forum 2024, Las Vegas: "Future is PayFac and GenAI" panel
- MRC Las Vegas 2024: host, "Marketplaces on the Rise: Payments and Risk"

#### A note on confidentiality

Stories are shared with details removed or changed so that no employer, client or customer can be identified. No employer or client data is used. Views are my own.

### Advisory (advisory.html)

- **Title tag:** Advisory - margin teardowns, cross-market and stablecoin cost sprints | Avi Reddy
- **Meta description:** Operator-led advisory on payment margin: two-day Margin Teardowns, Cross-Market Expansion and Stablecoin Cost Sprints, board sessions and retained advice.

**H1:** Advisory

I take on a small number of engagements where an operator's judgement changes the number. Each one is scoped to a decision, a set of moves and a deliverable.

**Button/link:** Start a conversation

#### Ways to work together

**Margin Teardown**

Two days on your own payments data: routing, approvals, pricing, disputes and FX. You get a prioritised 90-day list of moves with owners. **$17,500.**

**Cross-Market Expansion or Stablecoin Cost Sprint**

Six to eight days on one decision: how to acquire and price in a new market, or whether stablecoin settlement beats your current rail on cost. **$30,000-$40,000.**

**Board sessions and workshops**

A closed-door briefing or a half- or full-day workshop for a leadership team or board on the margin levers in front of them.

**Retained advisory**

Senior advice through a defined programme, with the Playbook refreshed quarterly for your markets. By proposal.

#### Typical questions I help answer

- Which BIN ranges, issuers or markets are costing us approvals, and where should that traffic go?
- Are we paying a fair acquirer markup, and what would interchange++ pass-through change?
- Which disputes are worth fighting, and what should the workflow look like?
- Where should the FX markup sit, and when does local acquiring pay for itself?
- Does stablecoin settlement beat our current cross-border rail on all-in cost?

#### How engagements run

- Short scoping call, then a written proposal with a fixed fee and a clear deliverable.
- Conflict checks before we start; I do not work on matters that conflict with existing commitments.
- Confidentiality agreement as standard. Client names are used only with written permission.

### Speaking (speaking.html)

- **Title tag:** Speaking - Payment tactics for margin wars | Avi Reddy
- **Meta description:** Keynotes, moderated sessions, closed-door briefings and workshops on payment tactics for winning back margin. Recent stages: Snowflake Summit 2025, Money20/20 USA 2024, Fiserv Forum 2024, MRC Las Vegas 2024.

**H1:** Speaking

Practical tactics, not trend talks. Every session covers specific moves an audience can make on Monday: how each one works, what it is worth, how it fails, who owns it, and how it differs by market.

**Button/link:** Enquire about a session

#### Signature talks

**Payment tactics for margin wars**

Flagship keynote, 30-45 minutes. Six specific moves, one at a time: re-routing a BIN range to a second acquirer, network tokens for card-on-file, a retry schedule for soft declines, interchange++ pass-through, a chargeback representment workflow and FX markup placement. Each comes with mechanics, metrics, failure modes, owners and the cross-market differences.

**PayFac and AI: tactics for sub-merchant margin**

Sub-merchant pricing, onboarding and underwriting cost, reserves and residual splits, and where AI already helps. Builds on the Fiserv Forum 2024 PayFac and GenAI panel.

**Marketplace payments and risk: payout, reserve and loss tactics**

Payout timing and holds by seller risk tier, rolling reserves, and which chargebacks to fight. Builds on hosting the MRC Las Vegas 2024 marketplaces session.

**Merchant data and cloud data sharing: finding basis points in your own data**

Using direct processor-to-merchant data sharing for approval-rate analysis by BIN, decline-code retry logic and fee checks against interchange++ statements. Builds on Snowflake Summit 2025 and Money20/20 USA 2024.

Also available as a closed-door briefing: **stablecoin settlement as a cost line for acquirers and merchants**, offered only after a conflict check.

#### Formats

- Keynotes, and headline slots at vendor-hosted customer events
- Moderating, hosting and firesides
- Closed-door executive briefings and board sessions
- Half-day and full-day workshops
- The Margin Wars Working Sessions: 8-12 peers, one lever, Chatham House rule
- Virtual sessions

#### Past stages

| Year | Event | Role | Topic |
| --- | --- | --- | --- |
| 2024 | Money20/20 USA 2024, Las Vegas | Session speaker with Prabhath Nanisetty, Snowflake | How merchants unlock value through cloud data sharing |
| 2024 | Fiserv Forum 2024, Las Vegas | Panelist, with Hersh Mansukhani and others | Future is PayFac and GenAI |
| 2024 | MRC Las Vegas 2024 | Host; co-host of a merchant cost-optimisation roundtable | Marketplaces on the Rise: Payments and Risk |
| — | Money20/20 USA, Data Cloud Now interview | Interviewee | Data and AI in payments |

#### For organisers

The speaker kit includes bios, talk abstracts, past stages and the fee sheet. Fees on request. [SPEAKER KIT LINK: add after approval]

### Briefing (The Margin Wars Briefing) (writing.html)

- **Title tag:** The Margin Wars Briefing - invite-only | Avi Reddy
- **Meta description:** The Margin Wars Briefing: a private monthly briefing for about 150 senior payments operators. One tactic per issue for winning back payment margin. By invitation.

**H1:** The Margin Wars Briefing

A private monthly briefing for about 150 people who own a payment cost, approval, loss or FX number. Each issue is one tactic. It is free, and you join by invitation.

**Button/link:** Request an invitation

#### Who it is for

- Heads of payments, and payments product and pricing leads at acquirers and PSPs
- Merchant payments and finance leads at enterprise and cross-border merchants
- Risk, disputes and treasury leads

Vendors' sales teams, investors without an operating role, and press are not invited.

#### What every issue contains

- The move, and its mechanics step by step
- Prerequisites
- The metric that proves it worked, and an impact range that is sourced or labelled as an assumption
- Failure modes and the rollback
- Who owns it
- How it differs in the US, UK/EU, Africa and APAC
- What I would do on Monday

#### What you will not get

News commentary, trend pieces, hot takes, sponsors or anything based on employer or client data.

#### Excerpt: Tactic card 01

**Re-route an under-performing BIN range to a second acquirer**

**The move.** Take a group of BINs that approve poorly or cost too much with your main acquirer, send a fixed share of that traffic to a second acquirer, and keep the rest as a holdout so the difference is measured, not assumed.

**Before you start.** Make sure stored credentials work on both acquirers, that both paths have the same 3-D Secure and SCA set-up, and that your primary contract has no volume tiers the move would break.

**Cross-market column.** In the US, check debit routing rules first. In the UK and EU, consumer interchange is capped, so the gain is mostly approvals and markup. In Africa and APAC, compare local and cross-border acquiring before routing by BIN.

The full card, with metrics, failure modes, owners and Monday actions, goes to readers. Excerpts are published about once a quarter.

### Contact (contact.html)

- **Title tag:** Contact | The Margin Wars - Avi Reddy
- **Meta description:** Contact Avi Reddy about a margin problem, a Margin Teardown, speaking, a Working Session or an invitation to The Margin Wars Briefing.

**H1:** Contact

The best first step is a short note on the margin problem you are working on. I reply to every serious enquiry.

#### Get in touch

- Email: {{contact.email}}
- LinkedIn: {{profile.avi.linkedin}}
- X: {{profile.x.handle}}

#### Helpful to include

- Your organisation, role and the markets you sell in
- The number you are trying to move (cost, approvals, losses or FX) in a few sentences
- Whether this is advisory, a teardown, speaking, a Working Session or a Briefing invitation

#### Please note

I take on a small number of engagements at a time and run a conflict check before any discussion of confidential detail.

## 5. Domain shortlist (availability checked 21 Oct 2026; nothing bought)

Method: registry RDAP lookups (Verisign for .com/.net; a 404 response means no registration record existed at the time of the check). Availability can change at any moment, and premium pricing is not checked.

| Domain | Status on 21 Oct 2026 | Fit | Recommendation |
|---|---|---|---|
| avineshreddy.com | Available (no registration record) | Personal name, exact match | **First choice** for the personal site |
| avireddyadvisory.com | Available | Matches the business name | **Buy alongside**, redirect to the main site |
| avireddypartners.com | Available | Suggests a firm with partners | Not recommended (implies a team) |
| avireddy.net | Available | Short name; .net is weaker | Optional defensive buy |
| **themarginwars.com** | Available (no registration record, 21 Oct 2026) | Brand chosen by Avi | **First choice for the brand**; avineshreddy.com stays the personal site, or redirect one to the other |
| themarginwars.net / .org / .io | Available (no registration record) | Defensive | Optional |
| themarginwars.co | Not verified (registry lookup timed out) | Defensive | Check at purchase |
| margin-wars.com | Available | Redirect | Optional |
| marginwars.com | **Registered** (created 12 Sep 2026) | - | Not available; check it is not a payments publication |
| railsandledgers.com | Available | Fallback name | Buy only if "Rails & Ledgers" is used instead |
| avireddy.com | Registered (since 2019) | - | Not available |
| reddyadvisory.com | Registered (since 2024) | - | Not available; avoid confusion |
| avireddy.io | Registered (since 2022) | - | Not available |
| avinesh.com | Registered (since 2000) | - | Not available |
| .co variants | Not verified (registry lookup timed out) | - | Check at purchase |

Note: avireddy.com and reddyadvisory.com are held by others; check that no similarly named advisory firm operates in the same market before finalising "Avi Reddy Advisory".

## 6. Launch checklist (Gate G3 - do not start before G0)

1. Avi approves all copy; every open item is resolved or removed.
2. Professional headshots added (with alt text).
3. Avi buys the domain(s) and chooses a host himself.
4. Remove the draft banner and `noindex`; add sitemap.xml, robots.txt and schema markup.
5. Point "Request an invitation" at the chosen inbox once the Briefing is set up (Gate G4); never add a public subscribe form.
6. Test on mobile, check every link, run an accessibility check. (Draft QA on 21 Oct 2026: all six pages checked at 320, 375, 768 and 1280 px - no horizontal overflow, header and main aligned, nav wraps cleanly, past-stages table scrolls inside its own frame on phones; `build/qa_site.mjs`.)
7. Update LinkedIn and X profile links to the new domain.
