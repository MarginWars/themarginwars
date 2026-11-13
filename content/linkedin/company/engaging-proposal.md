---
id: li-company-engaging
channel: linkedin-company
kind: proposal
status: draft
owner: channels
approvals: {}
sources: []
---

# The Margin Wars: making the LinkedIn company page engaging (proposal)

**Status: proposal only. Nothing has been changed, posted or scheduled on LinkedIn.** Drafted Tue 10 Nov 2026, about 5:45 PM PT, at Avi's request ("The LinkedIn page should be engaging", 5:35 PM PT). Soft launch still applies: every post below is a draft and needs Avi's explicit go before anything is edited or published.

Page: https://www.linkedin.com/company/themarginwars

**Where "current" comes from:** the copy filled in on 10 Nov 2026 (`about.md` / `about_paste.txt` in this folder), confirmed against the member-view screenshot `shot_linkedin_pink.png` (10:50 AM PT, 10 Nov): tagline "Payments tactics from the front lines.", Overview starting "Avi and Anitha run The Margin Wars as one team…", Financial Services, 2-10 employees, Follow + Message buttons only, no custom button visible. The live page was not re-opened for this proposal.

**Fact sources:** only approved copy that is live in `site_calm/` (home, about, advisory, speaking, writing/Briefing, warroom/Insights, contact, leak). The achievements bank was checked, but nothing from it was used unless it is already on the site; none of its confidential or unpublished figures appear here.

---

## 1. Tagline (max 120 characters)

| Current (38 chars) | Proposed (81 chars) |
|---|---|
| Payments tactics from the front lines. | **Nobody loses margin on the rate. Payments tactics for the line items nobody owns.** |

Why: the current line is a theme ("front lines"). The proposed line opens with the contrarian claim from the home page H1 and promises a tactic. Both halves are site copy (home H1 + "payment tactics" from the title tag). The current line stays on the cover image, so the brand line isn't lost.

Alternates (all ≤120, all site-sourced):
- "Nobody loses margin on the rate. We find the line items that do, rank them by basis points, and name an owner." (110 chars)
- "Payments tactics from the front lines. One move at a time, for US, UK/EU, Africa and APAC." (90 chars)

---

## 2. About / Overview (max 2,000 characters)

What changes: a hook in line 1 (the only thing visible before "see more"), short scannable blocks (*What you get here / Who it's for / Who's behind it*), and a closing CTA. The current version opens with names, which doesn't hook, and on purpose had no CTA.

### Current (2000 chars)

> Avi and Anitha run The Margin Wars as one team, for anyone who owns a payment cost number. Eight years working side by side. One team, for anyone tired of hearing “negotiate the rate”.
>
> Nobody loses margin on the rate. You lose it in the line items nobody owns. We find the line items eating your margin, rank them by basis points, and give each one an owner.
>
> Not one big number. A hundred small ones: downgrades, unchecked scheme fees, hidden FX, soft declines, lazy routing, avoidable cross-border fees. Together, they're the margin.
>
> Specific moves: net revenue over TPV, merchant of record by flow, FX by corridor, local rails, loss-based PayFac pricing. Each shown for US, UK/EU, Africa and APAC.
>
> Every tactic, the same way. The move and how it works, step by step. Prerequisites: contracts, data, systems, people. Metrics and impact range, sourced or labelled as an assumption. Failure modes, early warnings and rollback. Owner: who decides, who builds, who watches the number. Cross-continent campaign column: US, UK/EU, Africa, APAC.
>
>
> What we believe. The rate is the wrong fight. The money is in downgrades, scheme lines and unquoted FX. Net, not gross. Volume flatters. Price on net revenue and take rate. Every corridor is its own front. FX, rails and rules change at every border. Name the owner. No owner, no metric, no move. Know where it breaks. Every tactic ships with a rollback.
>
> Where we've made the case: Snowflake Summit 2025, Money20/20 USA 2024, Fiserv Forum 2024 and MRC Las Vegas 2024.
>
> Views are our own and do not represent any employer or client. No employer or client data is used in any material.

