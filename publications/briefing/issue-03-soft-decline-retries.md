---
id: briefing-issue-03-soft-decline-retries
channel: briefing
status: draft
owner: publications
approvals: {}
sources: []
---

# The Margin Wars Briefing — Issue 3 — Tactic card 03 (DRAFT, not for sending)
*Planned send: Tue 2 Feb 2027. From tactic list in 07 §5.*

## Set a retry schedule for soft declines (and stop retrying hard declines)

**The move.** Classify every decline by scheme category, never retry "do not retry" codes, and retry soft declines on a timed schedule within scheme limits.

## Mechanics
1. Map all decline codes to scheme categories (Visa cat 1 never-approve; 2 temporary; 3 data quality; 4 generic). Mastercard equivalent [GAP: Mastercard MAC codes source].
2. Block retries on category 1 (e.g. 04, 07, 14, 15, 41, 43, 46, 57).
3. Category 3: fix data (expiry, CVV, account updater) before any retry.
4. Category 2 (e.g. 51 insufficient funds): schedule retries around pay cycles; cap attempts below scheme limit.
5. Separate counters for CIT and MIT; log every attempt with credential (token vs PAN).
6. A/B test schedules on recurring billing with a holdout.

## Prerequisites
- Decline-code granularity from acquirer (raw, not normalised).
- Billing engine capable of scheduled retries per code.
- Account updater / token lifecycle (Issue 2).

## Metrics and expected impact
- Recovered approvals per 100 soft declines; retry fees paid; involuntary churn.
- **Scheme limits/fees (verified secondary sources; confirm against Visa Rules):** Visa allows 20 reattempts per card in rolling 30 days for categories 2–4 (raised from 15 on 19 May 2025); category 1 retries are never allowed and every one is feeable. Fees cited at $0.10 domestic / $0.25 cross-border per attempt. https://support.checkout.com/hc/en-us/articles/25482040901394-When-can-I-retry-a-declined-transaction ; https://chargebacks911.com/visa-excessive-reattempts-rule/ ; https://developers.tabapay.com/docs/network-authorization-best-practices
- **Recovery range: [Assumption]** — no neutral public benchmark verified; size from holdout. [GAP]

## Failure modes
- Retrying category 1 → fees and issuer distrust → hard block in code.
- Hammering issuer → velocity declines rise → space attempts.
- Cross-acquirer retries counted as reattempts (see Issue 1).
- Customer-unfriendly charges on insufficient funds → coordinate with dunning comms.

## Owner
Payments engineering builds; subscriptions/billing lead owns schedule; finance tracks fees vs recovery.

## Cross-market column
| Market | Notes |
|---|---|
| US | Visa fee applies to US domestic flows per TabaPay doc; pay-cycle timing (biweekly) matters |
| UK/EU | Retried CIT may need fresh SCA; MIT retries rely on initial mandate [GAP: source] |
| Africa | [GAP: local scheme/issuer retry behaviour; cross-border fee exposure higher] |
| APAC | Mandates such as India's e-mandate pre-debit notification constrain recurring retries [GAP: RBI source] |

## War story
[WAR STORY: CONFIRM WITH AVI]

## What I'd do Monday
1. Export 30 days of declines with raw codes; count category 1 retries.
2. Turn off category 1 retries.
3. Pull last quarter's excessive-retry fees from acquirer invoices.
4. Design one schedule test for category 2 on recurring billing.
