# Margin Wars Briefing: Method Changes Log

Each weekly public-signals run records the method it used, what worked or didn't, and the concrete changes for the next run. Changes are dated so later runs can see whether each one improved coverage or accuracy (scored through forecast-log.md and through stale figures caught before send).

---

## Run 1 (2026-10-26): baseline

**Baseline method used**
1. **Scope:** the last 2–4 weeks, plus anything pending or scheduled to take effect. Four regions (US, UK/EU, Africa, APAC), mapped to the Briefing's tactics (routing, tokens, retries, IC++, chargebacks, CEDP, FX/DCC, PayFac, stablecoin as a cost line).
2. **Sources, in order of preference:** network rule books, regulator, court and statute pages first. Then acquirer and processor merchant notices (e.g. Checkout.com merchant communications, TD fee schedules). Trade press (Payments Dive, PYMNTS, Electronic Payments International, TechCentral, ThisDay) is used only for dates and context. Every fact is cited with its URL and access date.
4. **Draft check:** every sourced figure in issues 01–03 and the playbook skeleton was checked against the current primary source and marked current, stale or gap-fill.
5. **Peer scan:** archive headlines for Payments Dive, Fintech Business Weekly, Brainfood, This Week in Fintech and Net Interest, to find what is crowded and what is open.
6. **Confidence:** High (primary source read directly), Medium (good secondary source, or seen only through a search summary), Low (single secondary source).
7. **Foresight:** 3–5 dated calls with probabilities and leading indicators (forecast-log.md).

**What run 1 showed**
- The most valuable findings came from **primary rule text, not news**. The Visa public rules PDF (edition of 18 Apr 2026) showed Issue 03's Category 1 list is incomplete and supplied rule 1.7.2.1 (Acquiring Identifier) for Issue 01. No news source covered either point.
- Gateway help articles can lag. The Checkout.com retry article cited in the drafts still says "15" in its body.
- federalregister.gov blocks automated fetches (CAPTCHA). The agency's own page (OCC bulletin, Treasury press release) worked.
- There wasn't time to check Payments NEXT, MPE, The Paypers or DCC/FX rules.

**Changes adopted from run 2 onward**
1. **A standing primary-source checklist, run every week before any news search:**
   - Visa public rules PDF: check the edition date and Summary of Changes.
   - Checkout.com merchant communications and network-roadmap articles.
   - PSR / FCA publications.
   - RBA payments and the Federal Register of Legislation (AU standards).
   - Federal Reserve Reg II and the interchange settlement site.
   - OCC and Treasury GENIUS pages.
   - ESMA / EBA / Council press.
   - SARB / National Treasury, CBN circulars, CBK, RBI notifications, HKMA, MAS.

   If an edition date or effective date changes, that alone triggers a read.