### Proposed (1975 chars)

```
Nobody loses margin on the rate. You lose it in the line items nobody owns.

Downgrades. Unchecked scheme fees. FX markup hiding inside the rate. Soft declines. Volume routed where it went last year. Local-eligible payments paying cross-border fees and FX twice. Not one big number. A hundred small ones. Together, they're the margin.

The Margin Wars is Avi and Anitha. Eight years working side by side. We find the line items eating your margin, rank them by basis points, and give each one an owner.

What you get here
• One tactic at a time, always the same shape: the move step by step, prerequisites, the proof metric (sourced or labelled as an assumption), failure modes and the rollback, and who owns it.
• Every tactic shown for US, UK/EU, Africa and APAC. Every corridor is its own front.
• Twelve moves on the site today, from net revenue over TPV and merchant of record by flow to FX by corridor, local rails, PayFac priced on who carries the loss, and pricing the agent channel before it prices you.

Who it's for
Payments, product and pricing leads at acquirers and PSPs. Payments and finance leads at enterprise merchants. Risk, disputes and treasury leads. Anyone tired of hearing "negotiate the rate".

Who's behind it
Anitha builds acquiring businesses market by market, from launch to enterprise portfolio. She set up Braintree Australia, twice.
On stage: Snowflake Summit 2025, Money20/20 USA 2024, Fiserv Forum 2024, MRC Las Vegas 2024.

Follow for tactics you can run on Monday. Got one bleeding number (cost per order, approvals, chargebacks or FX)? Bring it to us at themarginwars.com.

Views are our own and do not represent any employer or client. No employer or client data is used in any material.
```

Line-by-line sources: hook = home H1/lede; leak list = home "Where margin goes missing" + six fronts (FX, Routing, Cross-border problem lines); team line = About hero; "What you get" = home "Every tactic, the same way" + Briefing "What every issue contains" + About beliefs + warroom move titles (02, 05, 03, 06, 09, 01); "Who it's for" = Briefing "Who it is for" + About hero; "Who's behind it" = About roles and field records; stages = home "Where we've made the case"; CTA = Advisory hero ("Bring one bleeding number…") + Speaking ("moves for Monday"); last line = site footer.

