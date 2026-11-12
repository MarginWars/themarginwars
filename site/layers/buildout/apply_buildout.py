#!/usr/bin/env python3
"""Buildout layer (Avi approved 10 Nov 2026). Runs LAST in build.sh. Idempotent and deterministic.
1 404 page  2 contact form  3 briefing invite links  4 next blocks  5 SEO  6 speed (fonts, per-route CSS bundles, CLS)
No network access: fonts come from buildout/fonts_src (cached once)."""
import re,json,hashlib,shutil,html,os
from pathlib import Path
import tinycss2
H=Path(__file__).resolve().parent;ROOT=H.parent/'site_calm';PROD='https://themarginwars.com';e=html.escape
MAIL='mailto:avinesh.reddy@gmail.com'
def rd(p):return p.read_text()
def wr(p,s):p.write_text(s)
pages=sorted(p for p in ROOT.rglob('*.html') if not p.name.startswith('_'))

# ---------- shared assets ----------
shutil.copyfile(H/'contact.js',ROOT/'assets/contact.js')
suite=ROOT/'assets/suite.css';s=rd(suite);s=re.sub(r'\n?/\* buildout:.*\Z','',s,flags=re.S);wr(suite,s.rstrip()+'\n'+rd(H/'buildout.css'))

# ---------- 4 next blocks ----------
sp=rd(ROOT/'speaking.html');i=sp.index('<nav aria-label="Next" class="nextp">');NEXT=sp[i:sp.index('</nav>',i)+6]
def nextp(href,label):return re.sub(r'<a class="nm-inline" href="[^"]*">[^<]*</a></nav>$',f'<a class="nm-inline" href="{href}">{label} →</a></nav>',NEXT)
GAMES=['daily','deal','leak','quiz','tracewire']+[f'ep{n}' for n in range(1,10)]
for name,href,label in [('about','advisory.html','Advisory')]+[(g,'arcade.html','Arcade') for g in GAMES]:
 p=ROOT/(name+'.html');t=rd(p)
 if 'class="nextp"' in t:continue
 t=t.replace('</main>',nextp(href,label)+'</main>',1);wr(p,t)

# ---------- 3 briefing invite -> contact form preselected ----------
BRIEF='contact.html?topic=briefing#contact-form'
for p in pages:
 t=rd(p);n=re.sub(r'(<a\b[^>]*href=")(?:contact\.html|writing\.html|/contact\.html|/writing\.html)("[^>]*>\s*Request an invitation[^<]*</a>)',lambda m:m.group(1)+('/' if p.parent!=ROOT else '')+BRIEF+m.group(2),t)
 if n!=t:wr(p,n)

# ---------- 2 contact form ----------
TOPICS=['Margin Teardown','Campaign Sprint','Board sessions and workshops','Retained advisory','Briefing invitation','Something else']
opts=''.join(f'<label class="wk-opt"><input type="radio" name="topic" value="{e(x)}" required aria-describedby="cf-topic-e"><span class="wk-no" aria-hidden="true">{k+1:02d}</span><b>{e(x)}</b></label>' for k,x in enumerate(TOPICS))
def fld(n,label,typ='text',ac='',extra='',cls='',opt=False,ta=False):
 req='' if opt else ' required aria-required="true"'
 lab=f'<label class="cf-l" for="cf-{n}">{label}'+(' <span class="cf-opt">(optional)</span>' if opt else '')+'</label>'
 ctl=(f'<textarea class="cf-i" id="cf-{n}" name="{n}" rows="6"{req}{extra} aria-describedby="cf-{n}-e"></textarea>' if ta else f'<input class="cf-i" id="cf-{n}" name="{n}" type="{typ}"'+(f' autocomplete="{ac}"' if ac else '')+f'{req}{extra} aria-describedby="cf-{n}-e">')
 return f'<div class="cf-f{(" "+cls) if cls else ""}">{lab}{ctl}<p class="cf-err" id="cf-{n}-e" hidden></p></div>'
