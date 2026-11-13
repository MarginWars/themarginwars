"""Shared helpers: find outbound items and split front-matter."""
import fnmatch, re, subprocess
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parent.parent
LIM = yaml.safe_load((ROOT / 'qa/limits.yml').read_text())
def _m(rel, globs): return any(fnmatch.fnmatch(rel, g) for g in globs)
def items():
    out = []
    for p in sorted(ROOT.rglob('*.md')):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(('site/', '.git/', 'qa-out/')): continue
        if _m(rel, LIM['item_globs']) and not _m(rel, LIM.get('skip_globs', [])): out.append(p)
    return out
def split(p):
    t = p.read_text()
    if not t.startswith('---\n'): return None, t
    end = t.find('\n---', 4)
    if end < 0: return None, t
    try: fm = yaml.safe_load(t[4:end]) or {}
    except Exception as e: fm = {'__error__': str(e)}
    return fm, t[end + 4:].lstrip('\n')
def changed(base):
    if not base: return None
    r = subprocess.run(['git', 'diff', '--name-only', f'{base}...HEAD'], cwd=ROOT, capture_output=True, text=True)
    return set(r.stdout.split()) if r.returncode == 0 else None
