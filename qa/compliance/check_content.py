#!/usr/bin/env python3
"""Compliance gate for the public MarginWars repo.

Fails on: sensitive names/terms (matched by salted hash, so the list itself is never public),
banned motifs and phrases, personal data (phones, street addresses, non-allowlisted emails),
secrets/webhook URLs, and approval-gated names (the gated rules in banned.yml) that appear without an
`approvals:` reference to an approved row in ops/approvals.md.

Findings never print the matched sensitive text (CI logs on a public repo are public): they show
rule id, file, line and a masked token only.

Usage: check_content.py [--root DIR] [--extra-terms FILE] [PATH ...]
  --extra-terms  optional clear-text term file (one per line) kept OFF the repo, e.g. supplied in CI
                 from the COMPLIANCE_EXTRA_TERMS secret. Hashes in banned.yml are always applied.
Exit 1 on any finding.
"""
import argparse, fnmatch, hashlib, json, os, re, subprocess, sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
TEXT_EXT = {'.html', '.htm', '.css', '.js', '.mjs', '.cjs', '.json', '.jsonl', '.xml', '.txt', '.md', '.yml',
            '.yaml', '.toml', '.csv', '.ics', '.atom', '.rss', '.svg', '.py', '.sh', '.map', '.webmanifest', ''}
SKIP_DIRS = {'.git', 'node_modules', '.build', '__pycache__', '.wrangler', 'qa-out'}
TOK = re.compile(r'[a-z0-9]+')


def norm_tokens(s):
    return TOK.findall(s.lower())


def h(salt, gram):
    return hashlib.sha256((salt + '|' + gram).encode()).hexdigest()[:24]


def mask(s):
    s = s.strip()
    return (s[0] + '*' * (len(s) - 1)) if s else s


def load_cfg():
    return yaml.safe_load((HERE / 'banned.yml').read_text())


def front_matter(path, text):
    if path.suffix in ('.yml', '.yaml'):
        try:
            d = yaml.safe_load(text)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end > 0:
            try:
                d = yaml.safe_load(text[3:end])
                return d if isinstance(d, dict) else {}
            except Exception:
                return {}
    return {}


def approved_ids(root):
    """Approval ids (A-###) whose row in ops/approvals.md has status approved."""
    p = root / 'ops/approvals.md'
    ids = set()
    if p.exists():
        for line in p.read_text().splitlines():
            m = re.match(r'\|\s*(A-[\w-]+)\s*\|', line)
            if m and re.search(r'\|\s*approved\s*\|', line, re.I):
                ids.add(m.group(1))
    return ids


def list_files(root, paths):
    if paths:
        out = []
        for p in paths:
            p = Path(p)
            p = p if p.is_absolute() else (root / p)
            out += [x for x in p.rglob('*') if x.is_file()] if p.is_dir() else [p]
        return out
    try:
        r = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard'], cwd=root, capture_output=True, text=True, check=True)
        return [root / x for x in r.stdout.splitlines() if x and (root / x).is_file()]
    except Exception:
        out = []
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            out += [Path(dp) / f for f in fn]
        return out


def match_any(rel, globs):
    return any(fnmatch.fnmatch(rel, g) for g in (globs or []))


