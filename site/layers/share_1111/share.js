/* The Margin Wars: game share flow. Opens the networks' own share pages (x.com/intent/post, linkedin share-offsite);
   no third-party scripts, nothing is posted for the player. Spoiler-free: only scores, grids and dates are shared. */
(function(){
"use strict";
var SITE='https://themarginwars.com/',
    HIT=['\uD83D\uDFE6','\uD83D\uDFEA','\uD83D\uDFE9','\uD83D\uDFE8','\uD83D\uDFE5'],MISS='\u2B1C',
    HEX=['#8FB0E0','#A08FE6','#3FBF85','#D2A63A','#EA6259'],BAND=['#8FB0E0','#A08FE6','#3FBF85','#B7C1C9','#D2A63A','#EA6259'];
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function grid(m){return m.map(function(x,i){return x?HIT[i%HIT.length]:MISS}).join('')}
function gridHTML(m){var n=m.filter(Boolean).length;return '<span class="mws-grid" role="img" aria-label="'+n+' of '+m.length+' correct">'+m.map(function(x,i){return '<i'+(x?' style="background:'+HEX[i%HEX.length]+'"':' class="m0"')+'></i>'}).join('')+'</span>'}
function url(game,src){var p=game==='arcade'?'arcade':game;return SITE+p+'?utm_source='+src+'&utm_medium=social&utm_campaign=game-share&utm_content='+game}
/* X weighted length (twitter-text v3): URLs 23, emoji 2, CJK etc. 2, everything else 1 */
function xlen(t){var n=0;t=t.replace(/https?:\/\/\S+/g,function(){n+=23;return ''});
  var seg=[];try{seg=Array.from(new Intl.Segmenter('en',{granularity:'grapheme'}).segment(t),function(s){return s.segment})}catch(e){seg=Array.from(t)}
  seg.forEach(function(g){var c=g.codePointAt(0);if(/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|[\u2B1B\u2B1C]/u.test(g))n+=2;else if(c<=4351||(c>=8192&&c<=8205)||(c>=8208&&c<=8223)||(c>=8242&&c<=8247))n+=1;else n+=2});return n}
function xText(text,game){var u=url(game,'x'),lines=String(text).split('\n'),t;
  do{t=lines.join('\n')+'\n\n'+u;if(xlen(t)<=280)break;lines.splice(lines.length>1?lines.length-1:0,1)}while(lines.length);return t}
function xHref(text,game){return 'https://x.com/intent/post?text='+encodeURIComponent(xText(text,game))}
function liHref(game){return 'https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(url(game,'linkedin'))}
function ev(n){try{if(window.TMW_EV)window.TMW_EV(n)}catch(e){}}
function copy(t){var ok=false,a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;top:0;left:0;opacity:0;pointer-events:none';document.body.appendChild(a);a.select();
  try{ok=document.execCommand('copy')}catch(e){}document.body.removeChild(a);
  if(ok)return Promise.resolve();return navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()}
var native=function(){return !!(navigator.share&&window.matchMedia&&matchMedia('(pointer:coarse)').matches)};
/* o: {game, label, meta, score, marks, sub, text, card:{h,s}, hub} */
function box(o){
  var g=o.game,t=o.text;
  var card=o.hub?'':'<div class="mws-card"><span class="mws-band" aria-hidden="true">'+BAND.map(function(c){return '<i style="background:'+c+'"></i>'}).join('')+'</span>'+
    '<p class="mws-k"><span class="mws-m" aria-hidden="true">M</span>The Margin Wars · '+esc(o.label)+'</p>'+(o.meta?'<p class="mws-meta">'+esc(o.meta)+'</p>':'')+
    '<p class="mws-score">'+esc(o.score)+'</p>'+(o.marks?gridHTML(o.marks):'')+(o.sub?'<p class="mws-sub">'+esc(o.sub)+'</p>':'')+'</div>';
  var d=' data-g="'+esc(g)+'" data-t="'+esc(t)+'"';
  return '<div class="mws'+(o.hub?' mws-hubb':'')+'"'+d+(o.card?' data-h="'+esc(o.card.h)+'" data-s="'+esc(o.card.s)+'"':'')+'>'+card+
    (o.hub?'':'<pre class="mws-t" aria-label="Share text">'+esc(t)+'</pre>')+
    '<div class="mws-b'+(o.hub?' n3':'')+'"><button type="button" class="btn mws-nat" data-s="native" hidden>Share…</button>'+
    '<a class="btn mws-x" data-s="x" target="_blank" rel="noopener" href="'+esc(xHref(t,g))+'">Share on X</a>'+
    '<a class="btn mws-li" data-s="linkedin" target="_blank" rel="noopener" href="'+esc(liHref(g))+'">Share on LinkedIn</a>'+
    '<button type="button" class="btn alt mws-cp" data-s="copy">'+(o.hub?'Copy link':'Copy result')+'</button>'+
    (o.hub?'':'<button type="button" class="btn alt mws-dl" data-s="card">Download card</button>')+
    '</div><p class="mws-n" role="status" aria-live="polite"></p></div>';
}
function wireNative(r){[].forEach.call((r||document).querySelectorAll('.mws-nat'),function(b){if(native()){b.hidden=false;b.closest('.mws-b').classList.add('has-nat')}})}
function canvas(h,s,meta){var c=document.createElement('canvas'),W=1200,H=630;c.width=W;c.height=H;var x=c.getContext('2d');
  x.fillStyle='#F4F6F7';x.fillRect(0,0,W,H);BAND.forEach(function(b,i){x.fillStyle=b;x.fillRect(Math.round(i*W/6),0,Math.ceil(W/6),14)});
  x.fillStyle='#111417';x.fillRect(80,96,96,96);BAND.forEach(function(b,i){x.fillStyle=b;x.fillRect(92,108+i*12,8,12)});
  x.fillStyle='#F4F6F7';x.font='700 58px "Schibsted Grotesk",system-ui,sans-serif';x.fillText('M',110,166);
  x.fillStyle='#111417';x.font='700 30px "Schibsted Grotesk",system-ui,sans-serif';x.fillText('The Margin Wars',204,140);
  x.fillStyle='#5B656B';x.font='500 22px "Martian Mono",ui-monospace,monospace';x.fillText(meta||'',204,178);
  x.fillStyle='#111417';x.font='700 54px "Schibsted Grotesk",system-ui,sans-serif';var y=wrap(x,h,80,300,1040,64);
  x.fillStyle='#39434A';x.font='400 30px "Schibsted Grotesk",system-ui,sans-serif';wrap(x,s,80,y+56,1040,40);
  x.fillStyle='#B5237F';x.fillRect(80,530,6,40);x.fillStyle='#5B656B';x.font='500 22px "Martian Mono",ui-monospace,monospace';x.fillText('themarginwars.com',104,558);
  return c.toDataURL('image/png')}
function wrap(x,t,X,Y,W,L){var w=String(t).split(' '),l='';for(var i=0;i<w.length;i++){var s=l+w[i]+' ';if(x.measureText(s).width>W&&l){x.fillText(l.trim(),X,Y);l=w[i]+' ';Y+=L}else l=s}x.fillText(l.trim(),X,Y);return Y}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.mws [data-s]');if(!b)return;
  var w=b.closest('.mws'),g=w.dataset.g,t=w.dataset.t,s=b.dataset.s,m=w.querySelector('.mws-n');
  ev('share_'+s);
  if(s==='x')return; /* link opens x.com/intent/post */
  if(s==='linkedin'){copy(t).then(function(){m.textContent='Text copied, paste it into your post.'},function(){m.textContent='LinkedIn opened. Copy the text above into your post.'});return}
  if(s==='copy'){copy(w.classList.contains('mws-hubb')?t+'\n'+url(g,'copy'):t+'\n'+url(g,'copy')).then(function(){m.textContent='Copied. Paste it anywhere.'},function(){m.textContent='Copy failed: select the text above.'});return}
  if(s==='native'){navigator.share({title:'The Margin Wars',text:t,url:url(g,'native')}).catch(function(){});return}
  if(s==='card'){var a=document.createElement('a');a.href=canvas(w.dataset.h,w.dataset.s,'Arcade');a.download='margin-wars-'+g+'.png';document.body.appendChild(a);a.click();a.remove();m.textContent='Card downloaded. Attach it to your post.'}
});
var mo=window.MutationObserver&&new MutationObserver(function(){wireNative()});
document.addEventListener('DOMContentLoaded',function(){wireNative();if(mo&&native())mo.observe(document.body,{childList:true,subtree:true})});
window.MWS={box:box,grid:grid,gridHTML:gridHTML,url:url,xText:xText,xlen:xlen,xHref:xHref,liHref:liHref,canvas:canvas};
})();
