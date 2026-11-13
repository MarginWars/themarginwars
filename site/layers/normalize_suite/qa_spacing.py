"""Spacing gate: shared edge, section rhythm, heading->body gap, edge intrusion, gutter evenness.
Usage: qa_spacing.py PART PARTS [files]  -> $QA_OUT/spacing_PART.json"""
import json,sys,os
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).parent;OUT=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/prod_1109/qa')));OUT.mkdir(parents=True,exist_ok=True)
routes=json.loads((H/'routes.json').read_text());part=int(sys.argv[1]);parts=int(sys.argv[2])
routes=[r for r in routes if r['file'] in sys.argv[3].split(',')] if len(sys.argv)>3 else routes[part::parts]
WIDTHS=[int(x) for x in os.environ.get('SP_WIDTHS','320,375,390,430,768,1024,1280,1440,1920').split(',')]
JS=r'''()=>{
const W=innerWidth;const E=W<=330?16:W<768?16:W<1280?24:W<1440?104:W<1920?184:(W-1072)/2;
const R=W<768?64:W<1280?96:120;const HB=W<768?16:24;
const vis=e=>{const s=getComputedStyle(e);if(s.visibility=='hidden'||s.display=='none'||+s.opacity==0)return false;if(s.position=='absolute'&&s.clip!='auto'&&e.getBoundingClientRect().width<=1)return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
const inScroller=e=>{let x=e;while(x=x.parentElement){if(x===document.body)return false;const o=getComputedStyle(x).overflowX;if(o=='auto'||o=='scroll'||o=='hidden'&&x.scrollWidth>x.clientWidth+1)return true}return false};
const skip='[aria-hidden=true],svg,.vh,.sr-only,.skip,.f-skip,dialog:not([open]),[hidden],noscript';
const content=[...document.querySelectorAll('body *')].filter(e=>!e.closest(skip)&&(e.matches('img,video,iframe,button,input,select,textarea')||[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim().length>1))&&vis(e)&&getComputedStyle(e).position!='fixed');
const intr=[];let minL=1e9,minR=1e9;
for(const e of content){if(inScroller(e))continue;const r=e.getBoundingClientRect();if(e.matches('img,video,iframe')&&r.width>=W-1)continue;
 const L=r.left,Rr=W-r.right;minL=Math.min(minL,L);minR=Math.min(minR,Rr);
 if(L<E-2||Rr<E-2)intr.push({el:e.tagName+'.'+[...e.classList].slice(0,2).join('.'),t:(e.textContent||'').trim().slice(0,30),L:Math.round(L),R:Math.round(Rr)})}
// rhythm: consecutive section-level blocks; same surface => R between content, surface change => R each side
const bgOf=e=>{let x=e;while(x&&x!==document.documentElement){const b=getComputedStyle(x).backgroundColor;if(b!='rgba(0, 0, 0, 0)'&&b!='transparent')return b;x=x.parentElement}return 'rgb(255, 255, 255)'};
const own=e=>{const b=getComputedStyle(e).backgroundColor;return b!='rgba(0, 0, 0, 0)'&&b!='transparent'};
const main=document.querySelector('main');const blocks=[];
if(main)for(const c of main.children){if(!vis(c)||c.matches('nav,script,style,dialog,.nextp'))continue;
 if(c.matches('.wrap')){let lead=null;const n0=blocks.length;for(const k of c.children){if(!vis(k)||k.matches('script,style'))continue;if(k.matches('section,div')){blocks.push({el:k,wrap:c,lead});lead=null}else if(blocks.length>n0)blocks[blocks.length-1].tail=k;else lead=k}}
 else if(c.matches('.ab-band')){const f=c.querySelector(':scope>.ab-flow');blocks.push({el:f||c,band:c})}
 else blocks.push({el:c})}
const card=e=>{const c=getComputedStyle(e);return e.getBoundingClientRect().width<W-1&&(own(e)&&c.backgroundColor!==bgOf(e.parentElement)||['Top','Right','Bottom','Left'].every(s=>parseFloat(c['border'+s+'Width'])>0))};
const box=b=>{if(card(b.el)){const r=b.el.getBoundingClientRect();let t=r.top,bt=r.bottom;if(b.lead)t=Math.min(t,b.lead.getBoundingClientRect().top);if(b.tail)bt=Math.max(bt,b.tail.getBoundingClientRect().bottom);return {t,b:bt}}const kids=[...b.el.children].filter(k=>vis(k)&&!k.matches('script,style')&&getComputedStyle(k).position!='absolute');if(b.tail)kids.push(b.tail);if(b.lead)kids.push(b.lead);if(!kids.length)return null;return {t:Math.min(...kids.map(k=>k.getBoundingClientRect().top)),b:Math.max(...kids.map(k=>k.getBoundingClientRect().bottom))}};
const rhythm=[];const nm=e=>e.tagName+'.'+[...e.classList].slice(0,2).join('.');
const bw=(e,s)=>e&&!card(e)?parseFloat(getComputedStyle(e)['border'+s+'Width'])||0:0;
for(let i=0;i+1<blocks.length;i++){const A=blocks[i],B=blocks[i+1];const a=box(A),bb=box(B);if(!a||!bb)continue;a.b+=bw(A.el,'Bottom');bb.t-=bw(B.band||B.el,'Top');
 const sOf=x=>{let e=x.band||x.el;while(e&&e!==document.body&&!(own(e)&&e.getBoundingClientRect().width>=W-1))e=e.parentElement;return bgOf(e||document.body)};const sa=sOf(A),sb=sOf(B);if(bb.t<a.b-2)continue;const fp=document.body.classList.contains('f-page');if(fp){const C=W<768?24:32;const ps=(e,s)=>!card(e)&&parseFloat(getComputedStyle(e)['border'+s+'Width'])>0&&parseFloat(getComputedStyle(e)['padding'+s])>0;const want=(A.el.matches('.fx-itemhero'))?HB:C+(ps(B.el,'Top')?C:0)+(ps(A.el,'Bottom')?C:0);const g=bb.t-a.b;if(Math.abs(g-want)>2)rhythm.push({sec:nm(A.el)+'→'+nm(B.el),side:'component',v:Math.round(g),want});continue}
 if(sa==sb){const g=bb.t-a.b;if(Math.abs(g-R)>2)rhythm.push({sec:nm(A.el)+'→'+nm(B.el),side:'between',v:Math.round(g),want:R})}
 else{const Bs=B.band||B.el,As=A.band||A.el;const full=e=>e.getBoundingClientRect().width>=W-1;const edge=own(Bs)&&full(Bs)?Bs.getBoundingClientRect().top:As.getBoundingClientRect().bottom;
  const g1=edge-a.b,g2=bb.t-edge;
  if(i>0&&Math.abs(g1-R)>2)rhythm.push({sec:nm(A.el)+'→'+nm(B.el),side:'before-surface',v:Math.round(g1),want:R});
  if(Math.abs(g2-R)>2)rhythm.push({sec:nm(A.el)+'→'+nm(B.el),side:'after-surface',v:Math.round(g2),want:R})}}
const hb=[];for(const h of document.querySelectorAll('main h2,body>section h2')){if(!vis(h)||h.closest(skip)||h.closest('article,li,details,.card,.f-entry,.pc,figure,form,.gm,dialog,table,.rt-hero'))continue;let n=h.nextElementSibling;if(!n||!n.matches('p'))continue;if(!vis(n))continue;if(n.getBoundingClientRect().left>=h.getBoundingClientRect().right-1||n.getBoundingClientRect().top<h.getBoundingClientRect().top+2)continue;const g=n.getBoundingClientRect().top-h.getBoundingClientRect().bottom;if(Math.abs(g-HB)>2)hb.push({h:h.textContent.trim().slice(0,30),gap:Math.round(g),want:HB})}
const TO=(__TO_JS__);
return {E,R,HB,minL:Math.round(minL),minR:Math.round(minR),edgeDev:Math.abs(minL-E)>2||Math.abs(minR-E)>2,lr:Math.round(minL-minR),intr:intr.slice(0,15),nIntr:intr.length,rhythm,hb,overflow:document.documentElement.scrollWidth>innerWidth,textOverflow:TO.issues,nTextOverflow:TO.n}}'''
# Shared text-overflow check is injected below at runtime

# Inject the shared text-overflow check into the in-page probe.
JS=JS.replace('const TO=(__TO_JS__);','const TO=('+(H/'text_overflow_check.js').read_text().strip()+')();')
res={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for r in routes:
  for w in WIDTHS:
   c=b.new_context(viewport={'width':w,'height':900},reduced_motion='reduce');P=c.new_page()
   P.goto('http://localhost:8817/'+r['file'],wait_until='networkidle');P.evaluate('window.scrollTo(0,document.body.scrollHeight)');P.wait_for_timeout(120);P.evaluate('scrollTo(0,0)')
   res[f"{r['file']}|{w}"]=P.evaluate(JS);c.close()
  print('DONE',r['file'],flush=True)
(OUT/f'spacing_{part}.json').write_text(json.dumps(res,indent=1))
