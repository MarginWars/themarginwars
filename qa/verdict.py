#!/usr/bin/env python3
"""Aggregate the browser gate outputs into one pass/fail verdict.
Usage: qa/verdict.py OUT_DIR [--engines chromium,webkit,firefox] [--profiles core,devices]
Reads OUT_DIR/{text_overflow_*,spacing_*,matrix_<engine>_<profile>_*}.json and writes OUT_DIR/verdict.md + verdict.json.
A case fails when:
  text overflow  n > 0 or pageOverflow
  spacing        edgeDev, nIntr > 0, rhythm, hb (heading/body), overflow, nTextOverflow > 0
  matrix         any non-empty finding: sym, contrast, targets, overflow, spacing, errors, evalerr
                 (shoterr is reported as a warning)
Known issues may be waived in qa/known_issues.yml (list of {case: <glob>, gate: <gate>, reason, until: YYYY-MM-DD, issue: #n});
waivers past their date stop applying. Exit 0 = pass, 1 = fail, 2 = missing expected output."""
import argparse, fnmatch, glob, json, os, sys, datetime
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--engines', default='chromium'); ap.add_argument('--profiles', default='core'); ap.add_argument('--require', default='text-overflow,spacing', help="outputs that must exist besides the matrix; 'none' for a matrix-only run")
a = ap.parse_args(); O = Path(a.out)
REPO = Path(__file__).resolve().parent.parent
waivers = []
kf = REPO / 'qa/known_issues.yml'
if kf.exists():
    import yaml
    today = datetime.date.today().isoformat()
    waivers = [w for w in (yaml.safe_load(kf.read_text()) or []) if str(w.get('until', '9999')) >= today]
def waived(case, gate):
    return any(fnmatch.fnmatch(case, w['case']) and w.get('gate') in (gate, '*') for w in waivers)
def load(pat):
    d = {}
    for f in sorted(glob.glob(str(O / pat))): d.update(json.loads(Path(f).read_text()))
    return d
fails, warns, counts, missing, waived_n = [], [], {}, [], 0
def add(gate, case, detail):
    global waived_n
    if waived(case, gate): waived_n += 1; return
    fails.append((gate, case, detail))
to = load('text_overflow_*.json'); counts['text-overflow'] = len(to)
for k, v in to.items():
    if v.get('n') or v.get('pageOverflow'): add('text-overflow', k, f"{v.get('n')} issue(s){' + page overflow' if v.get('pageOverflow') else ''}")
sp = load('spacing_*.json'); counts['spacing'] = len(sp)
for k, v in sp.items():
    bad = [x for x in ('edgeDev', 'rhythm', 'hb', 'overflow') if v.get(x)]
    if v.get('nIntr'): bad.append(f"intrusions={v['nIntr']}")
    if v.get('nTextOverflow'): bad.append(f"textOverflow={v['nTextOverflow']}")
    if bad: add('spacing', k, ', '.join(bad) + (f" rhythm={json.dumps(v.get('rhythm'))[:160]}" if v.get('rhythm') else ''))
for e in a.engines.split(','):
    for p in a.profiles.split(','):
        m = load(f'matrix_{e}_{p}_*.json'); counts[f'matrix {e}/{p}'] = len(m)
        if not m: missing.append(f'matrix {e}/{p}')
        for k, v in m.items():
            v = dict(v); se = v.pop('shoterr', None)
            if se: warns.append(('matrix', f'{e}|{k}', 'screenshot: ' + se[:80]))
            v.pop('spacing_info', None)
            if v: add(f'matrix-{e}/{p}', k, '; '.join(f'{x}={json.dumps(y)[:120]}' for x, y in v.items()))
req = set() if a.require == 'none' else set(a.require.split(','))
if not to and 'text-overflow' in req: missing.append('text-overflow')
if not sp and 'spacing' in req: missing.append('spacing')
lines = ['# Browser gate verdict', '', '| Gate | Cases | Failing |', '|---|---:|---:|']
for g, n in counts.items():
    key = 'matrix-' + g.split()[1] if g.startswith('matrix') else g
    lines.append(f'| {g} | {n} | {sum(1 for f in fails if f[0] == key)} |')
lines += ['', f'Waived by qa/known_issues.yml: {waived_n}', f'Missing outputs: {", ".join(missing) or "none"}', '']
if fails:
    lines += ['## Failures', ''] + [f'- **{g}** `{c}`: {d}' for g, c, d in fails[:400]]
if warns:
    lines += ['', '## Warnings', ''] + [f'- {g} `{c}`: {d}' for g, c, d in warns[:100]]
(O / 'verdict.md').write_text('\n'.join(lines) + '\n')
(O / 'verdict.json').write_text(json.dumps({'counts': counts, 'fails': fails, 'warnings': warns, 'missing': missing, 'waived': waived_n}, indent=1))
print('\n'.join(lines[:12 + len(counts)]))
if fails: print(f'verdict: FAIL ({len(fails)} failing cases; see {O}/verdict.md)'); sys.exit(1)
if missing: print('verdict: MISSING OUTPUT'); sys.exit(2)
print('verdict: PASS')
