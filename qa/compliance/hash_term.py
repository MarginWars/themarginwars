#!/usr/bin/env python3
"""Print the banned.yml hash for a term without storing the term. Usage: hash_term.py "term" [...]"""
import hashlib, re, sys
from pathlib import Path
import yaml
salt = yaml.safe_load((Path(__file__).parent / 'banned.yml').read_text())['hashed_terms']['salt']
for t in sys.argv[1:]:
    g = ' '.join(re.findall(r'[a-z0-9]+', t.lower()))
    print(f"- {{h: {hashlib.sha256((salt + '|' + g).encode()).hexdigest()[:24]}, cat: sensitive}}")