def scan(root, files, cfg, extra_terms):
    salt = cfg['hashed_terms']['salt']
    nmax = cfg['hashed_terms'].get('ngram_max', 3)
    hashed = {x['h']: x.get('cat', 'sensitive') for x in cfg['hashed_terms']['hashes']}
    for t in extra_terms:
        g = ' '.join(norm_tokens(t))
        if g:
            hashed[h(salt, g)] = 'sensitive-extra'
    rules = [(r, re.compile(r['pattern'], re.I if r.get('ignore_case', True) else 0)) for r in cfg['rules']]
    gated = [(g, re.compile(g['pattern'], re.I)) for g in cfg['gated']]
    em = cfg['emails']
    em_re = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    allowed_domains = set(d.lower() for d in em['allowed_domains'])
    allowed_hashed = {x['h']: x.get('paths', ['**']) for x in em.get('allowed_hashed', [])}
    skip_globs = cfg.get('skip_paths', [])
    ok_ids = approved_ids(root)
    ap = HERE / 'approved_paths.yml'
    path_appr = (yaml.safe_load(ap.read_text()) or {}).get('grants', []) if ap.exists() else []
    findings = []
    for f in files:
        rel = f.relative_to(root).as_posix() if f.is_absolute() and str(f).startswith(str(root)) else f.as_posix()
        if match_any(rel, skip_globs):
            continue
        if f.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = f.read_bytes().decode('utf-8')
        except Exception:
            continue
        lines = text.splitlines()
        fm = None
        for i, line in enumerate(lines, 1):
            toks = norm_tokens(line)
            for n in range(1, nmax + 1):
                for j in range(len(toks) - n + 1):
                    g = ' '.join(toks[j:j + n])
                    hv = h(salt, g)
                    if hv in hashed:
                        findings.append({'file': rel, 'line': i, 'rule': 'sensitive-term:' + hashed[hv], 'match': mask(g)})
            for r, rx in rules:
                if match_any(rel, r.get('except_paths')):
                    continue
                if r.get('paths') and not match_any(rel, r['paths']):
                    continue
                for m in rx.finditer(line):
                    findings.append({'file': rel, 'line': i, 'rule': r['id'], 'match': mask(m.group()) if r.get('mask', True) else m.group()})
            for m in em_re.finditer(line):
                addr = m.group().lower().rstrip('.')
                dom = addr.split('@', 1)[1]
                if re.search(r'\.(?:png|jpe?g|webp|gif|svg|css|js|woff2?)$', dom):
                    continue
                if dom in allowed_domains or any(dom.endswith('.' + d) for d in allowed_domains):
                    continue
                globs = allowed_hashed.get(h(salt, addr))
                if globs and match_any(rel, globs):
                    continue
                findings.append({'file': rel, 'line': i, 'rule': 'pii:email', 'match': mask(addr)})
            for g, rx in gated:
                if match_any(rel, g.get('except_paths')):
                    continue
                if rx.search(line):
                    if fm is None:
                        fm = front_matter(f, text)
                    appr = (fm.get('approvals') or {}) if isinstance(fm, dict) else {}
                    if isinstance(appr, list):
                        appr = {k: v for d in appr if isinstance(d, dict) for k, v in d.items()}
                    ref = appr.get(g['approval_key']) if isinstance(appr, dict) else None
                    if not ref:
                        for gr in path_appr:
                            if match_any(rel, gr.get('paths')) and (gr.get('approvals') or {}).get(g['approval_key']):
                                ref = gr['approvals'][g['approval_key']]
                                break
                    if not ref or ref not in ok_ids:
                        findings.append({'file': rel, 'line': i, 'rule': 'gated:' + g['id'],
                                         'match': f"needs approvals: {{{g['approval_key']}: A-…}} with an approved row in ops/approvals.md"})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=str(HERE.parent.parent))
    ap.add_argument('--extra-terms')
    ap.add_argument('--json')
    ap.add_argument('paths', nargs='*')
    a = ap.parse_args()
    root = Path(a.root).resolve()
    cfg = load_cfg()
    extra = []
    src = a.extra_terms or os.environ.get('COMPLIANCE_EXTRA_TERMS_FILE')
    if src and Path(src).exists():
        extra = [l.strip() for l in Path(src).read_text().splitlines() if l.strip() and not l.startswith('#')]
    files = list_files(root, a.paths)
    res = scan(root, files, cfg, extra)
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1))
    for x in res[:400]:
        print(f"{x['file']}:{x['line']}: {x['rule']}: {x['match']}")
    print(f"compliance: {len(files)} files scanned, {len(res)} findings")
    sys.exit(1 if res else 0)


if __name__ == '__main__':
    main()
