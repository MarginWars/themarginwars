"""Home Briefing invite CTA (23 Nov 2026). Idempotent; runs LAST on site_calm.

Adds a compact invite strip as the first block on the home page (above the hero,
above the fold on desktop) reusing existing Briefing copy and the contact form
flow. Tags that strip and the existing hero Briefing button with distinct
utm_content / data-mk-content labels so clicks can be compared.
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup

H = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("@MW_ROOT@/site_calm")
rd = lambda p: p.read_text()
n = 0

def wr(p, s):
    global n
    if not p.exists() or rd(p) != s:
        p.write_text(s)
        n += 1

def must(cond, msg):
    if not cond:
        raise SystemExit("home_cta_1123: " + msg)

CSS_LINK = '<link data-home-cta="" href="/assets/home-cta.css" rel="stylesheet"/>'
MARKER_OPEN = '<!--home-cta-1123-->'
MARKER_CLOSE = '<!--/home-cta-1123-->'
STRIP = (
    MARKER_OPEN
    + '<aside aria-label="The Margin Wars Briefing" class="brief-top">'
    + '<div class="brief-top-inner">'
    + '<p class="brief-top-copy">The Margin Wars Briefing. One tactic a month. About 150 readers. Invite-only.</p>'
    + '<a class="btn nm-inline nm-primary" data-mk-content="index-top-briefing" '
    + 'href="contact.html?topic=briefing&amp;utm_source=themarginwars.com&amp;utm_medium=website'
    + '&amp;utm_campaign=always-on&amp;utm_content=index-top-briefing#contact-form">'
    + 'Request an invitation to the Briefing</a>'
    + '</div></aside>'
    + MARKER_CLOSE
)
HERO_OLD = (
    '<a class="btn alt nm-inline" href="contact.html?topic=briefing#contact-form">'
    'Request an invitation to the Briefing</a>'
)
HERO_NEW = (
    '<a class="btn alt nm-inline" data-mk-content="index-hero-briefing" '
    'href="contact.html?topic=briefing&amp;utm_source=themarginwars.com&amp;utm_medium=website'
    '&amp;utm_campaign=always-on&amp;utm_content=index-hero-briefing#contact-form">'
    'Request an invitation to the Briefing</a>'
)

wr(ROOT / "assets/home-cta.css", rd(H / "cta.css"))

p = ROOT / "index.html"
s = o = rd(p)

# CSS last among stylesheets (after eval.css).
s = s.replace(CSS_LINK, "")
head = s[:s.find("<body")]
last = list(re.finditer(r'<link\b[^>]*rel="stylesheet"[^>]*>', head))
must(last, "index.html: no stylesheet link")
i = last[-1].end()
s = s[:i] + CSS_LINK + s[i:]

# Strip: between the sticky header and main, so section rhythm inside main is unchanged.
if MARKER_OPEN in s:
    s = re.sub(re.escape(MARKER_OPEN) + r".*?" + re.escape(MARKER_CLOSE), STRIP, s, count=1, flags=re.S)
else:
    m = re.search(r"</header>", s)
    must(m, "index.html: header close")
    s = s[:m.end()] + STRIP + s[m.end():]
must('class="brief-top"' in s, "index.html: brief-top strip missing")
must(s.find('class="brief-top"') < s.find('<main'), "index.html: brief-top must sit above main")

if HERO_OLD in s:
    s = s.replace(HERO_OLD, HERO_NEW, 1)
must("data-mk-content=\"index-hero-briefing\"" in s, "index.html: hero Briefing button not tagged")
must("data-mk-content=\"index-top-briefing\"" in s, "index.html: top Briefing button not tagged")

if s != o:
    p.write_text(s)
    n += 1

# Refresh the assistant snapshot after this last HTML layer so it includes the strip.
# normalize_suite writes this earlier, before eval and this layer.
knowledge = []
for name in ("index", "about", "advisory", "speaking", "writing", "contact"):
    page = BeautifulSoup((ROOT / (name + ".html")).read_text(), "html.parser").select_one("main")
    for el in page.select("script,style,template"):
        el.decompose()
    text = "\n".join(t.strip() for t in page.stripped_strings)
    knowledge.append("=== PAGE: " + name + " ===\n" + text)
kp = pathlib.Path("@MW_ROOT@/review_deploy/functions/api/_knowledge.js")
payload = "export default " + json.dumps("\n\n".join(knowledge)) + ";\n"
if not kp.exists() or kp.read_text() != payload:
    kp.write_text(payload)
    n += 1

print(f"home_cta_1123: {n} file(s) changed")
