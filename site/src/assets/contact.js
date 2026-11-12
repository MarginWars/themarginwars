/* Contact form: validation, Turnstile, submit states. No visitor auto-reply. */
(function(){var f=document.getElementById('contact-form');if(!f)return;
var KEYS={'themarginwars-dev.pages.dev':'0x4AAAAAAF7sH18lHsCygRFq'},PROD='0x4AAAAAAF7re4tqJBnuPWrR',TEST='1x00000000000000000000AA';
var h=location.hostname,key=/^(localhost|127\.0\.0\.1|\[::1\])$/.test(h)?TEST:(KEYS[h]||(/\.themarginwars-dev\.pages\.dev$/.test(h)?KEYS['themarginwars-dev.pages.dev']:PROD));
var T={briefing:'Briefing invitation',teardown:'Margin Teardown',sprint:'Campaign Sprint',board:'Board sessions and workshops',retained:'Retained advisory',other:'Something else'};
var EM=/^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]{2,}$/;
var st=f.querySelector('.cf-status'),btn=f.querySelector('.cf-send'),body=f.querySelector('.cf-body'),done=document.getElementById('cf-done'),token='',wid=null,tsLoaded=false;
f.hidden=false;f.setAttribute('novalidate','');
try{var p=new URLSearchParams(location.search).get('topic');if(p&&T[p]){var r=f.querySelector('input[name=topic][value="'+T[p]+'"]');if(r)r.checked=true}}catch(e){}
function msg(n){var v=(f.elements[n]&&f.elements[n].value||'').trim();
 if(n==='name')return !v?'Please enter your name.':v.length>120?'Please keep your name under 120 characters.':'';
 if(n==='email')return !v?'Please enter your email address.':(v.length>200||!EM.test(v))?'Please enter a valid email address, like name@company.com.':'';
 if(n==='company')return v.length>160?'Please keep this under 160 characters.':'';
 if(n==='message')return v.length<10?'Please add a few words about what you need (at least 10 characters).':v.length>5000?'Please keep your message under 5000 characters.':'';
 if(n==='topic')return f.querySelector('input[name=topic]:checked')?'':'Please choose a topic.';return ''}
function show(n,m){var e=document.getElementById('cf-'+n+'-e');if(!e)return;e.textContent=m;e.hidden=!m;
 var els=n==='topic'?f.querySelectorAll('input[name=topic]'):[f.elements[n]];
 for(var i=0;i<els.length;i++){if(m)els[i].setAttribute('aria-invalid','true');else els[i].removeAttribute('aria-invalid')}
 var w=n==='topic'?f.querySelector('.cf-topic'):f.elements[n].closest('.cf-f');if(w)w.classList.toggle('cf-bad',!!m)}
var F=['topic','name','email','company','message'];
F.forEach(function(n){var el=n==='topic'?null:f.elements[n];if(el){el.addEventListener('blur',function(){if(el.value||el.getAttribute('aria-invalid'))show(n,msg(n))});el.addEventListener('input',function(){if(el.getAttribute('aria-invalid'))show(n,msg(n))})}});
f.addEventListener('change',function(e){if(e.target.name==='topic')show('topic','')});
function status(t,kind){st.textContent=t;st.className='cf-status'+(kind?' cf-'+kind:'');st.hidden=!t}
function loadTs(){if(tsLoaded)return;tsLoaded=true;window.__cfTs=function(){try{wid=turnstile.render('#cf-ts',{sitekey:key,theme:'light',size:'flexible',callback:function(t){token=t;if(pending){pending=false;f.requestSubmit?f.requestSubmit():f.dispatchEvent(new Event('submit',{cancelable:true}))}},'expired-callback':function(){token=''},'error-callback':function(){token=''}})}catch(e){}};
 var s=document.createElement('script');s.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=__cfTs';s.async=true;s.defer=true;document.head.appendChild(s)}
/* Load the human check only when someone starts using the form (keeps the page light). */
['focusin','pointerdown','touchstart','keydown'].forEach(function(ev){f.addEventListener(ev,loadTs,{passive:true})});
var pending=false;
function busy(b){btn.disabled=b;btn.setAttribute('aria-busy',b?'true':'false');btn.querySelector('span').textContent=b?'Sending…':'Send message';f.classList.toggle('cf-busy',b)}
f.addEventListener('submit',function(e){e.preventDefault();if(btn.disabled)return;var bad=[];
 F.forEach(function(n){var m=msg(n);show(n,m);if(m)bad.push(n)});
 if(bad.length){status(bad.length===1?'Please fix the highlighted field.':'Please fix the '+bad.length+' highlighted fields.','error');var first=bad[0]==='topic'?f.querySelector('input[name=topic]'):f.elements[bad[0]];first.focus();return}
 if(!token){loadTs();pending=true;status('Checking you are human…','');setTimeout(function(){if(pending){pending=false;status('Please complete the human check below, then send again.','error')}},10000);return}
 var data={name:f.elements.name.value,email:f.elements.email.value,company:f.elements.company.value,topic:(f.querySelector('input[name=topic]:checked')||{}).value,message:f.elements.message.value,website:f.elements.website.value,'cf-turnstile-response':token};
 busy(true);status('Sending your message…','');
 try{data.attribution=window.TMW_ATTR?window.TMW_ATTR():null}catch(x){}fetch('/api/contact',{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify(data)}).then(function(r){return r.json().catch(function(){return {ok:false}}).then(function(d){return {r:r,d:d}})}).then(function(x){busy(false);
  if(x.d&&x.d.ok){body.hidden=true;status('','');var ref=done.querySelector('.cf-ref');if(ref)ref.textContent=x.d.id?'Reference: '+x.d.id.slice(0,8):'';done.hidden=false;done.focus();return}
  token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}
  if(x.d&&x.d.errors){var ks=Object.keys(x.d.errors);ks.forEach(function(n){show(n,x.d.errors[n])});status(x.d.error||'Please check the highlighted fields.','error');var el=f.elements[ks[0]];if(el&&el.focus)el.focus();return}
  status((x.d&&x.d.error)||'Something went wrong sending your message. Please try again, or email us directly.','error');st.focus()
 }).catch(function(){busy(false);token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}status('We could not reach the server. Check your connection and try again, or email us directly.','error');st.focus()})});
var again=document.getElementById('cf-again');if(again)again.addEventListener('click',function(){f.reset();done.hidden=true;body.hidden=false;token='';try{if(wid!==null)turnstile.reset(wid)}catch(e){}f.elements.name.focus()});
})();
