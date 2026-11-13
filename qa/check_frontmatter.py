#!/usr/bin/env python3
"""Front-matter, schedule and character-limit gate for every outbound item.
- validates front-matter against schemas/content-item.schema.json
- approved/scheduled items need a PT schedule (-08:00/-07:00); on changed files it must be in the future
- character limits per channel from qa/limits.yml (X URLs count 23; threads split on lines of ---)
- weekly calendars in content/calendar/*.yml validate and point at existing items with matching schedules
Usage: check_frontmatter.py [--changed BASE_REF]"""
import argparse, datetime as dt, json, re, sys
import jsonschema, yaml
from _items import ROOT, LIM, items, split, changed
ap = argparse.ArgumentParser(); ap.add_argument('--changed'); a = ap.parse_args()
CH = changed(a.changed)
schema = json.loads((ROOT / 'schemas/content-item.schema.json').read_text())
cal_schema = json.loads((ROOT / 'schemas/calendar.schema.json').read_text())
V = jsonschema.Draft202012Validator(schema)
errs = []
URL = re.compile(r'https?://\S+')
def xlen(s): return len(URL.sub('x' * 23, s))
def body_text(b):  # strip markdown comments
    return re.sub(r'<!--.*?-->', '', b, flags=re.S).strip()
now = dt.datetime.now(dt.timezone.utc)
n = 0
for p in items():
    rel = p.relative_to(ROOT).as_posix(); fm, body = split(p); n += 1
    if fm is None: errs.append(f'{rel}: missing front-matter'); continue
    if '__error__' in fm: errs.append(f'{rel}: front-matter YAML error'); continue
    fmj = json.loads(json.dumps(fm, default=str))
    for e in V.iter_errors(fmj): errs.append(f'{rel}: front-matter: {e.json_path}: {e.message[:140]}')
    st, sch, chn = fm.get('status'), fm.get('schedule'), fm.get('channel')
    if st == 'approved' and fm.get('kind') not in ('profile', 'pack', 'proposal') and not sch:
        errs.append(f'{rel}: approved items need a schedule in PT')
    if sch and (CH is not None and rel in CH) and st in ('in-review', 'approved'):
        try:
            if dt.datetime.fromisoformat(str(sch)) <= now: errs.append(f'{rel}: schedule {sch} is in the past')
        except ValueError: errs.append(f'{rel}: schedule is not ISO 8601')
    lim = LIM['channels'].get(chn, {}); kind = fm.get('kind', 'post')
    text = body_text(body)
    if chn == 'x' and kind == 'thread' and 'thread_post' in lim:
        for i, part in enumerate(re.split(r'\n-{3,}\s*\n', text), 1):
            if xlen(part.strip()) > lim['thread_post']: errs.append(f'{rel}: X thread post {i} is {xlen(part.strip())} > {lim["thread_post"]}')
    elif kind == 'post' and 'post' in lim and st != 'draft':
        L = xlen(text) if chn == 'x' else len(text)
        if L > lim['post']: errs.append(f'{rel}: {chn} post is {L} > {lim["post"]} characters')
    for f, v in (fm.get('fields') or {}).items():
        m = (lim.get('profile') or {}).get(f)
        if m and len(v) > m: errs.append(f'{rel}: {chn} {f} is {len(v)} > {m}')
    if fm.get('subject') and 'subject' in lim and len(fm['subject']) > lim['subject']:
        errs.append(f'{rel}: subject is {len(fm["subject"])} > {lim["subject"]}')
for c in sorted((ROOT / 'content/calendar').glob('*.yml')):
    rel = c.relative_to(ROOT).as_posix(); d = yaml.safe_load(c.read_text()) or {}
    for e in jsonschema.Draft202012Validator(cal_schema).iter_errors(json.loads(json.dumps(d, default=str))): errs.append(f'{rel}: {e.message[:140]}')
    for it in d.get('items') or []:
        f = ROOT / it.get('file', '')
        if not f.exists(): errs.append(f'{rel}: missing item file {it.get("file")}'); continue
        fm, _ = split(f)
        if fm and str(fm.get('schedule')) != str(it.get('schedule')): errs.append(f'{rel}: schedule mismatch for {it["file"]}')
for e in errs: print(e)
print(f'frontmatter-limits: {n} items checked, {len(errs)} problems')
sys.exit(1 if errs else 0)
