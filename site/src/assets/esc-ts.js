/* Human check (Cloudflare Turnstile) for the assistant's "Talk to a human" form. Same widgets and keys as the contact form.
   Loaded lazily when the form opens. */
(function(){var KEYS={'themarginwars-dev.pages.dev':'0x4AAAAAAF7sH18lHsCygRFq'},PROD='0x4AAAAAAF7re4tqJBnuPWrR',TEST='1x00000000000000000000AA';
var h=location.hostname,key=/^(localhost|127\.0\.0\.1|\[::1\])$/.test(h)?TEST:(KEYS[h]||(/\.themarginwars-dev\.pages\.dev$/.test(h)?KEYS['themarginwars-dev.pages.dev']:PROD));
var loading=false,q=[],S=new WeakMap();
function api(cb){if(window.turnstile&&window.turnstile.render)return cb();q.push(cb);if(loading)return;loading=true;
 window.__tmwEscTs=function(){q.splice(0).forEach(function(f){try{f()}catch(e){}})};
 var s=document.createElement('script');s.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=__tmwEscTs';s.async=true;s.defer=true;document.head.appendChild(s)}
window.TMW_TS={
 load:function(form){if(S.has(form))return;var st={id:null,tok:'',wait:null};S.set(form,st);var box=form.querySelector('.ts');
  api(function(){st.id=turnstile.render(box,{sitekey:key,theme:'light',size:'flexible',
   callback:function(t){st.tok=t;if(st.wait){var w=st.wait;st.wait=null;w()}},'expired-callback':function(){st.tok=''},'error-callback':function(){st.tok=''}})})},
 get:function(form){var st=S.get(form);return st?st.tok:''},
 whenReady:function(form,fn,late){var st=S.get(form);if(!st){this.load(form);st=S.get(form)}if(st.tok)return fn();st.wait=fn;if(late)setTimeout(function(){if(st.wait===fn){st.wait=null;late()}},10000)},
 reset:function(form){var st=S.get(form);if(st&&st.id!=null){st.tok='';try{turnstile.reset(st.id)}catch(e){}}}
};})();
