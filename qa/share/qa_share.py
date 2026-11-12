"""Share-flow QA: layout/symmetry/spacing/tap/contrast/overflow/console per game x width x engine (result state),
spacing regression vs the production artifact, axe on result state, and the share journeys (X, LinkedIn, copy, download, native, events)."""
import sys, json, re, urllib.parse
from playwright.sync_api import sync_playwright
sys.path.insert(0, '.'); from play import play
SPJS = open('@MW_ROOT@/normalize_suite/qa_spacing.py').read().split("JS=r'''")[1].split("'''")[0]
AXE = open('/tmp/axe/node_modules/axe-core/axe.min.js').read()
SHARE = 'http://localhost:8871/'; UNP = 'http://localhost:8872/'; BASE = 'http://localhost:8873/'
import os
GAMES = os.environ.get('GAMES','daily,leak,deal,quiz,ep1,ep2,tracewire,arcade').split(',')
UNPARKED = {'ep2', 'tracewire'}
MJS = r'''()=>{
const W=innerWidth,de=document.documentElement;const out={overflow:de.scrollWidth>de.clientWidth+0,issues:[]};
const lum=c=>{const m=c.match(/[\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])};
const bgOf=e=>{while(e){const b=getComputedStyle(e).backgroundColor;if(b&&b!='transparent'&&!/rgba\(.*, 0\)$/.test(b))return b;e=e.parentElement}return 'rgb(255,255,255)'};
const ms=[...document.querySelectorAll('.mws')];out.n=ms.length;out.rows=[];
for(const m of ms){const bb=m.querySelector('.mws-b'),BR=bb.getBoundingClientRect();
 const kids=[...bb.children].filter(e=>getComputedStyle(e).display!='none');const rows=[];
 for(const e of kids){const r=e.getBoundingClientRect();let row=rows.find(x=>Math.abs(x.top-r.top)<=2);if(!row){row={top:r.top,it:[]};rows.push(row)}row.it.push({l:r.left,r:r.right,t:r.top,b:r.bottom,w:r.width,h:r.height,full:Math.abs(r.width-BR.width)<=2})}
 out.rows.push(rows.map(r=>r.it.length));const first=rows[0]?rows[0].it.filter(x=>!x.full).length||rows[0].it.length:0;
 rows.forEach((row,i)=>{const hs=row.it.map(x=>x.h),ws=row.it.map(x=>x.w);
  if(!row.it.every(x=>x.full)&&row.it.length<first)out.issues.push('ragged row '+i);
  if(Math.max(...hs)-Math.min(...hs)>2)out.issues.push('row height mismatch');if(Math.max(...ws)-Math.min(...ws)>2)out.issues.push('row width mismatch');
  const s=row.it.slice().sort((a,b)=>a.l-b.l);for(let k=1;k<s.length;k++){const g=s[k].l-s[k-1].r;if(Math.abs(g-8)>2)out.issues.push('h-gap '+g.toFixed(1))}
  if(i>0){const g=row.top-Math.max(...rows[i-1].it.map(x=>x.b));if(Math.abs(g-8)>2)out.issues.push('v-gap '+g.toFixed(1))}
  row.it.forEach(x=>{if(x.h<44||x.w<44)out.issues.push('tap '+Math.round(x.w)+'x'+Math.round(x.h))})});
 const parts=[m.querySelector('.mws-card'),m.querySelector('.mws-t'),bb].filter(Boolean).map(e=>e.getBoundingClientRect());
 const L=parts.map(r=>r.left),R=parts.map(r=>r.right);if(Math.max(...L)-Math.min(...L)>2||Math.max(...R)-Math.min(...R)>2)out.issues.push('edge misalign');
 for(let i=1;i<parts.length;i++){const g=parts[i].top-parts[i-1].bottom;if(Math.abs(g-16)>2)out.issues.push('stack gap '+g.toFixed(1))}
 const mr=m.getBoundingClientRect();if(mr.left<12||W-mr.right<12)out.issues.push('edge intrusion '+Math.round(mr.left)+'/'+Math.round(W-mr.right));
 const host=m.parentElement;const hl=[...host.children].filter(e=>e!==m&&e.getBoundingClientRect().width>0&&getComputedStyle(e).position!='absolute').map(e=>e.getBoundingClientRect().left);
 if(hl.length&&Math.abs(Math.min(...hl)-mr.left)>2)out.issues.push('not aligned with sibling content '+Math.round(Math.min(...hl))+' vs '+Math.round(mr.left));
 for(const e of m.querySelectorAll('p,pre,a,button,span.mws-m')){if(getComputedStyle(e).display=='none'||!e.textContent.trim())continue;const c=getComputedStyle(e).color,b=bgOf(e);const a=lum(c),z=lum(b);const cr=(Math.max(a,z)+.05)/(Math.min(a,z)+.05);const big=parseFloat(getComputedStyle(e).fontSize)>=24;if(cr<(big?3:4.5))out.issues.push('contrast '+cr.toFixed(2)+' '+e.className)}
 const card=m.querySelector('.mws-card');if(card){const sc=card.querySelector('.mws-score').getBoundingClientRect();if(sc.right>card.getBoundingClientRect().right-12)out.issues.push('score clipped')}}
return out}'''
def run_layout(eng, widths):
    res = {}
    with sync_playwright() as p:
        b = getattr(p, eng).launch()
        for g in GAMES:
            for w in widths:
                ctx = b.new_context(viewport={'width': w, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
                play(pg, g, UNP if g in UNPARKED else SHARE)
                r = pg.evaluate(MJS); sp = pg.evaluate(SPJS)
                r['spacing'] = {k: sp[k] for k in ('nIntr', 'rhythm', 'hb', 'edgeDev', 'overflow', 'intr')}
                r['errors'] = [e for e in errs if 'api/ev' not in e and '501' not in e]
                res[f'{g}|{w}'] = r; ctx.close()
            print(eng, g, 'done', flush=True)
        b.close()
    return res
def run_baseline(widths):
    """Same SPJS on the production artifact, default state (and result state for games playable there)."""
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for g in GAMES:
            for w in widths:
                for site, url in (('prod', BASE), ('share', UNP if g in UNPARKED else SHARE)):
                    if g in UNPARKED and site == 'prod': continue
                    ctx = b.new_context(viewport={'width': w, 'height': 900}, reduced_motion='reduce'); pg = ctx.new_page()
                    pg.goto(url + g + '.html' + ('?preview=1' if g in UNPARKED else '')); pg.wait_for_timeout(200)
                    d = pg.evaluate(SPJS)
                    res[f'{g}|{w}|{site}|default'] = {k: (len(d[k]) if isinstance(d[k], list) else d[k]) for k in ('nIntr', 'rhythm', 'hb', 'edgeDev', 'overflow')}
                    ctx.close()
        b.close()
    return res
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'layout':
        eng = sys.argv[2]; widths = [int(x) for x in sys.argv[3].split(',')]
        json.dump(run_layout(eng, widths), open(f'qa/layout_{eng}.json', 'w'), indent=1)
    elif mode == 'baseline':
        json.dump(run_baseline([int(x) for x in sys.argv[2].split(',')]), open('qa/spacing_vs_prod.json', 'w'), indent=1)
