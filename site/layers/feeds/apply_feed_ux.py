"""Six preview-only feed UX layers. Invoked by apply_feeds.py, never independently publishes."""
import sys as _s,pathlib as _p;_s.path.insert(0,str(_p.Path(__file__).resolve().parent.parent));from _mwguard import sensitive as _mw_sensitive
from pathlib import Path
from bs4 import BeautifulSoup as BS
from PIL import Image,ImageDraw,ImageFont
import json,html,datetime as dt,re,random,subprocess,urllib.parse,hashlib,shutil
H=Path(__file__).parent;D=H.parent/'site_calm';A=D/'assets/feeds';BASE='https://calm.themarginwars.pages.dev';TODAY='2026-11-08'
MARKETS={'us':'US','ukeu':'UK / EU','br':'Brazil','ca-latam':'Canada & LATAM','anz':'AU & NZ','global':'Global'}
RAILS={'cards':'Cards','bank':'Bank / ACH','instant':'Instant / A2A','authentication':'Authentication','cross-border':'Cross-border','infrastructure':'Infrastructure'}
e=html.escape
leads={
'au-surcharging':('neutral','Recheck checkout pricing: designated card-network surcharge rules changed.'),
'au-domestic-interchange':('cost down','Lower domestic interchange caps make pass-through worth checking; net merchant savings depend on your terms.'),
'au-net-compensation':('neutral','Check issuer incentives against the amended compensation rules.'),
'au-network-disclosure':('deadline','Use the new scheme-fee disclosures to challenge unexplained line items.'),
'au-acquirer-disclosure':('deadline','Compare published acquirer fees with your own card mix and contract.'),
'au-pass-through':('deadline','Ask your acquirer how the interchange reduction reached your statement.'),
'au-foreign-cards':('deadline','Review foreign-card pricing before the new caps apply.'),
'au-statements':('deadline','Make sure the new statement detail reaches your reconciliation process.'),
'au-scheme-roadmap':('neutral','Watch for the fee roadmap; it is not itself a price cap.'),
'nz-commercial-cards':('cost down','Lower regulated commercial-card interchange is coming; confirm what your acquirer passes through.'),
'ach-same-day-limit':('deadline','Check whether the larger Same Day ACH limit changes your payout routing.'),
'ach-availability':('deadline','Check payout promises against the receiving bank’s 9am availability duty.'),
'ach-iat':('deadline','Review how your ACH provider classifies international entries.'),
'ach-availability-exceptions':('deadline','Ask your bank which availability exceptions affect your credits.'),
'ach-iat-date-of-birth':('deadline','Check how your IAT integration will handle the optional date-of-birth field.'),
'ach-iat-contacts':('deadline','Confirm ownership of IAT contact registration with your ACH provider.'),
'uk-pricing-governance':('deadline','Ask for evidence behind relevant UK scheme-fee decisions, not a savings promise.'),
'uk-fee-transparency':('deadline','Prepare to reconcile fee triggers with acquiring invoices.'),
'uk-fee-logic-extension':('deadline','Some fee logic arrives later; acquirers can request it during the extension.'),
'uk-safeguarding':('neutral','Check how your provider reconciles and safeguards customer funds.'),
'eu-psr-position':('neutral','Track the EU legislative process; this milestone is not an application date.'),
'eu-psd3-position':('neutral','Track PSD3 separately from PSR; do not treat this vote as a go-live date.'),
'uk-rtgs-delay':('neutral','Remove the superseded November release from your implementation plan.'),
'ca-rtr-launch':('deadline','Check provider readiness for the scheduled RTR launch, not assumed availability.'),
'ca-eu-interlink':('neutral','Keep the proposed connection on your roadmap, not your live-route inventory.'),
'pix-dict-default':('neutral','Check refund integrations that rely on implicit monitoring defaults.'),
'pix-dict-rc':('neutral','Review recovery API changes before implementation; a candidate release is not a deadline.'),
'emv-3ds24':('neutral','Watch the 3DS draft; do not schedule a mandatory migration on this source alone.'),
'emv-3ds-extensions':('neutral','Ask your 3DS provider whether its product qualifies for the extension.'),
'emv-agentic-draft':('neutral','Separate consumer-intent design work from deployed network requirements.'),
'us-regii-watch':('neutral','Monitor the official docket; do not price a new debit cap from this preview.')}
def rail(x):
 id=x['id'];m=x['market']
 if id.startswith('emv-'):return ['cards','authentication'] if '3ds' in id else ['cards']
 if id.startswith('pix-'):return ['instant']
 if id.startswith('ach-'):return ['bank','cross-border'] if 'iat' in id else ['bank']
 if id=='uk-safeguarding':return ['bank','infrastructure']
 if id in ['eu-psr-position','eu-psd3-position']:return ['cards','bank','instant','authentication']
 if id=='uk-rtgs-delay':return ['bank','infrastructure']
 if id.startswith('ca-'):return ['instant','infrastructure']+(['cross-border'] if id=='ca-eu-interlink' else [])
 return ['cards']