FORM=('<!--bo-form--><form class="wk-route cform" id="contact-form" action="/api/contact" method="post" novalidate hidden aria-labelledby="cf-h">'
 '<div class="cf-body"><fieldset class="cf-topic"><legend id="cf-h">Choose a topic</legend><div class="wk-opts">'+opts+'</div><p class="cf-err" id="cf-topic-e" hidden></p></fieldset>'
 '<div class="cf-fields">'+fld('name','Name',ac='name',extra=' maxlength="120"')+fld('email','Email',typ='email',ac='email',extra=' maxlength="200" inputmode="email" spellcheck="false"')+fld('company','Company',ac='organization',extra=' maxlength="160"',cls='cf-co',opt=True)
 +fld('message','Message',extra=' maxlength="5000"',cls='cf-wide',ta=True)+
 '<div class="cf-hp" aria-hidden="true"><label for="cf-website">Website</label><input id="cf-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>'
 '<div class="cf-ts" id="cf-ts"></div><p class="cf-status" role="status" aria-live="polite" tabindex="-1" hidden></p>'
 f'<div class="cf-actions"><button class="btn nm-primary cf-send" type="submit" aria-busy="false"><span>Send message</span></button><p class="cf-alt">Or <a class="nm-inline nm-intext" href="{MAIL}">email us directly</a>.</p></div></div></div>'
 '<div class="cf-done" id="cf-done" tabindex="-1" hidden><h3>Message sent. Thank you.</h3><p>It is with the team now. If you need to add anything, <a class="nm-inline nm-intext" href="'+MAIL+'">email us directly</a>.</p><p class="cf-ref"></p><button class="btn alt cf-again" id="cf-again" type="button">Send another message</button></div>'
 '</form><script>document.getElementById("contact-form").hidden=false</script>'
 f'<noscript><p class="cf-nojs">The message form needs JavaScript. <a class="nm-inline nm-intext" href="{MAIL}">Email us directly</a> instead.</p></noscript><!--/bo-form-->')
p=ROOT/'contact.html';t=rd(p);t=re.sub(r'<!--bo-form-->.*?<!--/bo-form-->','',t,flags=re.S)
m=re.search(r'<a class="nm-inline nm-intext" href="https://www\.linkedin\.com/in/avi-reddy-64b07218[^"]*">Connect on LinkedIn</a></li></ul>',t)
assert m;t=t[:m.end()]+FORM+t[m.end():]
if '/assets/contact.js' not in t:t=t.replace('</body>','<script defer src="/assets/contact.js"></script></body>',1)
wr(p,t)

# ---------- 6a CLS: unhide research toolbars before first paint ----------
UNHIDE='<script data-bo="unhide">(function(){var q=document.querySelectorAll("[data-fx-tools][hidden],details.fx-refine[hidden]");for(var i=0;i<q.length;i++)q[i].hidden=false})()</script>'
for p in pages:
 t=rd(p)
 if 'data-fx-tools' not in t:continue
 t=t.replace(UNHIDE,'')
 m=re.search(r'<details class="fx-refine"[^>]*>.*?</details>',t,re.S)
 if not m:
  i=t.index('data-fx-tools');i=t.rfind('<div',0,i);depth=0;j=i
  for mm in re.finditer(r'<(/?)div\b',t[i:]):
   depth+=-1 if mm.group(1) else 1
   if depth==0:j=i+mm.start();break
  end=t.index('>',j)+1
 else:end=m.end()
 t=t[:end]+UNHIDE+t[end:];wr(p,t)

