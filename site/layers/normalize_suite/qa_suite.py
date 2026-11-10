import os
from pathlib import Path
import sys,json,re
from playwright.sync_api import sync_playwright
H=Path(__file__).parent;OUT=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/suite_1108')));OUT.mkdir(exist_ok=True)
routes=json.loads((H/'routes.json').read_text())
# Existing geometry/contrast helpers, shared with prior QA.
ns={'__file__':str(H.parent/'site_qa/about_full_1108/qa.py')};exec((H.parent/'site_qa/about_full_1108/qa.py').read_text().split('res={}')[0],ns)
M=ns['M'];CON=ns['CONTRAST']
TARGET=r'''()=>{let a=[];for(const e of document.querySelectorAll('a[href],button,summary,input,select,[role=button]')){let r=e.getBoundingClientRect();if(!r.width||!r.height||e.closest('[hidden],[aria-disabled=true]')||e.disabled||r.top<0)continue;let s=getComputedStyle(e);if(s.visibility==='hidden'||+s.opacity===0)continue;if(e.matches('input[type=checkbox],input[type=radio]')){let l=e.closest('label')||document.querySelector('label[for="'+e.id+'"]');if(l){r=l.getBoundingClientRect()}}if(r.width<43.9||r.height<43.9)a.push({el:e.tagName+'.'+e.className,t:(e.textContent||e.getAttribute('aria-label')||e.name||'').trim().slice(0,35),w:Math.round(r.width),h:Math.round(r.height)})}return a}'''
part=int(sys.argv[1]) if len(sys.argv)>1 else 0;parts=int(sys.argv[2]) if len(sys.argv)>2 else 1
if len(sys.argv)>3:routes=[r for r in routes if r['file'] in sys.argv[3].split(',')]
else:routes=routes[part::parts]
res={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for route in routes:
  f=route['file'];base=f.replace('/','_').replace('.html','')
  for w in (375,768,1280,1440):
   c=b.new_context(viewport={'width':w,'height':900},reduced_motion='reduce');P=c.new_page();errors=[];P.on('pageerror',lambda e:errors.append(str(e)))
   P.goto('http://localhost:8817/'+f,wait_until='networkidle');P.evaluate('window.scrollTo(0,document.body.scrollHeight)');P.wait_for_timeout(180);P.evaluate('window.scrollTo(0,0)')
   for state in ('default','expanded'):
    if state=='expanded':
     P.evaluate("""()=>{document.querySelectorAll('details').forEach(d=>d.open=true);document.querySelectorAll('[data-fx-tools],.fx-prefs').forEach(d=>d.hidden=false);let j=document.querySelectorAll('.wk-jack');if(j.length)j[j.length-1].click()}""")
     P.wait_for_timeout(80)
    k=f'{f}|{w}|{state}';r={'sym':P.evaluate(M),'contrast':P.evaluate(CON),'targets':P.evaluate(TARGET),'errors':errors,'overflow':P.evaluate('document.documentElement.scrollWidth>innerWidth')}
    res[k]={a:v for a,v in r.items() if v};P.screenshot(path=str(OUT/f'{base}_{w}_{state}.png'),full_page=True)
   c.close()
  print('DONE',part,f,flush=True)
 b.close()
(OUT/f'results_{part}.json').write_text(json.dumps(res,indent=1));print('FINISHED',part,len(res),sum(bool(v) for v in res.values()),flush=True)
