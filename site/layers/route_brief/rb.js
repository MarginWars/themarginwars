/* Route Brief: deterministic, no network calls. Enhances pre-rendered briefs. */
(function(){
  function init(r){
    var f=r.querySelector('.rb-pick'),arts=[].slice.call(r.querySelectorAll('.rb-brief')),none=r.querySelector('#rb-none'),pr=r.querySelector('.rb-print');
    if(!f)return;
    f.hidden=false;r.classList.add('rb-js');
    if(pr){pr.hidden=false;pr.addEventListener('click',function(){document.documentElement.classList.add('rb-printing');window.print();setTimeout(function(){document.documentElement.classList.remove('rb-printing')},500)});}
    function val(n){var x=f.querySelector('input[name="'+n+'"]:checked');return x?x.value:''}
    function up(){
      var m=val('rb-m'),p=val('rb-p'),hit=null;
      arts.forEach(function(a){if(a!==none&&a.getAttribute('data-m')===m&&a.getAttribute('data-p')===p)hit=a});
      arts.forEach(function(a){a.hidden=(a!==(hit||none))});
      r.setAttribute('data-state',hit?hit.id:'rb-none');
    }
    // mark which methods have a brief for the chosen market
    function marks(){
      var m=val('rb-m');
      [].slice.call(f.querySelectorAll('input[name="rb-p"]')).forEach(function(i){
        var ok=arts.some(function(a){return a.getAttribute('data-m')===m&&a.getAttribute('data-p')===i.value});
        i.parentNode.classList.toggle('rb-na',!ok);
        var s=i.parentNode.querySelector('.vh');if(!s){s=document.createElement('span');s.className='vh';i.parentNode.appendChild(s)}
        s.textContent=ok?'':' (not briefed yet)';
      });
    }
    f.addEventListener('change',function(e){
      if(e.target.name==='rb-m'){marks();
        var p=val('rb-p'),m=val('rb-m');
        var has=arts.some(function(a){return a.getAttribute('data-m')===m&&a.getAttribute('data-p')===p});
        if(!has){var first=arts.filter(function(a){return a.getAttribute('data-m')===m})[0];
          if(first){var i=f.querySelector('input[name="rb-p"][value="'+first.getAttribute('data-p')+'"]');if(i)i.checked=true}}
      }
      up();
    });
    marks();up();
    window.rbSet=function(m,p){var a=f.querySelector('input[name="rb-m"][value="'+m+'"]'),b=f.querySelector('input[name="rb-p"][value="'+p+'"]');if(a)a.checked=true;if(b)b.checked=true;marks();up()};
  }
  function go(){[].slice.call(document.querySelectorAll('.rbf')).forEach(init)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
