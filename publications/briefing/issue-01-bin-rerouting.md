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

## Metrics and expected impact
- **Primary:** approval rate on moved group, test vs holdout.
- **Secondary:** cost per approved transaction (bps), first-attempt approval share, fraud-to-sales and chargeback ratios on new MID.
- **Impact range: [Assumption — sized from your own step-2 data].** No credible public benchmark exists for BIN-level re-routing uplift specifically; vendor claims are not used. No employer or client figures.
- **Related public reference points (context, not a forecast):**
  - Australia: RBA estimates debit acceptance cost is "nearly 20 per cent lower" for merchants with least-cost routing — a network-routing analogue, not acquirer re-routing. https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/backgrounders/backgrounder-on-least-cost-routing.html
  - [GAP: find a neutral public study of multi-acquirer approval uplift; if none, keep as assumption.]

## Failure modes (early sign → rollback)
- **Lost volume tier at primary:** saving on one group wiped out by price step-up elsewhere → check contract bands before moving → model first.
- **Fraud moves with traffic / new MID has no history:** fraud-to-sales spike in week one → start small, ramp.
- **Credential mismatch:** spike in "invalid card" declines on B → end-to-end token test pre-launch.
- **Cross-acquirer retry loops:** decline on A retried on B, counted toward scheme reattempt limits (Visa: 20 retries/30 days for categories 2–4, none for category 1; per-attempt fees) → one routing decision per attempt. Sources: https://support.checkout.com/hc/en-us/articles/25482040901394-When-can-I-retry-a-declined-transaction ; https://chargebacks911.com/visa-excessive-reattempts-rule/ [CONFIRM against current Visa Rules before publishing]
- **Reconciliation breaks:** timing gaps from two settlement cycles → reconcile daily for month one.

## Owner
Head of payments decides; payments engineering builds the rule; finance tracks cost per approval; risk watches fraud/chargebacks on new MID; partner manager owns both acquirer contracts.

## Cross-market column
| Market | What changes |
|---|---|
| **US** | Debit: Regulation II requires issuers to enable ≥2 unaffiliated networks incl. card-not-present (effective 1 Jul 2023), and bars routing restrictions — so debit has a network-routing lever *in addition* to acquirer choice. Check both before changing debit routing. https://www.federalreserve.gov/newsevents/pressreleases/bcreg20221003a.htm ; https://www.ecfr.gov/on/2023-07-01/title-12/chapter-II/subchapter-A/part-235/section-235.7 |
| **UK/EU** | Consumer interchange capped at 0.2% debit / 0.3% credit in the EU (IFR 2015/751, Arts 3–4), so gains come mainly from approvals, SCA exemption rates and acquirer markup, not interchange. https://eur-lex.europa.eu/eli/reg/2015/751/oj/eng [GAP: cite UK retained caps + PSR cross-border UK–EEA interchange source] |
| **Africa** | Narrower acquirer choice; local vs cross-border acquiring usually matters more than BIN routing. Test local acquiring first. [GAP: public source on South Africa / Nigeria / Kenya acquiring market structure] [CONFIRM WITH AVI: South Africa experience] |
| **APAC** | Domestic schemes and local-acquiring requirements vary by market; route by market before BIN. Australia: dual-network debit with least-cost routing; domestic debit interchange ceiling 8c or 0.16%. https://www.rba.gov.au/payments-and-infrastructure/debit-cards/regulatory-framework.html [GAP: India/Japan/SEA local acquiring sources] |

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
