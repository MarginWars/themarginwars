"""Accent census: computed accent colours per route (default state, 1440). Usage: qa_accents.py OUT.json [width]"""
import json,sys,os
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).parent;routes=json.loads((H/'routes.json').read_text())
W=int(sys.argv[2]) if len(sys.argv)>2 else 1440
BASE=os.environ.get('QA_BASE','http://localhost:8817/')
JS=r'''()=>{
const P={sky:[143,176,224],mint:[63,191,133],gold:[210,166,58],coral:[234,98,89],magenta:[181,35,127],grey:[183,193,201],violet:[160,143,230]};
const parse=s=>{const out=[];const re=/rgba?\(([^)]+)\)/g;let m;while(m=re.exec(s)){const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);if(p.length>=3&&(p[3]===undefined||p[3]>0.05))out.push(p)}return out};
const near=(c)=>{for(const k in P){const q=P[k];if(Math.abs(c[0]-q[0])<=6&&Math.abs(c[1]-q[1])<=6&&Math.abs(c[2]-q[2])<=6)return k}const mx=Math.max(c[0],c[1],c[2]),mn=Math.min(c[0],c[1],c[2]);return (mx-mn>60)?'other:'+c.slice(0,3).join(','):null};
const hits=[];const vis=e=>{const r=e.getBoundingClientRect();if(r.width==0&&r.height==0)return false;const s=getComputedStyle(e);return s.visibility!='hidden'&&s.display!='none'};
const nm=e=>e.tagName.toLowerCase()+(e.classList.length?'.'+[...e.classList].filter(c=>c!='nm-inline').slice(0,2).join('.'):'');
for(const e of document.querySelectorAll('body *')){if(!vis(e)||e.closest('dialog:not([open]),[hidden],script,style,noscript,template'))continue;
 for(const pe of [null,'::before','::after']){const s=getComputedStyle(e,pe);if(pe&&(s.content=='none'||s.content=='normal'||s.display=='none'))continue;
  const props=[];const txt=!pe&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())||pe&&s.content.replace(/["']/g,'').trim();
  if(txt)props.push(['text',s.color]);props.push(['bg',s.backgroundColor]);if(s.backgroundImage!='none')props.push(['bgimg',s.backgroundImage]);
  for(const side of ['Top','Right','Bottom','Left'])if(parseFloat(s['border'+side+'Width'])>0&&s['border'+side+'Style']!='none')props.push(['border',s['border'+side+'Color']]);
  if(s.outlineStyle!='none'&&parseFloat(s.outlineWidth)>0)props.push(['outline',s.outlineColor]);
  if(s.boxShadow!='none')props.push(['shadow',s.boxShadow]);
  if(txt&&s.textDecorationLine.includes('underline'))props.push(['underline',s.textDecorationColor]);
  if(e instanceof SVGElement){props.push(['fill',s.fill]);props.push(['stroke',s.stroke])}
  const seen=new Set();for(const [p,v] of props)for(const c of parse(v)){const k=near(c);if(!k)continue;const key=k+p;if(seen.has(key))continue;seen.add(key);hits.push({acc:k,prop:p,el:nm(e)+(pe||'')})}}}
return {body:document.body.className,hits}}'''
res={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 c=b.new_context(viewport={'width':W,'height':900},reduced_motion='reduce');P=c.new_page()
 for r in routes:
  P.goto(BASE+r['file'],wait_until='networkidle');P.wait_for_timeout(100)
  res[r['file']]={'family':r['family'],**P.evaluate(JS)}
 b.close()
Path(sys.argv[1]).write_text(json.dumps(res,indent=0))
print('ok',len(res))
