"""Cross-engine / device QA matrix.
Usage: qa_matrix.py ENGINE PROFILESET PART PARTS  -> $QA_OUT/matrix_ENGINE_PROFILESET_PART.json
ENGINE: chromium | webkit | firefox.  PROFILESET: core (375/390/768/1440 widths, all routes) | devices (named devices + surfaces, key templates)
Per case: spacing (same JS as qa_spacing), symmetry, contrast, tap targets, console/page errors, overflow; closed and open states.
Screenshots (DPR 1, viewport-height crops of the first screen + full page) feed qa_diff.py."""
import json,sys,os,re
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).parent;OUT=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/polish_1110/qa')));OUT.mkdir(parents=True,exist_ok=True)
SHOTS=OUT/'shots';SHOTS.mkdir(exist_ok=True)
BASE=os.environ.get('QA_BASE','http://localhost:8817/')
ns={};src=(H/'qa_spacing.py').read_text();SPJS=src.split("JS=r'''")[1].split("'''")[0]
ns2={'__file__':str(H.parent/'site_qa/about_full_1108/qa.py')};exec((H.parent/'site_qa/about_full_1108/qa.py').read_text().split('res={}')[0],ns2)
M=ns2['M'];CON=ns2['CONTRAST']
TARGET=(H/'qa_suite.py').read_text().split("TARGET=r'''")[1].split("'''")[0]
eng,pset,part,parts=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
routes=json.loads((H/'routes.json').read_text())
KEY=['index.html','about.html','advisory.html','speaking.html','contact.html','writing.html','warroom.html','arcade.html','daily.html','ep1.html','calendar/index.html','wire/items/uk-fee-transparency/index.html']
def profiles(p):
  if pset=='core':return [('w375',{'viewport':{'width':375,'height':812}}),('w390',{'viewport':{'width':390,'height':844}}),('w768',{'viewport':{'width':768,'height':1024}}),('w1440',{'viewport':{'width':1440,'height':900}})]
  D=p.devices;mob=lambda n:{k:v for k,v in D[n].items() if not (eng=='firefox' and k=='is_mobile')}
  out=[('iPhoneSE',mob('iPhone SE (3rd gen)')),('iPhone15',mob('iPhone 15')),('iPhone15ProMax',mob('iPhone 15 Pro Max')),('Pixel7',mob('Pixel 7')),('GalaxyS',mob('Galaxy S24') if 'Galaxy S24' in D else mob('Galaxy S9+')),
   ('iPadMini',mob('iPad Mini')),('iPadMiniL',mob('iPad Mini landscape')),('iPadPro',mob('iPad Pro 11')),('iPadProL',mob('iPad Pro 11 landscape')),
   ('phoneL844',{'viewport':{'width':844,'height':390},'has_touch':eng!='firefox'}),('d1280',{'viewport':{'width':1280,'height':800}}),('d1920',{'viewport':{'width':1920,'height':1080}}),('d2560',{'viewport':{'width':2560,'height':1440}}),
   ('dark390',{'viewport':{'width':390,'height':844},'color_scheme':'dark'}),('dark1440',{'viewport':{'width':1440,'height':900},'color_scheme':'dark'}),
   ('reduced390',{'viewport':{'width':390,'height':844},'reduced_motion':'reduce'}),('forced1440',{'viewport':{'width':1440,'height':900},'forced_colors':'active'}),
   ('zoom200',{'viewport':{'width':720,'height':450},'device_scale_factor':2})]
  return out
sel=routes if pset=='core' else [r for r in routes if r['file'] in KEY]
sel=sel[part::parts]
if os.environ.get('QA_ONLY'):sel=[r for r in routes if r['file'] in os.environ['QA_ONLY'].split(',')]
res={}
with sync_playwright() as p:
 if eng=='chromium':b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 else:b=getattr(p,eng).launch()
 for name,prof in profiles(p):
  prof=dict(prof)
  if eng=='firefox':prof.pop('is_mobile',None)
  if pset=='core':prof.update(device_scale_factor=1,reduced_motion='reduce')
  for r in sel:
   f=r['file'];c=b.new_context(**prof);P=c.new_page();errs=[]
   P.on('pageerror',lambda e:errs.append('pageerror: '+str(e)[:160]));P.on('console',lambda m:errs.append('console: '+m.text[:160]) if m.type=='error' else None)
   try:
    P.goto(BASE+f,wait_until='networkidle',timeout=45000)
   except Exception as e:errs.append('goto: '+str(e)[:120])
   P.evaluate("async()=>{const h=document.body.scrollHeight;for(let y=0;y<h;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,25))}scrollTo({top:0,behavior:'instant'})}");P.wait_for_timeout(250)
   if name=='zoom200':P.evaluate("document.documentElement.style.fontSize='200%'");P.wait_for_timeout(150)
   base=f.replace('/','_').replace('.html','')
   for state in ('default','expanded'):
    if state=='expanded':
     P.evaluate("""()=>{document.querySelectorAll('details').forEach(d=>d.open=true);document.querySelectorAll('[data-fx-tools],.fx-prefs').forEach(d=>d.hidden=false);let j=document.querySelectorAll('.wk-jack');if(j.length)j[j.length-1].click()}""");P.wait_for_timeout(120)
    k=f'{f}|{name}|{state}'
    try:
     sp=P.evaluate(SPJS) if not name.startswith('zoom') else {}
     r2={'sym':P.evaluate(M),'contrast':P.evaluate(CON),'targets':P.evaluate(TARGET),'overflow':P.evaluate('document.documentElement.scrollWidth>innerWidth+1')}
    except Exception as e:sp={};r2={'evalerr':str(e)[:200]}
    if sp and pset=='core':r2['spacing']={x:sp[x] for x in ('edgeDev','nIntr','rhythm','hb','overflow') if sp.get(x)}
    elif sp:r2['spacing_info']={x:sp[x] for x in ('edgeDev','nIntr') if sp.get(x)}
    if errs:r2['errors']=list(dict.fromkeys(errs))
    res[k]={a:v for a,v in r2.items() if v}
    if state=='default':
     try:P.screenshot(path=str(SHOTS/f'{eng}_{name}_{base}.png'),full_page=(pset=='core'))
     except Exception as e:res[k]['shoterr']=str(e)[:100]
   c.close()
  print('DONE',eng,name,flush=True)
 b.close()
(OUT/f'matrix_{eng}_{pset}_{part}.json').write_text(json.dumps(res,indent=0))
print('FINISHED',eng,pset,part,len(res),sum(bool(v) for v in res.values()),flush=True)