2. **A standing "figures in drafts" register.** Each run, every number cited in a draft issue or playbook card is listed with its source and the date it was last checked. Any figure whose source changed, or that hasn't been checked within 30 days of its send date, is flagged. The check runs against the primary source; a gateway help page counts only as corroboration.
3. **Fetch-block fallbacks:** for federalregister.gov, go to the issuing agency's page first. For paywalled peers, scan headlines only and say so.
4. **Coverage gaps carried forward to run 2:** Payments NEXT, MPE, The Paypers, FX/DCC rule changes (incl. the EU PSR's currency-conversion provisions), Mastercard primary rules (Transaction Processing Rules / MAC), and whether the Mastercard Europe token requirement covers the UK.

---

## Run 2 (2026-11-02)

**Method used**
1. We ran the **standing primary-source checklist first**, before any news search. The Visa public rules PDF was downloaded, its edition date was read from the cover and from `pdfinfo`, and the Summary of Changes, Table 7-2, §1.7.2.1 and Table 11-29 were read in full. The rest of the list: Checkout.com merchant communications and support articles, the PSR, the RBA (and NAB's first transparency table), eCFR §235.7, the settlement site, the OCC and Treasury, the ESMA, EBA, Council and BoE pages, the SARB and National Treasury, the CBN, CBK and RBI, and the MAS and HKMA.
2. **Carried-forward gaps:**
   - EU PSR currency conversion was filled, through a consolidated rendering of the Council text.
   - Mastercard primary rules are still blocked, so we used acquirer fallbacks (Adyen, Checkout, Stripe).
   - Whether the Mastercard Europe token requirement covers the UK is still unverified.
   - Payments NEXT, MPE and The Paypers were all scanned.
3. **Figures-in-drafts register** built for Issues 01–03, the playbook skeleton and WS1–WS6. See section F of public-signals-2026-11-02.md.
4. **Fetch-block fallbacks used:** federalregister.gov (agency pages and search), mastercard.com (acquirer docs), NPCI PDFs (DFS FAQ and Business Standard), and SEC EDGAR (curl with a declared user agent).
5. **Forecast scoring:** all 5 run-1 calls were checked against primary sources before any new calls were written.

**What was missed (in run 1) and why**
- **The Mastercard TLID requirement (23 Oct 2026)** was missed. It sits in a Checkout.com *support* article, not in merchant communications, and run 1's checklist line only named merchant communications and the token roadmap. It was already in force when run 1 ran.
- **The timing of the Corner Post (8th Circuit) ruling** was missed. Run 1 treated Reg II as "stayed pending appeal" and had no court-docket watch, so a ruling issued on the same day as run 1 (26 Oct 2026) was not picked up.
- **Visa edition-date ambiguity.** Run 1 logged the edition as 18 Apr 2026, but the PDF at the same URL is the 24 Oct 2026 edition, created 23 Oct 2026, before run 1's access. That made F-20261026-5 close to pre-resolved. We can't tell whether run 1 read a cache or misread the cover.
- **Not done this run:** Mastercard primary rule text (blocked), confirmation that the RBA has republished the 30 Oct data, the PSR £150–200m source document, and a re-check of the WS2 VAMP figures and WS6 PayShap and GoTyme figures (not urgent given their send dates).

**Changes adopted from run 3 onward**
1. **Widen the checklist to include network-roadmap *support* articles and a court-docket watch.**
   - Add the Checkout.com support "network roadmap" and scheme-change articles (TLID-type mandates), plus the Stripe docs changelog for card-network changes, alongside merchant communications.
   - Add a standing docket watch for the 8th Circuit No. 25-3000 mandate and rehearing, the 6th Circuit *Linney's Pizza* case, and MDL 1720 / E.D.N.Y. (the settlement site plus a search on the hearing date).
   - Any decision or mandate there triggers a re-check of every US figure in the register.
2. **Provenance check on secondary sources, and edition-date capture.**
   - For every rule book, record both the cover edition date and the `pdfinfo` CreationDate.
   - A forecast about "the next edition" must name the edition it is measured against.

---

## Run 3 (2026-11-09)

**Method used**
1. **We followed both run-2 changes.**
   - *Widened primary checklist:* Visa PDF (cover date, `pdfinfo` CreationDate/ModDate and, newly, a SHA-256 hash, so "unchanged" is provable); Checkout.com merchant communications **and** support/network-roadmap articles; the Stripe docs changelog; PSR/FCA; RBA; Fed/eCFR; the settlement site; OCC/Treasury; Council and the **EP Legislative Observatory**; BoE; SARB/Treasury; CBN; CBK; RBI/NPCI; MAS/HKMA.
   - *Court-docket watch:* Justia (8th Cir. 25-3000), CourtListener (6th Cir. 25-6038), and the settlement site for MDL 1720.
2. After the checklist we ran news, the peer scan (Payments Dive, Brainfood, FBW, The Paypers, Payments NEXT, MPE, the fintechnewsletters aggregate), then regulation by region, then forecast scoring.
3. **Fallbacks used:**
   - EUR-Lex was blocked, so the UK IFR was read on legislation.gov.uk and the EU IFR is flagged for a manual check.
   - NPCI PDFs were blocked, so we relied on search plus MediaNama and FE.
   - Court dockets (CourtListener MDL, DocketBird) were blocked, so we used the settlement site.
   - cbn.gov.ng had no link to the regulation, so we used a full-text rehost and ThisDay.

**What was missed (in earlier runs) and why**
- **PSR PS26/1, the scheme-fee directions (30 Jul 2026; pricing governance live from 30 Nov 2026), was missed by runs 1 and 2.** The checklist line "PSR / FCA publications" was in practice run as "re-read the cross-border interchange review page". The scheme-fee market review is a separate workstream, so a page-specific check never saw it.
- **Mastercard M4M→SCOF switchover (31 Dec 2026) was missed by run 2.** The Checkout support article is dated the same day (24 Sep 2026) as the Europe-roadmap article run 2 did read. Run 2 read named articles rather than listing the support section's recent articles. The widened run-3 checklist caught it.
- **The *Linney's Pizza* argument date (22 Oct 2026) was not recorded in run 2**, because there was no docket watch until this run.
- **RBI E-mandate Framework 2026 (21 Apr 2026)** has been a primary source available all along, but runs 1–2 left it as a GAP. GAP items were carried forward without a targeted search.
- **Citation slip in run 2:** the PSR "21/27 months" figures were cited to the Council *statement of reasons*, which contains no month figures. The figure was right but the cite was wrong. It is now cited to ST 8543/1/26 REV 1 and ST 8535/1/26 REV 1.
- **Near-miss caught this run:** a search engine synthesis stated as fact that the settlement had been approved at the 16 Nov hearing (a future date), working from the *proposed* order. The settlement site check caught it.
- **Process gap:** none of run 2's recommended draft edits have been applied (draft files still dated 6 Nov). The register did not show this, because it tracked figures, not whether edits landed.

**Changes adopted from run 4 onward**
1. **Sweep each regulator's whole publication list, not a single tracked page, and target every GAP.** For each checklist regulator, list publications/policy statements dated since the last run (PSR "Publications" across all market reviews; RBA media releases; RBI notifications and master directions; NPCI circulars; CBN circulars; EP OEIL key events). For each Checkout/Stripe source, list the support section's recently updated articles rather than re-reading named ones. In addition, run one targeted search per open "[GAP]" in the drafts each week, and close or re-date it.
2. **Guard against search syntheses and track whether edits landed.**
   - (a) A search-engine synthesis may never be the sole basis for an event that is dated on or after the run date, or that comes from a "proposed" or draft document. Such events need the primary page (court site, regulator, docket) or are logged as "unverified".
   - (b) The figures-in-drafts register keeps the "Applied in draft?" column piloted this run. Any recommended edit not applied within 14 days of its send date is escalated in the report-back as a material item.
