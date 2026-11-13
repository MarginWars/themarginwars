"""Render the repo brand assets in .github/assets/ from the HTML sources here.

Usage: python3 .github/assets/src/render.py   (needs Playwright Chromium; set CHROME=/path to use another binary)
Fonts and colours come from the site (site/layers/buildout/fonts_src, site/src/assets/suite.css).
"""
import asyncio, os, pathlib
from playwright.async_api import async_playwright

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent
MARK = SRC.parents[2] / "brand" / "channel-assets" / "mark400.svg"

JOBS = [  # (page, query, width, height, scale, output, transparent)
    ("banner.html", "?mode=light", 1280, 300, 2, "banner-light.png", True),
    ("banner.html", "?mode=dark", 1280, 300, 2, "banner-dark.png", True),
    ("social.html", "", 1280, 640, 1, "social-preview.png", False),
]

async def main() -> None:
    async with async_playwright() as p:
        kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
        b = await p.chromium.launch(**kw)
        for page, q, w, h, s, out, transparent in JOBS:
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=s)
            await pg.goto((SRC / page).as_uri() + q)
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(OUT / out), omit_background=transparent)
            await pg.close()
        # Org avatar: the banded M mark (brand/channel-assets/mark400.svg) at 500x500.
        pg = await b.new_page(viewport={"width": 500, "height": 500})
        await pg.set_content(f'<body style="margin:0">{MARK.read_text()}</body>')
        await pg.evaluate("document.querySelector('svg').setAttribute('width','500');document.querySelector('svg').setAttribute('height','500')")
        await pg.screenshot(path=str(OUT / "org-avatar.png"))
        await b.close()

asyncio.run(main())
