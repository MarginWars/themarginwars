/* weekend UI layer: progressive enhancement only; every page works without it */
(function(){
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
/* Single swappable logo component. Options: 'current' | 'A' | 'B' | 'C' | 'D' (assets/logo/option_X). */
var LOGO='current';
function q(s,r){return [].slice.call((r||d).querySelectorAll(s))}
function el(t,c,h){var e=d.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function logo(){if(LOGO==='current')return;q('[data-logo]').forEach(function(a){var t=a.textContent;a.dataset.logo=LOGO;a.innerHTML='<img src="assets/logo/option_'+LOGO+'/lockup_light.svg" alt="'+t+'" height="28">'})}
/* settlement line: thin magenta rule tracking position on the page */
function hh(){var h=d.querySelector('body>header');if(h)d.documentElement.style.setProperty('--hh',h.offsetHeight+'px')}
function settle(){var b=el('div','wk-settle');b.setAttribute('aria-hidden','true');var i=el('i');b.appendChild(i);(d.querySelector('body>header')||d.body).appendChild(b);hh();addEventListener('resize',hh);var p=0;
 function u(){p=0;var h=d.documentElement.scrollHeight-innerHeight;i.style.transform='scaleX('+(h>0?Math.min(1,scrollY/h):1)+')'}
 addEventListener('scroll',function(){if(!p){p=1;requestAnimationFrame(u)}},{passive:true});addEventListener('resize',u);u()}
/* Advisory: settlement ledger */
function ledger(){q('.pg-advisory .cards').forEach(function(c){c.classList.add('wk-ledger');q('details.card',c).forEach(function(x,k){var s=x.querySelector('summary');if(s.querySelector('.wk-no'))return;var n=el('span','wk-no',String(k+1).padStart(2,'0'));n.setAttribute('aria-hidden','true');s.insertBefore(n,s.firstChild);var st=x.querySelector('.acc-b strong');if(st){var a=el('span','wk-amt',st.innerHTML);a.setAttribute('aria-hidden','true');s.insertBefore(a,s.querySelector('.acc-chev'))}})})}
/* Network: keyboard-operable route switchboard */
function board(){q('.tmap .tm-lanes').forEach(function(L,bi){var lanes=q('.tm-lane',L);if(lanes.length<2)return;L.classList.add('wk-board');
 var tl=el('div','wk-jacks');tl.setAttribute('role','tablist');tl.setAttribute('aria-label',(L.parentNode.querySelector('h2')||{}).textContent||'Routes');
 var tabs=lanes.map(function(ln,k){var r=ln.querySelector('.tm-r');var id='wkl'+bi+'-'+k;ln.id=id;ln.setAttribute('role','tabpanel');ln.removeAttribute('aria-label');
  var b=el('button','wk-jack',r.innerHTML+'<em>'+q('.tm-s',ln).length+'</em>');b.type='button';b.id=id+'t';b.setAttribute('role','tab');b.setAttribute('aria-controls',id);ln.setAttribute('aria-labelledby',b.id);ln.setAttribute('tabindex','0');
  q('.tm-s',ln).forEach(function(s){if(s.title&&!s.querySelector('.wk-desc')){var p=el('small','wk-desc');p.textContent=s.title;s.appendChild(p);s.removeAttribute('title')}});
  b.addEventListener('click',function(){sel(k,false)});tl.appendChild(b);return b});
 function sel(k,f){tabs.forEach(function(b,j){var on=j===k;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;lanes[j].hidden=!on});if(f)tabs[k].focus()}
 tl.addEventListener('keydown',function(e){var k=tabs.indexOf(d.activeElement),n=tabs.length;if(k<0)return;var m={ArrowRight:k+1,ArrowDown:k+1,ArrowLeft:k-1,ArrowUp:k-1,Home:0,End:n-1}[e.key];if(m==null)return;e.preventDefault();sel((m+n)%n,true)});
 L.parentNode.insertBefore(tl,L);sel(0,false)})}
/* Next: compact engagement router onto the existing email method */
function router(){if(!d.body.classList.contains('pg-contact'))return;var mail=q('main a[href^="mailto:"]')[0];if(!mail||d.querySelector('.wk-route'))return;
 var names=['Margin Teardown','Campaign Sprint','Board sessions and workshops','Retained advisory'];var base=mail.getAttribute('href').split('?')[0];
 var f=el('form','wk-route');f.setAttribute('aria-labelledby','wkr-h');var lg=(q('.eng-cta a')[0]||{}).textContent||'Ways to work together';
 f.innerHTML='<fieldset><legend id="wkr-h">'+lg+'</legend><div class="wk-opts">'+names.map(function(n,k){return '<label class="wk-opt"><input type="radio" name="wkr" value="'+n+'"'+(k?'':' checked')+'><span class="wk-no" aria-hidden="true">'+String(k+1).padStart(2,'0')+'</span><b>'+n+'</b></label>'}).join('')+'</div><div class="wk-go"><a class="btn" href="'+base+'">'+mail.textContent+' &rarr;</a></div></fieldset>';
 var go=f.querySelector('.wk-go a');function up(){var v=f.querySelector('input:checked').value;go.href=base+'?subject='+encodeURIComponent(v)}f.addEventListener('change',up);f.addEventListener('submit',function(e){e.preventDefault()});up();
 var sec=mail.closest('section');sec.appendChild(f)}
/* About: shared spine + timeline markers */
function about(){q('.pg-about .career').forEach(function(o){o.classList.add('wk-tl')});q('.pg-about .prints').forEach(function(p){if(!p.querySelector('.wk-spine')){var s=el('span','wk-spine');s.setAttribute('aria-hidden','true');p.appendChild(s)}})}
function go(){d.documentElement.classList.add('wk');if(RM)d.documentElement.classList.add('wk-rm');[logo,settle,ledger,board,router,about].forEach(function(f){try{f()}catch(e){}})}
d.readyState==='loading'?d.addEventListener('DOMContentLoaded',go):go();
})();
