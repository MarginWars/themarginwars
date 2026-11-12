#!/usr/bin/env python3
"""Game share flow layer (share_1111). Runs on a built copy (site_dist or a copy of it), never on site_calm,
so the in-place source layers stay untouched and idempotent. Idempotent itself.
Usage: apply_share.py TARGET_DIR
 - assets/share.js + assets/share.css on every game page and the Arcade hub
 - games.js: band-colour grid, shareBox -> result card with X / LinkedIn / copy / native share / card download
 - tracewire.js: same share block in the result panel
 - arcade.html: 'Share the Arcade' row
 - per-game 1200x630 OG cards (assets/brand/og/<game>.png) and og/twitter title, description, image, alt"""
import sys, re, shutil, html, pathlib, urllib.parse
from PIL import Image, ImageDraw
sys.path.insert(0, "@MW_ROOT@/linkedin_page_1110"); import gen
H = pathlib.Path(__file__).resolve().parent
D = pathlib.Path(sys.argv[1]).resolve()
assert D.name != "site_calm", "run on a built copy, not site_calm"
GAMES = ["daily", "tracewire", "leak", "deal", "quiz"] + [f"ep{i}" for i in range(1, 10)] + ["arcade"]
SITE = "https://themarginwars.com/"
A = D / "assets"
shutil.copyfile(H / "share.js", A / "share.js"); shutil.copyfile(H / "share.css", A / "share.css")

def sub1(s, old, new, label):
    if new in s: return s
    assert s.count(old) == 1, (label, s.count(old)); return s.replace(old, new)

# ---- games.js
g = A / "games.js"; s = g.read_text()
s = sub1(s, "function grid(m){return m.map(function(x){return x?'🟪':'⬜'}).join('')}",
         "function grid(m){return window.MWS?MWS.grid(m):m.map(function(x){return x?'🟪':'⬜'}).join('')}", "grid")
NEWBOX = "function shareBox(text,path,cardTitle,cardSub,o){o=o||{};return window.MWS?MWS.box({game:String(path).split(/[.?]/)[0],label:o.label||'',meta:o.meta||'',score:o.score||'',marks:o.marks,sub:o.sub||'',text:text,card:{h:cardTitle,s:cardSub}}):''}"
if NEWBOX not in s:
    m = re.search(r"function shareBox\(text,path,cardTitle,cardSub\)\{.*?\n\}\n", s, re.S); assert m, "shareBox"
    s = s[:m.start()] + NEWBOX + "\n" + s[m.end():]
for old, new in [
    ("'Five practitioner questions a day, every answer sourced.')", "'Five practitioner questions a day, every answer sourced.',{label:'Daily',meta:d+' · Pacific Time',score:score+'/5',marks:marks,sub:'Streak: '+st2.n})"),
    ("'Spot the Leak · The Margin Wars Arcade')", "'Spot the Leak · The Margin Wars Arcade',{label:'Spot the Leak',meta:'Illustrative statement',score:found+'/'+total,marks:Array.apply(null,Array(total)).map(function(_,i){return i<found}),sub:'Leaks found'})"),
    ("'Price the Deal · The Margin Wars Arcade')", "'Price the Deal · The Margin Wars Arcade',{label:'Price the Deal',meta:'Illustrative $400M merchant',score:pts+'/100'})"),
    ("'This month: Rails & Rules')", "'This month: Rails & Rules',{label:'Pub Quiz',meta:m,score:s+'/10',marks:mk})"),
    ("'The Margin Wars, Season 1 · Rank: '+rank)", "'The Margin Wars, Season 1 · Rank: '+rank,{label:'Season 1',meta:'Episode '+n+' · '+title,score:s+'/'+tot,sub:'Rank: '+rank})"),
]:
    s = sub1(s, old, new, old[:30])
s = s.replace("<p class=\"g-big\">'+grid(marks)+'</p>", "").replace("<p class=\"g-big\">'+grid(mk)+'</p>", "")  # card shows the grid once
s = sub1(s, "'<h3 aria-level=\"2\">'+found+'/'+total+' leaks found</h3>'+shareBox(", "'<h3 aria-level=\"2\">'+found+'/'+total+' leaks found</h3>'+(opt.ep?'':shareBox(", "leak-ep")
s = sub1(s, "sub:'Leaks found'})+(opt.ep?", "sub:'Leaks found'}))+(opt.ep?", "leak-ep2")
g.write_text(s)

