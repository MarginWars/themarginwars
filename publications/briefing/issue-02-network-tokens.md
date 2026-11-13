---
id: briefing-issue-02-network-tokens
channel: briefing
status: draft
owner: publications
approvals: {}
sources: []
---

# The Margin Wars Briefing — Issue 2 — Tactic card 02 (DRAFT, not for sending)
*Planned send: Tue 5 Jan 2027. From tactic list in 07 §5.*

## Turn on network tokens for card-on-file

**The move.** Provision scheme network tokens for your stored-card base and send the token (with cryptogram) instead of the PAN on card-on-file and recurring transactions, measured against a PAN holdout.

## Mechanics
1. Inventory stored credentials by scheme, issuer country, and whether they live in your vault or a PSP's.
2. Enable token requestor status directly with schemes or via your PSP/gateway (Visa Token Service, Mastercard MDES).
3. Bulk-provision tokens for the existing base; provision new cards at save time.
4. Send token + cryptogram on CIT and MIT; keep PAN fallback rules explicit.
5. Subscribe to token lifecycle updates (reissue, expiry) so stored credentials stay current.
6. Hold out a random 10–20% on PAN for 60–90 days; compare.

## Prerequisites
- Token requestor ID (yours, or your PSP's — note portability implications, card 11).
- Vault able to store token + PAN mapping; PCI scope reviewed.
- Gateway support for cryptograms on MIT; scheme token fees understood [GAP: public scheme token fee schedules].
- Issuer coverage check by market.

## Metrics and expected impact
- Approval rate, fraud rate, and involuntary churn on stored-card transactions, tokenised vs PAN holdout.
- **Public reference (scheme-reported, self-interested; network-wide averages, not a merchant forecast):**
  - Visa: 4.8% higher authorisation rate for tokenised vs PAN CNP (VisaNet, Jan–Dec 2025); 39.4% lower fraud rate (FY25). https://www.visa.com/en-us/solutions/tokenization
  - Visa earlier: ~3% auth uplift, 28% fraud reduction. https://usa.visa.com/content/dam/VCOM/regional/na/us/Solutions/documents/visas-journey-through-tokenization.pdf
  - [GAP: Mastercard public figure; independent (non-scheme) measurement.]
- **Your range: [Assumption]** — expect lower than scheme averages where your PAN approval rate is already high; size from holdout.

## Failure modes
- Token provisioning failures on some issuers → monitor provisioning success by BIN; PAN fallback.
- Token locked to PSP's requestor ID → harder to multi-acquire (ties to Issue 1, card 11).
- Retry counters: schemes may count token and PAN attempts separately; don't use switching as a retry dodge [CONFIRM current Visa Rules].
- Lifecycle updates not applied → stale credentials, rising declines.
- Token fees exceed uplift on low-ticket flows → model per-transaction economics.

## Owner
Payments product decides; card-vault owner builds; finance validates net value; risk tracks fraud.

## Cross-market column
| Market | Notes |
|---|---|
| US | Highest card-on-file share; [GAP: debit token routing interplay with Reg II dual-network] |
| UK/EU | Tokens interact with SCA: MIT exemptions and initial authentication; [GAP: EBA/SCA source] |
| Africa | Issuer token enablement uneven; Visa CEMEA cites 4.3% uplift (VisaNet Oct–Dec 2023) https://globalclient.visa.com/cemea-network-tokens [GAP: market-level issuer coverage] |
| APAC | India RBI card-on-file tokenisation mandate (merchants may not store card data) [GAP: cite RBI circular URL]; other markets voluntary |

## War story
[WAR STORY: CONFIRM WITH AVI]

## What I'd do Monday
1. Count stored credentials and who owns the vault/requestor ID.
2. Ask your PSP for token provisioning coverage by issuer.
3. Price token fees vs expected recovered approvals.
4. Set up a PAN holdout before switching anything.