Left out on purpose: the pending patent (so it doesn't read as a CV), "96 hours to 12", employer list, fees, the network/markets stats, "pending a trademark check".

---

## 3. Custom button

| Current | Proposed |
|---|---|
| None visible (Follow + Message only) | **Learn more** → `https://themarginwars.com/warroom?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=page-button` |

Why /warroom: it's the twelve tactics, so the button stays tactics-first and matches "tactics, not themes". It doesn't ask for a sale during the soft launch.
Alternative, once Avi wants inbound: **Contact us** → `https://themarginwars.com/contact?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=page-button-contact`.
Website field: keep `https://themarginwars.com` (canonical, untagged), matching the JSON-LD `sameAs` convention.

Links were built with `marketing/mint_link.py` conventions (`build()` with `write=False`). They are **not** registered in `marketing/links.csv` yet, so no live-looking registry entries exist before approval. Register on approval with, for example:
`python3 marketing/mint_link.py --dest https://themarginwars.com/warroom --source linkedin --medium social --campaign always-on --content page-button`

---

## 4. Specialties (20 of 20)

| Current | Proposed |
|---|---|
| None (left blank on 10 Nov) | Payments strategy; Payment margin; Interchange optimization; Scheme fees; FX pricing; Cross-border payments; Payment acceptance; Authorization rates; Payment routing; Local payment methods; Account-to-account payments; Merchant of record; PayFac and embedded payments; Payments pricing; Net revenue and take rate; Acquiring; Marketplace payments and risk; Agentic commerce; Stablecoin settlement; Payments advisory |

Each one maps to a front, move or format on the site (six fronts, twelve moves, Speaking topics). "Stablecoin settlement" is move 12 on /warroom. Drop it if Avi would rather keep it closed-door only, as on Speaking.

---

## 5. Featured / pinned post ideas

A company page pins one post at a time ("Feature on top of page"). Rotate these:

1. **Start here (pin first).** "Nobody loses margin on the rate." The six fronts in one carousel: problem → our move for each (home copy). CTA → `https://themarginwars.com/warroom?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=featured-start-here`
2. **Tactic card 01 excerpt: "Price the agent channel before it prices you."** This is the public Briefing excerpt, and it fits the spec's "one quarterly LinkedIn excerpt". CTA → `https://themarginwars.com/writing?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=featured-tactic-card`
3. **Spot the Leak challenge.** "One month of fees for an enterprise merchant. Three lines are wrong." Interactive, so good for comments. CTA → `https://themarginwars.com/leak?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=featured-spot-the-leak`
4. **Watch: Snowflake Summit 2025 keynote,** co-presented with Fiserv: zero-copy data between processor and merchant. Proof of stage. CTA → `https://themarginwars.com/speaking?utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=featured-watch`
5. **The Briefing:** "One tactic a month you can run on Monday. Free, by invitation." CTA → `https://themarginwars.com/contact?topic=briefing&utm_source=linkedin&utm_medium=social&utm_campaign=always-on&utm_content=featured-briefing`. (Leave out "About 150 readers" unless Avi confirms it is still current.)

---

## 6. Five first posts (drafts only, do not post)

Campaign tag `2026-11-linkedin-first-posts`, content `post-1` … `post-5`. Suggested rhythm, once Avi says go: one or two a week, with #1 first. Each has a hook, a concrete tactic, an owner or failure-mode beat, and one CTA link.

### Post 1: Downgrades (Interchange front) (824 chars)

```
Your rate didn't change. Your margin did.

That gap is usually downgrades: transactions that fall out of the rate you negotiated and into a worse one.

The usual causes:
• Missing Level 2/3 data
• Wrong card-present flags
• No AVS
• Late capture

The move:
1. Pull the qualification report.
2. Sort it by reason code.
3. Fix the biggest bucket first. Don't touch the rest yet.
4. Give that bucket one owner and one number to watch.

That's the whole tactic. No renegotiation. No new vendor. Just the line item nobody owns, now owned.

It's one of six fronts we work: interchange, scheme fees, FX, acceptance, routing and cross-border.

The other moves, one at a time: https://themarginwars.com/warroom?utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-linkedin-first-posts&utm_content=post-1

#payments #interchange
```

Sources: Home, Interchange front (problem / our move); Advisory route brief, US cards check 01; About, 'Name the owner'; Home, six fronts.

### Post 2: FX by corridor (FX front, move 03) (840 chars)

```
The FX markup hides inside the rate.

If your cross-border price is one blended number, you don't know what you're paying for currency conversion. Neither does the team that owns the corridor.

The move:
1. Quote the FX markup per corridor, per order.
2. Put it on its own line, next to interchange and scheme fees.
3. Then decide where it sits, on purpose, instead of by default.

Why per corridor? Because every corridor is its own front. FX, rails and rules change at every border. US, UK/EU, Africa and APAC each need their own answer.

Before you start: you need the order-level data and someone who owns the number. No owner, no metric, no move.

This is move 03 of twelve: https://themarginwars.com/warroom?utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-linkedin-first-posts&utm_content=post-2

#payments #crossborder #FX
```

Sources: Home, FX front; Insights/warroom move 03 SPREAD; About, 'Every corridor is its own front' and 'Name the owner'; Home/Briefing, four regions.

### Post 3: Net, not gross (war-story frame: Avi's field record) (941 chars)

```
Volume flatters.

Headline TPV makes every quarter look good. It says nothing about what you kept.

One line from Avi's field record: turned a loss-making acquiring platform profitable, a billion-dollar transaction-margin swing. That's a margin number, not a volume number.

The move:
• Report net revenue and take rate, not headline TPV.
• Reprice enterprise deals on net margin, not volume.
• Price PayFac and embedded payments on who carries the loss.

The failure mode to watch: a "great" deal at scale that loses money on every order once refunds, disputes and scheme lines land. Net, not gross.


Who we are and where we've made the case: https://themarginwars.com/about?utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-linkedin-first-posts&utm_content=post-3

#payments #acquiring #pricing
```

Sources: About, 'Net, not gross. Volume flatters.'; About, Avi field record; warroom moves 02 NET IT OUT, 08 RE-PRICE, 09 EMBED; About roles; 'Eight years working side by side'.

### Post 4: Scheme fee lines (with Spot the Leak) (759 chars)

```
Dozens of network fee lines per acquirer. Nobody checks them.

They're small. They're cryptic. They sit at the bottom of the statement. And together, they're part of the margin.

The move:
1. Map each scheme fee line to the rule that creates it.
2. Flag every line you shouldn't be paying.
3. Name one owner for the statement. Not finance and payments jointly. One person, with a number.

The rollback is simple: if a flag turns out wrong, you've lost an afternoon, not a contract.

Want to test your eye first? Spot the Leak: one month of fees for an enterprise merchant. Three lines are wrong. Find them.
https://themarginwars.com/leak?utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-linkedin-first-posts&utm_content=post-4

#payments #schemefees
```

Sources: Home, Scheme fees front; About, 'Name the owner' and 'Know where it breaks'; Spot the Leak page copy (/leak).

### Post 5: Local rails, one corridor (war-story frame: Anitha, Braintree Australia) (890 chars)

```
Anitha set up Braintree Australia. Twice.

Building a market from launch teaches you the thing every cost report hides: every corridor is its own front. FX, rails and rules change at every border.

The leak to hunt: local-eligible payments that still pay cross-border fees and FX twice.

The move:
1. Pick one corridor. Just one.
2. Run local acquiring or account-to-account against a control.
3. Score both on cost, approvals and settlement days.
4. Stablecoins? Same scorecard. No exceptions for the shiny option.

Prerequisites first: who can use the route, who owns the exception, and where the fee becomes a loss.

Got a corridor that's bleeding? Tell us which number, and where you sell. A few sentences will do.
https://themarginwars.com/contact?utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-linkedin-first-posts&utm_content=post-5

#payments #crossborder #localpayments
```

Sources: About, Anitha field record; About, 'Every corridor is its own front'; Home, Cross-border front; Advisory route brief, 'Three checks before you move'; Contact hero copy.

---

## 7. Cover and visuals (within the approved brand)

- **Cover:** keep `cover_1128x191.png` (Logo C ledger margin, pink `#B5237F` vertical rule, six-colour top strip, "Payments tactics from the front lines."). Optional variant: swap the cover line for the new hook "Nobody loses margin on the rate." so cover and tagline don't repeat each other. Keep the bottom-left clear for the logo overlap. The pink rule stays on the cover only.
- **Logo:** no change (`logo_400.png`, six-colour stacked rule on ink `#111417`; no pink).
- **Post cards (1080×1350 or 1200×1200):** ink `#111417` field or paper `#F4F6F7`, six-colour band as a thin top strip in the approved order (sky `#8FB0E0`, violet `#A08FE6`, mint `#3FBF85`, grey `#B7C1C9`, gold `#D2A63A`, coral `#EA6259`), front name in Martian Mono 600, hook in Schibsted Grotesk Bold. The "bp" tag is in muted `#5B656B`.
- **One colour per front (proposed, follows band order):** Interchange sky, Scheme fees violet, FX mint, Acceptance grey, Routing gold, Cross-border coral. Confirm it doesn't clash with role accents on the site before building templates.
- **Carousel for Featured #1:** six slides, one per front: "The problem." / "Our move." Copy is verbatim from the home page.
- **No** stock war imagery, no logo walls, no follower counts (per 06 spec tone).

---

## 8. Rules check

- No banned company names, stealth names, motifs or patent reference numbers. First names only. No individual names on network, market or partner entries.
- No new numbers or clients: every figure ($1.2 trillion TPV, billion-dollar swing, twelve moves, four regions, three leaks) is from live site copy.
- Banned-terms grep run on 10 Nov 2026 against this file: no matches (the command is in the agent report).
