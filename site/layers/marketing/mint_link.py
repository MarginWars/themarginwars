#!/usr/bin/env python3
"""Mint a UTM-tagged link and record it in marketing/links.csv (the campaign link registry).
Usage:
  mint_link.py --dest URL --source S --medium M --campaign C [--content X] [--term T] [--id ID] [--notes N]
  mint_link.py --list
Values are normalised to the tagging convention in MARKETING.md (lowercase, a-z 0-9 - . _ only).
Minting the same id again returns the existing URL (idempotent); a different definition for an existing id is refused."""
import argparse, csv, datetime, pathlib, re, sys, urllib.parse
REG = pathlib.Path(__file__).with_name("links.csv")
COLS = ["id", "destination", "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "url", "owner", "status", "created", "notes"]
MEDIUMS = {"website", "social", "email", "newsletter", "referral", "paid-social", "cpc", "display", "partner", "event", "qr", "chat"}
def norm(v):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9._-]+", "-", str(v or "").strip().lower())).strip("-")[:80]
def load():
    if not REG.exists(): return []
    with REG.open(newline="") as f: return list(csv.DictReader(f))
def save(rows):
    with REG.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n"); w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["id"]))
def build(dest, source, medium, campaign, content="", term=""):
    u = urllib.parse.urlsplit(dest)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True) if not k.startswith("utm_")]
    for k, v in (("utm_source", source), ("utm_medium", medium), ("utm_campaign", campaign), ("utm_content", content), ("utm_term", term)):
        if v: q.append((k, v))
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path or "/", urllib.parse.urlencode(q), u.fragment))
def mint(dest, source, medium, campaign, content="", term="", id=None, notes="", owner="avi", rows=None, write=True):
    source, medium, campaign, content, term = map(norm, (source, medium, campaign, content, term))
    if not (dest.startswith("https://") and source and medium and campaign): raise SystemExit("dest (https), source, medium and campaign are required")
    if medium not in MEDIUMS: raise SystemExit(f"medium '{medium}' is not in the convention: {sorted(MEDIUMS)}")
    rid = norm(id or "-".join(x for x in (campaign, source, content) if x))
    url = build(dest, source, medium, campaign, content, term)
    rows = load() if rows is None else rows
    for r in rows:
        if r["id"] == rid:
            if r["url"] != url: raise SystemExit(f"id {rid} already exists with a different link: {r['url']}")
            return r["url"]
    rows.append({"id": rid, "destination": dest, "utm_source": source, "utm_medium": medium, "utm_campaign": campaign, "utm_content": content, "utm_term": term,
                 "url": url, "owner": owner, "status": "active", "created": datetime.date.today().isoformat(), "notes": notes})
    if write: save(rows)
    return url
if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--dest"); a.add_argument("--source"); a.add_argument("--medium"); a.add_argument("--campaign")
    a.add_argument("--content", default=""); a.add_argument("--term", default=""); a.add_argument("--id"); a.add_argument("--notes", default=""); a.add_argument("--list", action="store_true")
    o = a.parse_args()
    if o.list:
        for r in load(): print(r["id"], r["url"], sep="\t")
        sys.exit(0)
    print(mint(o.dest, o.source, o.medium, o.campaign, o.content, o.term, o.id, o.notes))
