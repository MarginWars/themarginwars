/* The Margin Wars: first-party, cookieless measurement. sessionStorage only; no cookies, no third-party pixels.
   Active on production hosts only (dev/previews: off unless ?mk_test=1 for QA, held for the session). */
(function(){
 var H=location.hostname,S;try{S=window.sessionStorage;S.setItem('tmw_t','1');S.removeItem('tmw_t')}catch(e){S=null}
 var q;try{q=new URLSearchParams(location.search)}catch(e){q=null}
 var PROD=H==='themarginwars.com'||H==='www.themarginwars.com';
 if(!PROD&&S&&q&&q.get('mk_test')==='1')S.setItem('tmw_mk_test','1');
 if(PROD&&S&&q&&q.get('mk_test')==='1')S.setItem('tmw_mk_test','1');
 var QA=S&&S.getItem('tmw_mk_test')==='1';
 var ON=(PROD&&!navigator.webdriver)||QA; /* automated browsers (Lighthouse, test runners) are not visitors */
 var K='tmw_attr',st={};try{st=JSON.parse(S&&S.getItem(K)||'{}')||{}}catch(e){st={}}
 var t={},has=false;['source','medium','campaign','content','term'].forEach(function(k){var v=q&&q.get('utm_'+k);if(v){t[k]=v.slice(0,100);has=true}});
 var ref='';try{if(document.referrer){var r=new URL(document.referrer);if(r.hostname!==H)ref=r.hostname}}catch(e){}
 if(ref)t.referrer=ref;
 if(has||ref||!st.first){t.landing=location.pathname;t.at=new Date().toISOString();if(!st.first)st.first=t;if(has||ref||!st.last)st.last=t}
 var firstView=!st.v;st.v=1;try{S&&S.setItem(K,JSON.stringify(st))}catch(e){}
 window.TMW_ATTR=function(){return {first:st.first||null,last:st.last||null}};
 function send(e){if(!ON)return;var b=JSON.stringify({e:e,p:location.pathname,a:window.TMW_ATTR()});
  try{if(navigator.sendBeacon&&navigator.sendBeacon('/api/ev',new Blob([b],{type:'text/plain'})))return}catch(x){}
  try{fetch('/api/ev',{method:'POST',body:b,keepalive:true,headers:{'content-type':'text/plain'}})}catch(x){}}
 window.TMW_EV=send;
 if(firstView)send('visit');
 document.addEventListener('click',function(ev){var a=ev.target&&ev.target.closest&&ev.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'',u;
  try{u=new URL(h,location.href)}catch(x){return}
  if(/(^|\.)substack\.com$/.test(u.hostname))send('out_substack');
  else if(/(^|\.)linkedin\.com$/.test(u.hostname))send('out_linkedin');
  else if(u.hostname===H&&/^\/contact(\.html)?$/.test(u.pathname))send(/topic=briefing/i.test(u.search)?'cta_briefing':'cta_contact');
 },true);
})();