# ---------- 1 404 page ----------
tpl=rd(ROOT/'contact.html')
tpl=re.sub(r'<!--bo-form-->.*?<!--/bo-form-->','',tpl,flags=re.S).replace('<script defer src="/assets/contact.js"></script>','')
head,rest=tpl.split('<main',1);foot=rest[rest.index('</main>')+7:]
NF=('<main id="main" tabindex="-1"><section class="ihero"><h1><span>Page</span><span>not found</span></h1><p class="lede">That page is not here. It may have moved, or the link may be wrong.</p></section>'
 '<div class="wrap"><section><p class="eyebrow sx">404</p><h2>Try one of these</h2><ul class="nf-links">'
 '<li><a href="/"><b>Home</b><span>Payment tactics for winning back margin.</span></a></li>'
 '<li><a href="/advisory"><b>Advisory</b><span>Operator-led advisory on payment margin.</span></a></li>'
 '<li><a href="/wire/"><b>Research desk</b><span>What changed. Who it hits. When it matters.</span></a></li>'
 '<li><a href="/contact"><b>Contact</b><span>Bring us a margin problem.</span></a></li></ul></section></div></main>')
nf=head+NF+foot
nf=nf.replace('class="nm pg-contact"','class="nm pg-404"')
nf=re.sub(r'<title>.*?</title>','<title>Page not found | The Margin Wars</title>',nf,flags=re.S)
nf=re.sub(r'<meta[^>]*name="description"[^>]*>','<meta content="That page is not here. Try Home, Advisory, the research desk or Contact." name="description"/><meta content="noindex" name="robots"/>',nf,count=1)
nf=re.sub(r'<link[^>]*rel="canonical"[^>]*>','',nf)
# absolutise relative URLs (404 is served at any depth)
nf=re.sub(r'\b(href|src)="(?!https?:|/|#|mailto:|data:|tel:)([^"]+)"',lambda m:f'{m.group(1)}="/{m.group(2)}"',nf)
nf=re.sub(r'\b(srcset|imagesrcset)="([^"]+)"',lambda m:m.group(1)+'="'+', '.join(('/'+x.strip() if not x.strip().startswith(('/','http')) else x.strip()) for x in m.group(2).split(','))+'"',nf)
nf=re.sub(r'aria-current="page"','',nf)
wr(ROOT/'404.html',nf)
pages=sorted(p for p in ROOT.rglob('*.html'))

# ---------- 7 brand (approved logo C, band order, pink wordmark rule, tagline) ----------
import subprocess;subprocess.run(['python3',str(H/'make_brand_assets.py')],check=True)
OLD_BAND='#8FB0E0 0 16.667%,#3FBF85 16.667% 33.333%,#D2A63A 33.333% 50%,#EA6259 50% 66.667%,#B7C1C9 66.667% 83.333%,#A08FE6 83.333% 100%'
NEW_BAND='#8FB0E0 0 16.667%,#A08FE6 16.667% 33.333%,#3FBF85 33.333% 50%,#B7C1C9 50% 66.667%,#D2A63A 66.667% 83.333%,#EA6259 83.333% 100%'
s=rd(suite);s=s.replace(OLD_BAND,NEW_BAND);assert NEW_BAND in s;wr(suite,s)
ICONS='<!--bo-icons--><link href="/favicon.ico" rel="icon" sizes="48x48"/><link href="/icon.svg" rel="icon" type="image/svg+xml"/><link href="/apple-touch-icon.png" rel="apple-touch-icon"/><!--/bo-icons-->'
TAG='<p class="foot-tag">Payments tactics from the front lines.</p>'
for p in pages:
 t=rd(p);t=re.sub(r'<!--bo-icons-->.*?<!--/bo-icons-->','',t,flags=re.S);t=re.sub(r'<link\b[^>]*rel="(?:shortcut )?icon"[^>]*>','',t)
 t=t.replace('</head>',ICONS+'</head>',1);t=t.replace('<footer>'+TAG,'<footer>');t=t.replace('<footer>','<footer>'+TAG,1);wr(p,t)

# ---------- 5 SEO ----------
DATA={k:json.loads(rd(ROOT/f'assets/feeds/{k}.json')) for k in ['wire','calendar','bp-watch','route-briefs']}
def item_date(kind,id_):
 for x in DATA[kind]:
  if x['id']==id_:return x.get('published',x.get('added',x['date']))
