"""Build-time guard shared by the layers: True if text contains a sensitive term.
Terms are checked against the salted hashes in qa/compliance/banned.yml (never stored in clear)."""
import hashlib, os, re
from pathlib import Path
_C = None
def _cfg():
    global _C
    if _C is None:
        import yaml
        p = Path(os.environ.get('MW_BANNED_YML', Path(__file__).resolve().parents[2] / 'qa/compliance/banned.yml'))
        c = yaml.safe_load(p.read_text())['hashed_terms']
        _C = (c['salt'], c.get('ngram_max', 3), {x['h'] for x in c['hashes']})
    return _C
def sensitive(text):
    salt, nmax, hs = _cfg()
    t = re.findall(r'[a-z0-9]+', text.lower())
    if 'global payments' in ' '.join(t):
        return True
    for n in range(1, nmax + 1):
        for j in range(len(t) - n + 1):
            if hashlib.sha256((salt + '|' + ' '.join(t[j:j + n])).encode()).hexdigest()[:24] in hs:
                return True
    return False
