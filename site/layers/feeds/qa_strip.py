import os
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
H=Path(__file__).parent;rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for w in [375,390,430,768,1024,1280,1440]:
  for nojs in [False,True]:
   ctx=b.new_context(viewport={'width':w,'height':844},device_scale_factor=1,is_mobile=w<500,has_touch=w<500,java_script_enabled=not nojs)
   page=ctx.new_page();page.goto('http://localhost:8957/index.html',wait_until='networkidle');strip=page.locator('.f-strip');strip.scroll_into_view_if_needed()
   row=page.evaluate('''()=>{let s=document.querySelector('.f-strip'),c=getComputedStyle(s),r=s.getBoundingClientRect(),h=s.querySelector('.f-striphead').getBoundingClientRect(),p=s.querySelector('.f-stripstatus').getBoundingClientRect(),n=document.querySelector('.intro2'),nc=getComputedStyle(n);return {width:innerWidth,strip_left:h.left,site_edge:parseFloat(nc.paddingLeft),top:parseFloat(c.paddingTop),bottom:parseFloat(c.paddingBottom),rhythm:parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sec')),status_bottom_gap:r.bottom-p.bottom,status_height:p.height,strip_overflow:s.scrollWidth>s.clientWidth,fixed_height:c.maxHeight,items:[...s.querySelectorAll('.f-stripitem')].map(e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height}))}}''');row['nojs']=nojs
   assert abs(row['strip_left']-row['site_edge'])<=1,row
   assert row['top']==row['rhythm'] and row['bottom']==row['rhythm'],row
   assert row['status_bottom_gap']>=row['bottom']-1,row
   assert not row['strip_overflow'],row
   strip.screenshot(path=str(H/'qa'/f'home-strip-{w}-iphone-{nojs}.png'));rows.append(row);ctx.close()
 b.close()
(H/'qa/strip-measurements.json').write_text(json.dumps(rows,indent=2));print('Strip edges, rhythm, status clearance, iPhone emulation:',len(rows),'PASS')
