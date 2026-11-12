"""Route Brief layer (Nov 7 2026). Idempotent. Renders rb.json into site_calm index/advisory."""
import json,re,shutil,html
from pathlib import Path
H=Path(__file__).parent; D=H.parent/'site_calm'
d=json.loads((H/'rb.json').read_text())
for f in ('rb.css','rb.js','rb.json'): shutil.copy(H/f, D/'assets'/f)
e=html.escape
def lnk(t,u):
    ext=u.startswith('http')
    return '<li><a href="%s"%s>%s%s</a></li>'%(e(u),' target="_blank" rel="noopener"' if ext else '',e(t),'<span class="vh"> (opens in a new tab)</span>' if ext else '')
def art(s,first):
    p=s['path']
    rows=lambda xs,cls:''.join('<li class="%s"><b>%s</b><span>%s</span></li>'%(cls,e(a),e(b)) for a,b in xs)
    q=''.join('<li class="rb-q"><span class="rb-n" aria-hidden="true">%02d</span><div><b>%s</b><span>%s</span></div></li>'%(i+1,e(a),e(b)) for i,(a,b) in enumerate(s['questions']))
    mk={m['id']:m['label'] for m in d['markets']}; me={m['id']:m['label'] for m in d['methods']}
    return ('<article class="rb-brief" id="rb-%s" data-m="%s" data-p="%s" aria-labelledby="rb-%s-h">'
     '<div class="rb-bh"><p class="rb-k">%s · %s</p><h3 id="rb-%s-h">%s</h3></div>'
     '<div class="rb-path" aria-label="Payment path"><div class="rb-node"><b>%s</b><span>%s</span></div><span class="rb-arrow" aria-hidden="true"></span><div class="rb-node"><b>%s</b><span>%s</span></div></div>'
     '%s<div class="rb-cols"><section class="rb-col"><h4>Routes to investigate</h4><ul class="rb-list">%s</ul><p class="rb-note">%s</p></section>'
     '<section class="rb-col"><h4>Who sets the rules</h4><ul class="rb-list">%s</ul></section>'
     '<section class="rb-col"><h4>Three checks before you move</h4><ol class="rb-qs">%s</ol></section></div>'
     '%s<div class="rb-foot"><section class="rb-unk"><h4>What we do not know</h4><p>%s</p></section><section class="rb-src"><h4>Sources</h4><ul>%s</ul></section></div></article>')%(
     s['id'],s['market'],s['method'],s['id'],e(mk[s['market']]),e(me[s['method']]),s['id'],e(s['title']),
     e(p[0][0]),e(p[0][1]),e(p[1][0]),e(p[1][1]),('<p class="rb-proof"><span class="rb-k">Experience</span>%s</p>'%e(s['proof']) if s.get('proof') else ''),rows(s['rails'],'rb-r'),e(s['rails_note']),rows(s['authorities'],'rb-a'),q,st(s),e(s['unknowns']),''.join(lnk(a,b) for a,b in s['sources']))
def st(s):
    x=s.get('status')
    if not x: return ''
    return '<div class="rb-st"><h4>Rule status, dated</h4><dl>%s</dl></div>'%''.join('<div class="rb-sti"><dt>%s</dt><dd>%s</dd></div>'%(e(a),e(b)) for a,b in x)
def radios(name,items,leg,num):
    o=''.join('<label class="rb-opt"><input type="radio" name="rb-%s" value="%s"%s><span>%s</span></label>'%(name,i['id'],' checked' if k==0 else '',e(i['label'])) for k,i in enumerate(items))
    return '<fieldset class="rb-fs"><legend><span class="rb-k">%s</span>%s</legend><div class="rb-opts">%s</div></fieldset>'%(num,leg,o)
def block():
    arts=''.join(art(s,i==0) for i,s in enumerate(d['scenarios']))
    none=('<article class="rb-brief rb-none" id="rb-none" hidden aria-labelledby="rb-none-h"><div class="rb-bh"><p class="rb-k">Not briefed yet</p><h3 id="rb-none-h">We haven\'t published this pairing</h3></div>'
          '<div class="rb-foot"><section class="rb-unk"><h4>What we do not know</h4><p>Everything route-specific. We only publish a brief once every line has a source.</p></section>'
          '<section class="rb-src"><h4>Next step</h4><p><a href="contact.html">Bring us a margin problem</a></p></section></div></article>')
    return ('<!--rb--><section class="rbf" id="route-brief" aria-labelledby="rb-h"><div class="rb-in">'
     '<div class="rb-hd"><div><p class="rb-k rb-eb">Route brief</p><h2 id="rb-h">Follow the money. Find the friction.</h2>'
     '<p class="rb-lede">Pick a market and a payment method. See the rails, the rule-setters, the questions to ask and what nobody can know from outside.</p></div>'
     '<p class="rb-aside"><b>Terrain, not relationships.</b> Built only from entries on this site and the public sources listed. Nothing you pick is sent anywhere.</p></div>'
     '<form class="rb-pick" hidden onsubmit="return false" aria-label="Build your route brief">%s%s</form>'
     '<div class="rb-out" aria-live="polite">%s%s</div>'
     '<div class="rb-bar"><p>Options to investigate, not confirmed availability or advice.</p><div class="rb-acts"><button type="button" class="rb-print" hidden>Print this route brief</button><a class="rb-cta" href="contact.html">Bring us a margin problem</a></div></div>'
     '</div></section><!--/rb-->')%(radios('m',d['markets'],'Market','01 /'),radios('p',d['methods'],'Method','02 /'),arts,none)
B=block()
for n in ('index.html','advisory.html'):
    f=D/n; s=f.read_text()
    s=re.sub(r'<!--rb-->.*?<!--/rb-->','',s,flags=re.S)
    if 'assets/rb.css' not in s:
        s=s.replace('</head>','<link rel="stylesheet" href="assets/rb.css"><script src="assets/rb.js" defer></script></head>',1)
    m=re.search(r'<section\b(?=[^>]*\bclass="(?=[^"]*\btstrip\b)(?=[^"]*\btmap\b)[^"]*")[^>]*>',s)
    assert m,n
    i=m.start()
    s=s[:i]+B+s[i:]
    f.write_text(s); print('rb ->',n)

# About: proof line in the career accordion (Nov 8, approved by Avi). Idempotent.
PROOF='<p class="ab-proof"><!--proof-->Anitha set up Braintree Australia, twice.<!--/proof--></p>'
f=D/'about.html'; t=f.read_text()
t=re.sub(r'<p class="ab-proof"><!--proof-->.*?<!--/proof--></p>','',t)
k='<h3 class="ch">Career and terrain</h3><span class="acc-chev" aria-hidden="true"></span></summary><div class="acc-b">'
# New full About renders this approved fact in its Field record.
if k in t: t=t.replace(k,k+PROOF,1)
else: assert 'Field record' in t or 'field record' in t
if 'assets/rb.css' not in t: t=t.replace('</head>','<link rel="stylesheet" href="assets/rb.css"></head>',1)
f.write_text(t); print('proof -> about.html')