# ---- tracewire.js
t = A / "tracewire.js"; s = t.read_text()
if 'class="rt-mws"' not in s:
    s, n = re.subn(r"'<div class=\"rt-share\">.*?</p></div><p class=\"rt-next\"></p>'", "'<div class=\"rt-mws\"></div><p class=\"rt-next\"></p>'", s, flags=re.S); assert n == 1, "rt-share"
    s = sub1(s, "res.hidden=false;var tx=shareText();res.querySelector('.rt-txt').textContent=tx;",
             "res.hidden=false;var tx=shareText();res.querySelector('.rt-mws').innerHTML=window.MWS?MWS.box({game:'tracewire',label:'Tracewire',meta:'No. '+b.no+' · '+nice(b.date),score:fmt(st.t),sub:st.hints?st.hints+(st.hints>1?' hints':' hint'):'No hints. Clean run.',text:tx,card:{h:'Tracewire No. '+b.no+': solved in '+fmt(st.t),s:'Payments people: can you trace it faster?'}}):'';", "tw-inject")
    s, n = re.subn(r"\n var draw2=function\(\).*?\n res\.querySelector\('\[data-s=copy\]'\)\.onclick=function\(\)\{.*?\};", "", s, flags=re.S); assert n == 1, "tw-old-wiring"
t.write_text(s)

# ---- OG cards
OG = A / "brand/og"; OG.mkdir(parents=True, exist_ok=True)
mark = gen.render_mark(scale=8).convert("RGBA")
def wrap(d, text, f, w):
    out, line = [], ""
    for word in text.split():
        tl = (line + " " + word).strip()
        if d.textlength(tl, font=f) > w and line: out.append(line); line = word
        else: line = tl
    return out + [line]
def og_card(slug, kicker, title, desc):
    S = 2; W, Hh = 1200 * S, 630 * S
    im = Image.new("RGB", (W, Hh), gen.hx(gen.PAPER)); d = ImageDraw.Draw(im)
    bw = W / 6
    for i, c in enumerate(gen.BAND): d.rectangle([round(i * bw), 0, round((i + 1) * bw) - 1, 14 * S - 1], fill=gen.hx(c))
    m = mark.resize((96 * S, 96 * S), Image.Resampling.LANCZOS); im.paste(m, (80 * S, 80 * S), m)
    d.text((196 * S, 92 * S), "The Margin Wars", font=gen.font(gen.SG_BOLD, 30 * S), fill=gen.hx(gen.INK))
    d.text((196 * S, 136 * S), kicker, font=gen.font(gen.mm_path(), 20 * S), fill=gen.hx("#5B656B"))
    # word-free grid graphic, right side: 4 rows x 5 in band colours with paper gaps
    pat = ["11011", "10111", "11101", "11111"]; sz, gp = 56 * S, 12 * S; gx = W - 80 * S - 5 * sz - 4 * gp; gy = 214 * S
    hits = [gen.BAND[i] for i in (0, 1, 2, 4, 5)]
    for r, row in enumerate(pat):
        for c, on in enumerate(row):
            x0, y0 = gx + c * (sz + gp), gy + r * (sz + gp)
            if on == "1": d.rounded_rectangle([x0, y0, x0 + sz, y0 + sz], radius=8 * S, fill=gen.hx(hits[c]))
            else: d.rounded_rectangle([x0, y0, x0 + sz, y0 + sz], radius=8 * S, fill=gen.hx("#FFFFFF"), outline=gen.hx("#B7C1C9"), width=3 * S)
    tw = gx - 80 * S - 48 * S
    for size in (84, 76, 68, 60, 54):
        tf = gen.font(gen.SG_BOLD, size * S); tl = wrap(d, title, tf, tw)
        if len(tl) <= 2: break
    y = 226 * S
    for l in tl: d.text((80 * S, y), l, font=tf, fill=gen.hx(gen.INK)); y += round(size * 1.08 * S)
    df = gen.font(gen.SG_REG, 30 * S); y += 18 * S
    for l in wrap(d, desc, df, tw)[:3]: d.text((80 * S, y), l, font=df, fill=gen.hx("#39434A")); y += 40 * S
    d.rectangle([80 * S, 528 * S, 86 * S - 1, 570 * S], fill=gen.hx(gen.PINK))
    d.text((104 * S, 536 * S), "themarginwars.com/" + slug, font=gen.font(gen.mm_path(), 22 * S), fill=gen.hx("#5B656B"))
    im.resize((1200, 630), Image.Resampling.LANCZOS).save(OG / f"{slug}.png", optimize=True)