def node(s):return BS(s,'html.parser')
def itemurl(kind,id):return f'/{kind}/items/{id}/'
def toolbar(where):
 checks=lambda group,vals:''.join(f'<label class="fx-check"><input type="checkbox" name="{group}" value="{k}"><span>{e(v)}</span></label>' for k,v in vals.items())
 return f'''<!--feed-ux-controls--><div class="fx-tools" data-fx-tools hidden><nav class="fx-actions" aria-label="Research controls"><button type="button" data-prefs-open aria-expanded="false">My markets</button><button type="button" data-search-open>Search <kbd>/</kbd></button><a href="/digest/">Weekly digest</a></nav><p class="fx-visit" data-since aria-live="polite">All markets · all rails</p><section class="fx-prefs" hidden aria-label="My markets"><p class="f-k">Saved only in this browser. No account.</p><form><fieldset><legend>Markets</legend><div class="fx-checkgrid">{checks('market',MARKETS)}</div></fieldset><fieldset><legend>Rails & controls</legend><div class="fx-checkgrid">{checks('rail',RAILS)}</div></fieldset><div class="fx-prefbottom"><button type="button" data-prefs-reset>Show everything</button><p class="fx-prefs-status" aria-live="polite">No selection means all.</p></div></form></section></div><!--/feed-ux-controls-->'''
def search_dialog():
 return '''<dialog class="fx-search" aria-labelledby="fx-search-title"><div class="fx-searchhead"><h2 id="fx-search-title">Find the line item.</h2><button type="button" data-search-close aria-label="Close search">Close ✕</button></div><label for="fx-search-input">Search rules, dates and moves</label><input id="fx-search-input" type="search" placeholder="Try 3DS, Pix or interchange" autocomplete="off"><p class="fx-searchhint">↑ ↓ move · Enter opens · Esc closes. My markets applies.</p><p data-search-count role="status"></p><ol class="fx-results"></ol></dialog>'''
def scripts(soup):
 for src in ['/assets/feeds-ux.css']:
  if not soup.select_one(f'link[href="{src}"]'):soup.head.append(node(f'<link rel="stylesheet" href="{src}">'))
 for src in ['/assets/feeds-index.js','/assets/feeds-ux.js']:
  if not soup.select_one(f'script[src="{src}"]'):soup.head.append(node(f'<script src="{src}" defer></script>'))
 if not soup.select_one('.fx-search'):soup.body.append(node(search_dialog()))
def sharecontrols(kind,x):
 return f'''<section class="fx-share" aria-label="Share this item"><p class="f-k">Copy, then review before sharing.</p><div class="fx-shareactions"><button type="button" hidden data-snippet="linkedin" data-key="{kind}:{x['id']}">Copy LinkedIn text</button><button type="button" hidden data-snippet="email" data-key="{kind}:{x['id']}">Copy email text</button><a href="/assets/feeds/cards/{kind}-{x['id']}.png">Open share card ↗</a></div><p class="fx-copy-status" role="status"></p></section>'''
