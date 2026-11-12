import os
import json,sys,re,pathlib
from playwright.sync_api import sync_playwright
B='http://localhost:8817/'; OUT=pathlib.Path(__file__).parent
M=open('@MW_ROOT@/site_qa/measure.js').read()
PAGES=sys.argv[1].split(',') if len(sys.argv)>1 else 'index about advisory speaking writing warroom contact arcade daily deal leak quiz tracewire ep1 ep2 ep3 ep4 ep5 ep6 ep7 ep8 ep9'.split()
W=[320,375,390,430,768,1024,1280,1440]
CONTRAST=r"""()=>{function rgb(s){const m=s.match(/[\d.]+/g);return m?m.map(Number):[0,0,0,0]}
function L(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]}
function bg(e){while(e){const c=rgb(getComputedStyle(e).backgroundColor);if(c[3]===undefined||c[3]>0.5){if(getComputedStyle(e).backgroundImage!=='none'&&!c[3])return null;return c}e=e.parentElement}return [255,255,255]}
const out=[];document.querySelectorAll('main *, header *').forEach(e=>{if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;const r=e.getBoundingClientRect();if(!r.width)return;const cs=getComputedStyle(e);if(cs.visibility==='hidden'||+cs.opacity===0)return;if(e.closest('[aria-hidden=true],.wk-off,.sr,canvas,svg'))return;const b=bg(e);if(!b)return;const f=rgb(cs.color);if(f[3]!==undefined&&f[3]<0.5)return;const l1=L(f),l2=L(b);const cr=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);const big=parseFloat(cs.fontSize)>=24||(parseFloat(cs.fontSize)>=18.6&&+cs.fontWeight>=700);if(cr<(big?3:4.5))out.push({t:e.textContent.trim().slice(0,40),cr:+cr.toFixed(2),c:cs.color,b:String(b)})});return out.slice(0,10)}"""
VIS=r"""()=>{const o=[];document.querySelectorAll('main h1,main h2,main h3,main p,main li,main a,main button').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width||e.closest('details:not([open]) .acc-b,[hidden]'))return;let a=e,op=1;while(a){op*=+getComputedStyle(a).opacity;a=a.parentElement}if(op<0.5&&!e.closest('.wk-off'))o.push(e.tagName+':'+e.textContent.trim().slice(0,30))});return o.slice(0,8)}"""
CLICK=r"""()=>{const o=[];document.querySelectorAll('main a[href],header a[href],main button').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width||e.closest('[hidden],details:not([open]) .acc-b'))return;const x=r.left+Math.min(r.width/2,20),y=r.top+r.height/2;if(y<0||y>innerHeight)return;const t=document.elementFromPoint(x,y);if(t&&!(e===t||e.contains(t)||t.contains(e)))o.push(e.textContent.trim().slice(0,30)+' <- '+t.className)});return o.slice(0,6)}"""
res={}
with sync_playwright() as p:
  br=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
  for rm in ['no-preference','reduce']:
   for pg in PAGES:
    for w in W:
     for state in ['default','expanded']:
      if rm=='reduce' and w not in (375,1280): continue
      c=br.new_context(viewport={'width':w,'height':900},reduced_motion=rm); P=c.new_page(); errs=[]
      P.on('pageerror',lambda e:errs.append(str(e)))
      P.goto(B+pg+'.html',wait_until='networkidle'); P.wait_for_timeout(400)
      P.evaluate("()=>{window.scrollTo(0,document.body.scrollHeight)}"); P.wait_for_timeout(1800); P.evaluate("()=>window.scrollTo(0,0)")
      if state=='expanded':
        P.evaluate("()=>{document.querySelectorAll('details').forEach(d=>d.open=true);const t=[...document.querySelectorAll('.wk-jack')];if(t.length)t[t.length-1].click();const r=[...document.querySelectorAll('.wk-opt input')];if(r.length){r[r.length-1].click()}}")
        P.wait_for_timeout(700)
      k=f'{pg}_{w}_{state}_{rm}'
      r={'sym':P.evaluate(M),'contrast':P.evaluate(CONTRAST),'vis':P.evaluate(VIS),'click':P.evaluate(CLICK),'errs':errs}
      if rm=='no-preference': P.screenshot(path=str(OUT/f'{pg}_{w}_{state}.png'),full_page=True)
      res[k]={a:b for a,b in r.items() if b}
      c.close()
  br.close()
json.dump(res,open(OUT/('qa_results_'+str(abs(hash(sys.argv[1] if len(sys.argv)>1 else 'all')))+'.json'),'w'),indent=1)
bad={k:v for k,v in res.items() if v}
print(len(res),'runs;',len(bad),'with findings'); print(json.dumps(bad,indent=0)[:6000])
