(function(){
"use strict";
var QB=window.MW_QB||[],LS=window.localStorage,$=function(s,r){return (r||document).querySelector(s)};
function get(k,d){try{var v=LS.getItem('mw_'+k);return v===null?d:JSON.parse(v)}catch(e){return d}}
function set(k,v){try{LS.setItem('mw_'+k,JSON.stringify(v))}catch(e){}}
function ptDate(d){return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(d||new Date())}
function hash(s){var h=2166136261;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
function rng(seed){var a=hash(String(seed));return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function shuffle(arr,r){arr=arr.slice();for(var i=arr.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var t=arr[i];arr[i]=arr[j];arr[j]=t}return arr}
function pick(seed,n,pool){return shuffle(pool||QB,rng(seed)).slice(0,n)}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function base(){return location.protocol==='file:'?'https://review.themarginwars.pages.dev/':location.origin+location.pathname.replace(/[^/]*$/,'')}
function liURL(path){return 'https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(base()+path)}
window.MW={ptDate:ptDate,pick:pick,hash:hash,liURL:liURL,get:get,set:set,dealRange:dealRange};
/* quiz runner */
function runQs(el,qs,seed,opt,done){
  var i=0,score=0,marks=[],timer=null;
  function show(){
    if(i>=qs.length){clearInterval(timer);return done(score,marks)}
    var q=qs[i],r=rng(seed+':'+q.id),ord=shuffle([0,1,2,3],r),t=opt.time||0,left=t;
    el.innerHTML='<p class="gq-n">Question '+(i+1)+' of '+qs.length+(t?' · <span class="gq-t" aria-live="off">'+t+'s</span>':'')+'</p><h3 aria-level="2" class="gq-q">'+esc(q.q)+'</h3><div class="gq-o">'+ord.map(function(k){return '<button type="button" data-k="'+k+'">'+esc(q.options[k])+'</button>'}).join('')+'</div><div class="gq-f" aria-live="polite"></div>';
    function answer(k){
      clearInterval(timer);var ok=k===q.a;if(ok)score++;marks.push(ok);
      [].forEach.call(el.querySelectorAll('.gq-o button'),function(b){b.disabled=true;var bk=+b.dataset.k;if(bk===q.a)b.className='ok';else if(bk===k)b.className='no'});
      $('.gq-f',el).innerHTML='<p><b>'+(ok?'✓ Correct.':(k<0?'⏱ Time.':'✗ Not quite.'))+'</b> '+esc(q.options[q.a])+'. Source: <a href="'+esc(q.source)+'" target="_blank" rel="noopener">'+esc(q.source.replace(/^https?:\/\/(www\.)?/,'').split('/')[0])+'</a></p><button type="button" class="btn gq-next">'+(i+1<qs.length?'Next':'See result')+'</button>';
      $('.gq-next',el).focus();$('.gq-next',el).onclick=function(){i++;show()};
    }
    [].forEach.call(el.querySelectorAll('.gq-o button'),function(b){b.onclick=function(){answer(+b.dataset.k)}});
    if(t&&!opt.untimed()){timer=setInterval(function(){left--;var s=$('.gq-t',el);if(s)s.textContent=left+'s';if(left<=0)answer(-1)},1000)}
  }
  show();
}
function grid(m){return m.map(function(x){return x?'🟪':'⬜'}).join('')}
function shareBox(text,path,cardTitle,cardSub){
  var id='c'+Math.random().toString(36).slice(2,7);
  return '<div class="gs"><pre class="gs-t">'+esc(text)+'</pre><div class="gs-b"><a class="btn" target="_blank" rel="noopener" href="'+liURL(path)+'">Share on LinkedIn</a><button type="button" class="btn alt gs-copy" data-t="'+esc(text)+'">Copy result</button><button type="button" class="btn alt gs-png" data-h="'+esc(cardTitle)+'" data-s="'+esc(cardSub)+'">Download score card</button></div><p class="gs-m" role="status" aria-live="polite"></p></div>';
}
document.addEventListener('click',function(e){
  var c=e.target.closest('.gs-copy');if(c){var t=c.dataset.t,m=c.parentNode.parentNode.querySelector('.gs-m');(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){m.textContent='Copied. Paste it into your post.'},function(){m.textContent='Copy failed: select the text above.'})}
  var p=e.target.closest('.gs-png');if(p){var a=document.createElement('a');a.href=card(p.dataset.h,p.dataset.s);a.download='margin-wars-score.png';a.click()}
});
function card(h,s){var c=document.createElement('canvas');c.width=1200;c.height=627;var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,1200,627);x.fillStyle='#B5237F';x.beginPath();x.moveTo(0,0);x.lineTo(420,0);x.lineTo(240,627);x.lineTo(0,627);x.fill();x.fillStyle='#8A1A61';x.font='900 64px "Big Shoulders Display",Impact,sans-serif';x.fillText('THE MARGIN WARS',300,140);x.font='800 46px Archivo,Arial,sans-serif';wrap(x,h,300,250,840,56);x.font='500 32px Archivo,Arial,sans-serif';wrap(x,s,300,440,840,42);x.font='700 26px Archivo,Arial,sans-serif';x.fillText('The Margin Wars · the Arcade',300,580);return c.toDataURL('image/png')}
function wrap(x,t,X,Y,W,L){var w=String(t).split(' '),l='';for(var i=0;i<w.length;i++){var s=l+w[i]+' ';if(x.measureText(s).width>W&&l){x.fillText(l,X,Y);l=w[i]+' ';Y+=L}else l=s}x.fillText(l,X,Y)}
/* Daily */
function daily(el){
  var d=ptDate(),key='daily_'+d,prev=get(key,null),qs=pick('daily:'+d,5);
  function fin(score,marks){
    if(!prev){var st=get('streak',{n:0,last:''}),y=ptDate(new Date(Date.now()-864e5));st.n=(st.last===y)?st.n+1:(st.last===d?st.n:1);st.last=d;set('streak',st);set(key,{s:score,m:marks})}
    var st2=get('streak',{n:1});
    var txt='The Margin Wars Daily '+d+'\n'+score+'/5 '+grid(marks)+'\nStreak: '+st2.n+'\nCan you beat it?';
    el.innerHTML='<h3 aria-level="2">'+score+'/5 today</h3><p class="g-big">'+grid(marks)+'</p><p>Streak: <b>'+st2.n+'</b> day'+(st2.n===1?'':'s')+'. A new five questions drops at midnight PT.</p>'+shareBox(txt,'daily.html?ref=share-li','I scored '+score+'/5 on today\u2019s Margin Wars Daily','Five practitioner questions a day, every answer sourced.')+'<p>Want the why behind the answers? <a href="https://themarginwars.substack.com/?ref=arcade">Read the dispatch</a>.</p>';
    location.hash='done';
  }
  if(prev)fin(prev.s,prev.m);else runQs(el,qs,'daily:'+d,{untimed:function(){return true}},fin);
}
/* Leak */
var LEAK=[["Visa/Mastercard interchange (pass-through)","$1,742,310",0],["Network assessment fees (pass-through)","$148,920",0],["Acquirer processing margin 0.12%","$96,000",0],["Non-qualified surcharge 1.10% on chip card-present sales","$61,380",1,"A blanket 'non-qualified' surcharge on chip card-present sales is a classic tiered-pricing leak. Under interchange-plus, you should see the actual interchange category instead."],["Authorization fees $0.03 × 2.1M","$63,000",0],["Chargeback handling 412 × $25","$10,300",0],["PCI non-compliance fee (merchant attested compliant, AOC on file)","$4,950",1,"A non-compliance fee charged while a valid Attestation of Compliance is on file means the acquirer's records are wrong. Claim it back."],["Cross-currency fee on USD sales to US-issued cards","$38,640",1,"A cross-currency fee on domestic-currency sales to domestic cards suggests a misconfigured merchant category or currency. Check the settlement currency setup."],["Monthly gateway fee","$1,500",0],["Network token provisioning","$2,210",0],["Account updater hits 18,400 × $0.10","$1,840",0],["Statement fee","$25",0]];
function leak(el,opt){
  opt=opt||{};var found=0,tries=0,total=LEAK.filter(function(l){return l[2]}).length;
  el.innerHTML='<p class="illus">ILLUSTRATIVE: a fictional enterprise merchant, "Northwind Outfitters", $80M/month card volume. Not a real statement.</p><p>Find the <b>'+total+'</b> leaks. Tap a line you think is wrong. You have 5 taps.</p><table class="lk"><thead><tr><th scope="col">Line item (October)</th><th scope="col">Amount</th></tr></thead><tbody>'+LEAK.map(function(l,i){return '<tr><td><button type="button" data-i="'+i+'">'+esc(l[0])+'</button></td><td>'+l[1]+'</td></tr>'}).join('')+'</tbody></table><div class="lk-f" aria-live="polite"></div>';
  [].forEach.call(el.querySelectorAll('.lk button'),function(b){b.onclick=function(){
    var l=LEAK[+b.dataset.i];b.disabled=true;tries++;
    if(l[2]){found++;b.className='ok';b.insertAdjacentHTML('beforeend','<span class="why">✓ '+esc(l[3])+'</span>')}else{b.className='no';b.insertAdjacentHTML('beforeend','<span class="why">✗ Looks normal.</span>')}
    if(found===total||tries>=5){[].forEach.call(el.querySelectorAll('.lk button'),function(x){x.disabled=true});
      var txt='The Margin Wars: Spot the Leak\nI found '+found+'/'+total+' leaks in an enterprise fee statement.\nCan you?';
      $('.lk-f',el).innerHTML='<h3 aria-level="2">'+found+'/'+total+' leaks found</h3>'+shareBox(txt,'leak.html?ref=share-li','I found '+found+'/'+total+' leaks in an enterprise fee statement','Spot the Leak · The Margin Wars Arcade')+(opt.ep?'':'<div class="lk-cta"><p><b>Your real statement has more lines than this.</b> The Margin Teardown finds them for you: $17,500, fixed scope.</p><a class="btn" href="advisory.html">See the Margin Teardown</a></div>');
      if(opt.done)opt.done(found,total)}
  }});
}
/* Deal */
var DEAL={vol:400e6,ticket:85,debit:0.40,credit_ic:0.020,scheme:0.0013,mlo:0.0010,mhi:0.0025};
function dealRange(p){p=p||DEAL;var dv=p.vol*p.debit,tx=dv/p.ticket,dic=tx*0.22+dv*0.0005,cic=p.vol*(1-p.debit)*p.credit_ic,sch=p.vol*p.scheme,pt=(dic+cic+sch)/p.vol;return{pt:pt,lo:pt+p.mlo,hi:pt+p.mhi,dic:dic,cic:cic,sch:sch}}
function deal(el){
  var from=(new URLSearchParams(location.search).get('from')||'').replace(/[^A-Za-z\- ]/g,'').slice(0,20),R=dealRange();
  el.innerHTML=(from?'<p class="chal">'+esc(from)+' challenged you to price this deal.</p>':'')+'<p class="illus">ILLUSTRATIVE: fictional merchant profile and assumptions, for practice only.</p><dl class="dp"><dt>Merchant</dt><dd>"Harbor &amp; Pine", US omnichannel home goods</dd><dt>Annual card volume</dt><dd>$400M</dd><dt>Average ticket</dt><dd>$85</dd><dt>Mix</dt><dd>40% regulated debit, 60% credit</dd><dt>Assumed credit interchange (illustrative)</dt><dd>2.00%</dd><dt>Assumed scheme fees (illustrative)</dt><dd>0.13% of volume</dd></dl><label for="dr">Your quoted all-in blended rate (%)</label><input id="dr" inputmode="decimal" placeholder="e.g. 1.65"><button type="button" class="btn" id="dgo">Price it</button><div class="dk" aria-live="polite"></div>';
  $('#dgo').onclick=function(){
    var v=parseFloat(($('#dr').value||'').replace('%',''))/100;if(!(v>0&&v<0.1)){$('.dk').innerHTML='<p>Enter a rate between 0 and 10%.</p>';return}
    var pct=function(x){return (x*100).toFixed(2)+'%'},inr=v>=R.lo&&v<=R.hi,off=inr?0:Math.min(Math.abs(v-R.lo),Math.abs(v-R.hi)),pts=Math.max(0,100-Math.round(off*10000*4));
    $('.dk').innerHTML='<h3 aria-level="2">'+(inr?'Sound. ':v<R.lo?'Too thin: the acquirer will claw it back. ':'Leaking margin. ')+'Score '+pts+'/100</h3><p>Sound range: <b>'+pct(R.lo)+' to '+pct(R.hi)+'</b></p><pre class="fm">Regulated debit IC = txns × ($0.21 + $0.01) + 5 bps × value   [Reg II]\n                   = $'+Math.round(R.dic).toLocaleString()+'\nCredit IC          = $240M × 2.00% (assumed) = $'+Math.round(R.cic).toLocaleString()+'\nScheme fees        = $400M × 0.13% (assumed) = $'+Math.round(R.sch).toLocaleString()+'\nPass-through       = '+pct(R.pt)+'\nSound range        = pass-through + 0.10% to 0.25% acquirer margin (assumed)</pre><p class="fine">Reg II cap: <a href="https://www.federalregister.gov/documents/2023/11/14/2023-24034/debit-card-interchange-fees-and-routing" target="_blank" rel="noopener">Federal Register, 2023</a>. Other inputs are illustrative assumptions.</p>'+shareBox('The Margin Wars: Price the Deal\nI scored '+pts+'/100 pricing a $400M enterprise merchant.\nYour move.','deal.html?ref=share-li','I scored '+pts+'/100 pricing a $400M enterprise deal','Price the Deal · The Margin Wars Arcade')+'<div class="chx"><h4>Consultant? Challenge your client</h4><label for="cf">Your first name</label><input id="cf" maxlength="20"><button type="button" class="btn alt" id="cgo">Make challenge link</button><p class="cl" aria-live="polite"></p></div><div class="lk-cta"><p>Real deals have 40+ inputs. The Margin Teardown models yours: $17,500.</p><a class="btn" href="advisory.html">See the Margin Teardown</a></div>';
    $('#cgo').onclick=function(){var n=($('#cf').value||'').replace(/[^A-Za-z\- ]/g,'').slice(0,20);var u=base()+'deal.html?ref=challenge&from='+encodeURIComponent(n);$('.cl').innerHTML='<a href="'+esc(u)+'">'+esc(u)+'</a> <a class="btn alt" target="_blank" rel="noopener" href="'+liURL('deal.html?ref=challenge&from='+encodeURIComponent(n))+'">Share</a>'};
  };
}
/* Quiz */
function quiz(el){
  var m=ptDate().slice(0,7),qs=pick('quiz:'+m,10),ut=$('#untimed');
  el.innerHTML='<button type="button" class="btn" id="qstart">Start the round (10 questions, 20s each)</button>';
  $('#qstart').onclick=function(){runQs(el,qs,'quiz:'+m,{time:20,untimed:function(){return ut&&ut.checked}},function(s,mk){
    var lb=get('lb_'+m,[]);el.innerHTML='<h3 aria-level="2">'+s+'/10</h3><p class="g-big">'+grid(mk)+'</p><label for="ini">Initials for your device leaderboard</label><input id="ini" maxlength="3"><button type="button" class="btn alt" id="isave">Save</button>'+shareBox('The Margin Wars Pub Quiz, '+m+'\n'+s+'/10 '+grid(mk),'quiz.html?ref=share-li','I scored '+s+'/10 in the Margin Wars Pub Quiz','This month: Rails & Rules')+'<div id="lbx"></div><div class="lk-cta"><p>Top scorers are invited to the Briefing: about 150 senior operators, monthly.</p><a class="btn" href="https://themarginwars.substack.com/?ref=quiz">Join the Briefing waitlist</a></div>';
    function draw(){var l=get('lb_'+m,[]);$('#lbx').innerHTML='<h4>Leaderboard: stored on this device only</h4><ol>'+l.map(function(r){return '<li>'+esc(r.i)+' · '+r.s+'/10</li>'}).join('')+'</ol>'}
    $('#isave').onclick=function(){var i=($('#ini').value||'???').replace(/[^A-Za-z]/g,'').toUpperCase().slice(0,3)||'???';lb.push({i:i,s:s});lb.sort(function(a,b){return b.s-a.s});set('lb_'+m,lb.slice(0,10));$('#isave').disabled=true;draw()};draw();
  })};
}
/* Episodes */
function countdown(el){var t=Date.parse(el.dataset.drop);function tick(){var s=Math.max(0,Math.floor((t-Date.now())/1000));el.textContent=s?Math.floor(s/86400)+'d '+Math.floor(s%86400/3600)+'h '+Math.floor(s%3600/60)+'m':'Live now';}tick();setInterval(tick,30000)}
var DEAL2={a:0.60,am:0.0015,b:0.40,bm:0.0035};
function deal2(el,done){var R=dealRange(),D=DEAL2,bl=R.pt+D.a*D.am+D.b*D.bm,f=function(x){return (x*100).toFixed(2)+'%'};
  el.innerHTML='<p class="fine"><b>ILLUSTRATIVE.</b> Fictional merchant and fictional quotes, built for practice. Not real pricing from any provider.</p><p>Same $400M merchant as Price the Deal, now split across two acquirers. Acquirer A routes '+D.a*100+'% of volume at pass-through + '+f(D.am)+'. Acquirer B routes '+D.b*100+'% at pass-through + '+f(D.bm)+'. Pass-through (interchange + scheme) is '+f(R.pt)+'. What is the blended all-in rate?</p><p><label>Your answer (%) <input id="d2v" type="number" step="0.01" inputmode="decimal"></label> <button type="button" class="btn" id="d2go">Lock it in</button></p><div id="d2o" aria-live="polite"></div>';
  $('#d2go').onclick=function(){var v=parseFloat($('#d2v').value)/100;if(isNaN(v))return;this.disabled=true;var ok=Math.abs(v-bl)<=0.0003;
    $('#d2o').innerHTML='<p><b>'+(ok?'Correct.':'Not quite.')+'</b> Blended = '+f(R.pt)+' + ('+D.a+' × '+f(D.am)+') + ('+D.b+' × '+f(D.bm)+') = <b>'+f(bl)+'</b>. Moving share to the cheaper acquirer is the reserve you hold back for the right moment.</p>';done(ok?1:0,1)}}
function ep(el){
  var n=+el.dataset.ep,ids=el.dataset.qs.split(','),qs=QB.filter(function(q){return ids.indexOf(q.id)>=0}),need=+el.dataset.need,prev=n>1&&!get('ep'+(n-1),null)&&!(/preview/.test(location.search)&&(/^(review\.themarginwars\.pages\.dev|localhost|127\.0\.0\.1)$/.test(location.hostname)));
  var title=el.dataset.title,rank=el.dataset.rank;
  var op=el.dataset.open&&Date.now()<Date.parse(el.dataset.open)&&!(/preview/.test(location.search)&&(/^(review\.themarginwars\.pages\.dev|localhost|127\.0\.0\.1)$/.test(location.hostname)));if(op){el.innerHTML='<p class="lock">🔒 This episode opens in <b data-drop="'+el.dataset.open+'">soon</b>. Play the <a href="daily.html">Daily</a> while you wait.</p>';countdown(el.querySelector('[data-drop]'));return}
  if(prev){el.innerHTML='<p class="lock">🔒 Clear Episode '+(n-1)+' first. <a href="ep'+(n-1)+'.html">Go to Episode '+(n-1)+'</a></p>';return}
  function win(s,tot){var ok=s>=need;if(ok)set('ep'+n,{s:s,rank:rank});
    $('#epout').innerHTML=ok?'<div class="ins" aria-hidden="true">'+Array(n+1).join('<i></i>')+'</div><h3 aria-level="2">Episode cleared. Rank: '+esc(rank)+'</h3>'+shareBox('I cleared Episode '+n+': '+title+' in The Margin Wars, Season 1.\nRank: '+rank,'ep'+n+'.html?ref=share-li','I cleared Episode '+n+': '+title,'The Margin Wars, Season 1 · Rank: '+rank)+'<div class="cliff">'+$('#cliff').innerHTML+'</div>':'<h3 aria-level="2">'+s+'/'+tot+'. You need '+need+' to clear.</h3><button type="button" class="btn" onclick="location.reload()">Regroup and retry</button>'}
  var to={untimed:function(){return true}};if(el.dataset.time){var u=document.createElement('p');u.innerHTML='<label><input type="checkbox" id="eput"> Play untimed</label>';el.parentNode.insertBefore(u,el);to={time:+el.dataset.time,untimed:function(){var c=$('#eput');return c&&c.checked}}}
  if(el.dataset.deal2){deal2(el,function(f,t){var b=document.createElement('div');el.appendChild(b);b.innerHTML='<h3 aria-level="2">Now the briefing questions</h3><div id="eq"></div>';runQs($('#eq'),qs,'ep'+n,to,function(s){win(s+f,qs.length+t)})});return}
  if(el.dataset.leak){leak(el,{ep:1,done:function(f,t){var b=document.createElement('div');el.appendChild(b);setTimeout(function(){b.innerHTML='<h3 aria-level="2">Now the briefing questions</h3><div id="eq"></div>';runQs($('#eq'),qs,'ep'+n,{untimed:function(){return true}},function(s){win(s+f,qs.length+t)})},50)}})}
  else runQs(el,qs,'ep'+n,to,win);
}
function hub(){[].forEach.call(document.querySelectorAll('[data-epst]'),function(e){var v=get('ep'+e.dataset.epst,null);if(v)e.textContent='Cleared · '+v.rank});var st=get('streak',null),s=$('#hubstreak');if(s&&st)s.textContent='Daily streak: '+st.n}
document.addEventListener('DOMContentLoaded',function(){
  var g=$('[data-game]');[].forEach.call(document.querySelectorAll('[data-drop]'),countdown);hub();
  if(!g)return;({daily:daily,leak:leak,deal:deal,quiz:quiz,ep:ep})[g.dataset.game](g);
});
})();
