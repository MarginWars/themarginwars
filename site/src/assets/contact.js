/* Contact form: validation, Turnstile, submit states. No visitor auto-reply. */
(function(){var f=document.getElementById('contact-form');if(!f)return;
var KEYS={'themarginwars-dev.pages.dev':'0x4AAAAAAF7sH18lHsCygRFq'},PROD='0x4AAAAAAF7re4tqJBnuPWrR',TEST='1x00000000000000000000AA';
var h=location.hostname,key=/^(localhost|127\.0\.0\.1|\[::1\])$/.test(h)?TEST:(KEYS[h]||(/\.themarginwars-dev\.pages\.dev$/.test(h)?KEYS['themarginwars-dev.pages.dev']:PROD));
var T={briefing:'Briefing invitation',teardown:'Margin Teardown',sprint:'Campaign Sprint',board:'Board sessions and workshops',retained:'Retained advisory',other:'Something else'};
var EM=/^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]{2,}$/;
var st=f.querySelector('.cf-status'),btn=f.querySelector('.cf-send'),body=f.querySelector('.cf-body'),done=document.getElementById('cf-done'),token='',wid=null,tsLoaded=false;
f.hidden=false;f.setAttribute('novalidate','');
var more=f.querySelector('.cf-more'),ttl=document.getElementById('cf-title'),led=document.getElementById('cf-lede'),lab=f.querySelector('label[for=cf-message]'),sendL=btn.querySelector('span');
var COPY={'Margin Teardown':['Book a Teardown','Tell us what you want torn down. Your email is enough to start. A line is optional.','What do you want torn down?','Send request'],'Briefing invitation':['Request a Briefing invitation','Your email is enough. A line is optional.','What would you like to tell us?','Send request']};
var COPY_DEFAULT=['Send us a message','Your email is enough to start. A line is optional.','What do you need?','Send message'];
function ev(n){var sent=false;function send(){if(sent||!window.TMW_EV)return;sent=true;try{window.TMW_EV(n)}catch(e){}}send();if(!sent){document.addEventListener('DOMContentLoaded',send);window.addEventListener('load',send);setTimeout(send,0)}}
function evOnce(n){var k='tmw_form_'+n+'_'+location.pathname.replace(/[^a-z0-9]+/gi,'-');try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,'1')}catch(e){}ev(n)}
function seen(){evOnce('form_view')}
if(typeof IntersectionObserver==='function'){var io=new IntersectionObserver(function(ents){if(ents.some(function(e){return e.isIntersecting})){seen();io.disconnect()}},{threshold:0.15,rootMargin:'0px'});io.observe(f.closest('#book')||f)}else seen();
['focusin','input'].forEach(function(evn){f.addEventListener(evn,function(){evOnce('form_start')},{passive:true})});
function skin(){var c=f.querySelector('input[name=topic]:checked'),k=COPY[c&&c.value]||COPY_DEFAULT;if(ttl)ttl.textContent=k[0];if(led)led.textContent=k[1];if(lab){lab.textContent='';lab.appendChild(document.createTextNode(k[2]+' '));var opt=document.createElement('span');opt.className='cf-opt';opt.textContent='(optional)';lab.appendChild(opt)}if(sendL){sendL.textContent=k[3];sendL.dataset.l=k[3]}}
try{var p=new URLSearchParams(location.search).get('topic');if(p&&T[p]){var r=f.querySelector('input[name=topic][value="'+T[p]+'"]');if(r)r.checked=true}}catch(e){}
skin();
function msg(n){var v=(f.elements[n]&&f.elements[n].value||'').trim();
 if(n==='name')return v.length>120?'Please keep your name under 120 characters.':'';
 if(n==='email')return !v?'Please enter your email address.':(v.length>200||!EM.test(v))?'Please enter a valid email address, like name@company.com.':'';
 if(n==='company')return v.length>160?'Please keep this under 160 characters.':'';
 if(n==='message')return v.length>5000?'Please keep this under 5000 characters.':'';
 if(n==='topic')return f.querySelector('input[name=topic]:checked')?'':'Please choose a topic.';return ''}
function show(n,m){var e=document.getElementById('cf-'+n+'-e');if(!e)return;e.textContent=m;e.hidden=!m;
 var els=n==='topic'?f.querySelectorAll('input[name=topic]'):[f.elements[n]];
 for(var i=0;i<els.length;i++){if(m)els[i].setAttribute('aria-invalid','true');else els[i].removeAttribute('aria-invalid')}
 var w=n==='topic'?f.querySelector('.cf-topic'):f.elements[n].closest('.cf-f');if(w)w.classList.toggle('cf-bad',!!m)}
