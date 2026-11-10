import os
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
H=Path(__file__).parent;O=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/suite_1108')));N={'__file__':str(H/'qa_suite.py')};exec((H/'qa_suite.py').read_text().split('part=int')[0],N);R=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for w in [375,1440]:
  P=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');P.goto('http://localhost:8817/index.html',wait_until='networkidle')
  P.locator('[data-prefs-open]').click();P.locator('.fx-check').first.click();P.locator('[data-prefs-reset]').hover()
  P.screenshot(path=str(O/f'actions_prefs_{w}.png'),full_page=True)
  R.append({'route':'/','width':w,'state':'selected markets/reset hover','contrast':P.evaluate(N['CON'])})
  P.locator('[data-search-open]').click();P.locator('.fx-search input').fill('debit');P.keyboard.press('ArrowDown');P.screenshot(path=str(O/f'actions_search_{w}.png'));R.append({'route':'/','width':w,'state':'search modal keyboard result','contrast':P.evaluate(N['CON'])});P.keyboard.press('Escape')
  P.goto('http://localhost:8817/advisory.html',wait_until='networkidle');P.locator('.rb-fs').first.locator('input').nth(1).check();P.locator('.rb-fs').nth(1).locator('input').nth(1).check();P.locator('.rb-fs').first.locator('input').nth(1).focus();P.keyboard.press('ArrowLeft');P.screenshot(path=str(O/f'actions_route_{w}.png'),full_page=True)
  title=P.locator('.rb-brief:not([hidden]) h3').all_text_contents();assert title,title
  R.append({'route':'advisory','width':w,'state':'changed radio/focus','title':title,'contrast':P.evaluate(N['CON'])})
  P.goto('http://localhost:8817/deal.html',wait_until='networkidle');P.locator('#dr').fill('1.65');P.locator('#dgo').click();assert P.locator('.dk').inner_text().strip();P.screenshot(path=str(O/f'actions_deal_{w}.png'),full_page=True)
  R.append({'route':'deal','width':w,'state':'calculated answer','text':P.locator('.dk').inner_text(),'contrast':P.evaluate(N['CON'])})
  for route in ['daily','quiz']:
   P.goto('http://localhost:8817/'+route+'.html',wait_until='networkidle');P.locator('.gm button').first.click();
   if route=='quiz':P.locator('.gm button').first.click()
   assert P.locator('.gm button.ok,.gm button.no').count()>0,route
   P.screenshot(path=str(O/f'actions_{route}_{w}.png'),full_page=True);R.append({'route':route,'width':w,'state':'answered','contrast':P.evaluate(N['CON'])})
  P.close()
(O/'actions.json').write_text(json.dumps(R,indent=2));print('Functional states:',len(R),'contrast findings:',sum(bool(r['contrast']) for r in R))
