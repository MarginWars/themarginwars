#!/usr/bin/env python3
"""Idempotent preview-only feed layer. Run AFTER copy, UI and Route Brief scripts.
Source of truth: site_calm/assets/feeds/*.json. No network or publishing side effects.
"""
import sys as _s,pathlib as _p;_s.path.insert(0,str(_p.Path(__file__).resolve().parent.parent));from _mwguard import sensitive as _mw_sensitive
import datetime as dt,html,json,os,re,shutil,urllib.parse,xml.etree.ElementTree as ET
from email.utils import format_datetime
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parent/'site_calm';DATA=ROOT/'assets/feeds';OUT=ROOT/'feeds'
BASE=os.environ.get('FEED_BASE_URL','https://calm.themarginwars.pages.dev').rstrip('/')
assert 'themarginwars.pages.dev' in BASE and BASE!='https://themarginwars.pages.dev','Preview feed base required'
NOW='2026-11-08';STAMP=NOW+'T14:00:00Z';PREVIEW='Preview, pending Avi’s review'
MARKETS={'us':'US','ukeu':'UK / EU','br':'Brazil','ca-latam':'Canada & LATAM','anz':'AU & NZ','global':'Global'}
TYPES=['network rule','regulation','policy'];e=html.escape
OUT.mkdir(exist_ok=True);DATA.mkdir(exist_ok=True)
def load(n):return json.loads((DATA/(n+'.json')).read_text())
wire=load('wire');dates=load('calendar');bp=load('bp-watch');routes=load('route-briefs')
NOW=max(x.get('published',x['date']) for x in wire+bp+routes);STAMP=NOW+'T14:00:00Z'
# Validate editorial inputs early. Null effective dates are intentional, never guessed.
for name,items in [('wire',wire),('calendar',dates),('bp-watch',bp),('route-briefs',routes)]:
 assert len({i['id'] for i in items})==len(items),name+' duplicate IDs'
 for x in items:
  assert re.fullmatch('[a-z0-9-]+',x['id']),x['id']
  assert x['source'].startswith('https://'),x
  dt.date.fromisoformat(x['date'])
  if x.get('effective'):dt.date.fromisoformat(x['effective'])
  assert x.get('market') in MARKETS,x
  if name=='wire':assert x['type'] in TYPES
  text=json.dumps(x).lower()
  assert not _mw_sensitive(text),('prohibited term',x['id'])
for f in ['feeds.css','feeds.js']:shutil.copyfile(H/f,ROOT/'assets'/f)
def day(d):return dt.date.fromisoformat(d).strftime('%d %b %Y').lstrip('0')
def href(path):return BASE+path
AT='http://www.w3.org/2005/Atom';ET.register_namespace('atom',AT)
def desc(x,kind):
 if kind=='wire':return f"{PREVIEW}. {x['changed']} Who: {x['hits']}. Effective: {x.get('effective') or 'Not confirmed / not applicable'}. Official source: {x['source']}"
 if kind=='bp-watch':return f"{PREVIEW}. {x['impact']} Method: {x['method']} The move: {x['move']} Official source: {x['source']}"
 return f"{PREVIEW}. {x.get('description','')} Official source: {x['source']}"
# Share the reviewed impact annotations with RSS/Atom/JSON, not only the web view.
from apply_feed_ux import prepare_annotations
FEED_ANNOTATIONS=prepare_annotations(wire)
_original_desc=desc
def desc(x,kind):
 a=FEED_ANNOTATIONS.get(x['id'] if kind=='wire' else x.get('wire_id',''))
 lead=(x['move'] if kind=='bp-watch' else a['so_what']) if a else ''
 return (f"[{a['impact']}] So what for merchants: {lead} " if a else '')+_original_desc(x,kind)
def url(x,kind):
 return href('/'+('calendar' if kind=='calendar' else kind)+'/items/'+x['id']+'/')
def tag(p,name,text=None,**attrs):
 q=ET.SubElement(p,name,attrs)
 if text is not None:q.text=str(text)
 return q
