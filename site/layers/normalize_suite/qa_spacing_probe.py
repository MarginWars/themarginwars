import os
import json,sys
from collections import Counter
from playwright.sync_api import sync_playwright
pages=sys.argv[1].split(',')
JS=r'''()=>{const W=innerWidth;const c=Counter=new Map();for(const e of document.querySelectorAll('body *')){if(e.closest('nav,header,.lk-rail,[aria-hidden=true],svg,figure'))continue;const has=[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim().length>1)||e.matches('img,button,input,select,a');if(!has)continue;const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;const s=getComputedStyle(e);if(s.visibility=='hidden'||s.position=='fixed')continue;let x=e;let clip=false;while(x=x.parentElement){const o=getComputedStyle(x).overflowX;if(o=='auto'||o=='scroll'){clip=true;break}}if(clip)continue;const L=Math.round(r.left),R=Math.round(W-r.right);c.set('L'+L,(c.get('L'+L)||0)+1);}return [...c].sort((a,b)=>b[1]-a[1]).slice(0,6)}'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for f in pages:
  for w in (320,375,768,1024,1280,1440,1920):
   P=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');P.goto('http://localhost:8817/'+f,wait_until='networkidle')
   print(f,w,P.evaluate(JS));P.close()
