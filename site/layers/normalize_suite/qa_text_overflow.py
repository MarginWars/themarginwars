#!/usr/bin/env python3
"""Text-overflow gate: fail if any text's scrollWidth exceeds its clientWidth,
or if text ink spills outside its element's or card's padding box.
Usage:
  qa_text_overflow.py [PART PARTS] [file,file]
Env:
  QA_OUT   output directory (default: site_qa/gofurther_1112/qa)
  QA_BASE  base URL (default: http://127.0.0.1:8817/)
  TO_WIDTHS  comma-separated widths (default: 360,390,768,1024,1280,1440)
Exit 1 if any issue is found.
"""
import json, sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

H = Path(__file__).parent
OUT = Path(os.environ.get('QA_OUT', str(H.parent / 'site_qa/gofurther_1112/qa')))
OUT.mkdir(parents=True, exist_ok=True)
BASE = os.environ.get('QA_BASE', 'http://127.0.0.1:8817/')
WIDTHS = [int(x) for x in os.environ.get('TO_WIDTHS', '360,390,768,1024,1280,1440').split(',') if x]
JS = (H / 'text_overflow_check.js').read_text()
routes = json.loads((H / 'routes.json').read_text())
part, parts = 0, 1
if len(sys.argv) > 2:
    part, parts = int(sys.argv[1]), int(sys.argv[2])
if len(sys.argv) > 3:
    routes = [r for r in routes if r['file'] in sys.argv[3].split(',')]
else:
    routes = routes[part::parts]

res = {}
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None, args=['--no-sandbox'])
    for r in routes:
        f = r['file']
        for w in WIDTHS:
            c = b.new_context(viewport={'width': w, 'height': 900}, reduced_motion='reduce', device_scale_factor=1)
            page = c.new_page()
            try:
                try:
                    cdp = page.context.new_cdp_session(page)
                    cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
                except Exception:
                    pass
                page.goto(BASE + f, wait_until='domcontentloaded', timeout=45000)
                page.evaluate('() => document.fonts && document.fonts.ready')
                page.evaluate("async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 20)); } scrollTo(0, 0); }")
                page.wait_for_timeout(80)
                data = page.evaluate(JS)
            except Exception as e:
                data = {'n': 1, 'issues': [{'kind': 'error', 'el': 'PAGE', 't': str(e)[:160], 'w': w}], 'pageOverflow': False}
            c.close()
            key = f'{f}|{w}'
            res[key] = data
            if data.get('n') or data.get('pageOverflow'):
                fails += 1
        print('DONE', f, flush=True)
    b.close()

outp = OUT / f'text_overflow_{part}.json'
outp.write_text(json.dumps(res, indent=1))
niss = sum(v.get('n', 0) for v in res.values())
print('FINISHED', part, 'cases', len(res), 'failing-cases', fails, 'issues', niss, flush=True)
raise SystemExit(1 if fails else 0)