var F=['email','message','topic','name','company'];
F.forEach(function(n){var el=n==='topic'?null:f.elements[n];if(el){el.addEventListener('blur',function(){if(el.value||el.getAttribute('aria-invalid'))show(n,msg(n))});el.addEventListener('input',function(){if(el.getAttribute('aria-invalid'))show(n,msg(n))})}});
f.addEventListener('change',function(e){if(e.target.name==='topic'){show('topic','');skin()}});
function status(t,kind){st.textContent=t;st.className='cf-status'+(kind?' cf-'+kind:'');st.hidden=!t}
function loadTs(){if(tsLoaded)return;tsLoaded=true;window.__cfTs=function(){try{wid=turnstile.render('#cf-ts',{sitekey:key,theme:'light',size:'flexible',callback:function(t){token=t;if(pending){pending=false;f.requestSubmit?f.requestSubmit():f.dispatchEvent(new Event('submit',{cancelable:true}))}},'expired-callback':function(){token=''},'error-callback':function(){token=''}})}catch(e){}};
 var s=document.createElement('script');s.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=__cfTs';s.async=true;s.defer=true;document.head.appendChild(s)}
/* Load the human check only when someone starts using the form (keeps the page light; a third-party fetch on view would also stall QA networkidle). */
['focusin','pointerdown','touchstart','keydown'].forEach(function(ev){f.addEventListener(ev,loadTs,{passive:true})});
var pending=false;
function busy(b){btn.disabled=b;btn.setAttribute('aria-busy',b?'true':'false');btn.querySelector('span').textContent=b?'Sending…':(sendL&&sendL.dataset.l||'Send message');f.classList.toggle('cf-busy',b)}
f.addEventListener('submit',function(e){e.preventDefault();if(btn.disabled)return;var bad=[];
 F.forEach(function(n){var m=msg(n);show(n,m);if(m)bad.push(n)});
 if(bad.length){evOnce('form_error');status(bad.length===1?'Please fix the highlighted field.':'Please fix the '+bad.length+' highlighted fields.','error');if(more&&/^(topic|name|company)$/.test(bad[0]))more.open=true;var first=bad[0]==='topic'?f.querySelector('input[name=topic]'):f.elements[bad[0]];first.focus();return}
 if(!token){loadTs();pending=true;status('Checking you are human…','');setTimeout(function(){if(pending){pending=false;evOnce('form_error');status('Please complete the human check below, then send again.','error')}},10000);return}
 evOnce('form_submit');
 var data={name:f.elements.name.value,email:f.elements.email.value,company:f.elements.company.value,topic:(f.querySelector('input[name=topic]:checked')||{}).value,message:f.elements.message.value,website:f.elements.website.value,'cf-turnstile-response':token};
 busy(true);status('Sending your message…','');
 try{data.attribution=window.TMW_ATTR?window.TMW_ATTR():null}catch(x){}fetch('/api/contact',{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify(data)}).then(function(r){return r.json().catch(function(){return {ok:false}}).then(function(d){return {r:r,d:d}})}).then(function(x){busy(false);
  if(x.d&&x.d.ok){body.hidden=true;status('','');var ref=done.querySelector('.cf-ref');if(ref)ref.textContent=x.d.id?'Reference: '+x.d.id.slice(0,8):'';done.hidden=false;done.focus();return}
  token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}
  evOnce('form_error');
  if(x.d&&x.d.errors){var ks=Object.keys(x.d.errors);ks.forEach(function(n){show(n,x.d.errors[n])});status(x.d.error||'Please check the highlighted fields.','error');if(more&&/^(topic|name|company)$/.test(ks[0]))more.open=true;var el=f.elements[ks[0]];if(el&&el.focus)el.focus();return}
  status((x.d&&x.d.error)||'Something went wrong sending your message. Please try again, or email us directly.','error');st.focus()
 }).catch(function(){busy(false);token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}evOnce('form_error');status('We could not reach the server. Check your connection and try again, or email us directly.','error');st.focus()})});
var again=document.getElementById('cf-again');if(again)again.addEventListener('click',function(){f.reset();skin();done.hidden=true;body.hidden=false;token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}f.elements.email.focus()});
})();