def meta_set(t, attr, key, val):
    pat = re.compile(r'<meta content="[^"]*" %s="%s"/>' % (attr, re.escape(key)))
    tag = '<meta content="%s" %s="%s"/>' % (html.escape(val, quote=True), attr, key)
    assert len(pat.findall(t)) == 1, key; return pat.sub(lambda _: tag, t)

for slug in GAMES:
    p = D / f"{slug}.html"; t = p.read_text()
    title = html.unescape(re.search(r"<title>([^<]*)</title>", t).group(1))
    desc = html.unescape(re.search(r'<meta content="([^"]*)" property="og:description"/>', t).group(1))
    h1 = [html.unescape(x) for x in re.findall(r"<span>([^<]*)</span>", re.search(r"<h1>(.*?)</h1>", t).group(1))]
    big = h1[1] if slug.startswith("ep") else " ".join(h1)
    kicker = "Arcade · Season 1 · " + h1[0] if slug.startswith("ep") else "Arcade"
    og_card(slug, kicker, big, desc)
    img = SITE + f"assets/brand/og/{slug}.png"; alt = f"{big}: {desc}" if not desc.startswith(big) else desc
    for attr, key, val in [("property", "og:title", title), ("name", "twitter:title", title), ("property", "og:image", img), ("name", "twitter:image", img), ("property", "og:image:alt", alt)]:
        t = meta_set(t, attr, key, val)
    if 'name="twitter:image:alt"' not in t: t = t.replace('<meta content="%s" name="twitter:image"/>' % img, '<meta content="%s" name="twitter:image"/><meta content="%s" name="twitter:image:alt"/>' % (img, html.escape(alt, quote=True)), 1)
    if "/assets/share.css" not in t: t = t.replace("</head>", '<link href="/assets/share.css" rel="stylesheet"/></head>', 1)
    if "/assets/share.js" not in t:
        t, n = re.subn(r'(<script src="assets/(?:games|tracewire_boards)\.js)', r'<script src="/assets/share.js"></script>\1', t, count=1)
        if n == 0: t = t.replace('<script defer="" src="/assets/mk.js"></script>', '<script src="/assets/share.js"></script><script defer="" src="/assets/mk.js"></script>', 1)
    if slug == "arcade" and 'class="mws-hub"' not in t:
        ht = "The Margin Wars Arcade: five games for payments practitioners. Every fact is sourced."
        u = lambda src: SITE + "arcade?utm_source=" + src + "&utm_medium=social&utm_campaign=game-share&utm_content=arcade"
        q = lambda v: urllib.parse.quote(v, safe="-_.!~*'()")
        xh = "https://x.com/intent/post?text=" + q(ht + "\n\n" + u("x")); lh = "https://www.linkedin.com/sharing/share-offsite/?url=" + q(u("linkedin"))
        e = lambda v: html.escape(v, quote=True)
        hub = ('<section class="mws-hub" aria-labelledby="mws-h"><p class="eyebrow">Share</p><h2 id="mws-h">Share the Arcade</h2>'
               f'<div class="mws mws-hubb" data-g="arcade" data-t="{e(ht)}"><div class="mws-b n3"><button type="button" class="btn mws-nat" data-s="native" hidden>Share…</button>'
               f'<a class="btn mws-x" data-s="x" target="_blank" rel="noopener" href="{e(xh)}">Share on X</a>'
               f'<a class="btn mws-li" data-s="linkedin" target="_blank" rel="noopener" href="{e(lh)}">Share on LinkedIn</a>'
               '<button type="button" class="btn alt mws-cp" data-s="copy">Copy link</button></div><p class="mws-n" role="status" aria-live="polite"></p></div></section>')
        anchor = '<section id="history">'; assert t.count(anchor) == 1; t = t.replace(anchor, hub + anchor, 1)
    p.write_text(t)
print("SHARE: share.js/css on", len(GAMES), "pages; OG cards in", OG.relative_to(D))
