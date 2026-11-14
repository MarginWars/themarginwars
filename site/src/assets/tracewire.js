/* Tracewire: daily payments word-path puzzle. Boards in window.RT_BOARDS (machine-verified unique). */
(function(){
var d=document,root=d.querySelector('[data-game=tracewire]');if(!root)return;
var B=window.RT_BOARDS||[],Q=new URLSearchParams(location.search),PREV=Q.has('preview')&&(/^(review\.themarginwars\.pages\.dev|([a-z0-9-]+\.)?themarginwars-dev\.pages\.dev|localhost|127\.0\.0\.1)$/.test(location.hostname));
var COL=['#2F6FDE','#0E9F7E','#E07A1F','#7A4CD9','#C9A227','#1F8FB3','#5B8C2A','#3D4A5C'];
var R=matchMedia('(prefers-reduced-motion: reduce)').matches;
function pt(){return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date())}
function ls(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem('mw_rt_'+k));localStorage.setItem('mw_rt_'+k,JSON.stringify(v))}catch(e){return null}}
function buzz(p){try{navigator.vibrate&&navigator.vibrate(p)}catch(e){}}
function el(t,c,h){var e=d.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fmt(s){s=Math.max(0,Math.round(s));return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function nice(ds){return new Date(ds+'T12:00:00Z').toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',timeZone:'UTC'})}
var today=pt(),first=B.length?B[0].date:'';
if(!B.length){root.innerHTML='<p>Board unavailable.</p>';return}
if(today<first&&!PREV){
 root.innerHTML='<div class="rt-lock"><p class="rt-k">Launching soon</p><h2>The first board drops '+nice(first)+'</h2><p>A new board every day at midnight PT. Same board for everyone.</p><p class="rt-cd" aria-live="polite"></p></div>';
 var cd=root.querySelector('.rt-cd'),T=Date.parse(first+'T08:00:00Z');
 (function tick(){var s=(T-Date.now())/1000;if(s<=0){location.reload();return}cd.textContent=Math.floor(s/86400)+'d '+Math.floor(s%86400/3600)+'h '+Math.floor(s%3600/60)+'m';setTimeout(tick,30000)})();return}
var idx=0;for(var i=0;i<B.length;i++)if(B[i].date<=today)idx=i;if(!PREV&&today>B[B.length-1].date){root.innerHTML='<div class="rt-lock"><p class="rt-k">Between boards</p><h2>The next board is coming</h2><p>New Tracewire boards are on the way. Play the <a href="daily.html">Daily</a> while you wait.</p></div>';return}
if(PREV&&Q.get('b')){idx=Math.min(B.length-1,Math.max(0,(+Q.get('b')||1)-1))}else if(PREV&&today<first)idx=0;
var b=B[idx],N=b.size,G=b.grid,W=b.words.slice().sort(function(x,y){return b.solution[y].length-b.solution[x].length||(x<y?-1:1)});
var key=b.date,st=ls('s_'+key)||{found:[],hints:0,t:0,done:false,rev:{}};st.rev=st.rev||{};
var colorOf={};W.forEach(function(w,i){colorOf[w]=COL[i%COL.length]});
function cid(r,c){return r+','+c}
var owner={};W.forEach(function(w){b.solution[w].forEach(function(p){owner[cid(p[0],p[1])]=w})});
/* UI */
root.innerHTML='';
var top=el('div','rt-top');
top.innerHTML='<div class="rt-meta"><span class="rt-no">No. '+b.no+'</span><span class="rt-day">'+nice(b.date)+' &middot; '+N+'&times;'+N+'</span></div><h2 class="rt-title">'+esc(b.title)+'</h2><div class="rt-stats"><span class="rt-time" aria-label="Time">0:00</span><span class="rt-h" aria-label="Hints used">Hints 0</span><span class="rt-strk"></span></div>';
root.appendChild(top);
if(PREV){var pk=el('div','rt-pick');var sel='<label>Preview board <select>';B.forEach(function(x,i){sel+='<option value="'+(i+1)+'"'+(i===idx?' selected':'')+'>'+x.no+' &middot; '+nice(x.date)+' &middot; '+x.size+'x'+x.size+'</option>'});pk.innerHTML=sel+'</select></label>';pk.querySelector('select').onchange=function(){Q.set('b',this.value);location.search=Q.toString()};root.insertBefore(pk,top)}
var stage=el('div','rt-stage');stage.style.setProperty('--n',N);var board=el('div','rt-board');board.style.setProperty('--n',N);board.setAttribute('role','grid');board.setAttribute('aria-label','Letter grid');
var svg=d.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','rt-svg');svg.setAttribute('aria-hidden','true');
var tiles={};
for(var r=0;r<N;r++)for(var c=0;c<N;c++){var ch=G[r][c],t=el('div',ch==='#'?'rt-t rt-wall':'rt-t');t.dataset.r=r;t.dataset.c=c;if(ch!=='#'){t.innerHTML='<span>'+ch+'</span>';t.setAttribute('role','gridcell');t.setAttribute('aria-label',ch);tiles[cid(r,c)]=t}board.appendChild(t)}
board.appendChild(svg);stage.appendChild(board);
var toast=el('p','rt-toast');toast.setAttribute('role','status');toast.setAttribute('aria-live','polite');root.appendChild(stage);root.appendChild(toast);
var slots=el('div','rt-slots');root.appendChild(slots);
var tools=el('div','rt-tools');tools.innerHTML='<button type="button" class="rt-b" data-a="undo">Undo</button><button type="button" class="rt-b" data-a="hint">Hint</button><button type="button" class="rt-b" data-a="reset">Reset</button>';root.appendChild(tools);
var how=el('details','rt-how');how.innerHTML='<summary>How to play</summary><p>Find the hidden payments terms. Drag through letters up, down, left or right (never diagonally), then release. Or tap letters one by one and tap the last letter again to submit. Every open tile is used exactly once, and there is exactly one solution.</p><p>Hint reveals the next letter of a word and clears your current path. Undo removes your last word. A new board drops every day at midnight PT; boards get bigger through the week, with the biggest on Sunday.</p>';root.appendChild(how);
var res=el('div','rt-res');res.hidden=true;root.appendChild(res);
function renderSlots(){slots.innerHTML='';W.forEach(function(w){var f=st.found.indexOf(w)>=0,row=el('div','rt-slot'+(f?' on':''));row.style.setProperty('--wc',colorOf[w]);var rv=st.rev[w]||0;for(var i=0;i<w.length;i++){var s=el('i',null,f||i<rv?w[i]:'');if(!f&&i<rv)s.className='rv';if(f)s.style.transitionDelay=(i*35)+'ms';row.appendChild(s)}row.setAttribute('aria-label',f?w:w.length+' letters');slots.appendChild(row)})}
function center(k){var t=tiles[k],bb=board.getBoundingClientRect(),q=t.getBoundingClientRect();return[(q.left+q.width/2-bb.left),(q.top+q.height/2-bb.top)]}
function line(path,col,cls){if(path.length<2&&cls!=='cur')return '';var p=path.map(function(k){return center(k).join(',')}).join(' ');var w=Math.max(6,tiles[path[0]].getBoundingClientRect().width*.22);return '<polyline class="'+cls+'" points="'+p+'" stroke="'+col+'" stroke-width="'+w+'"/>'}
var path=[],moved=false,dragging=false;
function draw(){var bb=board.getBoundingClientRect();svg.setAttribute('viewBox','0 0 '+bb.width+' '+bb.height);var h='';st.found.forEach(function(w){h+=line(b.solution[w].map(function(p){return cid(p[0],p[1])}),colorOf[w],'lk')});if(path.length)h+=line(path,'#111417','cur');svg.innerHTML=h}
function paint(){Object.keys(tiles).forEach(function(k){var t=tiles[k],w=owner[k],f=st.found.indexOf(w)>=0;t.classList.toggle('rt-on',f);t.style.setProperty('--wc',f?colorOf[w]:'');t.classList.toggle('sel',path.indexOf(k)>=0);t.classList.toggle('hd',!f&&hinted(k))});draw();top.querySelector('.rt-h').textContent='Hints '+st.hints}
function hinted(k){var w=owner[k],n=st.rev[w]||0;if(!n)return false;var sp=b.solution[w];for(var i=0;i<n;i++)if(cid(sp[i][0],sp[i][1])===k)return true;return false}
function say(m,cls){toast.textContent=m;toast.className='rt-toast show '+(cls||'');clearTimeout(say.t);say.t=setTimeout(function(){toast.className='rt-toast'},1600)}
function free(k){return tiles[k]&&st.found.indexOf(owner[k])<0}
function adj(a,b2){var x=a.split(','),y=b2.split(',');return Math.abs(x[0]-y[0])+Math.abs(x[1]-y[1])===1}
var t0=null,timer=null;
function startClock(){if(st.done||timer)return;t0=Date.now()-st.t*1000;timer=setInterval(tickC,250)}
function tickC(){st.t=(Date.now()-t0)/1000;top.querySelector('.rt-time').textContent=fmt(st.t);if(Math.round(st.t)%5===0)save()}
function save(){ls('s_'+key,st)}
function extend(k){if(!free(k))return;var i=path.indexOf(k);if(i>=0){if(i===path.length-2){path.pop();buzz(4)}return}if(path.length&&!adj(path[path.length-1],k))return;path.push(k);buzz(6);var t=tiles[k];t.classList.remove('pop');void t.offsetWidth;t.classList.add('pop')}
function submit(){var word=path.map(function(k){return tiles[k].textContent}).join('');var hit=null;W.forEach(function(w){if(st.found.indexOf(w)<0){var sp=b.solution[w].map(function(p){return cid(p[0],p[1])});if(sp.join('|')===path.join('|'))hit=w}});
 if(hit){st.found.push(hit);buzz(R?0:[12,30,18]);lockAnim(hit);path=[];save();renderSlots();paint();if(st.found.length===W.length)win();else say(hit+' locked in','ok');return}
 if(path.length>1){var rw=W.indexOf(word)>=0&&st.found.indexOf(word)<0;say(rw?'Right word, wrong trace':(path.length<3?'Keep tracing':'Not on today\u2019s list'),'no');if(path.length>2){buzz([20,40,20]);path.forEach(function(k){var t=tiles[k];t.classList.remove('shake');void t.offsetWidth;t.classList.add('shake')})}}
 path=[];paint()}
function lockAnim(w){b.solution[w].forEach(function(p,i){var t=tiles[cid(p[0],p[1])];t.style.setProperty('--d',(i*40)+'ms');t.classList.remove('lockin');void t.offsetWidth;t.classList.add('lockin')})}
function tileAt(x,y){var e=d.elementFromPoint(x,y);e=e&&e.closest&&e.closest('.rt-t');if(!e||!board.contains(e)||e.classList.contains('rt-wall'))return null;var q=e.getBoundingClientRect(),dx=x-(q.left+q.width/2),dy=y-(q.top+q.height/2);if(dx*dx+dy*dy>Math.pow(q.width*.46,2))return null;return cid(e.dataset.r,e.dataset.c)}
board.addEventListener('pointerdown',function(e){if(st.done)return;var k=tileAt(e.clientX,e.clientY);if(!k||!free(k))return;e.preventDefault();startClock();try{board.setPointerCapture(e.pointerId)}catch(x){}dragging=true;moved=false;
 if(path.length&&k===path[path.length-1]&&path.length>1){dragging=false;submit();return}
 if(path.length&&(adj(path[path.length-1],k)&&path.indexOf(k)<0)){extend(k)}else if(path.indexOf(k)>=0){path=path.slice(0,path.indexOf(k)+1)}else{path=[k];buzz(6)}paint()});
board.addEventListener('pointermove',function(e){if(!dragging)return;e.preventDefault();var k=tileAt(e.clientX,e.clientY);if(k&&k!==path[path.length-1]){var n=path.length;extend(k);if(path.length!==n)moved=true;paint()}});
function up(){if(!dragging)return;dragging=false;if(moved&&path.length>1)submit()}
board.addEventListener('pointerup',up);board.addEventListener('pointercancel',up);
board.addEventListener('touchmove',function(e){if(dragging)e.preventDefault()},{passive:false});
tools.addEventListener('click',function(e){var a=e.target.closest('button');if(!a||st.done)return;a=a.dataset.a;startClock();
 if(a==='undo'){if(!st.found.length){say('Nothing to undo');return}var w=st.found.pop();say(w+' removed');}
 if(a==='reset'){if(!st.found.length&&!path.length)return;st.found=[];say('Board reset')}
 if(a==='hint'){var cand=W.filter(function(w){return st.found.indexOf(w)<0});var w=cand.sort(function(x,y){return((st.rev[y]||0)/y.length)-((st.rev[x]||0)/x.length)||x.length-y.length})[0];st.rev[w]=(st.rev[w]||0)+1;st.hints++;buzz(10);if(st.rev[w]>=w.length){st.found.push(w);lockAnim(w)}say('Hint: next letter of a '+w.length+'-letter word','hint');}
 path=[];save();renderSlots();paint();if(st.found.length===W.length)win()});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&path.length){path=[];paint()}});
