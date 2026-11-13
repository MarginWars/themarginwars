# The Margin Wars Briefing: public signals and approach

*Week of 2 November 2026 · Run #2 · Public sources only, all accessed 2 Nov 2026*

## Public signals (week of 2026-11-02)

**Previous runs:** [week of 26 October 2026](page-content-2026-10-26.md) (run #1, baseline). Full sourced findings for this week, including the figures-in-drafts register, are in public-signals-2026-11-02.md.

1. **A US appeals court has struck down the 21-cent debit fee cap, but nothing changes yet.** On 26 October the 8th Circuit agreed that the Fed's Reg II cap must be rebuilt on a transaction-specific cost basis, and sent it back to the Fed without setting a new number. The ruling only takes effect when the court issues its mandate, which on our reading cannot happen before about mid-December. The routing rule that lets merchants choose a second debit network is not affected. [8th Circuit opinion, No. 25-3000](https://ecf.ca8.uscourts.gov/opndir/26/10/253000P.pdf) · [Payments Dive](https://www.paymentsdive.com/news/fed-loses-debit-card-cap-appeal/872785/) · [eCFR §235.7](https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-235/section-235.7)
2. **Visa published a new rules edition dated 24 October 2026, and the retry limits held.** Up to 20 reattempts in 30 days are still allowed for Categories 2–4, and none for Category 1, which still includes 12, R0, R1 and R3. The new edition also bans non-zero "verification" authorisations, adds Anticipated Amount Validation for $0 checks, and stops issuers returning code 51 to an account verification. [Visa Core Rules, 24 Oct 2026, Table 7-2 and §7.3.10](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)
3. **Mastercard now requires the Transaction Link Identifier on every merchant-initiated payment (from 23 October).** If the original customer-initiated payment ran through another provider, the merchant has to supply the identifier, so multi-acquirer and migration set-ups must store and pass it. [Checkout.com: Mastercard TLID](https://support.checkout.com/hc/en-us/articles/33589249067538-Mastercard-Transaction-Link-Identifier) · [Stripe docs: Mastercard TLID](https://docs.stripe.com/payments/cards/mastercard-tlid)
4. **Not tokenising now has a price in several regions.** According to one acquirer's notice:
   - Visa Europe charges 7.5 bps on approved authorisations that carry neither a token nor 3DS.
   - Mastercard charges 4 bps on non-tokenised card-on-file payments in Asia Pacific outside Australia and New Zealand.
   - Both networks have 5 bps fees in the UAE, starting October 2026 (Visa) and January 2027 (Mastercard).

   [Checkout.com: network token incentives and fees](https://www.checkout.com/merchant-communications/reminder---network-tokens-incentives-and-fees)
5. **EU governments have formally adopted their position on the new payments rules (PSD3 and the Payment Services Regulation), 27–0, on 29 October.** The European Parliament's second-reading vote is next. The regulation will replace today's currency-conversion benchmark with an aggregated mid-market rate, but only about 21 months after it enters into force. [Council vote, PSD3](https://data.consilium.europa.eu/doc/document/ST-15152-2026-INIT/en/pdf) · [Council vote, PSR](https://data.consilium.europa.eu/doc/document/ST-15154-2026-INIT/en/pdf) · [paymentslaw.eu: PSR Article 5](https://paymentslaw.eu/psr/art-5/compare/)
6. **Australia's first published merchant-fee averages show foreign cards costing more than twice as much as domestic credit.** NAB's July–September table puts the average merchant service fee at 0.58% overall, 0.80% for domestic card-present credit, and about 1.95% for foreign-issued cards. A 1.0% interchange cap on foreign cards follows in April 2027. [NAB average merchant service fees, Jul–Sep 2026](https://www.nab.com.au/content/dam/nab/documents/guides/payment-and-merchants/average-merchant-service-fees-july-to-september-2026.pdf) · [RBA transparency requirements](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/appendix-c.html)
7. **India will start charging merchants 0.4% on UPI payments above ₹2,000, capped at ₹300, once a start date is set.** Smaller payments, which are more than 95% of merchant volume, stay free. The launch was pushed from 15 October to "after Diwali", and no new date has been set. [Finance ministry FAQ](https://financialservices.gov.in/sites/default/files/2026-09/FAQs---Merchant-Discount-Rate--MDR--on-Select-UPI--P2M--Transactions_0.pdf) · [Business Standard](https://www.business-standard.com/finance/news/upi-mdr-deferred-until-after-diwali-new-date-to-be-notified-npci-126101300556_1.html)
8. **Still waiting:**
   - The US swipe-fee settlement's final hearing is on 16 November.
   - The UK regulator has not set a level or date for its UK–EEA fee cap.
   - South Africa has not republished its cross-border crypto rules.

   [Settlement proposed final order](https://www.interchangeequitablereliefsettlement.com/Content/Documents/%5BProposed%5D%20Class%20Settlement%20Order%20and%20Final%20Judgment.pdf) · [PSR cross-border interchange review](https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/) · [EWN](https://www.ewn.co.za/treasury-to-revise-crypto-rule-proposals-after-draft-elicited-thousands-of-comments)

## Our approach

The approach itself is unchanged: one tactic per issue, four markets side by side, primary sources first, and gaps left visible. This week's read is that the most useful material for operators is in rule text that peers are not covering. Agentic commerce, stablecoin theses and earnings recaps are crowded. The TLID requirement, the Visa verification changes, the stacking of fees on non-tokenised traffic and Australia's published fee averages are open. We will put these into the existing drafts rather than start new pieces.

**Issue 01 (dual-network and multi-acquirer routing, sends 1 December 2026)**

- Add one sentence to the US column saying that the 21-cent cap still applies until the 8th Circuit's mandate issues, that no replacement has been set, and that the routing rule in §235.7 is unaffected. The issue should not promise any new rate.
- Replace the "[CONFIRM]" retry citation with the Visa rules (24 October 2026 edition, Table 7-2).
- Add the Mastercard TLID requirement as a prerequisite for routing merchant-initiated payments across acquirers.
- Fill the UK gap with the 1.15% (debit) and 1.5% (credit) UK–EEA online rates, and the APAC gap with Australia's surcharge ban, the coming 1.0% foreign-card cap and the NAB fee averages.
- Describe the settlement as "pending" whatever happens at the hearing.
- Re-read the EU interchange caps before sending. They were last checked more than 30 days before the send date.

**Issue 02 (network tokens, sends 5 January 2027)**

- Keep Visa's 4.8% approval uplift and 39.4% fraud reduction, which are still on Visa's site.
- Drop the older 3% and 28% figures, and label the 4.3% CEMEA figure as 2023 data.
- Add a "cost of not tokenising" line by region: Europe 7.5 bps, Asia Pacific 4 bps, UAE 5 bps, cited to the acquirer notice.
- Keep the UK marked as unconfirmed for Mastercard's Europe card-on-file token requirement.
- Add Visa Recurrent Service and Visa Europe's October 2027 approval-rate thresholds as reasons why tokens and authentication will matter more.
- Leave the Mastercard Europe card-on-file fee as a gap. The only figures we found trace back to a source we exclude.

**Issue 03 (retries and decline codes, sends 2 February 2027)**

- Add 12, R0, R1 and R3 to the Category 1 list, and cite Table 7-2 of the 24 October 2026 edition (pages 547–549).
- Add three rules from the new edition:
  - code 51 on a $0 account verification is an issuer error, not a retry signal;
  - non-zero "verification" authorisations are now banned;
  - Anticipated Amount Validation is the sanctioned way to pre-check funds.
- Add a Mastercard column, labelled as acquirer-sourced: never retry after MAC 03 or 21; limits of 10 attempts in 24 hours and 35 in 30 days.
- Cite the $0.25 cross-border fee to the acquirer notice and note that Visa's own fee schedule is not public.
- Add the TLID to the prerequisites for retrying merchant-initiated payments.
- Find a primary RBI source for the e-mandate rules.

**Playbook cards**

- Card 05 (chargebacks): add the AVS liability shift in parts of Asia Pacific, Europe and Latin America.
- Card 07 (FX and DCC): add the regulation's mid-market-rate rule, marked "adopted, not yet applicable".
- Card 08 (PayFac): remove Visa's CEMEA PayFac certification, which Visa has dropped.
- Card 10 (APMs): add India's UPI charge.
- Card 11 (portability): add TLID portability.

**Working sessions**

- WS4: flag the coming change of currency-conversion benchmark.
- WS3: find the source document for the £150–200m UK figure before the session.

## Expected vs happened

Run 1 made five calls. One has resolved and four are too early to score.

- **Hit, resolved early.** We said Visa's next public rules edition would keep the 20-in-30 retry limit and the Category 1 ban (85%), and the 24 October 2026 edition does (Brier score 0.0225). There is a caveat: that edition's file was created on 23 October, before the call was made. So the call told us less than it appeared to, and we have made a fresh call on the edition after this one.
- **Too early, moving our way.** EU governments adopted both texts 27–0 on 29 October, which supports our 70% call that PSD3 and the regulation reach the Official Journal by 31 March 2027.
- **Too early, no movement.**
  - The US settlement call (60% by 31 January 2027) still turns on the 16 November hearing.
  - The UK cap proposal (30%) has seen no movement.
  - The South African crypto redraft (45%) has seen no movement.

**What we did not expect:** the 8th Circuit's debit-cap ruling (26 October) and Mastercard's TLID requirement (23 October) were both missed by run 1. Both now shape Issue 01.

## Foresight

| Call | Likelihood | By |
|---|---|---|
| European Parliament approves both PSD3 and the Payment Services Regulation at second reading without amendments | 80% | 31 Dec 2026 |
| The 8th Circuit issues its mandate, so the 21-cent cap's vacatur takes effect | 40% | 31 Jan 2027 |
| India's 0.4% UPI merchant charge above ₹2,000 goes live | 55% | 31 Jan 2027 |
| Court grants final approval of the US Visa/Mastercard settlement by year-end | 35% | 31 Dec 2026 |
| Visa's next public rules edition after October 2026 keeps the 20-in-30 limit and the Category 1 ban | 85% | 31 May 2027 |

**What we're watching:**

- the 16 November settlement hearing;
- any petition for rehearing in the 8th Circuit case, due around 10 December;
- the European Parliament plenary, indicatively 14 December;
- an NPCI circular setting a start date for the UPI charge;
- the RBA republishing the first fee data;
- the PSR's merchant survey;
- South Africa's February Budget.

## Method changes

- **Watch network-roadmap support articles and court dockets, not just announcements.** Run 1 missed Mastercard's TLID requirement because it sat in an acquirer support article, and the debit-cap ruling because it had no court watch. Both are now on the weekly checklist.
- **Check where a secondary source got its numbers.** If they trace back to a source we exclude, we log a gap and do not use them. For rule books, we record both the cover date and the file's creation date, so a forecast about "the next edition" names the edition it is measured against.

## Sources

All accessed 2 Nov 2026:

- [Visa Core Rules and Visa Product and Service Rules, 24 Oct 2026](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)
- [8th Circuit opinion, Corner Post v. Board of Governors, No. 25-3000](https://ecf.ca8.uscourts.gov/opndir/26/10/253000P.pdf)
- [Payments Dive: Fed loses debit card cap appeal](https://www.paymentsdive.com/news/fed-loses-debit-card-cap-appeal/872785/)
- [Consumer Finance Monitor on the 8th Circuit ruling](https://www.consumerfinancemonitor.com/2026/10/28/eighth-circuit-invalidates-federal-reserves-21-cent-debit-card-interchange-fee-cap-holding-that-the-durbin-amendment-requires-a-transaction-specific-cost-analysis/)
- [eCFR 12 CFR 235.7 (Reg II routing)](https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-235/section-235.7)
- [Checkout.com: Mastercard Transaction Link Identifier](https://support.checkout.com/hc/en-us/articles/33589249067538-Mastercard-Transaction-Link-Identifier)
- [Stripe docs: Mastercard Transaction Link ID](https://docs.stripe.com/payments/cards/mastercard-tlid)
- [Checkout.com: network token incentives and fees](https://www.checkout.com/merchant-communications/reminder---network-tokens-incentives-and-fees)
- [Checkout.com: changes to Visa system integrity fees](https://www.checkout.com/merchant-communications/changes-to-visa-system-integrity-fees)
- [Checkout.com: when can I retry a declined transaction](https://support.checkout.com/hc/en-us/articles/25482040901394-When-can-I-retry-a-declined-transaction)
- [Adyen: non-transactional scheme fees](https://help.adyen.com/knowledge/finance/invoices/what-are-non-transactional-scheme-fees)
- [Checkout.com: Mastercard network token roadmap for Europe](https://support.checkout.com/hc/en-us/articles/39223370002962-What-is-Mastercard-s-network-token-roadmap-for-Europe)
- [Visa: tokenization](https://www.visa.com/en-us/solutions/tokenization)
- [Visa Q4 FY2026 earnings call transcript (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/10/28/visa-v-q4-2026-earnings-call-transcript/)
- [Council of the EU vote result, PSD3](https://data.consilium.europa.eu/doc/document/ST-15152-2026-INIT/en/pdf)
- [Council of the EU vote result, PSR](https://data.consilium.europa.eu/doc/document/ST-15154-2026-INIT/en/pdf)
- [2eu.brussels: Council approves payment rules positions](https://2eu.brussels/en/news/eu-council-unanimously-approves-positions-on-new-payment-rules-ahead-of-parliament-s-final-vote)
- [paymentslaw.eu: PSR Article 5 (currency conversion)](https://paymentslaw.eu/psr/art-5/compare/)
- [Interchange settlement: proposed final order](https://www.interchangeequitablereliefsettlement.com/Content/Documents/%5BProposed%5D%20Class%20Settlement%20Order%20and%20Final%20Judgment.pdf)
- [Celt Payments: settlement final approval hearing](https://celtpayments.com/news/settlement-final-approval-hearing-nov-2026/)
- [PSR cross-border interchange review](https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/)
- [NAB: RBA transparency reporting](https://www.nab.com.au/business/payments-and-merchants/rba-transparency-reporting)
- [NAB average merchant service fees, Jul–Sep 2026](https://www.nab.com.au/content/dam/nab/documents/guides/payment-and-merchants/average-merchant-service-fees-july-to-september-2026.pdf)
- [RBA conclusions paper, Appendix C (transparency)](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/appendix-c.html)
- [RBA backgrounder on least-cost routing](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/backgrounders/backgrounder-on-least-cost-routing.html)
- [India Department of Financial Services: UPI MDR FAQ](https://financialservices.gov.in/sites/default/files/2026-09/FAQs---Merchant-Discount-Rate--MDR--on-Select-UPI--P2M--Transactions_0.pdf)
- [Business Standard: UPI MDR deferred](https://www.business-standard.com/finance/news/upi-mdr-deferred-until-after-diwali-new-date-to-be-notified-npci-126101300556_1.html)
- [EWN: South Africa to revise crypto rules](https://www.ewn.co.za/treasury-to-revise-crypto-rule-proposals-after-draft-elicited-thousands-of-comments)
- [Brainfood archive](https://www.fintechbrainfood.com/archive)
- [Fintech Business Weekly archive](https://fintechbusinessweekly.substack.com/archive)
- [The Paypers: payments](https://thepaypers.com/payments)
