import os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json,subprocess
MEASURE="()=>{let bad=[];document.querySelectorAll('.fx-checkgrid,.fx-actions,.fx-shareactions,.fx-digestgrid,.f-stripgrid,.f-feedgrid,.f-markets').forEach(c=>{if(!c.getBoundingClientRect().height)return;let rs=[];[...c.children].filter(x=>x.getBoundingClientRect().height>0).forEach(x=>{let r=x.getBoundingClientRect(),row=rs.find(a=>Math.abs(a[0].top-r.top)<2);if(row)row.push(r);else rs.push([r])});rs.forEach(row=>{if(row.length<rs[0].length&&row[0].width<c.clientWidth-2)bad.push('orphan '+c.className);if(row.length>1&&(Math.max(...row.map(x=>x.height))-Math.min(...row.map(x=>x.height))>2||Math.max(...row.map(x=>x.width))-Math.min(...row.map(x=>x.width))>2))bad.push('unequal '+c.className)})});return {overflow:document.documentElement.scrollWidth>innerWidth,symmetry:bad}}"
H=Path(__file__).parent;O=H/'qa-ux';O.mkdir(exist_ok=True);checks=[];functional=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for state in ['default','nojs','reduced']:
  for width in [375,390,430,768,1024,1280,1440]:
   ctx=b.new_context(viewport={'width':width,'height':1000},is_mobile=width<500,has_touch=width<500,java_script_enabled=state!='nojs',reduced_motion='reduce' if state=='reduced' else 'no-preference')
   for slug in ['wire','calendar','bp-watch','feeds','digest','home']:
    page=ctx.new_page();errors=[];page.on('pageerror',lambda er:errors.append(str(er)))
    page.goto('http://localhost:8957/'+('index.html' if slug=='home' else slug+'/'),wait_until='networkidle')
    if slug=='home':page.locator('.f-strip').scroll_into_view_if_needed()
    data=page.evaluate(MEASURE);data.update(page=slug,width=width,state=state,errors=errors);checks.append(data)
    if state=='default' and width in [375,1440]:
     if slug=='home':page.locator('.f-strip').screenshot(path=str(O/f'home-{width}.png'))
     else:page.screenshot(path=str(O/f'{slug}-{width}.png'))
    # Expanded states: all rule disclosures and secondary page filters open.
    page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    if state!='nojs' and page.locator('[data-prefs-open]').count():page.locator('[data-prefs-open]').first.click()
    expanded=page.evaluate(MEASURE);checks.append(dict(page=slug,width=width,state=state+'-expanded',errors=[],**expanded))
    if state=='default' and width in [375,1440]:
     if slug=='wire':
      page.locator('.f-entry').first.scroll_into_view_if_needed();page.screenshot(path=str(O/f'wire-expanded-{width}.png'));page.locator('.fx-tools').first.scroll_into_view_if_needed();page.screenshot(path=str(O/f'wire-mymarkets-{width}.png'))
      page.keyboard.press('/');page.locator('#fx-search-input').fill('3DS');page.screenshot(path=str(O/f'search-{width}.png'));page.keyboard.press('ArrowDown');assert page.evaluate('document.activeElement.matches(".fx-results a")');page.keyboard.press('Escape');assert not page.locator('.fx-search').is_visible()
     if slug=='calendar':
      page.locator('.fx-timeline details').evaluate_all('(es)=>es.forEach(e=>e.open=false)');page.locator('.fx-timeline').evaluate('e=>e.scrollIntoView({block:"start"})');page.screenshot(path=str(O/f'calendar-countdown-{width}.png'))
     if slug=='digest':
      page.emulate_media(media='print');page.pdf(path=str(O/f'digest-{width}.pdf'),format='A4',print_background=True);subprocess.run(['pdftoppm','-png','-scale-to','1440','-singlefile',str(O/f'digest-{width}.pdf'),str(O/f'digest-print-{width}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
      info=subprocess.check_output(['pdfinfo',str(O/f'digest-{width}.pdf')],text=True);functional.append({'print_width':width,'one_page':'Pages:           1' in info});assert 'Pages:           1' in info
    page.close()
   ctx.close()
 # Preference persistence across all five requested surfaces.
 ctx=b.new_context(viewport={'width':375,'height':1000});page=ctx.new_page();page.goto('http://localhost:8957/wire/',wait_until='networkidle');page.locator('[data-prefs-open]').first.click();page.locator('input[name=market][value=anz]').check();page.locator('input[name=rail][value=cards]').check()
 for slug in ['wire','calendar','bp-watch','feeds','home']:
  page.goto('http://localhost:8957/'+('index.html' if slug=='home' else slug+'/'),wait_until='networkidle');assert page.evaluate('JSON.parse(localStorage.getItem("mw-feed-prefs-v1")).markets[0]')=='anz'
  visible=page.locator('.f-entry[data-market]:visible');assert visible.evaluate_all('(es)=>es.every(e=>e.dataset.market==="anz"&&e.dataset.rails.split(" ").includes("cards"))')
  if slug=='home':assert page.locator('.f-stripitem small').evaluate_all('(es)=>es.every(e=>e.textContent.includes("AU & NZ"))')
 functional.append({'preferences':'five surfaces persisted and matched'})
 # Fresh context tests since-last-visit and clipboard (no external send).
 ctx=b.new_context(viewport={'width':375,'height':1000},permissions=['clipboard-read','clipboard-write']);ctx.add_init_script("localStorage.setItem('mw-feed-last-visit','2026-11-07T00:00:00Z')");page=ctx.new_page();page.goto('http://localhost:8957/wire/',wait_until='networkidle');expect(page.locator('[data-since]').first).to_contain_text('31 since');page.locator('.fx-details').first.locator('summary').click();page.locator('[data-snippet=linkedin]').first.click();expect(page.locator('.fx-copy-status').first).to_contain_text('Copied');clip=page.evaluate('navigator.clipboard.readText()');assert 'Official source: https://' in clip and 'Preview' in clip;functional.append({'since':'31 expected','clipboard':'source included; nothing sent'})
 b.close()
(O/'results.json').write_text(json.dumps({'render_checks':checks,'functional':functional},indent=2));bad=[c for c in checks if c['overflow'] or c['symmetry'] or c['errors']];print('QA checks',len(checks),'issues',json.dumps(bad,indent=2));print('Functional',functional)