def rss(name,title,items,kind,page):
 r=ET.Element('rss',{'version':'2.0'});c=tag(r,'channel');tag(c,'title','The Margin Wars | '+title+' [Preview]');tag(c,'link',href(page));tag(c,'description',PREVIEW+' — official sources, practical moves.');tag(c,'language','en-us');tag(c,'lastBuildDate',format_datetime(dt.datetime.fromisoformat(STAMP.replace('Z','+00:00'))));tag(c,'{'+AT+'}link',href=href('/feeds/'+name+'.xml'),rel='self',type='application/rss+xml')
 for x in items:
  i=tag(c,'item');tag(i,'title',x['title']);tag(i,'link',url(x,kind));tag(i,'guid',href('/feeds/id/'+kind+'/'+x['id']),isPermaLink='false');tag(i,'pubDate',format_datetime(dt.datetime.fromisoformat((x.get('published',x.get('added',x['date'])))+'T14:00:00+00:00')));tag(i,'description',desc(x,kind));tag(i,'category',MARKETS[x['market']])
 ET.ElementTree(r).write(OUT/(name+'.xml'),encoding='utf-8',xml_declaration=True)
def atom(name,title,items,kind,page):
 ns='{'+AT+'}';a=ET.Element(ns+'feed');tag(a,ns+'title','The Margin Wars | '+title+' [Preview]');tag(a,ns+'id',href('/feeds/'+name+'.atom'));tag(a,ns+'updated',STAMP);tag(a,ns+'subtitle',PREVIEW);tag(a,ns+'link',href=href('/feeds/'+name+'.atom'),rel='self',type='application/atom+xml');tag(a,ns+'link',href=href(page));author=tag(a,ns+'author');tag(author,ns+'name','The Margin Wars')
 for x in items:
  q=tag(a,ns+'entry');tag(q,ns+'title',x['title']);tag(q,ns+'id',href('/feeds/id/'+kind+'/'+x['id']));tag(q,ns+'updated',(x.get('published',x.get('added',x['date'])))+'T14:00:00Z');tag(q,ns+'link',href=url(x,kind));tag(q,ns+'summary',desc(x,kind));tag(q,ns+'category',term=x['market'])
 ET.ElementTree(a).write(OUT/(name+'.atom'),encoding='utf-8',xml_declaration=True)
