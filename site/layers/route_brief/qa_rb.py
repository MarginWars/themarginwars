import os
import json,sys
from playwright.sync_api import sync_playwright
OUT='@MW_ROOT@/site_qa/route_brief_1108_proof/'
W=[375,768,1024,1280,1440]
ST=[('anz','card'),('anz','instant'),('anz','bank'),('us','bank'),('us','card'),('ukeu','card'),('br','instant'),('br','card')]
SYM='''()=>{const r=document.querySelector('.rbf');const f=[];const vis=e=>e.offsetParent!==null;
for(const sel of ['.rb-pick','.rb-opts','.rb-hd','.rb-brief:not([hidden]) .rb-path','.rb-brief:not([hidden]) .rb-cols','.rb-brief:not([hidden]) .rb-foot','.tm-lanes']){
 for(const c of r.querySelectorAll(sel)){if(!vis(c))continue;const k=[...c.children].filter(vis).filter(e=>!e.classList.contains('rb-arrow')&&e.tagName!=='LEGEND');
  const rows={};k.forEach(e=>{const b=e.getBoundingClientRect();const t=Math.round(b.top/3);(rows[t]=rows[t]||[]).push(b)});
  const rs=Object.values(rows);const n0=rs[0]?rs[0].length:0;const cr=c.getBoundingClientRect();
  rs.forEach((row,i)=>{if(row.length<n0&&!(row.length==1&&Math.abs(row[0].width-cr.width)<3))f.push(sel+' ragged row '+i);
   const h=row.map(b=>b.height),w=row.map(b=>b.width);if(Math.max(...h)-Math.min(...h)>2)f.push(sel+' height diff '+h.join('/'));
   if(row.length>1&&Math.max(...w)-Math.min(...w)>2)f.push(sel+' width diff '+w.join('/'))});}}
const b=r.getBoundingClientRect();if(document.documentElement.scrollWidth>document.documentElement.clientWidth+1)f.push('page overflow');
for(const e of r.querySelectorAll('*')){if(vis(e)&&!e.classList.contains('vh')&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')f.push('overflow '+e.className)}
const inr=r.querySelector('.rb-in').getBoundingClientRect();if(Math.abs((inr.left-b.left)-(b.right-inr.right))>2)f.push('margins');
return f}'''
res={}
with sync_playwright() as p:
 br=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for page in ['index','advisory']:
  for w in W:
   pg=br.new_page(viewport={'width':w,'height':900});pg.goto(f'http://127.0.0.1:18793/{page}.html');pg.wait_for_timeout(600)
   pg.evaluate("document.fonts.ready")
   for m,me in ST:
    pg.evaluate(f"rbSet('{m}','{me}')");pg.locator('.rbf').scroll_into_view_if_needed();pg.evaluate("document.querySelector('.rbf').classList.add('rv-in')");pg.wait_for_timeout(700)
    st=pg.evaluate("document.querySelector('.rbf').getAttribute('data-state')")
    f=pg.evaluate(SYM);res[f'{page}_{w}_{m}-{me}']={'state':st,'fails':f}
    pg.add_style_tag(content='header,.site-head,nav[aria-label],[class*=progress]{visibility:hidden!important}');pg.locator('.rbf').screenshot(path=f'{OUT}{page}_{w}_{m}-{me}.png')
   pg.locator('.tmap').scroll_into_view_if_needed();pg.wait_for_timeout(1500)
   tf=pg.evaluate('''()=>{const c=document.querySelector('.tmap .wk-jacks')||document.querySelector('.tm-lanes');const cw=c.getBoundingClientRect().width;const f=[];const k=[...c.children];const rows={};k.forEach(e=>{const b=e.getBoundingClientRect();const t=Math.round(b.top/3);(rows[t]=rows[t]||[]).push(b)});const rs=Object.values(rows);rs.forEach((row,i)=>{if(row.length<rs[0].length&&!(row.length==1&&row[0].width>cw-20))f.push('lane ragged row '+i);const h=row.map(b=>b.height);if(Math.max(...h)-Math.min(...h)>2)f.push('lane h '+h.map(Math.round).join('/'))});if(document.documentElement.scrollWidth>document.documentElement.clientWidth+1)f.push('overflow');return [k.length,rs.map(r=>r.length),f]}''')
   res[f'{page}_{w}_terrain']={'fails':tf[2],'lanes':tf[0],'rows':tf[1]}
   pg.locator('.tmap').screenshot(path=f'{OUT}{page}_{w}_terrain.png')
   pg.close()
 # keyboard
 pg=br.new_page(viewport={'width':1280,'height':900});pg.goto('http://127.0.0.1:18793/index.html');pg.wait_for_timeout(500)
 pg.focus('input[name=rb-m][value=us]');pg.keyboard.press('ArrowRight');pg.wait_for_timeout(100)
 k1=pg.evaluate("[document.activeElement.value,document.querySelector('.rbf').dataset.state]")
 pg.keyboard.press('ArrowRight');pg.keyboard.press('Tab');pg.wait_for_timeout(100)
 k2=pg.evaluate("[document.activeElement.name,document.activeElement.value,document.querySelector('.rbf').dataset.state]")
 fonts=pg.evaluate("[document.fonts.check('16px \"Schibsted Grotesk\"'),document.fonts.check('12px \"Martian Mono\"')]")
 errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
 reqs=[];pg.on('request',lambda r:reqs.append(r.url))
 pg.reload();pg.wait_for_timeout(800);pg.evaluate("rbSet('us','card')")
 res['keyboard']={'after_arrow':k1,'after_tab':k2,'fonts':fonts,'jserrors':errs,'rb_requests':[u for u in reqs if 'rb' in u]}
 # reduced motion
 pg2=br.new_page(viewport={'width':1280,'height':900},reduced_motion='reduce');pg2.goto('http://127.0.0.1:18793/index.html');pg2.wait_for_timeout(500)
 res['reduced_anim']=pg2.evaluate("getComputedStyle(document.querySelector('.rb-arrow'),'::before').animationName")
 # nojs
 for w in [375,1280]:
  c=br.new_context(java_script_enabled=False,viewport={'width':w,'height':900});q=c.new_page();q.goto('http://127.0.0.1:18793/index.html')
  res[f'nojs_{w}']=q.evaluate("[document.querySelector('.rb-pick').hidden,[...document.querySelectorAll('.rb-brief')].filter(a=>a.offsetParent).length, document.querySelectorAll('.tmap .tm-lane').length]")
  q.locator('.rbf').screenshot(path=f'{OUT}nojs_index_{w}.png');c.close()
 # switchboard still below
 res['switch_below']=pg.evaluate("document.querySelector('.rbf').compareDocumentPosition(document.querySelector('.tmap'))&4?true:false")
 br.close()
json.dump(res,open(OUT+'qa_rb.json','w'),indent=1)
bad={k:v for k,v in res.items() if isinstance(v,dict) and v.get('fails')}
print(json.dumps(bad,indent=1)[:3000]);print({k:v for k,v in res.items() if not k.startswith(('index_','advisory_'))})
