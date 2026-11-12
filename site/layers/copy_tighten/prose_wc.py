import os
import sys
from playwright.sync_api import sync_playwright
P='index about advisory speaking writing warroom contact arcade daily deal leak quiz tracewire ep1 ep2 ep3 ep4 ep5 ep6 ep7 ep8 ep9'.split()
t=0
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox']); pg=b.new_page(viewport={'width':1440,'height':900})
  for n in P:
    pg.goto(f'http://localhost:{sys.argv[1]}/{n}.html',wait_until='networkidle')
    w=pg.evaluate("()=>[...document.querySelectorAll('main p')].filter(e=>e.offsetParent).reduce((a,e)=>a+e.innerText.split(/\\s+/).filter(Boolean).length,0)"); t+=w; print(n,w)
  print('TOTAL',t)
