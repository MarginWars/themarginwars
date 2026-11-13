#!/usr/bin/env python3
"""Claims gate (adapted from instip scripts/check-claims.mjs). A floor, not the review.
For publishable items (qa/limits.yml publishable_channels) at status in-review or approved, every number in the
body must be backed: it appears in a facts/approved.yml entry listed in `sources:`, or in a source file listed in
`sources:`, or the line carries [Assumption] and a facts/assumptions.yml entry lists it.
Drafts are reported as warnings only. Exit 1 on any failure."""
import re, sys
import yaml
from _items import ROOT, LIM, items, split
F = {x['id']: x for x in (yaml.safe_load((ROOT / 'facts/approved.yml').read_text()) or {}).get('facts', []) if x.get('status') == 'approved'}
A = {x['id']: x for x in (yaml.safe_load((ROOT / 'facts/assumptions.yml').read_text()) or {}).get('assumptions') or []}
NUM = re.compile(r'(?<![\w/#.-])\d[\d,]*(?:\.\d+)?(?:\s?(?:%|bps|bp|x|k|m|bn|million|billion))?(?![\w/-])', re.I)
SKIP = [re.compile(p) for p in [r'https?://\S+', r'\{\{[^}]*\}\}', r'\]\([^)]*\)', r'`[^`]*`', r'\b(?:19|20)\d\d\b', r'\b\d{1,2}:\d{2}\b', r'^\s*(?:#+\s*)?\d+[.)]\s', r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*', r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2}\b']]
fails, warns, n = [], 0, 0
for p in items():
    fm, body = split(p)
    if not fm or fm.get('channel') not in LIM['publishable_channels']: continue
    n += 1; rel = p.relative_to(ROOT).as_posix()
    backed = set()
    for s in fm.get('sources') or []:
        sid = s.split('#', 1)[1] if s.startswith('facts/approved.yml#') else None
        if sid and sid in F: backed |= set(map(str, F[sid].get('numbers') or [])) | set(NUM.findall(F[sid]['claim']))
        elif (ROOT / s.split('#')[0]).is_file(): backed |= {x.replace(',', '') for x in NUM.findall((ROOT / s.split('#')[0]).read_text(errors='ignore'))}
    for aid in fm.get('assumptions') or []:
        if aid in A: backed |= set(map(str, A[aid].get('numbers') or []))
    gate = fm.get('status') in ('in-review', 'approved')
    for i, line in enumerate(body.splitlines(), 1):
        l = line
        for rx in SKIP: l = rx.sub(' ', l)
        for m in NUM.finditer(l):
            num = re.match(r'[\d,.]+', m.group()).group().replace(',', '').rstrip('.')
            if num in backed or m.group().replace(',', '') in backed: continue
            if '[Assumption]' in line and any(num in map(str, A[x].get('numbers') or []) for x in fm.get('assumptions') or [] if x in A): continue
            if gate: fails.append(f'{rel}:{i}: unsourced number "{m.group().strip()}"')
            else: warns += 1
for f in fails[:300]: print(f)
print(f'claims: {n} publishable items, {len(fails)} unsourced numbers in in-review/approved items, {warns} in drafts (warning)')
sys.exit(1 if fails else 0)
