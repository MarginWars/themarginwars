# The Margin Wars Working Sessions: session design

## Overview

The files list eight candidate Working Sessions (07 §6 calendar), while 03 models 4 sessions in Year 1 and 6 in Year 2 and 10 targets three by Day 90. No file names exactly six. Best-supported six used here: the 07 calendar rows with distinct tactics and one session per region where possible. Dropped: Money20/20 Middle East, Riyadh (repeats Issue 7 and its network is unconfirmed) and Money20/20 USA, Las Vegas (Issue 11; third Las Vegas session). The Africa row in 07 has no date or venue; it is anchored here to Seamless Africa, Johannesburg, 25–26 Oct 2027 from 02 as a proposal [CONFIRM WITH AVI].

| # | Date | Conference | City | Tactic | Source |
|---|---|---|---|---|---|
| 1 | Feb 2027 (Fintech Meetup runs 22–24 Feb 2027) | Fintech Meetup 2027 | Las Vegas, US (The Venetian) | Issue 3 / Card 03: soft-decline retry schedule | 07 §6 calendar row 1; 02 Conference Map row 10 (dates, <https://fintechmeetup.com/hotel>) |
| 2 | Mar 2027 (MRC Vegas runs 15–18 Mar 2027) | MRC Vegas 2027 | Las Vegas, US (ARIA) | Issue 5 / Card 05: chargeback representment triage | 07 §6 calendar row 2; 02 row 23 (<https://merchantriskcouncil.org/events/2027/mrc-vegas-2027>) |
| 3 | Apr 2027 (MRC London runs 26–28 Apr 2027) | MRC London 2027 | London, UK (InterContinental O2) | Issue 4 / Card 04: IC++ renegotiation, UK/EU edition | 07 §6 calendar row 3; 02 row 17 (<https://merchantriskcouncil.org/events/2027/mrc-london-2027>) |
| 4 | Jun 2027 (Money20/20 Europe runs 8–10 Jun 2027) | Money20/20 Europe 2027 | Amsterdam, NL (RAI) | Issue 7 / Card 07: FX markup placement and when to go local | 07 §6 calendar row 4; 02 row 6 (<https://europe.money2020.com/>) |
| 5 | Sep 2027 (Sibos runs 20–23 Sep 2027) | Sibos 2027 | Singapore (Marina Bay Sands) | Issue 12 / Card 12: stablecoin settlement on one payout corridor as a cost line | 07 §6 calendar row 6 (flags conflict check); 02 row 1 (<https://www.sibos.com/about/future-sibos>) |
| 6 | Oct 2027 (Seamless Africa runs 25–26 Oct 2027) — proposed | Seamless Africa 2027 | Johannesburg, South Africa (Sandton Convention Centre) | Issue 10 / Card 10: steer one high-cost segment to pay-by-bank or a local APM | 07 §6 calendar row 8 (date/venue left [CONFIRM WITH AVI]); anchor event from 02 row 3 (<https://www.terrapinn.com/exhibition/seamless-africa/index.stm>) |

**Alternates**

- Money20/20 USA, Las Vegas, 19–21 Oct 2027 — Issue 11 orchestration exit terms — Swap in if Africa date fails
- Money20/20 Middle East, Riyadh, 14–16 Sep 2027 — Issue 7 local acquiring vs cross-border — Network unconfirmed in 07

**Standard run of show (2.5 h, shared by all six; exercises vary)**

| Time | Block |
|---|---|
| 0:00–0:05 | Arrival, Chatham House rules, no recording |
| 0:05–0:15 | Avi presents the tactic card (slides 2–4) |
| 0:15–0:25 | Data deep-dive: the sourced exhibits (slides 5–7) |
| 0:25–0:55 | Round: each attendee gives current number (as a range) and main blocker (≈2.5 min each) |
| 0:55–1:00 | Cluster blockers on a whiteboard |
| 1:00–1:30 | Exercise 1 in pairs (session worksheet) |
| 1:30–1:35 | Break |
| 1:35–2:05 | Failure modes + cross-market differences, whole group (slides 8–10) |
| 2:05–2:10 | War story [CONFIRM WITH AVI] |
| 2:10–2:25 | Exercise 2 / commitments: each attendee writes one Monday action and the metric |
| 2:25–2:30 | Close, NPS card, next session |
| After | Dinner (optional) |

## Session 1: Issue 3 / Card 03: soft-decline retry schedule

- **Date:** Feb 2027 (Fintech Meetup runs 22–24 Feb 2027)
- **Conference / city:** Fintech Meetup 2027, Las Vegas, US (The Venetian)
- **Source:** 07 §6 calendar row 1; 02 Conference Map row 10 (dates, <https://fintechmeetup.com/hotel>)
- **Objective:** Agree a retry policy that never retries hard declines and schedules soft declines inside scheme limits.
- **Decision attendees leave with:** Each attendee leaves with a signed-off retry rule set (blocked codes, schedule for category 2, data fixes for category 3) and a 30-day holdout plan.
- **Ideal attendees:** Payments engineering leads, subscription/billing owners, payments product heads at recurring-revenue merchants and platforms; 8–12 seats, at least 3 non-US.

**Pre-work**

- 30 days of declines with raw response codes, counted by Visa category (template provided)
- Last quarter's excessive-retry fees from acquirer invoices
- Current retry schedule written as a timeline

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Decline-code triage worksheet: classify own top 20 codes into categories 1–4 and mark retry / fix / never; Exercise 2 = Schedule sketch: draw a 30-day retry timeline for one soft-decline code.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + Chatham House rules | None | — |
| 2 | The move in one sentence | Card 03 summary | Sourced (Issue 3) |
| 3 | Decline categories 1–4 with example codes | Code table | Sourced: <https://developers.tabapay.com/docs/network-authorization-best-practices> ; <https://chargebacks911.com/visa-excessive-reattempts-rule/> (confirm vs Visa Rules) [CONFIRM WITH AVI] |
| 4 | Scheme limits: 20 reattempts / 30 days, none on category 1 | Rule summary + change date 19 May 2025 | Sourced: <https://support.checkout.com/hc/en-us/articles/25482040901394-When-can-I-retry-a-declined-transaction> |
| 5 | Fee exposure math | $0.10 domestic / $0.25 cross-border per feeable attempt × your attempt counts | Fees sourced (secondary): <https://chargebacks911.com/visa-excessive-reattempts-rule/> ; volumes [Assumption] |
| 6 | Mastercard equivalent | Merchant Advice Codes and retry rules | [GAP] |
| 7 | Schedule design: pay-cycle timing, spacing, CIT vs MIT counters | Illustrative timeline | Illustrative [Assumption] |
| 8 | Measuring recovery: holdout design | Metric: recovered approvals per 100 soft declines | Method only; no benchmark [GAP] |
| 9 | Failure modes + early warnings | From card 03 | Sourced (Issue 3) |
| 10 | Cross-market: US / UK-EU (SCA on retried CIT) / Africa / APAC (India e-mandate) | Comparison table | [GAP] for UK-EU, Africa, APAC sources |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments + Monday actions | Commitment sheet | — |

**Exercises / worksheets**

- Decline-code triage worksheet: classify own top 20 codes into categories 1–4 and mark retry / fix / never
- Retry-fee calculator: input feeable attempts by region and get monthly fee exposure
- Schedule sketch: draw a 30-day retry timeline for one soft-decline code

**Takeaways**

- Category 1 retries are pure cost: block them in code
- Category 3 needs a data fix before any retry
- Separate CIT and MIT counters and log credential type
- Prove recovery with a holdout, not before/after

**Handouts**

- **One-pager:** Card 03 summary, category table, scheme limits with source URLs
- **Calculator:** Retry-fee exposure + recovered-approval value; all inputs user-supplied [Assumption]
- **Checklist:** Ten-point retry-policy audit (blocked codes, spacing, counters, logging, dunning comms)

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- Scheme rules and fees change; re-verify against current Visa Rules the week before [CONFIRM WITH AVI]
- Attendees may bring employer data; keep all outputs anonymised ranges
- Mastercard rules not yet sourced [GAP]

## Session 2: Issue 5 / Card 05: chargeback representment triage

- **Date:** Mar 2027 (MRC Vegas runs 15–18 Mar 2027)
- **Conference / city:** MRC Vegas 2027, Las Vegas, US (ARIA)
- **Source:** 07 §6 calendar row 2; 02 row 23 (<https://merchantriskcouncil.org/events/2027/mrc-vegas-2027>)
- **Objective:** Decide which disputes to fight, which to accept, and which to prevent, by reason code and net value.
- **Decision attendees leave with:** Each attendee leaves with a fight / accept / prevent matrix by reason code and a target ratio headroom under Visa's monitoring program.
- **Ideal attendees:** Heads of disputes, risk and fraud leads, marketplace trust & safety, finance partners at high-CNP merchants; 8–12, mixed regions.

**Pre-work**

- Win rate and volume by top 10 reason codes (last 6 months)
- Handling cost per case [Assumption] if unknown
- Current VAMP-style ratio estimate (fraud + disputes ÷ settled CNP)

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Reason-code triage: place own top 10 codes on the fight/accept/prevent matrix; Exercise 2 = Ratio headroom calculator: current ratio vs threshold, cases to remove to reach target.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + rules | None | — |
| 2 | The move | Card 05 summary | [GAP] Card 05 not yet drafted |
| 3 | Why now: Visa VAMP ratio and thresholds | Formula + thresholds: merchant Excessive ≥150 bps from 1 Apr 2026 (AP, Canada, EU, US), ≥220 bps CEMEA; min 1,500 counts | Sourced: <https://corporate.visa.com/content/dam/VCOM/corporate/visa-perspectives/security-and-trust/documents/visa-acquirer-monitoring-program-fact-sheet-2025.pdf> ; <https://support.checkout.com/hc/en-us/articles/26990138066450-Update-to-the-Visa-Acquirer-Monitoring-Program-VAMP> |
| 4 | What's excluded: pre-dispute resolutions, CE 3.0-qualified fraud | Program rules | Sourced (same Visa fact sheet) |
| 5 | Net recovery math | Win rate × value − handling cost, by reason code | Method; inputs [Assumption] |
| 6 | Fight / accept / prevent matrix | 2×2 template | Template |
| 7 | Evidence packs by reason code | Example evidence list | [GAP] scheme reason-code docs |
| 8 | Mastercard dispute monitoring | Thresholds | [GAP] |
| 9 | Failure modes | Over-fighting, missed deadlines, prevention tools double-counting | Card 05 [GAP] |
| 10 | Cross-market | CEMEA threshold differs; LAC; UK/EU; APAC | Partly sourced; Africa/APAC specifics [GAP] |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments | Commitment sheet | — |

**Exercises / worksheets**

- Reason-code triage: place own top 10 codes on the fight/accept/prevent matrix
- Ratio headroom calculator: current ratio vs threshold, cases to remove to reach target

**Takeaways**

- Fight by net value, not by volume
- Pre-dispute resolution and CE 3.0 move cases out of the ratio
- Know your headroom to the 150 bps line (220 bps in CEMEA)
- Build evidence packs per reason code

**Handouts**

- **One-pager:** VAMP formula, thresholds, exclusions with sources
- **Calculator:** Net recovery by reason code + ratio headroom [Assumption]
- **Checklist:** Representment workflow: deadlines, evidence, owner, QA

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- Card 05 is not yet written; draft it before the session [GAP]
- Fraud teams may want vendor recommendations; keep the session vendor-neutral

## Session 3: Issue 4 / Card 04: IC++ renegotiation, UK/EU edition

- **Date:** Apr 2027 (MRC London runs 26–28 Apr 2027)
- **Conference / city:** MRC London 2027, London, UK (InterContinental O2)
- **Source:** 07 §6 calendar row 3; 02 row 17 (<https://merchantriskcouncil.org/events/2027/mrc-london-2027>)
- **Objective:** Decompose the effective rate into interchange, scheme fees and acquirer markup, and set a renegotiation ask.
- **Decision attendees leave with:** Each attendee leaves with a fee decomposition of one statement, a target markup, and a negotiation one-pager.
- **Ideal attendees:** Finance and procurement leads, heads of payments at UK/EU merchants selling cross-border; 8–12.

**Pre-work**

- One redacted monthly acquirer statement
- Pricing model in force (blended, IC+, IC++)
- Share of volume that is UK–EEA cross-border CNP

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Statement teardown: label each fee line IC / scheme / markup / unknown; Exercise 2 = Negotiation role-play in pairs: merchant vs acquirer.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + rules | None | — |
| 2 | The move | Card 04 summary | [GAP] Card 04 not drafted |
| 3 | Anatomy of the effective rate | IC + scheme + markup stack | Concept |
| 4 | EU caps: 0.2% debit, 0.3% credit (consumer) | IFR 2015/751 Arts 3–4 | Sourced: <https://eur-lex.europa.eu/eli/reg/2015/751/oj/eng> |
| 5 | UK–EEA CNP: 1.15% debit / 1.5% credit; PSR estimates £150–200m/yr extra cost | PSR market review | Sourced: <https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/> |
| 6 | Cap status: interim cap dropped; High Court upheld PSR powers 15 Jan 2026 | Timeline | Sourced: <https://www.psr.org.uk/news-and-updates/latest-news/news/high-court-backs-psr-s-powers-to-cap-cross-border-card-fees/> (re-check status before session) |
| 7 | Scheme fees: the line nobody audits | Example lines | [GAP] public scheme fee schedules |
| 8 | Blended → IC++ break-even | Calculator walkthrough | Inputs [Assumption] |
| 9 | Negotiation levers and contract traps | Volume tiers, minimums, notice periods | Practice [Assumption] |
| 10 | Cross-market: US / UK-EU / Africa / APAC | Comparison | US Reg II debit sourced; others [GAP] |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments | — | — |

**Exercises / worksheets**

- Statement teardown: label each fee line IC / scheme / markup / unknown
- Break-even calculator: blended vs IC++ on own mix
- Negotiation role-play in pairs: merchant vs acquirer

**Takeaways**

- You cannot negotiate a number you have not decomposed
- In the EU, interchange is capped, so markup and scheme fees are the lever
- UK–EEA CNP is a live regulatory cost line: track the PSR
- Fix tiers and notice periods before price

**Handouts**

- **One-pager:** Rate anatomy, EU caps, UK–EEA rates and PSR status with URLs
- **Calculator:** Blended vs IC++ break-even [Assumption]
- **Template:** Negotiation ask letter skeleton (not sent; for attendees' own use)
- **Checklist:** Contract clauses to read before renegotiating

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- PSR cap status may change before April 2027; re-verify
- Statements contain confidential pricing; redact before the room [CONFIRM WITH AVI]
- Card 04 needs drafting [GAP]

## Session 4: Issue 7 / Card 07: FX markup placement and when to go local

- **Date:** Jun 2027 (Money20/20 Europe runs 8–10 Jun 2027)
- **Conference / city:** Money20/20 Europe 2027, Amsterdam, NL (RAI)
- **Source:** 07 §6 calendar row 4; 02 row 6 (<https://europe.money2020.com/>)
- **Objective:** Decide where FX margin sits (DCC, multi-currency pricing, settlement conversion) and the trigger for local acquiring.
- **Decision attendees leave with:** Each attendee leaves with an FX placement choice per top corridor and a volume trigger for local acquiring.
- **Ideal attendees:** Treasury leads, cross-border payments product heads, finance at merchants selling in 3+ currencies; 8–12, at least 2 APAC/Africa.

**Pre-work**

- Top 5 currency pairs by volume
- FX spread paid or earned (bps) per pair [Assumption] if unknown
- Current conversion point (who converts, when)

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Corridor map: plot top pairs on volume vs spread; Exercise 2 = Local-acquiring trigger calculator per market.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + rules | None | — |
| 2 | The move | Card 07 summary | [GAP] Card 07 not drafted |
| 3 | Three places FX margin can sit | DCC vs MCP vs settlement conversion diagram | Concept |
| 4 | EU disclosure: conversion charges as % markup over ECB reference rate | Reg 2019/518 Art 3a | Sourced: <https://eur-lex.europa.eu/eli/reg/2019/518/oj> |
| 5 | Measuring spread vs a reference rate | Method: compare executed rate to ECB / mid-market | Method; data [Assumption] |
| 6 | Conversion and approval effects of local-currency pricing | Benchmark | [GAP] |
| 7 | Local vs cross-border acquiring cost | Interchange differences; UK–EEA CNP example 1.15%/1.5% vs 0.2%/0.3% | Sourced: <https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/> |
| 8 | Local-acquiring trigger model | Volume threshold calculator | Inputs [Assumption] |
| 9 | Failure modes | DCC complaints, hedging gaps, entity/licensing costs | Practice [Assumption] |
| 10 | Cross-market | US / UK-EU / Africa (FX controls) / APAC | [GAP] Africa FX-control and APAC sources |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments | — | — |

**Exercises / worksheets**

- Corridor map: plot top pairs on volume vs spread
- Local-acquiring trigger calculator per market

**Takeaways**

- Know who earns the spread on each corridor
- In the EU, markups must be disclosed vs the ECB rate, so they can be compared
- Cross-border interchange can dwarf the FX spread: price both
- Set a volume trigger for local acquiring before you need it

**Handouts**

- **One-pager:** FX placement options, EU disclosure rule, cross-border interchange example with URLs
- **Calculator:** Corridor spread + local-acquiring trigger [Assumption]
- **Checklist:** Questions to ask your acquirer about conversion

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- Card 07 also shown for Riyadh in 07; we dropped Riyadh to avoid duplication [CONFIRM WITH AVI]
- FX hedging advice may stray into regulated advice; keep to cost mechanics

## Session 5: Issue 12 / Card 12: stablecoin settlement on one payout corridor as a cost line

- **Date:** Sep 2027 (Sibos runs 20–23 Sep 2027)
- **Conference / city:** Sibos 2027, Singapore (Marina Bay Sands)
- **Source:** 07 §6 calendar row 6 (flags conflict check); 02 row 1 (<https://www.sibos.com/about/future-sibos>)
- **Objective:** Compare the all-in cost of one cross-border payout corridor on the current rail vs stablecoin settlement, as a cost line only.
- **Decision attendees leave with:** Each attendee leaves with a filled cost-comparison sheet for one corridor and a go / no-go test design.
- **Ideal attendees:** Treasury and payouts leads at banks, marketplaces and payroll/payout platforms with APAC/Africa corridors; compliance lead in the room; 8–12.

**Pre-work**

- One corridor's current all-in cost components (FX, correspondent fees, pre-funding days)
- Compliance constraints memo (high level)

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Cost-stack worksheet: current rail vs stablecoin path for one corridor; Exercise 2 = Go/no-go criteria drafting in pairs.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + rules + conflict statement | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 2 | The move | Card 12 summary | [GAP] Card 12 not drafted |
| 3 | All-in cost stack of a cross-border payout | FX + correspondent + pre-funding cost of capital + ops | Concept |
| 4 | Benchmark: average cost of cross-border payments | World Bank Remittance Prices Worldwide or similar | [GAP] |
| 5 | Stablecoin path cost stack | On/off-ramp fees, network fees, FX at ramps, custody, compliance | Components only; figures [GAP] |
| 6 | Pre-funding and liquidity effect | Days of pre-funding × cost of capital | Inputs [Assumption] |
| 7 | Regulatory status by market | US / UK-EU (MiCA) / Singapore (MAS) / Africa | [GAP] cite primary regulator pages |
| 8 | Test design: one corridor, capped volume, holdout | Template | Template |
| 9 | Failure modes | Ramp liquidity, depeg, compliance, reconciliation | Practice [Assumption] |
| 10 | Cross-market comparison | Table | [GAP] |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments | — | — |

**Exercises / worksheets**

- Cost-stack worksheet: current rail vs stablecoin path for one corridor
- Go/no-go criteria drafting in pairs

**Takeaways**

- Treat stablecoins as a cost line, not a thesis
- Pre-funding cost is often the hidden line
- Regulatory status decides the corridor before price does
- Test one capped corridor with a holdout

**Handouts**

- **One-pager:** Cost stack and regulatory checklist with sources (to be completed)
- **Calculator:** Corridor all-in cost comparison [Assumption]
- **Checklist:** Compliance and treasury questions before a pilot

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- Most figures still [GAP]; must be sourced before delivery
- Risk of drifting into theses (kill criterion); moderator must hold to cost line

## Session 6: Issue 10 / Card 10: steer one high-cost segment to pay-by-bank or a local APM

- **Date:** Oct 2027 (Seamless Africa runs 25–26 Oct 2027) — proposed
- **Conference / city:** Seamless Africa 2027, Johannesburg, South Africa (Sandton Convention Centre)
- **Source:** 07 §6 calendar row 8 (date/venue left [CONFIRM WITH AVI]); anchor event from 02 row 3 (<https://www.terrapinn.com/exhibition/seamless-africa/index.stm>)
- **Objective:** Pick one high-cost checkout segment and design a steering test to a local instant-payment or APM rail.
- **Decision attendees leave with:** Each attendee leaves with a chosen segment, rail, incentive design and cost/conversion test plan.
- **Ideal attendees:** Checkout owners, payments product heads and finance at merchants and platforms in South Africa, Nigeria, Kenya plus UK/EU and APAC peers; 8–12.

**Pre-work**

- Cost per transaction by method for top segment
- Conversion by method
- Current APMs offered

**Run of show:** standard 2.5 h (Overview), with Exercise 1 = Segment picker: rank segments by cost × volume; Exercise 2 = Steering design canvas: rail, placement, incentive, guardrails.

**Presentation outline**

| # | Slide | Data / exhibit | Status |
|---|---|---|---|
| 1 | Title + rules | None | — |
| 2 | The move | Card 10 summary | [GAP] Card 10 not drafted |
| 3 | Cost per transaction: card vs pay-by-bank | Segment cost comparison | Inputs [Assumption] |
| 4 | South Africa: PayShap limit raised to R50,000 by BankservAfrica; bank-set pricing | Rail facts | Sourced: <https://techcentral.co.za/payshap-payment-limit-raised-to-r50-000/254663/> |
| 5 | Bank pricing varies: e.g. free under R5,000 then R7 (one bank) | Example tariffs | Sourced: <https://gotyme.co.za/personal/media/money-skills-landing/what-are-the-transaction-limits-for-payshap> (consumer tariff; merchant pricing [GAP]) |
| 6 | Other markets: UK open banking, India UPI, Nigeria, Kenya M-Pesa | Comparison | [GAP] |
| 7 | Steering levers: default order, incentives, surcharging rules | Rules by market | [GAP] surcharging law sources |
| 8 | Test design and metrics | Cost per txn, conversion, refunds/disputes | Template |
| 9 | Failure modes | Conversion drop, refund flows, reconciliation, fraud (APP scams) | Practice [Assumption] |
| 10 | Cross-market table | US / UK-EU / Africa / APAC | Partly sourced |
| 11 | War story | [CONFIRM WITH AVI] | [CONFIRM WITH AVI] |
| 12 | Commitments | — | — |

**Exercises / worksheets**

- Segment picker: rank segments by cost × volume
- Steering design canvas: rail, placement, incentive, guardrails

**Takeaways**

- Steer one segment, not the whole checkout
- Rail pricing is set per bank in South Africa: check your bank's tariff
- Measure conversion and cost together
- Plan refunds and reconciliation before launch

**Handouts**

- **One-pager:** Rail facts by market with URLs
- **Calculator:** Segment cost and conversion break-even [Assumption]
- **Checklist:** Launch checklist for a local APM

**War story:** [CONFIRM WITH AVI] — slot left blank for Avi.

**Risks and open questions**

- Date and city not set in 07 [CONFIRM WITH AVI]
- Seamless Africa (25–26 Oct) falls the week after Money20/20 USA (19–21 Oct): travel load
- Africa network depth for invites [CONFIRM WITH AVI]

## Cross-session

**Arc**

- Feb–Mar (US): approval and loss basics, retries then disputes: fast wins, data the room already has
- Apr–Jun (UK/EU): cost structure, IC++ then FX: needs statements and corridor data
- Sep (APAC): stablecoin settlement as a cost line, gated by conflict check
- Oct (Africa): steering to local rails, closes the year with the cross-market lens
- Each session feeds the next: the anonymised notes become the next Briefing issue's war-story prompts and the Playbook card update

**Reusable template assets**

- **Slide master:** Title, rules, move, exhibits, failure modes, cross-market, war story, commitments (12-slide skeleton)
- **Pre-work pack:** Invite email, data request template, redaction guide
- **Worksheet template:** Two exercises per session on one A4/letter sheet
- **Calculator shell:** Spreadsheet with inputs tab, assumptions labelled, outputs tab
- **One-pager template:** Card summary + sourced exhibits + URLs
- **Commitment card + NPS card:** Monday action, metric, follow-up date
- **Post-session note template:** Anonymised, titles not companies, sent in 48h

**Production needs**

- Venue or host per city; Avi pays venue unless host does (03 C17) [CONFIRM WITH AVI]
- Printed handouts for 12 + PDF versions; card PDF from Briefing
- Whiteboard/flipchart, name cards with first names and titles only
- Calculator built in Sheets/Excel; tested before each session
- Source re-verification the week before each session (regulatory figures move)
- Sponsor rules if any: one seat, no pitch, no contact list (07 §6)
- Budget and pricing: by proposal (internal pricing is kept off the public repo)

## Top open questions for Avi

- Which six? Confirm this set vs swapping in Money20/20 USA (Issue 11) or Riyadh [CONFIRM WITH AVI]
- Africa session: city, date and whether Seamless Africa is the right anchor [CONFIRM WITH AVI]
- Sibos stablecoin session: conflict check outcome and what can be said [CONFIRM WITH AVI]
- War stories for each session [CONFIRM WITH AVI]
- Hosts/sponsors per city and pricing to test [CONFIRM WITH AVI]
- Cards 04, 05, 07, 10 and 12 need drafting before their sessions [GAP]
