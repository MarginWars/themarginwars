---
id: briefing-issue-01-bin-rerouting
channel: briefing
status: draft
owner: publications
approvals: {}
sources: []
---

# The Margin Wars Briefing — Issue 1 — Tactic card 01 (POLISHED DRAFT, not for sending)
*Planned send: Tue 1 Dec 2026, 6:00 am PT. Source draft: 07_Substack_Launch_Pack.md §10. Draft for Avi's review; nothing published or sent.*

## Re-route an under-performing BIN range to a second acquirer

**The move.** Take one group of card BINs that approves poorly or costs too much on your primary acquirer, send a fixed share of it to a second acquirer, and keep a holdout so the difference is provable.

**Why it is a margin lever.** Approval rates and all-in cost are not uniform across issuers. Acquirers differ in issuer treatment of their traffic, local presence and pricing. A narrow, measured re-route can win back approvals and basis points without reopening the whole contract.

## Mechanics
1. Pull 90 days of authorisation data by BIN (6–8 digits), issuer country, card type (debit/credit/commercial/prepaid), channel (CIT, MIT/recurring, card-on-file) and decline code.
2. Rank BIN groups by **lost-approval value** = declined attempts × (portfolio approval rate − group approval rate) × average ticket, and separately by cost per approved transaction (bps: interchange + scheme + acquirer markup).
3. Pick one group large enough to measure, small enough to be safe (e.g. one issuer's debit range).
4. Add a gateway/orchestration rule sending a fixed share (e.g. 50%) of that group to acquirer B; the rest stays on A as holdout. One routing decision per attempt, logged.
5. Run across a full billing cycle and payday effects. Compare approval, first-attempt approval, fraud, chargeback and all-in cost per approval for both arms.
6. If the result holds, move the full group; if not, roll back and record why.

## Prerequisites
- Second acquirer signed, live MID in the right country, pricing understood line by line.
- Portable credentials: network tokens or a vault you control, not acquirer-locked tokens (see Issue 2 and card 11).
- Same 3DS/SCA set-up, MCC and descriptor on both paths.
- Reconciliation that ingests two settlement files and two fee reports.
- Primary contract checked for volume commitments / tier breaks.
- For Mastercard merchant-initiated payments (MITs): if the first cardholder-initiated transaction ran on acquirer A and you route the MIT to acquirer B, capture, store and send the Transaction Link Identifier (TLID). Checkout.com (article updated 11 Nov 2026) says Mastercard will require the TLID on economically related MITs from 1 Aug 2027; other processors have cited earlier dates, so check yours. [GAP: second source / Mastercard primary. Do not treat 23 Oct 2026 as the required-by date.] https://support.checkout.com/hc/en-us/articles/33589249067538-Mastercard-Transaction-Link-Identifier

## Metrics and expected impact
- **Primary:** approval rate on moved group, test vs holdout.
- **Secondary:** cost per approved transaction (bps), first-attempt approval share, fraud-to-sales and chargeback ratios on new MID.
- **Impact range: [Assumption — sized from your own step-2 data].** No credible public benchmark exists for BIN-level re-routing uplift specifically; vendor claims are not used. No employer or client figures.
- **Related public reference points (context, not a forecast):**
  - Australia: RBA estimates debit acceptance cost is "nearly 20 per cent lower" for merchants with least-cost routing — RBA estimate (2024 data); a network-routing analogue, not acquirer re-routing. https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/backgrounders/backgrounder-on-least-cost-routing.html
  - [GAP: find a neutral public study of multi-acquirer approval uplift; if none, keep as assumption.]

## Failure modes (early sign → rollback)
- **Lost volume tier at primary:** saving on one group wiped out by price step-up elsewhere → check contract bands before moving → model first.
- **Fraud moves with traffic / new MID has no history:** fraud-to-sales spike in week one → start small, ramp.
- **Credential mismatch:** spike in "invalid card" declines on B → end-to-end token test pre-launch.
- **Cross-acquirer retry loops:** decline on A retried on B, counted toward scheme reattempt limits (Visa Core Rules, 24 Oct 2026, Table 7-2, pp. 547–549: up to 20 reattempts in 30 days for categories 2–4; a merchant must never resubmit category 1) → one routing decision per attempt. https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf
- **Reconciliation breaks:** timing gaps from two settlement cycles → reconcile daily for month one.

## Owner
Head of payments decides; payments engineering builds the rule; finance tracks cost per approval; risk watches fraud/chargebacks on new MID; partner manager owns both acquirer contracts.

## Cross-market column
| Market | What changes |
|---|---|
| **US** | Debit: Regulation II requires issuers to enable ≥2 unaffiliated networks incl. card-not-present (effective 1 Jul 2023), and bars routing restrictions — so debit has a network-routing lever *in addition* to acquirer choice. Check both before changing debit routing. https://www.federalreserve.gov/newsevents/pressreleases/bcreg20221003a.htm ; https://www.ecfr.gov/on/2023-07-01/title-12/chapter-II/subchapter-A/part-235/section-235.7 The Reg II 21-cent debit interchange cap was vacated and remanded to the Fed by the 8th Circuit on 26 Oct 2026 (*Corner Post v. Board of Governors*, No. 25-3000); the court set no replacement rate. The current cap stays in force until the mandate issues. Dual-network routing under §235.7 is not the subject of that ruling. https://ecf.ca8.uscourts.gov/opndir/26/10/253000P.pdf The Visa/Mastercard interchange settlement is pending: hearing held 16 Nov 2026, decision reserved. The judge said he would rule as soon as possible, and that rejecting the deal would mean a 2027 trial. No written order yet (the settlement site still states the Court has not given final approval). Re-check 30 Nov and the morning of 1 Dec before send. https://www.paymentsdive.com/news/visa-mastercard-face-possible-trial/874834/ ; https://www.interchangeequitablereliefsettlement.com/ |
| **UK/EU** | Consumer interchange is capped at 0.2% debit / 0.3% credit in the EU (IFR 2015/751, Arts 3–4) and under the UK's retained IFR (Art 3: 0.2% on any UK debit card transaction; Art 4: 0.3% on any UK credit card transaction). Gains come mainly from approvals, SCA exemption rates and acquirer markup, not interchange. EU: https://eur-lex.europa.eu/eli/reg/2015/751/oj/eng [CONFIRM: re-read EU Arts 3–4 in a normal browser before the 1 Dec send; EUR-Lex blocked automated checks after 26 Oct.] UK: https://www.legislation.gov.uk/eur/2015/751/article/3 ; https://www.legislation.gov.uk/eur/2015/751/article/4 UK–EEA card-not-present (online) consumer interchange is 1.15% debit / 1.5% credit (raised from 0.2% / 0.3% after EU withdrawal). The PSR found the increases cost businesses £150–200 million a year. No cap is in force: the PSR decided not to proceed with an interim cap and is consulting on a methodology for a longer-term cap. https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/ |
| **Africa** | Narrower acquirer choice; local vs cross-border acquiring usually matters more than BIN routing. Test local acquiring first. Nigeria: a Central Bank of Nigeria circular (PSS/DIR/PUB/CIR/001/004, 15 Jun 2026) requires that a licensed institution (alone or with related entities) with more than 25% market share in consumer issuing, in any rolling 12-month period, hold no more than 15% of merchant acquiring in the same period, and the reverse; full compliance by 31 Dec 2026. https://www.cbn.gov.ng/Out/2026/CCD/CIRCULAR%20ON%20INTRODUCTION%20OF%20MARKET%20STRUCTURE%20REQUIREMENTS%2C%20DATA%20LOCALISATION%2C%20ULTIMATE%20BENEFICIAL%20OWNERSHIP%20DISCLOSURE%2C%20AND%20SYSTEMIC%20OVERSIGHT%20MEASURES%20IN%20THE%20NIGERIA%20PAYMENTS%20SYSTEM.pdf [GAP: public source on South Africa / Kenya acquiring market structure] [CONFIRM WITH AVI: South Africa experience] |
| **APAC** | Domestic schemes and local-acquiring requirements vary by market; route by market before BIN. Australia: dual-network debit with least-cost routing; domestic debit interchange ceiling 8c or 0.16%; consumer credit cap 0.3%; surcharging banned on eftpos, Mastercard and Visa from 1 Oct 2026; a 1.0% cap on foreign-issued cards starts 1 Apr 2027. https://www.rba.gov.au/payments-and-infrastructure/debit-cards/regulatory-framework.html ; https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/interchange-fees.html ; https://www.legislation.gov.au/F2016L00837/2026-10-01/2026-10-01/text/original/pdf [GAP: India/Japan/SEA local acquiring sources] |

## War story
[WAR STORY: CONFIRM WITH AVI — leave blank. Must be sanitised; no employer, client or customer identifiable.]

## What I'd do Monday
1. Request 90 days of auth data by BIN and decline code from your processor.
2. Rank the top three BIN groups by lost-approval value.
3. Read the primary acquirer contract for volume commitments.
4. Confirm stored credentials work on a second acquirer.
5. Launch one 50/50 test with a holdout and a written rollback rule.

*Next issue (Tue 5 Jan 2027): turning on network tokens for card-on-file.*

---
### Editor's change log vs 07 §10
- Defined lost-approval value formula; added first-attempt approval metric.
- Replaced unsourced cross-market text with verified citations (Reg II, IFR, RBA); gaps marked.
- Added scheme reattempt-limit exposure to retry-loop failure mode.
- Fixed cross-reference (token portability now points to Issue 2 / card 11).
- 16 Nov 2026 (public-signals runs 2–4): US debit-cap status and pending settlement; Visa Table 7-2 retry cite; Mastercard TLID prerequisite (date conflict flagged); UK retained IFR caps; Australia surcharge ban, credit cap and foreign-card cap. See edits-2026-11-16.md.
- 23 Nov 2026 (public-signals run 5): settlement wording updated after the 16 Nov hearing (decision reserved, no order); UK–EEA CNP interchange filled from the PSR review page; Nigeria CBN issuing/acquiring cap added to the Africa cell. EU IFR 0.2%/0.3% still flagged for a manual EUR-Lex check. TLID date caveat unchanged. See edits-2026-11-23.md.
