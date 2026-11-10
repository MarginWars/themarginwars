import os
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
H=Path(__file__).parent;O=H/'qa';O.mkdir(exist_ok=True);checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,headless=True,args=['--no-sandbox'])
 for state in ['default','nojs','reduced']:
  for width in [375,390,430,768,1024,1280,1440]:
   context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1,java_script_enabled=state!='nojs',reduced_motion='reduce' if state=='reduced' else 'no-preference')
   for slug in ['wire','bp-watch','calendar','feeds','home']:
    page=context.new_page();errs=[];page.on('pageerror',lambda er:errs.append(str(er)))
    page.goto('http://localhost:8957/'+(slug+'/' if slug!='home' else 'index.html'),wait_until='networkidle')
    target=page.locator('.f-strip') if slug=='home' else page.locator('body')
    if slug=='home':target.scroll_into_view_if_needed()
    # All default entries are expanded, no accordions; tests include filtered states below.
    result=page.evaluate('''()=>{const bad=[];document.querySelectorAll('.f-feedgrid,.f-markets,.f-stripgrid,.f-facts').forEach(c=>{let rs=[];[...c.children].filter(x=>!x.hidden).forEach(x=>{const r=x.getBoundingClientRect();let row=rs.find(y=>Math.abs(y[0].top-r.top)<=2);if(row)row.push(r);else rs.push([r])});rs.forEach(row=>{if(row.length<rs[0].length&&row[0].width<c.clientWidth-2)bad.push('orphan '+c.className);if(row.length>1&&(Math.max(...row.map(x=>x.height))-Math.min(...row.map(x=>x.height))>2||Math.max(...row.map(x=>x.width))-Math.min(...row.map(x=>x.width))>2))bad.push('unequal '+c.className)});});return {overflow:document.documentElement.scrollWidth>innerWidth,symmetry:bad,headings:document.querySelectorAll('h1').length}}''')
    result.update(page=slug,width=width,state=state,errors=errs)
    # Screenshot first fold plus whole page for visual audit; Home captures just the strip.
    if slug=='home':target.screenshot(path=str(O/f'home-strip-{width}-{state}.png'))
    else:
     page.screenshot(path=str(O/f'{slug}-{width}-{state}.png'),full_page=False)
     if state=='default' and width in [375,1440]:page.screenshot(path=str(O/f'{slug}-{width}-full.png'),full_page=True)
    if state!='nojs' and slug in ['wire','calendar']:
     page.select_option('#f-market','anz');result['filtered_count']=page.locator('.f-entry:visible').count();result['filter_match']=page.locator('.f-entry:visible:not([data-market="anz"])').count()==0
     if slug=='wire':
      page.select_option('#f-type','regulation');result['type_match']=page.locator('.f-entry:visible:not([data-type="regulation"])').count()==0
     page.screenshot(path=str(O/f'{slug}-{width}-{state}-filtered.png'))
    if slug=='feeds' and state=='default':
     # Keyboard reaches all navigation controls without a trap; clipboard copied over localhost.
     page.keyboard.press('Tab');result['keyboard_first']=page.evaluate('document.activeElement.textContent')
     page.locator('[data-copy]').first.click();page.wait_for_function("document.querySelector('.f-live').textContent.length>0");result['copy_state']=page.locator('.f-live').inner_text()
    checks.append(result);page.close()
   context.close()
 browser.close()
(O/'results.json').write_text(json.dumps(checks,indent=2));bad=[c for c in checks if c['overflow'] or c['symmetry'] or c['errors'] or c.get('filter_match')==False or c.get('type_match')==False]
print('Checks',len(checks),'failures',len(bad));print(json.dumps(bad,indent=2))
