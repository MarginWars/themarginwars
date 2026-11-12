() => {
 const vw=document.documentElement.clientWidth, out=[];
 const vis=e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.position!=='absolute'&&cs.position!=='fixed'};
 const desc=e=>{let s=e.tagName.toLowerCase();if(e.id)s+='#'+e.id;if(e.classList.length)s+='.'+[...e.classList].slice(0,2).join('.');const p=e.parentElement;return (p&&p.tagName!=='BODY'?(p.id?'#'+p.id+' > ':(p.classList[0]?'.'+p.classList[0]+' > ':'')):'')+s};
 if(document.documentElement.scrollWidth>vw+1) out.push({type:'overflow',el:'html',n:{scrollWidth:document.documentElement.scrollWidth,clientWidth:vw}});
 // offenders for overflow
 if(document.documentElement.scrollWidth>vw+1){document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&r.right>vw+2&&getComputedStyle(e).position!=='fixed'){let a=e.parentElement,inside=false;while(a){const cs=getComputedStyle(a);if(/(hidden|auto|scroll|clip)/.test(cs.overflowX)){inside=true;break}a=a.parentElement}if(!inside&&out.filter(o=>o.type==='overflow-el').length<5)out.push({type:'overflow-el',el:desc(e),n:{right:Math.round(r.right),vw}})}})}
 document.querySelectorAll('body *').forEach(c=>{
  const cs=getComputedStyle(c); if(!/grid|flex/.test(cs.display)) return;
  if(c.closest('header,nav,footer,svg,button,summary,.hero,canvas,select,label,form')) return;
  const ch=[...c.children].filter(vis); if(ch.length<2) return;
  const sig=e=>e.tagName+'.'+(e.classList[0]||'');const sg=new Set(ch.map(sig));if(sg.size>1&&!(sg.size===2&&ch.length>=4))return;
  const cr=c.getBoundingClientRect(); if(cr.width<200) return;
  const R=ch.map(e=>({e,r:e.getBoundingClientRect()}));
  const avgW=R.reduce((a,x)=>a+x.r.width,0)/R.length; if(avgW<120) return; // inline chip/tag lists
  if(cs.display.includes('flex')&&cs.flexDirection.startsWith('column')) return;
  const rows=[];R.sort((a,b)=>a.r.top-b.r.top||a.r.left-b.r.left).forEach(x=>{const row=rows.find(r=>Math.abs(r[0].r.top-x.r.top)<=2);row?row.push(x):rows.push([x])});
  if(rows.length===rows.flat().length && rows.length>1) return; // single column stack
  const full=x=>x.r.width>=cr.width-6;
  const n0=rows[0].length; const id=desc(c);
  rows.forEach((row,i)=>{
   if(i>0&&row.length<n0&&!(row.length===1&&full(row[0]))) out.push({type:'ragged-row',el:id,n:{row:i+1,items:row.length,firstRow:n0,total:R.length}});
   if(row.length>1){const h=row.map(x=>x.r.height),w=row.map(x=>x.r.width);
    if(Math.max(...h)-Math.min(...h)>2) out.push({type:'unequal-height',el:id,n:{row:i+1,heights:h.map(Math.round)}});
    if(cs.display.includes('grid')&&Math.max(...w)-Math.min(...w)>2&&!row.some(full)) out.push({type:'unequal-width',el:id,n:{row:i+1,widths:w.map(Math.round)}});
    const g=parseFloat(cs.columnGap); if(!isNaN(g)){row.sort((a,b)=>a.r.left-b.r.left);for(let k=1;k<row.length;k++){const d=row[k].r.left-row[k-1].r.right;if(Math.abs(d-g)>2&&cs.display.includes('grid')){out.push({type:'gap-mismatch',el:id,n:{row:i+1,gap:Math.round(d),expected:g}});break}}}}
  });
 });
 // outer margins: boxed blocks (border/background/grid) vs their parent's content box
 document.querySelectorAll('main *, body > section, body > section *').forEach(e=>{if(!vis(e)||/^(P|H[1-6]|A|BLOCKQUOTE|SPAN|LI|IMG|BUTTON|SUMMARY|LABEL|INPUT|SVG|B|SMALL|EM|STRONG|TH|TD|TR|TABLE|THEAD|TBODY)$/i.test(e.tagName))return;const cs=getComputedStyle(e);const boxed=/grid|flex/.test(cs.display)||cs.backgroundColor!=='rgba(0, 0, 0, 0)'||parseFloat(cs.borderLeftWidth)>0;if(!boxed)return;const p=e.parentElement;if(!p||/grid|flex/.test(getComputedStyle(p).display))return;const pr=p.getBoundingClientRect(),pc=getComputedStyle(p);const L=pr.left+parseFloat(pc.paddingLeft)+parseFloat(pc.borderLeftWidth),Rr=pr.right-parseFloat(pc.paddingRight)-parseFloat(pc.borderRightWidth);const r=e.getBoundingClientRect();if(r.width<vw*0.5||r.width>=Rr-L-2)return;const l=r.left-L,rt=Rr-r.right;if(Math.abs(l-rt)>2&&out.filter(o=>o.type==='off-centre').length<6)out.push({type:'off-centre',el:desc(e),n:{left:Math.round(l),right:Math.round(rt)}})});
 // closed summaries equal height among siblings
 document.querySelectorAll('details').forEach(d=>{});
 const seen=new Set();return out.filter(o=>{const k=o.type+o.el+JSON.stringify(o.n);if(seen.has(k))return false;seen.add(k);return true});
}
