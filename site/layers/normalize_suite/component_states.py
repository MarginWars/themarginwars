import os
from pathlib import Path
from playwright.sync_api import sync_playwright
O=Path(os.environ.get('QA_OUT',str(Path(__file__).parent.parent/'site_qa/suite_1108')))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for w in [375,1440]:
  P=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');P.goto('http://localhost:8817/index.html',wait_until='networkidle');P.locator('[data-prefs-open]').click();P.locator('.fx-check').first.click();P.locator('[data-prefs-reset]').hover();P.add_style_tag(content='body>header{visibility:hidden!important}');P.locator('.f-strip').screenshot(path=str(O/f'home_wire_actions_{w}.png'))
  P.goto('http://localhost:8817/advisory.html',wait_until='networkidle');P.locator('.rb-fs input').first.focus();P.keyboard.press('ArrowRight');P.add_style_tag(content='body>header{visibility:hidden!important}');P.locator('#route-brief').screenshot(path=str(O/f'route_brief_focus_{w}.png'));P.close()