def jsonfeed(name,title,items,kind,page):
 obj=dict(version='https://jsonfeed.org/version/1.1',title='The Margin Wars | '+title+' [Preview]',home_page_url=href(page),feed_url=href('/feeds/'+name+'.json'),description=PREVIEW,language='en-US',items=[dict(id=href('/feeds/id/'+kind+'/'+x['id']),url=url(x,kind),title=x['title'],content_text=desc(x,kind),date_published=x.get('published',x.get('added',x['date']))+'T14:00:00Z',tags=[MARKETS[x['market']]]) for x in items]);(OUT/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def bundle(name,title,items,kind,page):
 rss(name,title,items,kind,page);atom(name,title,items,kind,page);jsonfeed(name,title,items,kind,page)
# Current research batch: publication timestamps describe this briefing, not the source's announcement.
wire.sort(key=lambda x:(-dt.date.fromisoformat(x.get('published',x['date'])).toordinal(),x.get('rank',100)))
bundle('wire','The Rulebook Wire',wire,'wire','/wire/')
for m,l in MARKETS.items():bundle('wire-'+m,'The Rulebook Wire / '+l,[x for x in wire if x['market']==m],'wire','/wire/?market='+m)
bundle('bp-watch','Basis-Point Watch',bp,'bp-watch','/bp-watch/')
bundle('calendar','Effective-Date Calendar',dates,'calendar','/calendar/')
bundle('route-briefs','Route Brief Updates',routes,'route-briefs','/feeds/#route-updates')
def icaltext(s):return s.replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
def fold(s):
 lines=[];cur='';n=0
 for c in s:
  b=len(c.encode('utf8'))
  if n+b>75:lines.append(cur);cur=' '+c;n=1+b
  else:cur+=c;n+=b
 lines.append(cur);return '\r\n'.join(lines)
ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//The Margin Wars//Effective Dates Preview//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:The Margin Wars — Preview dates','X-WR-CALDESC:'+icaltext(PREVIEW+'; all-day source-calendar dates, not Pacific-time deadlines. Past milestones retained for context.')]
for x in dates:
 start=dt.date.fromisoformat(x['date']);end=start+dt.timedelta(days=1)
 ics+=['BEGIN:VEVENT','UID:'+x['id']+'@themarginwars.com','DTSTAMP:20261108T140000Z','DTSTART;VALUE=DATE:'+start.strftime('%Y%m%d'),'DTEND;VALUE=DATE:'+end.strftime('%Y%m%d'),'SUMMARY:'+icaltext('[PREVIEW] '+x['title']),'DESCRIPTION:'+icaltext(x['kind']+'. '+x['description']+'\nOfficial source: '+x['source']+'\n'+PREVIEW),'URL:'+url(x,'calendar'),'TRANSP:TRANSPARENT',('STATUS:TENTATIVE' if x['kind']=='Policy expectation' else 'STATUS:CONFIRMED'),'SEQUENCE:0','END:VEVENT']
ics+=['END:VCALENDAR'];(OUT/'dates.ics').write_bytes(('\r\n'.join(fold(s) for s in ics)+'\r\n').encode())
AUTO='<!--feeds-discovery-->'+''.join(f'<link rel="alternate" type="{typ}" title="{e(title)} [Preview]" href="/feeds/{file}">' for typ,title,file in [('application/rss+xml','The Rulebook Wire','wire.xml'),('application/atom+xml','The Rulebook Wire — Atom','wire.atom'),('application/feed+json','The Rulebook Wire — JSON','wire.json'),('application/rss+xml','Basis-Point Watch','bp-watch.xml'),('application/rss+xml','Effective Dates','calendar.xml'),('text/calendar','Effective Dates — calendar','dates.ics'),('application/rss+xml','Route Brief Updates','route-briefs.xml')])+'<!--/feeds-discovery-->'
def subscribe(name,label='Copy RSS URL'):
 return f'<div class="f-subscribe"><a href="/feeds/{name}.xml">RSS</a><a href="/feeds/{name}.atom">Atom</a><a href="/feeds/{name}.json">JSON</a><button hidden type="button" data-copy="/feeds/{name}.xml">{label}</button></div>'
def flag(x):
 return '<a href="mailto:avinesh.reddy@gmail.com?'+e(urllib.parse.urlencode({'subject':'Wire correction: '+x['title'],'body':'Item: '+x['id']+'\nOfficial source / correction:\n'}))+'">Flag a change we missed</a>'
def links(x,kind='wire'):
 return f'<div class="f-links"><a href="{e(x["source"])}" rel="noopener" target="_blank">Official source ↗<span class="f-sr"> (opens in a new tab)</span></a><a href="{e(url(x,kind))}">Permalink</a>{flag(x)}</div>'
def filters(types=True):
 opts=''.join(f'<option value="{m}">{e(l)}</option>' for m,l in MARKETS.items());ts=''.join(f'<option value="{t}">{t.title()}</option>' for t in TYPES)
 return '<form class="f-filter" hidden aria-label="Filter entries"><label for="f-market">Market<select id="f-market"><option value="">All markets</option>'+opts+'</select></label>'+('<label for="f-type">Type<select id="f-type"><option value="">All types</option>'+ts+'</select></label>' if types else '')+'<output id="f-count" aria-live="polite"></output></form><noscript><p class="f-note">All items are shown. Use your browser’s Find command to locate a market.</p></noscript>'
def shell(slug,title,deck,body,n,kicker):
 nav=''.join(f'<a href="/{s}/"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in [('wire','Wire'),('bp-watch','BP Watch'),('calendar','Calendar'),('feeds','Subscribe')])
 text=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | The Margin Wars — Preview</title><meta name="robots" content="noindex,nofollow"><meta name="feed-base" content="{e(BASE)}"><meta name="description" content="{e(deck)}"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..900&family=Martian+Mono:wght@300..600&display=swap"><link rel="stylesheet" href="/assets/feeds.css"><script src="/assets/feeds.js" defer></script>{AUTO}</head><body class="f-page"><a class="f-skip" href="#f-main">Skip to content</a><div class="f-shell"><header class="f-header"><a class="f-brand" href="/index.html">The Margin Wars</a><nav aria-label="Payments intelligence">{nav}</nav></header><div class="f-preview f-k"><b>{PREVIEW}</b><span>Research desk / {day(NOW)}</span></div><main id="f-main"><section class="f-hero" data-n="{n}"><p class="f-k">{e(kicker)}</p><h1>{e(title)}</h1><p class="f-deck">{e(deck)}</p><div class="f-jumps"><a href="/wire/">The rule</a><a href="/bp-watch/">The margin</a><a href="/calendar/">The deadline</a><a href="/index.html#route-brief">The route</a></div></section>{body}<p class="f-live" aria-live="polite"></p></main><footer class="f-footer"><span>Rules change. Own the line item.</span><a href="/index.html">Back to The Margin Wars ↗</a><a href="/contact.html">Bring us a margin problem</a></footer></div></body></html>'''
 p=ROOT/slug/'index.html';p.parent.mkdir(exist_ok=True);p.write_text(text)
 # Screen-reader label without relying on another stylesheet.
 text=p.read_text().replace('</head>','<style>.f-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}</style></head>');p.write_text(text)
def wirecard(x):
 effective=(x['date_kind']+' · '+day(x['effective'])) if x.get('effective') else 'Not confirmed / not applicable'
 meta=('<span>Source · '+day(x['source_date'])+'</span>') if x.get('source_date') else ''
 return f'''<article class="f-entry" id="{x['id']}" data-market="{x['market']}" data-type="{x['type']}"><div class="f-meta"><time datetime="{x['date']}">{day(x['date'])}</time><span>{e(MARKETS[x['market']])}</span><span class="f-tag">{e(x['type'])}</span>{meta}</div><div><h2><a href="#{x['id']}">{e(x['title'])}</a></h2><p>{e(x['changed'])}</p><dl class="f-facts"><div><dt>Who it hits</dt><dd>{e(x['hits'])}</dd></div><div><dt>Effective / milestone</dt><dd>{e(effective)}</dd></div></dl>{links(x)}</div></article>'''
shell('wire','The Rulebook Wire.','What changed. Who it hits. When it matters.',subscribe('wire')+'<p class="f-note">Recent changes + upcoming dates. Baselines labelled. Entry date = briefing date, not announcement date.</p>'+filters()+'<div class="f-ledger">'+''.join(wirecard(x) for x in wire)+'</div>','01','Payment intelligence / source → consequence')
bpcards=''
for k,x in enumerate(bp):
 bpcards+=f'''<article class="f-entry" id="{x['id']}" data-market="{x['market']}"><div class="f-meta"><span class="f-datebig">0{k+1}</span><span>{e(MARKETS[x['market']])}</span><span class="f-tag">Weekly watch</span></div><div><h2>{e(x['title'])}</h2><p class="f-impact">{e(x['impact'])}</p><p class="f-note">{e(x['method'])}</p><h3>The move</h3><p>{e(x['move'])}</p><div class="f-links"><a href="/wire/#{x['wire_id']}">Read the rule →</a></div>{links(x,'bp-watch')}</div></article>'''
shell('bp-watch','Basis-Point Watch.','Three changes. Three moves. No invented savings.',subscribe('bp-watch')+'<div class="f-weekline">Week of 09 Nov 2026 / Editorial analysis, not a savings forecast</div><div class="f-ledger">'+bpcards+'</div>','02','The margin / ranked by decision value')
future=sorted([x for x in dates if x['date']>=NOW],key=lambda x:x['date']);past=sorted([x for x in dates if x['date']<NOW],key=lambda x:x['date'],reverse=True)
def datecard(x):
 return f'''<article class="f-entry" id="{x['id']}" data-market="{x['market']}"><div class="f-meta"><time class="f-datebig" datetime="{x['date']}">{day(x['date'])}</time><span>{e(MARKETS[x['market']])}</span><span class="f-tag">{e(x['kind'])}</span></div><div><h2>{e(x['title'])}</h2><p>{e(x['description'])}</p>{links(x,'calendar')}<div class="f-links"><a href="/wire/#{x['wire_id']}">Read the rule →</a></div></div></article>'''
calbody='<div class="f-subscribe"><a href="/feeds/dates.ics">Subscribe / download .ics</a><button hidden type="button" data-copy="/feeds/dates.ics">Copy calendar URL</button><a href="/feeds/calendar.xml">RSS</a></div><p class="f-note">All-day dates follow the source jurisdiction, not a Pacific-time deadline. Past milestones are retained. Proposals without a confirmed date stay on the Wire, not in your calendar.</p>'+filters(False)+'<section class="f-dategroup"><p class="f-k">Next up / '+str(len(future))+' dates</p><div class="f-ledger">'+''.join(datecard(x) for x in future)+'</div></section><section class="f-dategroup"><p class="f-k">Implementation record / '+str(len(past))+' past milestones</p><div class="f-ledger">'+''.join(datecard(x) for x in past)+'</div></section>'
shell('calendar','Know the next date.','Effective dates, policy expectations and legislative milestones. Clearly separated.', '<div class="f-calendar">'+calbody+'</div>','03','The deadline / no speculative dates')
feedcards=''
for n,name,deck,path,slug in [('01','The Rulebook Wire','The rule, the affected market and the official source.','wire','wire'),('02','Basis-Point Watch','A weekly top three that turns changes into moves.','bp-watch','bp-watch'),('03','Effective-Date Calendar','Dates you can subscribe to, not another list to check.','calendar','calendar'),('04','Route Brief Updates','A changelog connecting rule changes to payment routes.','route-briefs','index.html#route-brief')]:
 jump='/'+slug+('/' if '.html' not in slug else '')
 feedcards+=f'<article class="f-feedcard"><span class="f-k">{n} / Subscribe</span><h2><a href="{jump}">{name}</a></h2><p>{deck}</p><p class="f-path">/feeds/{path}.xml</p>'+subscribe(path)+('</article>')
marketcards=''.join(f'<div class="f-market"><strong>{e(l)}</strong><div class="f-links"><a href="/feeds/wire-{m}.xml">RSS</a><a href="/feeds/wire-{m}.atom">Atom</a><a href="/feeds/wire-{m}.json">JSON</a></div></div>' for m,l in MARKETS.items())
routelist=''.join(f'<article class="f-entry" id="update-{x["id"]}"><div class="f-meta"><time>{day(x["date"])}</time><span>{e(MARKETS[x["market"]])}</span></div><div><h3><a href="/index.html#rb-{x["route_id"]}">{e(x["title"])}</a></h3><p>{e(x["description"])}</p><div class="f-links"><a href="{e(x["source"])}">Official source</a>{flag(x)}</div></div></article>' for x in routes)
shell('feeds','The signal. Not the scroll.','Four ways to follow the rules that move payment margin.','<div class="f-feedgrid">'+feedcards+'</div><section class="f-marketfeeds"><p class="f-k">One market. Less noise.</p><h2>Follow your terrain.</h2><div class="f-markets">'+marketcards+'</div></section><section class="f-marketfeeds"><h2>Put dates in your calendar.</h2><p class="f-note">Add the URL as a calendar subscription for updates. Importing the file once will not refresh it.</p><div class="f-subscribe"><a href="/feeds/dates.ics">Open .ics calendar</a><button hidden type="button" data-copy="/feeds/dates.ics">Copy calendar URL</button></div></section><section class="f-marketfeeds" id="route-updates"><p class="f-k">Route Brief Updates</p><h2>The route, with a date stamp.</h2>'+routelist+'</section><section class="f-marketfeeds"><h2>Source first. Publish after review.</h2><p class="f-note">Primary sources only. Drafts are not mandates; proposals are not effective rules. Estimates need a method. No automatic publishing: the daily research queue feeds editorial review. RSS and Atom work in feed readers; JSON is for integrations.</p></section>','04','The subscription desk / reader-owned, no algorithm')
# Decorate existing site pages without replacing any other worker’s content.
stripitems=[]
seen_markets=set()
for x in wire:
 if x['market'] in seen_markets:continue
 seen_markets.add(x['market'])
 if len(stripitems)>=3:break
 stripitems.append(f'<article class="f-stripitem"><small>{e(MARKETS[x["market"]])} / {e(x["type"])}</small><a href="/wire/#{x["id"]}">{e(x["title"])}</a></article>')
strip='<!--feeds-home--><section class="f-strip" aria-labelledby="f-latest"><div class="f-striphead"><h2 id="f-latest">Latest from the Wire</h2><a href="/wire/">Open the research desk ↗</a></div><div class="f-stripgrid">'+''.join(stripitems)+'</div><p class="f-stripstatus">'+PREVIEW+'</p></section><!--/feeds-home-->'
for p in ROOT.rglob('*.html'):
 if p.parent.name in ['wire','bp-watch','calendar','feeds']:continue
 s=p.read_text();s=re.sub(r'<!--feeds-discovery-->.*?<!--/feeds-discovery-->','',s,flags=re.S);s=s.replace('</head>',AUTO+'</head>',1)
 s=re.sub(r'<!--feeds-home-->.*?<!--/feeds-home-->','',s,flags=re.S)
 s=re.sub(r'<!--feeds-badge-->.*?<!--/feeds-badge-->','',s,flags=re.S)
 if p.name in ['index.html','advisory.html']:
  if '/assets/feeds.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/feeds.css"></head>',1)
  if '/assets/feeds.js' not in s:s=s.replace('</head>','<script src="/assets/feeds.js" defer></script></head>',1)
  for x in routes:
   pat=r'(<article class="rb-brief" id="rb-'+re.escape(x['route_id'])+r'".*?<div class="rb-bh">.*?</h3>)'
   badge='<!--feeds-badge--><span class="f-update">Updated '+day(x['date'])+' · Preview · <a href="/wire/#'+x['wire_id']+'">Linked rule context ↗</a></span><!--/feeds-badge-->'
   s=re.sub(pat,lambda m:m.group(1)+badge,s,count=1,flags=re.S)
 if p.name=='index.html' and p.parent==ROOT:
  end=s.find('</section>',s.find('<section class="hero"'))
  assert end>0;s=s[:end+10]+strip+s[end+10:]
 p.write_text(s)
# Publish only our MIME rules, preserving all prior header policy.
hp=ROOT/'_headers';hs=hp.read_text() if hp.exists() else '';hs=re.sub(r'\n# feeds-headers.*?# /feeds-headers\n','\n',hs,flags=re.S)
hs=hs.rstrip()+'\n';hs+='\n# feeds-headers\n/feeds/*.xml\n  Content-Type: application/rss+xml; charset=utf-8\n  Cache-Control: public, max-age=300\n/feeds/*.atom\n  Content-Type: application/atom+xml; charset=utf-8\n/feeds/*.json\n  Content-Type: application/feed+json; charset=utf-8\n/feeds/dates.ics\n  Content-Type: text/calendar; charset=utf-8\n  Content-Disposition: inline; filename="margin-wars-dates-preview.ics"\n# /feeds-headers\n';hp.write_text(hs)
print('FEEDS:',len(wire),'Wire;',len(bp),'BP Watch;',len(dates),'calendar;',len(routes),'route updates;',len(list(OUT.glob('*.xml'))),'RSS feeds')

# Feed-owned UX layer runs last, after all generated content.
from apply_feed_ux import apply as apply_feed_ux
apply_feed_ux()
