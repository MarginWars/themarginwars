# Margin Wars Briefing: Public Signals & Approach

*Week of 26 October 2026 · Run #1 · Public sources only, all accessed 26 Oct 2026*

## Public signals (week of 2026-10-26)

1. **Visa's rules list more "never retry" codes than most cheat-sheets.** Category 1 includes 12, R0, R1 and R3 as well as 04/07/14/15/41/43/46/57. The limit is up to 20 reattempts in 30 days for Categories 2–4. [Visa Rules, 18 Apr 2026, Table 7-2](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)
2. **Retrying through a different acquirer can break Visa's rules.** Reattempts must not change the Acquiring Identifier, MCC, country or POS fields of the original request. [Visa Rules §1.7.2.1](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)
3. **Mastercard Europe now requires network tokens for card-on-file payments** (from 1 Oct 2026). Guest checkout follows in 2028 and all e-commerce in 2030. [Checkout.com](https://support.checkout.com/hc/en-us/articles/39223370002962-What-is-Mastercard-s-network-token-roadmap-for-Europe) · [Mastercard](https://www.mastercard.com/global/en/news-and-trends/press/2024/june/mastercard-reimagines-online-checkout-commits-to-reaching-100-e-commerce-tokenization-by-2030-in-europe.html)
4. **Visa CE3.0 now counts prior purchases at other merchants** (from 24 Oct 2026), which should make friendly-fraud disputes easier to win. [Visa Rules, Summary of Changes](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf) · [Payments Marketplace](https://payments-marketplace.com/insights/visa-compelling-evidence-october-2026/)
5. **US swipe-fee settlement: final hearing 16 Nov 2026.** Terms: credit interchange down 10 bps for 5 years, standard credit capped at 125 bps, merchants can decline premium and commercial cards, and surcharging gets easier. Walmart and others object. [Settlement notice](https://interchangeequitablereliefsettlement.com/Content/Documents/Publication%20Notice.pdf) · [Payments Dive](https://www.paymentsdive.com/news/visa-mastercard-urge-court-to-approve-fee-settlement/833241/)
6. **Australia banned card surcharges on 1 Oct 2026** and set debit at 8c/0.16% and consumer credit at 0.3%. A **1.0% cap on foreign-issued cards** follows on 1 Apr 2027. [RBA](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/interchange-fees.html) · [RBA FAQ](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/faqs/index.html)
7. **UK–EEA online card fees are still 1.15% (debit) and 1.5% (credit).** The PSR's power to cap them was upheld, but there's no cap level or date yet. [PSR](https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/)
8. **Visa's US DCAP pays 0.10% net** on consumer-credit customer-initiated transactions that are both authenticated and tokenised. Stored-credential transactions don't qualify. [Checkout.com](https://support.checkout.com/hc/en-us/articles/34456715799570-What-is-Visa-s-Digital-Commerce-Authentication-Program-DCAP)
9. **India's 2026 e-mandate framework** sets the recurring-payment rules: a pre-debit notice at least 24 hours ahead, and no extra authentication up to ₹15,000. [RBI](https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13374)
10. **Nigeria: no extension to the 1 Jan 2027 deadline for storing payment data in-country.** [ThisDay](https://www.thisdaylive.com/2026/10/08/cbn-insists-on-data-localisation-says-no-extension-in-january-2027-deadline/)
11. **Stablecoin rules are taking shape.** The US OCC's final GENIUS rule takes effect 18 Jan 2027. EU platforms must drop non-MiCA stablecoins (ESMA, 8 Oct). South Africa will redraft its cross-border crypto rules. [OCC](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-50.html) · [ESMA](https://www.esma.europa.eu/press-news/esma-news/esma-sets-out-supervisory-expectations-services-related-unauthorised) · [TechCentral](https://techcentral.co.za/treasury-crypto-rules-rethink-mtbps/287515/)
12. **Stablecoin payouts are live on the networks, but demand is thin.** Visa Direct is in production with USDC prefunding, and Mastercard has launched a platform with BVNK. Yet only 1 of 148 firms in a Cleveland Fed survey uses stablecoins. [Visa](https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-direct-moves-stablecoin-pilots-production.html) · [Mastercard](https://www.mastercard.com/us/en/news-and-trends/press/2026/october/mastercard-and-bvnk-launch-global-money-platform-to-power-a-mult.html) · [Cleveland Fed](https://www.clevelandfed.org/publications/economic-commentary/2026/ec-202622-will-us-firms-adopt-stablecoins)

## Our approach

- **One tactic per issue, four markets side by side** (US, UK/EU, Africa, APAC), always expressed in basis points or cost.
- **Primary sources first:** network rule books, regulators and courts. Trade press is used only for dates and context. Every fact carries a link and an access date.
- **Gaps stay visible.** If we can't verify something, we say so rather than fill it in.
- **No fluff:** we skip themes the peers already cover (AI agents, stablecoin theses) unless there is a cost line an operator can act on.

## Expected vs happened

Run 1 is the baseline, so there were no earlier calls to score. From the next run, every call below is checked against what happened and marked hit, miss or too early, with a score.

## Foresight

| Call | Likelihood | By |
|---|---|---|
| Court gives final approval to the US Visa/Mastercard settlement | 60% | 31 Jan 2027 |
| EU PSD3 + Payment Services Regulation published in the Official Journal | 70% | 31 Mar 2027 |
| UK regulator proposes a specific UK–EEA interchange cap | 30% | 30 Jun 2027 |
| South Africa publishes a revised draft of its cross-border crypto rules | 45% | 31 Mar 2027 |
| Visa keeps its 20-in-30-days retry limit in its next public rules edition | 85% | 31 May 2027 |

**What we're watching:** the 16 Nov hearing; EU Parliament's vote (indicatively 14 Dec); the PSR merchant survey; South Africa's February Budget; Visa's next Summary of Changes.

## Method changes

- **Weekly primary-source checklist:** network rule editions and regulator pages are checked before any news search.
- **Every figure in our drafts is re-checked against its primary source before send**, with the date it was last checked.
- **Gateway help pages are corroboration only.** This week one still showed an outdated retry limit.

## Sources

All accessed 26 Oct 2026:
- [Visa Core Rules (public edition, 18 Apr 2026)](https://usa.visa.com/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)
- [Checkout.com: Mastercard Europe token roadmap](https://support.checkout.com/hc/en-us/articles/39223370002962-What-is-Mastercard-s-network-token-roadmap-for-Europe)
- [Checkout.com: Visa DCAP](https://support.checkout.com/hc/en-us/articles/34456715799570-What-is-Visa-s-Digital-Commerce-Authentication-Program-DCAP)
- [Mastercard 2030 tokenisation release](https://www.mastercard.com/global/en/news-and-trends/press/2024/june/mastercard-reimagines-online-checkout-commits-to-reaching-100-e-commerce-tokenization-by-2030-in-europe.html)
- [Payments Marketplace: Visa CE3.0](https://payments-marketplace.com/insights/visa-compelling-evidence-october-2026/)
- [Interchange equitable-relief settlement notice](https://interchangeequitablereliefsettlement.com/Content/Documents/Publication%20Notice.pdf)
- [Payments Dive: settlement filings](https://www.paymentsdive.com/news/visa-mastercard-urge-court-to-approve-fee-settlement/833241/)
- [RBA conclusions: interchange](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/interchange-fees.html)
- [RBA FAQ](https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/faqs/index.html)
- [PSR cross-border interchange review](https://www.psr.org.uk/our-work/market-reviews/market-review-into-cross-border-interchange-fees/)
- [RBI e-mandate framework 2026](https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13374)
- [ThisDay: CBN data localisation](https://www.thisdaylive.com/2026/10/08/cbn-insists-on-data-localisation-says-no-extension-in-january-2027-deadline/)
- [OCC Bulletin 2026-50](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-50.html)
- [ESMA on non-MiCA stablecoins](https://www.esma.europa.eu/press-news/esma-news/esma-sets-out-supervisory-expectations-services-related-unauthorised)
- [TechCentral: SA crypto rules rethink](https://techcentral.co.za/treasury-crypto-rules-rethink-mtbps/287515/)
- [Visa Direct stablecoin production](https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-direct-moves-stablecoin-pilots-production.html)
- [Mastercard–BVNK Global Money Platform](https://www.mastercard.com/us/en/news-and-trends/press/2026/october/mastercard-and-bvnk-launch-global-money-platform-to-power-a-mult.html)
- [Cleveland Fed stablecoin survey](https://www.clevelandfed.org/publications/economic-commentary/2026/ec-202622-will-us-firms-adopt-stablecoins)
- [Regulation Tomorrow: PSD3 Council position](https://www.regulationtomorrow.com/2026/10/psd3-council-of-eu-publishes-first-reading-position-with-view-to-adoption/)

The full signal list (31 items, with confidence ratings) is in public-signals-2026-10-26.md.