addEventListener('resize',function(){draw()});
function streak(){if(PREV||b.date!==today)return ls('streak')||{n:0,best:0};var s=ls('streak')||{n:0,best:0,last:''};if(s.last===today)return s;var y=new Date(Date.parse(today+'T12:00:00Z')-864e5).toISOString().slice(0,10);s.n=s.last===y?s.n+1:1;s.best=Math.max(s.best,s.n);s.last=today;ls('streak',s);return s}
function shareText(){var sq={'#2F6FDE':'\uD83D\uDFE6','#0E9F7E':'\uD83D\uDFE9','#E07A1F':'\uD83D\uDFE7','#7A4CD9':'\uD83D\uDFEA','#C9A227':'\uD83D\uDFE8','#1F8FB3':'\uD83D\uDFE6','#5B8C2A':'\uD83D\uDFE9','#3D4A5C':'\u2B1B'};var row=W.map(function(w){return sq[colorOf[w]]}).join('');return 'Tracewire No. '+b.no+' ('+b.size+'x'+b.size+')\n'+row+'\n\u23F1 '+fmt(st.t)+' \u00B7 \uD83D\uDCA1 '+st.hints+(st.hints?' hints':' hints, clean run')+'\nPayments people: can you trace it faster?'}
function base(){return location.protocol==='file:'?'https://review.themarginwars.pages.dev/':location.origin+location.pathname.replace(/[^/]*$/,'')}
function cardImg(){var c=d.createElement('canvas');c.width=1200;c.height=627;var x=c.getContext('2d');var g=x.createLinearGradient(0,0,1200,627);g.addColorStop(0,'#8A1A61');g.addColorStop(1,'#B5237F');x.fillStyle=g;x.fillRect(0,0,1200,627);
 x.fillStyle='#fff';x.font='900 88px "Big Shoulders Display", sans-serif';x.fillText('TRACEWIRE',64,130);x.font='700 30px Archivo, sans-serif';x.globalAlpha=.85;x.fillText('No. '+b.no+'  \u00B7  '+nice(b.date)+'  \u00B7  '+b.size+'\u00D7'+b.size,64,180);x.globalAlpha=1;
 x.font='900 150px "Big Shoulders Display", sans-serif';x.fillText(fmt(st.t),64,380);x.font='700 34px Archivo, sans-serif';x.fillText(st.hints?st.hints+(st.hints>1?' hints':' hint'):'No hints. Clean run.',64,440);
 x.font='800 30px Archivo, sans-serif';x.fillText('Payments people: can you trace it faster?',64,560);
 var S=Math.min(64,420/N),ox=1200-64-S*N,oy=(627-S*N)/2;x.fillStyle='rgba(255,255,255,.12)';x.beginPath();x.roundRect?x.roundRect(ox-14,oy-14,S*N+28,S*N+28,22):x.rect(ox-14,oy-14,S*N+28,S*N+28);x.fill();
 for(var r=0;r<N;r++)for(var cc=0;cc<N;cc++){var k=cid(r,cc);x.fillStyle=G[r][cc]==='#'?'rgba(17,20,23,.45)':colorOf[owner[k]];x.beginPath();var px=ox+cc*S+4,py=oy+r*S+4;x.roundRect?x.roundRect(px,py,S-8,S-8,S*.18):x.rect(px,py,S-8,S-8);x.fill();if(G[r][cc]!=='#'){x.strokeStyle='rgba(255,255,255,.6)';x.lineWidth=2;x.stroke()}}
 x.font='700 22px Archivo, sans-serif';x.fillStyle='rgba(255,255,255,.8)';x.fillText('The Margin Wars  |  Arcade',64,600);return c}
