"""Weekend copy + payments-depth rules (Nov 7 2026). Idempotent text rules applied to site_calm/*.html.
Run: python3 apply_copy_weekend.py [site_dir]"""
import sys, pathlib, html
D = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '@MW_ROOT@/site_calm')
R = {
'index.html': [
 ("Your payment margin is leaking. We find where, and close it.",
  "Nobody loses margin on the rate. You lose it in the line items nobody owns."),
 ("We take your statement apart line by line, decide which moves are worth making, and help you make them in every market you sell in.",
  "We tear the statement down line by line, rank the moves by basis points recovered, and stay until each one has an owner and a number, in every market you sell in."),
 ("Transactions qualify for a worse rate than they should because of missing data, the wrong card-present or card-not-present flags, or late capture.",
  "Transactions fall to a worse interchange category because of missing Level 2/3 data, a wrong card-present flag, a missing AVS result, or capture that lands after the auth window."),
 ("We sort downgrades by cause and fix the data or flow behind each one.",
  "We pull the qualification report, sort every downgrade by reason code, and fix the field, flag or capture timing behind each one, biggest bucket first."),
 ("We put the cost of a decline next to the cost of a fee, so the two can be traded off openly.",
  "We split declines into soft and hard, retry the soft ones on the right schedule, turn on network tokens and account updater, and tune 3DS exemptions, then put each lost sale next to the fee line so the trade-off is priced."),
 ("We set routing rules on all-in cost and approval, and keep a reserve of volume you can move.",
  "We route on all-in cost per approved order, not on rate card. Debit goes least-cost where the rules allow, failover is tested, and a share of volume stays portable so the next price talk has leverage."),
 ("We pick a corridor, test local rails or account-to-account payments, and measure the result.",
  "We pick one corridor, acquire locally or switch on the local A2A or instant rail, hold out a control, and compare all-in cost, approval and settlement days before rolling it out. Stablecoin settlement gets the same test, on the same scorecard."),
],
'advisory.html': [
 ("Bring us one number you need to move: cost per order, approval rate, losses or FX.",
  "Bring one number that's bleeding: cost per order, approval rate, chargeback losses or FX."),
 ("Two days on your own payments data. We go through net revenue and pricing, merchant-of-record exposure, FX and local rails, disputes, tax, and agent channels where you have them.",
  "Two days inside your own payments data: interchange qualification and downgrades, scheme-fee lines, decline codes, routing, chargeback ratios, FX markup by corridor, merchant-of-record exposure and tax."),
 ("Another is whether stablecoin settlement beats your current rail on all-in cost.",
  "Another is whether stablecoin settlement beats your current rail once on-ramp, off-ramp, FX and treasury float are counted."),
],
'about.html': [
 ("Margin leaks through the line items, not the headline rate. Take the statement line by line.",
  "Everyone haggles over the rate. The money is in downgrades, scheme lines and FX nobody quoted."),
 ("keynote co-presenter with Brandy Wood, VP Product, Fiserv.", "keynote co-presenter with Brandy, VP Product, Fiserv."),
 ("interview with Ryan Green on", "interview with Ryan on"),
],
'speaking.html': [
 ("Tactics, not trend talks.", "No trend decks. No future-of-payments slides."),
 ("Keynote co-presenter with Brandy Wood, VP Product, Fiserv", "Keynote co-presenter with Brandy, VP Product, Fiserv"),
 ("keynote co-presenter with Brandy Wood, VP Product, Fiserv.", "keynote co-presenter with Brandy, VP Product, Fiserv."),
 ("Session speaker with Prabhath Nanisetty, Snowflake", "Session speaker with Prabhath, Snowflake"),
 ("How merchants unlock value through cloud data sharing", "Merchant cloud data sharing: finding basis points in your own data"),
 ("Panelist, with Hersh Mansukhani and others", "Panelist, with Hersh and others"),
 ("interview with Ryan Green on", "interview with Ryan on"),
],
'writing.html': [
 ("A private monthly briefing for about 150 people who own a payment cost, approval, loss or FX number.",
  "One tactic a month, written so you can run it on Monday, for about 150 people who own a payment cost, approval, loss or FX number."),
],
'contact.html': [
 ("Tell us in a few sentences which number is hurting: cost, approvals, losses or FX.",
  "Tell us which number is bleeding (cost, approvals, chargebacks or FX) and where you sell. A few sentences is enough."),
],
}
miss=[]
for f, rules in R.items():
    p=D/f; s=p.read_text()
    for a,b in rules:
        for A,B in ((a,b),(html.escape(a,quote=False),html.escape(b,quote=False)),(a.replace("'","&#x27;"),b.replace("'","&#x27;")),(a.replace("'","’"),b.replace("'","’"))):
            if A in s: s=s.replace(A,B); break
        else:
            if b not in s and html.escape(b,quote=False) not in s: miss.append((f,a[:60]))
    p.write_text(s)
print("MISSES:",miss)
