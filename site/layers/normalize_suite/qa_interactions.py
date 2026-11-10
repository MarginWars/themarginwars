import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
H=Path(__file__).parent;O=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/suite_1108')));ns={'__file__':str(H/'qa_suite.py')};code=(H/'qa_suite.py').read_text();exec(code.split('part=int')[0],ns)
R=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for w in (320,390,430,1024):
  for f in ('index.html','about.html','advisory.html','deal.html','wire/index.html','calendar/index.html','feeds/index.html','digest/index.html'):
   P=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');P.goto('http://localhost:8817/'+f,wait_until='networkidle');P.evaluate('window.scrollTo(0,document.body.scrollHeight)');P.wait_for_timeout(150);P.evaluate('window.scrollTo(0,0)')
   for state in ('default','expanded'):
    if state=='expanded':P.evaluate("document.querySelectorAll('details').forEach(e=>e.open=true);document.querySelectorAll('.fx-prefs').forEach(e=>e.hidden=false)")
    r={'sym':P.evaluate(ns['M']),'contrast':P.evaluate(ns['CON']),'targets':P.evaluate(ns['TARGET']),'overflow':P.evaluate('document.documentElement.scrollWidth>innerWidth')};R.append({'file':f,'w':w,'state':state,'findings':{k:v for k,v in r.items() if v}})
    P.screenshot(path=str(O/f'extra_{f.replace(chr(47),chr(95)).replace(chr(46)+"html","")}_{w}_{state}.png'),full_page=True)
   P.close()
 for f in ('index.html','wire/index.html','calendar/index.html'):
  P=b.new_page(viewport={'width':375,'height':900});P.goto('http://localhost:8817/'+f,wait_until='networkidle');P.keyboard.press('/');P.wait_for_timeout(150)
  assert P.locator('.fx-search').evaluate('(e)=>e.open'),f
  P.locator('.fx-search input').fill('debit');P.keyboard.press('ArrowDown');assert P.evaluate("document.activeElement.matches('.fx-results a')"),f
  P.keyboard.press('Escape');assert not P.locator('.fx-search').evaluate('(e)=>e.open'),f
  P.locator('[data-prefs-open]').click();P.locator('.fx-check').first.click();assert P.locator('.fx-check input').first.is_checked(),f
  P.locator('[data-prefs-reset]').click();assert P.locator('.fx-check input:checked').count()==0,f
  R.append({'file':f,'interaction':'search / arrows / Escape / prefs / reset','findings':{}});P.close()
 # Every generated route retains static content without JavaScript, not just the template sample.
 for row in json.loads((H/'routes.json').read_text()):
  P=b.new_page(java_script_enabled=False,viewport={'width':375,'height':900});P.goto('http://localhost:8817/'+row['file'],wait_until='domcontentloaded')
  assert P.locator('main').is_visible(),row['file'];assert P.locator('h1').count(),row['file']
  R.append({'file':row['file'],'mode':'nojs','findings':{}});P.close()
(O/'interactions.json').write_text(json.dumps(R,indent=1));print('Extra',len(R),'runs;',sum(bool(r['findings']) for r in R),'findings')
