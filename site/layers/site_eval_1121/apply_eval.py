"""Site evaluation fixes (21 Nov 2026 site walkthrough). Idempotent; runs LAST on site_calm.
 a) Advisory: offers + prices + 'Book a Teardown' directly under the hero (Route brief and Terrain follow).
 b) Home: one-line credibility strip under the hero (facts/approved.yml: together-years, margin swing, stages).
 c) Home: Route brief + Terrain blocks removed (they live on /advisory); link kept.
 d) Footer: 'working brand name, pending a trademark check' removed on every page; Privacy link added.
 e) /privacy page (generated from contact.html's shell) + link under the contact form; sitemap entry.
 f) Tracewire: compact title + how-to on phones; grid ARIA (rows, walls, word slots). Leak/Ep2 statement table fits
    at 320/375. Styles in assets/eval.css (linked after the last stylesheet on every page)."""
import re, pathlib, datetime
H = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("@MW_ROOT@/site_calm")
rd = lambda p: p.read_text()
n = 0
def wr(p, s):
    global n
    if not p.exists() or rd(p) != s: p.write_text(s); n += 1
def must(cond, msg):
    if not cond: raise SystemExit("site_eval_1121: " + msg)
PAGES = sorted(p for p in ROOT.glob("*.html"))
CSS_LINK = '<link data-eval="" href="/assets/eval.css" rel="stylesheet"/>'
TM = '<p>© 2026 The Margin Wars. The Margin Wars is a working brand name, pending a trademark check.</p>'
PRIV = '<a class="nm-inline" href="privacy.html">Privacy</a>'
# ---------- assets ----------
wr(ROOT / "assets/eval.css", rd(H / "eval.css"))
# ---------- d) footer + eval.css link, every page (privacy.html is generated below from contact.html) ----------
for p in PAGES:
    if p.name == "privacy.html": continue
    s = o = rd(p)
    s = s.replace(TM, '<p>© 2026 The Margin Wars.</p>')
    m = re.search(r'<p class="foot-links">(.*?)</p>', s)
    if m and PRIV not in m.group(1):
        s = s[:m.end() - 4] + PRIV + s[m.end() - 4:]
    s = s.replace(CSS_LINK, '')
    head = s[:s.find('<body')]
    last = list(re.finditer(r'<link\b[^>]*rel="stylesheet"[^>]*>', head))
    must(last, f"{p.name}: no stylesheet link")
    i = last[-1].end(); s = s[:i] + CSS_LINK + s[i:]
    if s != o: p.write_text(s); n += 1
# ---------- a) advisory ----------
p = ROOT / "advisory.html"; s = o = rd(p)
if 'class="offers"' not in s:
    i = s.find('<section><p class="eyebrow sx">02</p><h2>Ways to work together</h2>'); must(i > 0, "advisory offers section")
    j = s.find('</section>', i) + len('</section>'); off = s[i:j]; s = s[:i] + s[j:]
    off = off.replace('<section><p class="eyebrow sx">02</p><h2>Ways to work together</h2>',
                      '<section aria-labelledby="off-h" class="offers"><p class="eyebrow sx">01</p><h2 id="off-h">Ways to work together</h2>')
    off = off.replace('</div></section>', '</div><p class="off-cta"><a class="btn nm-inline nm-primary" href="contact.html">Book a Teardown</a></p></section>')
    k = s.find('<section aria-label="At a glance" class="statband">'); must(k > 0, "advisory statband")
    s = s[:k] + off + s[k:]
    s = s.replace('<section aria-labelledby="rt-h" class="route"><p class="eyebrow sx">01</p>', '<section aria-labelledby="rt-h" class="route"><p class="eyebrow sx">02</p>')
    must('class="eyebrow sx">03</p><h2>Questions clients bring us' in s, "advisory numbering")
s = re.sub(r'</section>\n\s*\n<section', '</section>\n<section', s)
if s != o: p.write_text(s); n += 1
# ---------- b) + c) home ----------
p = ROOT / "index.html"; s = o = rd(p)
CRED = ('<section aria-label="Who you would work with" class="cred"><p class="cred-line">'
        'Avi &amp; Anitha: eight years side by side. Terrain: US, UK/EU, South Africa, India, Singapore, Australia &amp; NZ. '
        '<a class="nm-inline nm-intext" href="about.html">The field record →</a></p></section>')
if 'class="cred"' in s:
    s = re.sub(r'<section aria-label="Who you would work with" class="cred">.*?</section>', CRED, s, flags=re.S)
if 'class="cred"' not in s:
    i = s.find('<section aria-labelledby="f-latest" class="f-strip">'); must(i > 0, "home f-strip")
    s = s[:i] + CRED + s[i:]
for cls in ('<section aria-labelledby="rb-h" class="rbf" id="route-brief">', '<section aria-labelledby="ts-h" class="tstrip tmap">'):
    i = s.find(cls)
    if i < 0: continue
    # balanced </section> match
    depth, k = 0, i
    for m in re.finditer(r'<section\b|</section>', s[i:]):
        depth += 1 if m.group(0) != '</section>' else -1
        if depth == 0: k = i + m.end(); break
    tail = s[k:k + 12]
    if tail.startswith('<!--/rb-->'): k += len('<!--/rb-->')
    s = s[:i] + s[k:]