function win(){st.done=true;clearInterval(timer);timer=null;save();var s=streak();root.classList.add('solved');buzz([20,60,20,60,40]);
 Object.keys(tiles).forEach(function(k,i){tiles[k].style.setProperty('--d',((+k.split(',')[0]+ +k.split(',')[1])*45)+'ms');tiles[k].classList.add('wave')});
 var src=b.sources.map(function(x){return '<a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+(x.kind==='history'?'History source':'Payments source')+'</a>'}).join(' &middot; ');
 res.innerHTML='<p class="rt-k">Tracewire</p><h3>Solved in '+fmt(st.t)+'</h3><div class="rt-sum"><div><b>'+fmt(st.t)+'</b><span>Time</span></div><div><b>'+st.hints+'</b><span>Hints</span></div><div><b>'+(s.n||0)+'</b><span>Streak</span></div><div><b>'+(s.best||0)+'</b><span>Best</span></div></div>'+
 '<div class="rt-story"><p class="rt-k">Season 1, Episode '+b.ep+' &middot; From the war room</p><p>'+esc(b.story.history)+' '+esc(b.story.payments)+'</p><p class="rt-tac"><b>Tactic:</b> '+esc(b.story.tactic)+'</p><p class="fine">'+src+'. Historical claims follow museum and historical sources; we say "associated with", not "invented by".</p><a class="rt-ep" href="ep'+b.ep+'.html">Play Episode '+b.ep+'</a></div>'+
 '<div class="rt-share"><img class="rt-card" alt="Score card for Tracewire No. '+b.no+'"><pre class="rt-txt"></pre><div class="rt-sb"><button type="button" class="rt-b pri" data-s="copy">Copy result</button><a class="rt-b" target="_blank" rel="noopener" data-s="li">Share on LinkedIn</a><a class="rt-b" data-s="dl" download="tracewire-'+b.no+'.png">Download card</a></div><p class="fine">Nothing is posted for you. Copy the text, attach the card, and tag the payments people you want to beat.</p></div><p class="rt-next"></p>';
 res.hidden=false;var tx=shareText();res.querySelector('.rt-txt').textContent=tx;
 var draw2=function(){var c=cardImg(),u=c.toDataURL('image/png');res.querySelector('.rt-card').src=u;res.querySelector('[data-s=dl]').href=u};(d.fonts&&d.fonts.ready?d.fonts.ready:Promise.resolve()).then(draw2);
 res.querySelector('[data-s=li]').href='https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(base()+'tracewire.html?utm_source=linkedin&utm_medium=social&utm_campaign=visitor-share&utm_content=tracewire');
 res.querySelector('[data-s=copy]').onclick=function(){var bt=this;(navigator.clipboard?navigator.clipboard.writeText(tx+'\n'+base()+'tracewire.html'):Promise.reject()).then(function(){bt.textContent='Copied'},function(){bt.textContent='Select the text above'})};
 var nx=res.querySelector('.rt-next');(function tk(){var n=new Date(),p=new Date(n.toLocaleString('en-US',{timeZone:'America/Los_Angeles'})),m=new Date(p);m.setHours(24,0,0,0);var s2=(m-p)/1000;nx.textContent='Next board in '+Math.floor(s2/3600)+'h '+Math.floor(s2%3600/60)+'m';setTimeout(tk,30000)})();
 setTimeout(function(){res.scrollIntoView({behavior:R?'auto':'smooth',block:'start'})},R?0:700)}
var sk=ls('streak');if(sk&&sk.n)top.querySelector('.rt-strk').textContent='Streak '+sk.n;
renderSlots();paint();top.querySelector('.rt-time').textContent=fmt(st.t);
if(st.done){root.classList.add('solved');win()}
window.RT={board:b,solve:function(){return b.solution},state:st};
})();
