import os
import sys
from playwright.sync_api import sync_playwright
port=sys.argv[1]
P='index about advisory speaking writing warroom contact arcade daily deal leak quiz tracewire ep1 ep2 ep3 ep4 ep5 ep6 ep7 ep8 ep9'.split()
t=0
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox']); pg=b.new_page(viewport={'width':1440,'height':900})
  for n in P:
    pg.goto(f'http://localhost:{port}/{n}.html',wait_until='networkidle')
    w=len(pg.evaluate("()=>(document.querySelector('main')||document.body).innerText").split()); t+=w; print(n,w)
  print('TOTAL',t)