SECTION={'wire':'Rulebook Wire','calendar':'Effective Dates','bp-watch':'Basis-Point Watch','route-briefs':'Route Briefs'}
def url_of(p):
 r=p.relative_to(ROOT).as_posix()
 if r=='index.html':return PROD+'/'
 if r.endswith('/index.html'):return PROD+'/'+r[:-10]
 return PROD+'/'+r[:-5]
def meta_get(t,attr,key):
 m=re.search(r'<meta\b[^>]*'+attr+'="'+re.escape(key)+r'"[^>]*>',t)
 if not m:return None
 c=re.search(r'content="([^"]*)"',m.group(0));return html.unescape(c.group(1)) if c else None
ORG={'@type':'Organization','@id':PROD+'/#org','name':'The Margin Wars','url':PROD+'/','slogan':'Payments tactics from the front lines.','logo':{'@type':'ImageObject','url':PROD+'/assets/brand/icon-512.png','width':512,'height':512},'image':PROD+'/assets/brand/og-default.png','sameAs':['https://themarginwars.substack.com','https://www.linkedin.com/company/themarginwars'],'member':[{'@type':'Person','@id':PROD+'/about#avi','name':'Avi','sameAs':['https://www.linkedin.com/in/avi-reddy-64b07218']},{'@type':'Person','@id':PROD+'/about#anitha','name':'Anitha'}]}
titles={};descs={};sitemap=[]
for p in pages:
 rel=p.relative_to(ROOT).as_posix();t=rd(p)
 t=re.sub(r'<!--bo-seo-->.*?<!--/bo-seo-->','',t,flags=re.S)
 if rel=='404.html':wr(p,t);continue
 url=url_of(p);parts=rel.split('/')
 title=html.unescape(re.search(r'<title>(.*?)</title>',t,re.S).group(1)).strip()
 desc=meta_get(t,'name','description') or ''
 ogd=meta_get(t,'property','og:description');ogimg=meta_get(t,'property','og:image');ogt=meta_get(t,'property','og:title')
 item=len(parts)==4 and parts[1]=='items'
 if item:
  kind=parts[0];sec=SECTION[kind];base=ogt or title.split(' | ')[0]
  title=f'{base} | {sec} | The Margin Wars'
  if ogd:desc=ogd
  if kind=='calendar':
   x=next(x for x in DATA['calendar'] if x['id']==parts[2]);import datetime as _dt
   desc=f"{_dt.date.fromisoformat(x['date']).strftime('%d %b %Y').lstrip('0')}, {x['kind'].lower()}. {desc}"
  if kind=='route-briefs':desc=f"{base}. {desc}"
 if rel=='digest/index.html':desc='The week. The moves. Three moves to own, five signals worth opening and the next dates on the calendar.'
 m=re.fullmatch(r'digest/(\d{4}-\d{2}-\d{2})/index.html',rel)
 if m:
  title=f'Weekly Digest, edition {m.group(1)} | The Margin Wars';desc=f'Edition {m.group(1)}. The week. The moves. Three moves to own, five signals worth opening and the next dates on the calendar.'
 t=re.sub(r'<title>.*?</title>',f'<title>{e(title,quote=False)}</title>',t,count=1,flags=re.S)
 t=re.sub(r'<meta\b[^>]*name="description"[^>]*>',f'<meta content="{e(desc)}" name="description"/>',t,count=1)
 # robots: indexable on production; non-production hosts get X-Robots-Tag from _headers / robots function
 t=re.sub(r'<meta\b[^>]*name="robots"[^>]*>','',t)
 t=re.sub(r'<link\b[^>]*rel="canonical"[^>]*>','',t)
 t=re.sub(r'<meta\b[^>]*(?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>','',t)
 t=re.sub(r'<meta\b[^>]*name="feed-base"[^>]*>','<meta content="'+PROD+'" name="feed-base"/>',t)
 og_title=(ogt or title.split(' | ')[0].split(' - ')[0]) if item else title.split(' | ')[0]
 if not ogimg:
  pm=re.search(r'assets/plates/(plate-\d+)-1200\.jpg',t);ogimg=f'{PROD}/assets/brand/og-default.png';iw,ih='1200','630'
 else:iw,ih='1200','630'
 ld=[]
 if rel=='index.html':ld=[ORG,{'@type':'WebSite','@id':PROD+'/#site','name':'The Margin Wars','url':PROD+'/','publisher':{'@id':PROD+'/#org'}}]
 elif item:
  a={'@type':'Article','headline':og_title[:110],'description':desc,'url':url,'mainEntityOfPage':url,'image':ogimg,'publisher':{'@id':PROD+'/#org'},'isPartOf':{'@type':'CollectionPage','name':SECTION[parts[0]],'url':PROD+'/'+parts[0]+'/'}}
  d=item_date(parts[0],parts[2])
  if d:a['datePublished']=d
  ld=[ORG,a]
 else:ld=[ORG,{'@type':'WebPage','name':og_title,'description':desc,'url':url,'isPartOf':{'@id':PROD+'/#site'},'publisher':{'@id':PROD+'/#org'}}]
 seo=('<!--bo-seo-->'+f'<link href="{url}" rel="canonical"/>'
  +f'<meta content="{"article" if item else "website"}" property="og:type"/><meta content="The Margin Wars" property="og:site_name"/><meta content="en_US" property="og:locale"/>'
  +f'<meta content="{e(og_title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="{url}" property="og:url"/>'
  +f'<meta content="{ogimg}" property="og:image"/><meta content="{iw}" property="og:image:width"/><meta content="{ih}" property="og:image:height"/><meta content="{e(og_title)}" property="og:image:alt"/>'
  +f'<meta content="summary_large_image" name="twitter:card"/><meta content="{e(og_title)}" name="twitter:title"/><meta content="{e(desc)}" name="twitter:description"/><meta content="{ogimg}" name="twitter:image"/>'
  +'<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':ld},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script><!--/bo-seo-->')
 t=t.replace('</title>','</title>'+seo,1) if False else re.sub(r'(<meta\b[^>]*name="description"[^>]*>)',lambda m:m.group(1)+seo,t,count=1)
 wr(p,t);titles.setdefault(title,[]).append(rel);descs.setdefault(desc,[]).append(rel)
 lm=item_date(parts[0],parts[2]) if item else '2026-11-10'
 sitemap.append((url,lm))