s = s.replace('<link rel="stylesheet" href="assets/rb.css"><script src="assets/rb.js" defer></script>', '')
s = re.sub(r'<link href="assets/rb\.css" rel="stylesheet"/>(<script defer="" src="assets/rb\.js"></script>)?', '', s)
if 'id="route-brief"' not in s: s = s.replace('<!--rb-->', '').replace('<!--/rb-->', '')
RC = '<p class="rt-cta"><a class="nm-inline" href="advisory.html">See Advisory →</a></p></section>'
RC2 = '<p class="rt-cta"><a class="nm-inline" href="advisory.html">See Advisory →</a><a class="nm-inline" href="advisory.html#route-brief">Route brief and terrain map →</a></p></section>'
if RC2 not in s:
    i = s.find('<section aria-labelledby="rt-hc" class="route route-c">'); must(i > 0, "home route-c")
    j = s.find(RC, i); must(j > 0, "home rt-cta"); s = s[:j] + RC2 + s[j + len(RC):]
if s != o: p.write_text(s); n += 1
# ---------- e) privacy page + contact form note + sitemap ----------
p = ROOT / "contact.html"; s = o = rd(p)
NOTE = '<p class="cf-priv">We keep what you send so we can reply. <a class="nm-inline nm-intext" href="privacy.html">How we handle it</a>.</p>'
if NOTE not in s:
    a = '<p class="cf-alt">Or <a class="nm-inline nm-intext" href="mailto:hello@themarginwars.com">email us directly</a>.</p></div>'
    must(a in s, "contact cf-actions"); s = s.replace(a, a + NOTE, 1)
if s != o: p.write_text(s); n += 1
shell = rd(ROOT / "contact.html")
hi, he = shell.find('<main'), shell.find('</main>') + len('</main>')
main_open = re.match(r'<main[^>]*>', shell[hi:]).group(0)
body = rd(H / "privacy_main.html").strip()
mn = shell[hi:he]; nx = re.search(r'<nav aria-label="Next" class="nextp">.*?</nav>', mn, flags=re.S); must(nx, "contact nextp")
nxt = re.sub(r'<a class="nm-inline" href="[^"]*">[^<]*</a></nav>$', '<a class="nm-inline" href="contact.html">Contact →</a></nav>', nx.group(0))
body = body.replace('{NEXTP}', nxt)
pv = shell[:hi] + main_open + body + '</main>' + shell[he:]
# head: title, description, canonical, og/twitter, JSON-LD breadcrumb; body classes
T, D = "Privacy | The Margin Wars", "What themarginwars.com collects, where it is kept, and how to reach us about it. No cookies of our own, no third-party pixels."
pv = re.sub(r'<title>.*?</title>', f'<title>{T}</title>', pv, count=1, flags=re.S)
for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
    pv = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + '/>', f'<meta content="{D}" {attr}/>', pv)
for attr in ('property="og:title"', 'name="twitter:title"'):
    pv = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + '/>', f'<meta content="{T}" {attr}/>', pv)
pv = pv.replace('https://themarginwars.com/contact"', 'https://themarginwars.com/privacy"')
pv = re.sub(r'<script type="application/ld\+json">.*?</script>', '', pv, flags=re.S)
pv = re.sub(r'<script>\(function\(\)\{var d=document;\nfunction esc.*?</script>', '', pv, flags=re.S)  # assistant widget script
pv = re.sub(r'<script[^>]*src="/?assets/contact\.js"[^>]*></script>', '', pv)
pv = pv.replace(' aria-current="page"', '')
wr(ROOT / "privacy.html", pv)
p = ROOT / "sitemap.xml"; s = o = rd(p)
if '/privacy</loc>' not in s:
    s = s.replace('</urlset>', '<url><loc>https://themarginwars.com/privacy</loc><lastmod>2026-11-21</lastmod></url>\n</urlset>')
if s != o: p.write_text(s); n += 1
# ---------- f) tracewire mobile hero: preload its display font so the visible title does not shift layout ----------
p = ROOT / "tracewire.html"; s = o = rd(p)
FPRE = '<link as="font" crossorigin="" href="/assets/fonts/archivo-latin-79dc5e10.woff2" rel="preload" type="font/woff2"/>'
s = s.replace(FPRE, '')
k = s.find('<link', s.find('<head')); must(k > 0, "tracewire head link anchor"); s = s[:k] + FPRE + s[k:]
if s != o: p.write_text(s); n += 1
# ---------- f) tracewire grid ARIA ----------
p = ROOT / "assets/tracewire.js"; s = o = rd(p)
G0 = ("for(var r=0;r<N;r++)for(var c=0;c<N;c++){var ch=G[r][c],t=el('div',ch==='#'?'rt-t rt-wall':'rt-t');t.dataset.r=r;t.dataset.c=c;"
      "if(ch!=='#'){t.innerHTML='<span>'+ch+'</span>';t.setAttribute('role','gridcell');t.setAttribute('aria-label',ch);tiles[cid(r,c)]=t}board.appendChild(t)}")
G1 = ("for(var r=0;r<N;r++){var rw=el('div','rt-row');rw.setAttribute('role','row');for(var c=0;c<N;c++){var ch=G[r][c],t=el('div',ch==='#'?'rt-t rt-wall':'rt-t');t.dataset.r=r;t.dataset.c=c;"
      "t.setAttribute('role','gridcell');if(ch!=='#'){t.innerHTML='<span>'+ch+'</span>';t.setAttribute('aria-label',ch);tiles[cid(r,c)]=t}else t.setAttribute('aria-label','Blocked square');rw.appendChild(t)}board.appendChild(rw)}")
S0 = "row.setAttribute('aria-label',f?w:w.length+' letters');"
S1 = "row.setAttribute('role','group');row.setAttribute('aria-label',f?w:w.length+' letters');"
if G1 not in s: must(G0 in s, "tracewire grid loop"); s = s.replace(G0, G1)
if S1 not in s: must(S0 in s, "tracewire slot label"); s = s.replace(S0, S1)
if s != o: p.write_text(s); n += 1
print(f"site_eval_1121: {n} file(s) changed")
