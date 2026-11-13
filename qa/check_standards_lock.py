#!/usr/bin/env python3
"""Standards lock (adapted from instip scripts/check-standards.mjs). standards.lock.json pins the sha256 of every
governance file adopted from the group standards. A change to one of them must be deliberate: rerun with --write in
the same PR (the PR then shows both the file and the lock changing, and CODEOWNERS review applies)."""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; L = ROOT / 'standards.lock.json'
lock = json.loads(L.read_text()); bad = []
for e in lock['entries']:
    p = ROOT / e['local']
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if '--write' in sys.argv: e['sha256'] = h
    elif h != e['sha256']: bad.append(f"{e['local']}: {'missing' if h is None else 'changed without re-recording the lock'}")
if '--write' in sys.argv:
    L.write_text(json.dumps(lock, indent=2) + '\n'); print('standards lock re-recorded'); sys.exit(0)
for b in bad: print(b)
print(f"standards-lock: {len(lock['entries'])} entries, {len(bad)} drifted"); sys.exit(1 if bad else 0)