dupt={k:v for k,v in titles.items() if len(v)>1};dupd={k:v for k,v in descs.items() if len(v)>1}
assert not dupt,('duplicate titles',dupt);assert not dupd,('duplicate descriptions',dupd)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n' for u,d in sorted(sitemap))+'</urlset>\n'
wr(ROOT/'sitemap.xml',sm)
wr(ROOT/'robots.txt','User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://themarginwars.com/sitemap.xml\n')
hp=ROOT/'_headers';hs=rd(hp);hs=re.sub(r'\s*# bo-headers.*?# /bo-headers\n','\n',hs,flags=re.S);hs=re.sub(r'\n{3,}','\n\n',hs).rstrip()+'\n'
hs+=('\n# bo-headers\n# Non-production hosts are never indexed (production themarginwars.com has no X-Robots-Tag).\n'
 'https://themarginwars.pages.dev/*\n  X-Robots-Tag: noindex\nhttps://themarginwars-dev.pages.dev/*\n  X-Robots-Tag: noindex\nhttps://:sub.themarginwars-dev.pages.dev/*\n  X-Robots-Tag: noindex\n'
 '/assets/b/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n  Access-Control-Allow-Origin: *\n'
 '/api/*\n  X-Robots-Tag: noindex\n# /bo-headers\n')
wr(hp,hs)

print(f'BUILDOUT: 404 + contact form + next blocks + SEO ({len(sitemap)} sitemap URLs)')
