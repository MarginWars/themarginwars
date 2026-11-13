#!/usr/bin/env python3
"""Link gate.
  --docs      every relative link in repo markdown resolves to a file in the repo
  --dist DIR  every internal href/src in the built site resolves (Pages rules: /x -> x.html, /d/ -> d/index.html)
  --external  (nightly) HEAD/GET every external URL in the built site and content; report 4xx/5xx
  --utm       content `links:` ids exist in the UTM registry (site/layers/marketing/links.csv)"""
import argparse, csv, html, re, sys, urllib.parse
from pathlib import Path
from _items import ROOT, items, split
ap = argparse.ArgumentParser(); ap.add_argument('--docs', action='store_true'); ap.add_argument('--dist'); ap.add_argument('--external', action='store_true'); ap.add_argument('--utm', action='store_true')
a = ap.parse_args(); errs = []; n = 0
if a.docs:
    for p in ROOT.rglob('*.md'):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(('site/', '.git/', 'qa-out/', 'node_modules/')): continue
        for m in re.finditer(r'\]\(([^)\s]+)\)', p.read_text(errors='ignore')):
            u = m.group(1)
            if re.match(r'^(?:[a-z]+:|#|\{\{)', u): continue
            n += 1; t = (p.parent / urllib.parse.unquote(u.split('#')[0])).resolve()
            if not t.exists(): errs.append(f'{rel}: broken link {u}')
def resolve(dist, base, u):
    path = urllib.parse.unquote(urllib.parse.urlsplit(u).path)
    t = (dist / path.lstrip('/')) if path.startswith('/') else (base / path)
    cands = [t, Path(str(t) + '.html'), t / 'index.html']
    return any(c.exists() and c.is_file() for c in cands)
if a.dist:
    dist = Path(a.dist).resolve()
    for p in dist.rglob('*.html'):
        t = re.sub(r'(<script\b[^>]*>).*?</script>', r'\1', p.read_text(errors='ignore'), flags=re.S)  # keep src, drop inline JS
        for m in re.finditer(r'\b(?:href|src)="([^"]+)"', t):
            u = html.unescape(m.group(1))
            if re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#|data:)', u, re.I) or not urllib.parse.urlsplit(u).path: continue
            n += 1
            if not resolve(dist, p.parent, u): errs.append(f'{p.relative_to(dist)}: broken internal link {u}')
if a.utm or a.docs:
    reg = set()
    lc = ROOT / 'site/layers/marketing/links.csv'
    if lc.exists():
        for r in csv.DictReader(lc.open()): reg.add(r.get('id') or r.get('link_id') or '')
    for p in items():
        fm, _ = split(p)
        for lid in (fm or {}).get('links') or []:
            n += 1
            if lid.split(':', 1)[-1] not in reg and lid not in reg: errs.append(f'{p.relative_to(ROOT)}: link id {lid} not in the UTM registry')
if a.external:
    import requests
    urls = set()
    for p in (ROOT / 'site/dist').rglob('*.html'): urls |= set(re.findall(r'href="(https?://[^"]+)"', p.read_text(errors='ignore')))
    for p in items(): urls |= set(re.findall(r'https?://[^\s)>\]"]+', p.read_text(errors='ignore')))
    for u in sorted(urls):
        u = html.unescape(u); n += 1
        try:
            r = requests.head(u, timeout=15, allow_redirects=True, headers={'User-Agent': 'themarginwars-linkcheck'})
            if r.status_code in (403, 405, 429, 999) or r.status_code >= 500: r = requests.get(u, timeout=20, headers={'User-Agent': 'Mozilla/5.0 themarginwars-linkcheck'})
            if r.status_code >= 400 and r.status_code not in (403, 429, 999): errs.append(f'external {r.status_code}: {u}')
        except Exception as e: errs.append(f'external error: {u} ({type(e).__name__})')
for e in errs[:300]: print(e)
print(f'links: {n} checked, {len(errs)} broken')
sys.exit(1 if errs else 0)
