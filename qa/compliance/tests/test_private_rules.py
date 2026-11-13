#!/usr/bin/env python3
"""Regression test for the private:* compliance rules: every line of the fail fixture must be caught,
and nothing in the pass fixture (public prices, third-party names, ordinary words) may be."""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
CHECK = HERE.parent / 'check_content.py'
def run(name):
    r = subprocess.run([sys.executable, str(CHECK), '--root', str(HERE), str(HERE / name)], capture_output=True, text=True)
    return {int(l.split(':')[1]) for l in r.stdout.splitlines() if l.startswith(name + ':')}
fail_lines = len((HERE / 'private_should_fail.md').read_text().splitlines())
caught = run('private_should_fail.md'); missed = set(range(1, fail_lines + 1)) - caught
false_pos = run('private_should_pass.md')
print(f"private rules: {len(caught)}/{fail_lines} caught, {len(false_pos)} false positives")
sys.exit(1 if missed or false_pos else 0)
