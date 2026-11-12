#!/usr/bin/env python3
"""Campaign landing-page template on the approved brand (shell, nav, footer and CSS from the live site).
Usage: make_landing.py SPEC.json [--out DIR]   -> writes DIR/lp/<slug>.html (default: a private preview folder).
Pages are noindex by default and are NOT added to the sitemap. Publishing = writing into site_calm/lp/ and running build.sh,
which needs Avi's explicit go per campaign (see MARKETING.md)."""
import html, json, pathlib, re, sys
SITE = pathlib.Path("@MW_ROOT@/site_calm")
e = lambda s: html.escape(str(s), quote=True)
def render(spec):
    assert len(spec["stats"]) == 4 and len(spec["steps"]) == 4, "template grid is symmetric at four stats and four steps"  # four stats / four steps keep the 4-column grids balanced
    shell = (SITE / "advisory.html").read_text()
    t = re.sub(r"<!--bo-seo-->.*?<!--/bo-seo-->", "", shell, flags=re.S)
    url = f"https://themarginwars.com/lp/{spec['slug']}"
    t = re.sub(r"<title>.*?</title>", f"<title>{e(spec['title'])} | The Margin Wars</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta\b[^>]*name="description"[^>]*>', f'<meta content="{e(spec["description"])}" name="description"/>'
        f'<meta content="noindex, follow" name="robots"/><link href="{url}" rel="canonical"/>'
        f'<meta content="website" property="og:type"/><meta content="The Margin Wars" property="og:site_name"/><meta content="{e(spec["title"])}" property="og:title"/>'
        f'<meta content="{e(spec["description"])}" property="og:description"/><meta content="{url}" property="og:url"/>'
        f'<meta content="https://themarginwars.com/assets/brand/og-default.png" property="og:image"/><meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/>'
        f'<meta content="summary_large_image" name="twitter:card"/>', t, count=1)
    t = re.sub(r'aria-current="page" ', "", t)
    n = int(spec.get("plate", 2))
    pic = (f'<picture><source sizes="(min-width:960px) 600px, 92vw" srcset="/assets/plates/plate-{n}-640.avif 640w, /assets/plates/plate-{n}-1200.avif 1200w" type="image/avif"/>'
           f'<img alt="" decoding="async" height="900" fetchpriority="high" sizes="(min-width:960px) 600px, 92vw" src="/assets/plates/plate-{n}-1200.jpg" srcset="/assets/plates/plate-{n}-640.jpg 640w, /assets/plates/plate-{n}-1200.jpg 1200w" width="1200"/></picture>')
    cta = f'/contact.html?topic={e(spec.get("cta_topic", ""))}#contact-form'
    main = (f'<main id="main" tabindex="-1"><section class="ihero ih-pl"><div class="ih-copy"><p class="eyebrow">{e(spec.get("eyebrow", ""))}</p><h1>{e(spec["title"])}</h1>'
        f'<p class="lede">{e(spec["lede"])}</p><a class="btn nm-inline nm-primary" data-lp-cta="" href="{cta}">{e(spec["cta_label"])}</a></div>'
        f'<figure class="plate ih-art"><div class="plate-frame"><div class="plate-mat"><div class="plate-mark">{pic}</div><span aria-hidden="true" class="plate-sweep"></span></div></div></figure></section>'
        '<div class="wrap"><section aria-label="At a glance" class="statband">' + "".join(f'<div class="st"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in spec["stats"]) + '</section>'
        '<section aria-labelledby="lp-h" class="route"><p class="eyebrow sx">01</p><h2 id="lp-h">How it works</h2><ol class="rt-ol"><span aria-hidden="true" class="rt-line"><i></i></span>'
        + "".join(f'<li class="rt-s" style="--k:{i}"><span aria-hidden="true" class="rt-plate">{i+1:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(spec["steps"])) + '</ol></section>'
        f'<section aria-labelledby="lp-c" class="route"><p class="eyebrow sx">02</p><h2 id="lp-c">{e(spec["cta_label"])}</h2><p class="lede">{e(spec.get("proof", ""))}</p>'
        f'<p><a class="btn nm-inline nm-primary" data-lp-cta="" href="{cta}">{e(spec["cta_label"])}</a></p></section></div></main>')
    i, j = t.find("<main"), t.find("</main>") + len("</main>")
    t = t[:i] + main + t[j:]
    # root-relative assets so the page works at /lp/<slug>
    t = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|data:)([^"]+)"', r'\1="/\2"', t)
    t = re.sub(r'(srcset)="(?!/)(assets/[^"]+)"', lambda m: m.group(1) + '="' + re.sub(r"(^|, )assets/", r"\1/assets/", m.group(2)) + '"', t)
    return t
if __name__ == "__main__":
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else pathlib.Path(__file__).with_name("preview")
    (out / "lp").mkdir(parents=True, exist_ok=True); p = out / "lp" / f"{spec['slug']}.html"; p.write_text(render(spec)); print(p)