def prepare_annotations(wire):
 annotations={x['id']:{'impact':leads.get(x['id'],('neutral','Review the official source before changing your payment flow.'))[0],'so_what':leads.get(x['id'],('neutral','Review the official source before changing your payment flow.'))[1],'rails':rail(x)} for x in wire}
 # Preserve reviewed annotations for future daily research; never silently infer cost direction.
 annotation_file=A/'ux.json'
 if annotation_file.exists():annotations.update(json.loads(annotation_file.read_text()))
 for x in wire:
  a=annotations[x['id']];a['source']=x['source']
  assert a['impact'] in ['cost up','cost down','deadline','neutral']
  assert a['rails'] and all(r in RAILS for r in a['rails'])
  assert isinstance(a['so_what'],str) and len(a['so_what'])<=250
  assert not _mw_sensitive(json.dumps(a)),x['id']
 annotation_file.write_text(json.dumps(annotations,ensure_ascii=False,indent=2)+'\n')
 return annotations

def apply():
 wire=json.loads((A/'wire.json').read_text());cal=json.loads((A/'calendar.json').read_text());bp=json.loads((A/'bp-watch.json').read_text());routes=json.loads((A/'route-briefs.json').read_text())
 wire.sort(key=lambda x:(-dt.date.fromisoformat(x.get('published',x['date'])).toordinal(),x.get('rank',100)))
 annotations=prepare_annotations(wire)
 index=[];lookup={x['id']:x for x in wire};allitems=[]
 for kind,items in [('wire',wire),('calendar',cal),('bp-watch',bp),('route-briefs',routes)]:
  for x in items:
   ref=x['id'] if kind=='wire' else x['wire_id'];ann=annotations[ref]
   lead=ann['so_what'] if kind!='bp-watch' else x['move']
   rec=dict(key=kind+':'+x['id'],id=x['id'],kind=kind,title=x['title'],market=x['market'],market_label=MARKETS[x['market']],rails=ann['rails'],rail_labels=[RAILS[r] for r in ann['rails']],impact=ann['impact'],lead=lead,source=x['source'],date=x['date'],published=x.get('published',x.get('added',x['date']))+'T14:00:00Z',effective=x.get('effective') if kind=='wire' else x['date'] if kind=='calendar' else None,url=itemurl(kind,x['id']),source_date=x.get('source_date'))
   rec['text']=' '.join(str(x.get(k,'')) for k in ['changed','description','hits','method','impact','move'])
   rec['linkedin']=f"{x['title']}\n\nSo what for merchants: {lead}\n\nOfficial source: {x['source']}\nRead the brief: {BASE+rec['url']}\n\nPreview, pending Avi’s review."
   rec['email']=f"Subject: Payments watch — {x['title']}\n\n{lead}\n\nOfficial source: {x['source']}\nBrief: {BASE+rec['url']}\n\nPreview, pending Avi’s review."
   index.append(rec);allitems.append((kind,x,ann,rec))
 (A/'search-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');(D/'assets/feeds-index.js').write_text('window.MWFeedIndex='+json.dumps(index,ensure_ascii=False).replace('</','<\\/')+';\n')
 for f in ['feeds-ux.css','feeds-ux.js']:shutil.copy(H/f,D/'assets'/f)
 # Render cards deterministically at build, using installed brand fonts.
 carddir=A/'cards';carddir.mkdir(exist_ok=True);fontfile='@MW_FONTS@/SchibstedGrotesk-Regular.ttf';monofile=subprocess.check_output(['fc-match','Martian Mono','-f','%{file}'],text=True)
 def font(n,mono=False):return ImageFont.truetype(monofile if mono else fontfile,n)
 def wrap(text,f,width):
  words=text.split();out=[];line=''
  for word in words:
   test=(line+' '+word).strip()
   if f.getlength(test)>width and line:out.append(line);line=word
   else:line=test
  if line:out.append(line)
  return out
 for kind,x,ann,r in allitems:
  cp=carddir/f'{kind}-{x["id"]}.png';finger=hashlib.sha256(('impact-card-v2'+json.dumps(r,sort_keys=True)).encode()).hexdigest();fp=cp.with_suffix('.sha256')
  if cp.exists() and fp.exists() and fp.read_text()==finger:continue
  im=Image.new('RGB',(1200,630),'#101315');draw=ImageDraw.Draw(im)
  rng=random.Random(31)
  for _ in range(9000):
   px=rng.randrange(1200);py=rng.randrange(630);draw.point((px,py),fill=rng.choice(['#121518','#14171A','#0F1214']))
  draw.rectangle((24,24,1175,605),outline='#62666A',width=1);draw.line((64,104,1136,104),fill='#B5237F',width=4)
  draw.text((64,55),'THE MARGIN WARS',font=font(28,True),fill='#F4F6F7');draw.text((1136,55),kind.upper(),font=font(20,True),fill='#F3A5D6',anchor='ra')
  draw.text((64,134),r['market_label'].upper()+' / '+ann['impact'].upper(),font=font(26,True),fill='#F3A5D6')
  lines=wrap(x['title'],font(61),1065);y=180
  for ln in lines:draw.text((64,y),ln,font=font(61),fill='#F4F6F7');y+=70
  y=max(y+24,345)
  for ln in wrap(r['lead'],font(40),1060):draw.text((64,y),ln,font=font(40),fill='#CFD5DA');y+=48
  host=urllib.parse.urlparse(x['source']).netloc.removeprefix('www.');draw.line((64,534,1136,534),fill='#62666A');draw.text((64,554),'SOURCE / '+host,font=font(18,True),fill='#CFD5DA');draw.text((1136,554),'PREVIEW · PENDING REVIEW',font=font(12,True),fill='#F3A5D6',anchor='ra');im.save(cp);fp.write_text(finger)
 # Modify only generated feed pages; Home changes remain inside the marked strip.
 for slug,kind,items in [('wire','wire',wire),('calendar','calendar',cal),('bp-watch','bp-watch',bp),('feeds','route-briefs',routes)]:
  path=D/slug/'index.html';soup=BS(path.read_text(),'html.parser');scripts(soup)
  hero=soup.select_one('.f-hero');hero.insert_after(node(toolbar(slug)))
  for jump in soup.select('.f-jumps'):jump.decompose()
  nav=soup.select_one('.f-header nav')
  if not nav.select_one('a[href="/digest/"]'):nav.append(node('<a href="/digest/">Digest</a>'))
  oldfilter=soup.select_one('.f-filter')
  if oldfilter:
   refinement=node('<details class="fx-refine" hidden><summary>Refine this page <span aria-hidden="true">＋</span></summary></details>');rd=refinement.details;oldfilter.insert_before(refinement);rd.append(oldfilter.extract())
  byid={x['id']:x for x in items}
  for art in soup.select('.f-entry'):
   id=art.get('id');x=byid.get(id)
   if x is None and id and id.startswith('update-'):x=byid.get(id[7:])
   if x is None:continue
   ref=x['id'] if kind=='wire' else x.get('wire_id');ann=annotations.get(ref,{'rails':['cards'],'impact':'neutral','so_what':''})
   art['data-rails']=' '.join(ann['rails']);art['data-market']=x['market'];art['data-published']=x.get('published',x.get('added',x['date']))+'T14:00:00Z'
   main=art.find_all('div',recursive=False)[-1];heading=main.find(['h2','h3'],recursive=False);heading.extract()
   if heading.a:
    if kind=='route-briefs':
     target=heading.a['href'];main.append(node(f'<div class="f-links"><a href="{e(target)}">Open Route Brief →</a><a href="{itemurl(kind,x["id"])}">Permalink</a></div>'))
    heading.a.unwrap()
   summary=node('<details class="fx-details"><summary>Rule, source & share <span aria-hidden="true">＋</span></summary><div class="fx-detailbody"></div></details>');body=summary.select_one('.fx-detailbody')
   for child in list(main.contents):body.append(child.extract())
   body.append(node(sharecontrols(kind,x)));main.append(heading)
   main.append(node(f'<p class="fx-impact" data-impact="{ann["impact"]}">{ann["impact"]}</p><p class="fx-so"><span>So what for merchants</span>{e(ann["so_what"] if kind!="bp-watch" else x["move"])}</p>'))
   main.append(summary)
   if kind=='calendar':
    art['data-event-date']=x['date'];main.insert(0,node(f'<p class="fx-countdown" data-countdown="{x["date"]}">Date fixed · {x["date"]}</p>'))
   # True share permalink, separate from parent-page anchors.
   for a in art.select('.f-links a'):
    if a.get_text(strip=True)=='Permalink':a['href']=itemurl(kind,x['id'])
  # Market-specific subscriptions and route updates participate in My markets.
  if slug=='feeds':
   for cell,m in zip(soup.select('.f-market'),MARKETS):cell['data-market']=m;cell['data-fx-filter']='true'
  if slug=='calendar':
   timeline='<section class="fx-timeline" aria-labelledby="fx-timeline-h"><p class="f-k">Terrain / the next dated moves</p><h2 id="fx-timeline-h">One timeline per market.</h2><p class="f-note">Day counts use today’s Pacific date. Source dates remain all-day jurisdiction dates.</p>'
   for m,label in MARKETS.items():
    events=sorted([x for x in cal if x['market']==m and x['date']>=TODAY],key=lambda x:x['date'])
    rs=sorted({r for z in events for r in annotations[z['wire_id']]['rails']});nextdate=(f'<span data-countdown="{events[0]["date"]}">{events[0]["date"]}</span>' if events else '<span>No confirmed date</span>')
    timeline+=f'<div class="fx-timeline-row" data-market="{m}" data-rails="{" ".join(rs)}" data-fx-filter="true"><details><summary><strong>{e(label)}</strong>{nextdate}</summary><ol>'
    for x in events:
     ann=annotations[x['wire_id']];timeline+=f'<li data-market="{m}" data-rails="{" ".join(ann["rails"])}" data-fx-filter="true" data-event-date="{x["date"]}"><time datetime="{x["date"]}">{e(x["date"])}</time><a href="{itemurl("calendar",x["id"])}">{e(x["title"])}</a><span data-countdown="{x["date"]}">Date fixed</span></li>'
    if not events:timeline+='<li class="f-note">No confirmed upcoming date in this edition.</li>'
    timeline+='</ol></details></div>'
   timeline+='</section>';soup.select_one('.f-calendar').insert(0,node(timeline))
  # Upgrade old in-page rule links to item URLs with OG metadata.
  for a in soup.select('a[href^="/wire/#"]'):a['href']=itemurl('wire',a['href'].split('#')[-1])
  path.write_text(str(soup))
 # Individual item pages have server-rendered OG metadata; sharing does not depend on JS.
 for kind,x,ann,r in allitems:
  parent_slug='feeds' if kind=='route-briefs' else kind
  parent=BS((D/parent_slug/'index.html').read_text(),'html.parser');article=parent.find(id=('update-' if kind=='route-briefs' else '')+x['id']);assert article
  article.select_one('details')['open']='';article.find(['h2','h3']).name='h1';article['class']=article.get('class',[])+['fx-single']
  new=BS((D/parent_slug/'index.html').read_text(),'html.parser');main=new.select_one('#f-main');main.clear();main.append(node(f'<p class="fx-back"><a href="/{parent_slug}/">← Back to {kind.replace("-"," ")}</a></p>'));main.append(node(toolbar('item')));main.append(node(f'<section class="fx-itemhero"><p class="f-k">{e(kind)} / sourced decision brief</p></section>'));main.append(article);main.append(node(f'<figure class="fx-cardproof"><img src="/assets/feeds/cards/{kind}-{x["id"]}.png" alt="Share card: {e(x["title"])}" width="1200" height="630"><figcaption>Preview share artwork. Copy text only; nothing posts automatically.</figcaption></figure>'));main.append(node('<p class="f-live" aria-live="polite"></p>'))
  new.title.string=x['title']+' | The Margin Wars — Preview'
  for t in new.select('meta[property^="og:"],meta[name^="twitter:"],link[rel="canonical"]'):t.decompose()
  for prop,value in [('og:type','article'),('og:title',x['title']),('og:description',r['lead']),('og:url',BASE+r['url']),('og:image',BASE+f'/assets/feeds/cards/{kind}-{x["id"]}.png'),('og:image:width','1200'),('og:image:height','630'),('og:image:alt',x['title'])]:new.head.append(node(f'<meta property="{prop}" content="{e(value)}">'))
  new.head.append(node(f'<meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{BASE+r["url"]}">'))
  path=D/r['url'].strip('/')/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(new))
 # Home: keep all enhancements within the strip and feed-owned assets.
 path=D/'index.html';text=path.read_text();match=re.search(r'<!--feeds-home-->(.*?)<!--/feeds-home-->',text,re.S);assert match
 strip_soup=BS(match[1],'html.parser');strip=strip_soup.select_one('.f-strip');assert strip
 for old in strip.select('.fx-tools'):old.decompose()
 strip.select_one('.f-striphead').insert_after(node(toolbar('home')))
 for a in strip.select('.f-stripitem a'):
  id=a.get('href','').split('#')[-1]
  if id in lookup:a['href']=itemurl('wire',id)
 text=text[:match.start(1)]+str(strip_soup)+text[match.end(1):]
 for src,tag in [('/assets/feeds-ux.css','<link rel="stylesheet" href="/assets/feeds-ux.css">'),('/assets/feeds-index.js','<script src="/assets/feeds-index.js" defer></script>'),('/assets/feeds-ux.js','<script src="/assets/feeds-ux.js" defer></script>')]:
  if src not in text:text=text.replace('</head>',tag+'</head>',1)
 if 'class="fx-search"' not in text:text=text.replace('</body>',search_dialog()+'</body>',1)
 path.write_text(text)
 # Only load route-link JS on Advisory; preferences/search aren't injected into unrelated sections.
 # Weekly print edition, with an immutable dated URL retained on later runs.
 asof=dt.date.fromisoformat(max(x['date'] for x in wire));week_end=asof-dt.timedelta(days=(asof.weekday()+1)%7);week_start=week_end-dt.timedelta(days=6);latest=week_end.isoformat()
 week_wire=[x for x in wire if week_start.isoformat()<=x['date']<=latest]
 weekly_bp=[x for x in bp if week_start.isoformat()<=x['date']<=latest]
 top=sorted(week_wire,key=lambda x:x.get('rank',100))[:5];upcoming=sorted([x for x in cal if x['date']>=latest and x.get('added',latest)<=latest],key=lambda x:x['date'])[:3]
 dig=f'<article class="fx-digest"><header class="fx-digesthead"><p class="f-k">The Margin Wars / Weekly signal / {latest}</p><h1>The week. The moves.</h1><p>{week_start.strftime("%d %b")}–{week_end.strftime("%d %b %Y")} · Preview, pending Avi’s review</p><button type="button" hidden data-print>Save as PDF</button><span class="fx-printhelp">Choose Save as PDF in the print dialog.</span></header><section><h2>Three moves to own</h2><div class="fx-digestgrid">'
 for x in weekly_bp:dig+=f'<article><h3>{e(x["title"])}</h3><p>{e(x["move"])}</p><small>{e(x["impact"])}</small><a href="{e(x["source"])}">Official source ↗</a></article>'
 dig+='</div></section><section><h2>Five signals worth opening</h2><ol class="fx-digestsignals">'
 for x in top:dig+=f'<li><strong>{e(MARKETS[x["market"]])}</strong><a href="{itemurl("wire",x["id"])}">{e(x["title"])}</a><a class="fx-digestsource" href="{e(x["source"])}">Source ↗</a></li>'
 dig+='</ol></section><section><h2>Next on the calendar</h2><ul class="fx-digestdates">'
 for x in upcoming:dig+=f'<li><time>{x["date"]}</time><a href="{itemurl("calendar",x["id"])}">{e(x["title"])}</a></li>'
 dig+='</ul></section><footer>Primary sources. No automatic savings claims. Full source links remain clickable in the PDF.</footer></article>'
 template=BS((D/'wire/index.html').read_text(),'html.parser');template.title.string='Weekly Digest | The Margin Wars — Preview';template.body['class']=['f-page','fx-digestpage'];main=template.select_one('#f-main');main.clear();main.append(node(dig));(D/'digest').mkdir(exist_ok=True)
 archives=sorted({p.name for p in (D/'digest').iterdir() if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}',p.name)}|{latest},reverse=True)
 archive='<nav class="fx-digestarchive" aria-label="Digest archive"><span class="f-k">Dated editions</span>'+''.join(f'<a href="/digest/{d}/">{d}</a>' for d in archives)+'</nav>';main.append(node(archive));(D/'digest/index.html').write_text(str(template));ap=D/'digest'/latest;ap.mkdir(exist_ok=True);(ap/'index.html').write_text(str(template))
 print(f'Feed UX: {len(allitems)} OG item pages/cards; shared markets/rails; timeline; search; digest',latest)
