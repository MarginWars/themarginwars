/* Micro-feedback for Daily, Spot the Leak, Price the Deal, Pub Quiz: haptic tick and score count-up. */
(function(){if(!window.MutationObserver)return;var R=matchMedia('(prefers-reduced-motion: reduce)').matches;
function buzz(p){try{navigator.vibrate&&navigator.vibrate(p)}catch(e){}}
new MutationObserver(function(ms){ms.forEach(function(m){var t=m.target;if(m.type==='attributes'&&t.tagName==='BUTTON'){if(t.className==='ok')buzz(15);else if(t.className==='no')buzz([25,40,25])}})}).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']})})();
(function(){var b=document.querySelector('body>.sold-l'),f=document.querySelector('footer');if(b&&f){var w=document.createElement('p');w.className='sold-dock';w.appendChild(b);f.appendChild(w)}})();
