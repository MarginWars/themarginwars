#!/usr/bin/env python3
"""make_dist: copy site_calm -> site_dist, then self-host fonts and replace each page's stylesheet
links with per-route purged bundles. site_calm is never modified, so every build layer stays idempotent.
Deploy site_dist."""
import re,json,hashlib,shutil,html,os
from pathlib import Path
import tinycss2
H=Path(__file__).resolve().parent;SRC=H.parent/'site_calm';ROOT=H.parent/'site_dist'
def rd(p):return p.read_text()
def wr(p,s):p.write_text(s)
tmp=ROOT.with_name('site_dist.tmp');shutil.rmtree(tmp,ignore_errors=True);shutil.copytree(SRC,tmp)
shutil.rmtree(ROOT,ignore_errors=True);tmp.rename(ROOT)
pages=sorted(ROOT.rglob('*.html'))
# ---------- 6b fonts: self-host (latin + latin-ext) ----------
FD=ROOT/'assets/fonts';FD.mkdir(exist_ok=True)
fmap=dict(l.split() for l in rd(H/'fonts_src/map.txt').splitlines() if l.strip())
gcss=rd(H/'fonts_src/google.css');FACES={}
for sub,b in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face\s*{[^}]*})',gcss):
 if sub not in('latin','latin-ext'):continue
 fam=re.search(r"font-family: '([^']+)'",b).group(1);u=re.search(r'url\((https://[^)]+)\)',b).group(1);name=fmap[u]
 shutil.copyfile(H/'fonts_src'/name,FD/name);FACES.setdefault(fam,[]).append(re.sub(r'\s+',' ',b.replace(u,'/assets/fonts/'+name)).replace('; ',';').replace(' {','{').replace('{ ','{').replace(' }','}'))
PRELOAD={'Schibsted Grotesk':fmap[[u for u in fmap if 'schibsted' in fmap[u] and 'ext' not in fmap[u]][0]],'Martian Mono':fmap[[u for u in fmap if 'martian' in fmap[u] and 'ext' not in fmap[u]][0]]}

# ---------- 6c per-route CSS bundles with safe purge ----------
BD=ROOT/'assets/b';shutil.rmtree(BD,ignore_errors=True);BD.mkdir()
JS_TOK={}
def js_tokens(path):
 if path not in JS_TOK:
  try:JS_TOK[path]=set(re.findall(r'[A-Za-z_][\w-]*',rd(path)))
  except FileNotFoundError:JS_TOK[path]=set()
 return JS_TOK[path]
PSEUDO_FN=re.compile(r':(?:not|is|where|has|matches|-webkit-any|nth-child|nth-last-child|host|host-context|lang|dir)\(')
def required_tokens(sel):
 # strip functional pseudo-class arguments (optional or negated tokens)
 out='';i=0;depth=0
 while i<len(sel):
  m=PSEUDO_FN.match(sel,i) if depth==0 else None
  if sel[i]=='(':depth+=1;i+=1;continue
  if sel[i]==')':depth-=1;i+=1;continue
  if depth==0:out+=sel[i]
  i+=1
 if '\\' in out:return None  # escaped selectors: keep
 out=re.sub(r'\[[^\]]*\]','',out)
 return set(re.findall(r'[.#](-?[A-Za-z_][\w-]*)',out))
def purge(rules,keep):
 res=[]
 for r in rules:
  if r.type in('whitespace','comment'):continue
  if r.type=='qualified-rule':
   prelude=tinycss2.serialize(r.prelude).strip()
   sels=[x.strip() for x in split_top(prelude)]
   ok=False
   for s_ in sels:
    req=required_tokens(s_)
    if req is None or req<=keep:ok=True;break
   if ok:res.append(prelude+'{'+tinycss2.serialize(r.content).strip()+'}')
  elif r.type=='at-rule':
   kw=r.lower_at_keyword;pre=tinycss2.serialize(r.prelude).strip()
   if kw in('media','supports','container','layer','document') and r.content is not None:
    inner=purge(tinycss2.parse_rule_list(r.content,skip_comments=True,skip_whitespace=True),keep)
    if inner:res.append('@'+kw+' '+pre+'{'+''.join(inner)+'}')
   else:
    res.append('@'+kw+(' '+pre if pre else '')+('{'+tinycss2.serialize(r.content).strip()+'}' if r.content is not None else ';'))
 return res
def split_top(s):
 out=[];d=0;cur=''
 for ch in s:
  if ch in'([':d+=1
  elif ch in')]':d-=1
  if ch==','and d==0:out.append(cur);cur=''
  else:cur+=ch
 out.append(cur);return out
def minify(css):
 css=re.sub(r'\s+',' ',css);css=re.sub(r'\s*([{};,>])\s*',r'\1',css);css=css.replace(';}','}')
 return css.strip()
def absurls(css,base):
 def f(m):
  q,u=m.group(1),m.group(2).strip()
  if re.match(r'(?:/|data:|https?:|#)',u):return m.group(0)
  return f'url({q}/{(base+"/"+u).lstrip("/") if base else u}{q})'
 return re.sub(r'url\(\s*([\'"]?)([^\'")]+)\1\s*\)',f,css)
PARSED={}
def sheet(href,page):
 path=href.split('?')[0]
 fp=(ROOT/path.lstrip('/')) if path.startswith('/') else (page.parent/path)
 fp=fp.resolve();key=str(fp)
 if key not in PARSED:
  css=rd(fp);base=fp.parent.relative_to(ROOT).as_posix();base='' if base=='.' else base
  css=absurls(css,base)
  PARSED[key]=tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True)
 return PARSED[key]
LINK=re.compile(r'<link\b[^>]*rel="stylesheet"[^>]*>')
bundles={}
for p in pages:
 t=rd(p)
 t=re.sub(r'<!--bo-fonts-->.*?<!--/bo-fonts-->','',t,flags=re.S)
 hm=re.search(r'<head>.*?</head>',t,re.S);head=hm.group(0)
 links=list(LINK.finditer(head))
 if not links:continue
 fams=[]
 for l in links:
  h_=re.search(r'href="([^"]+)"',l.group(0)).group(1)
  if 'fonts.googleapis.com/css' in h_:fams+=[html.unescape(x).replace('+',' ').split(':')[0] for x in re.findall(r'family=([^&]+)',h_)]
 # safelist: classes/ids in markup + tokens of inline scripts and of every script the page loads
 keep=set()
 for c in re.findall(r'\bclass="([^"]*)"',t):keep|=set(c.split())
 keep|=set(re.findall(r'\bid="([^"]+)"',t))
 for sc in re.findall(r'<script\b[^>]*>(.*?)</script>',t,re.S):keep|=set(re.findall(r'[A-Za-z_][\w-]*',sc))
 for src in re.findall(r'<script\b[^>]*src="([^"]+)"',t):
  if src.startswith('http'):continue
  sp_=src.split('?')[0];js_p=(ROOT/sp_.lstrip('/')) if sp_.startswith('/') else (p.parent/sp_)
  keep|=js_tokens(js_p.resolve())
 keep|={'rv','rv-in','rv-on','open','on','js','wk','wk-rm','lk-js','lk-on','nm'}
 # group consecutive local stylesheet links into segments (preserve cascade w.r.t. inline <style>)
 segs=[];cur=[]
 items=re.split(r'(<link\b[^>]*rel="stylesheet"[^>]*>|<style\b.*?</style>|<script\b.*?</script>)',head,flags=re.S)
 newhead='';fonts_done=False
 def flush():
  global newhead
 out=[]
 def emit_seg(seg):
  css=[]
  for h_ in seg:css+=purge(sheet(h_,p),keep)
  body=minify(''.join(css))
  return body
 cur=None
 for chunk in items:
  if not chunk:continue
  if LINK.fullmatch(chunk):
   h_=html.unescape(re.search(r'href="([^"]+)"',chunk).group(1))
   if 'fonts.googleapis.com/css' in h_:
    if not fonts_done:
     fonts_done=True
     faces=''.join(f for fam in dict.fromkeys(fams) for f in FACES.get(fam,[]))
     pre=''.join(f'<link as="font" crossorigin="" href="/assets/fonts/{PRELOAD[fam]}" rel="preload" type="font/woff2"/>' for fam in ['Schibsted Grotesk','Martian Mono'] if fam in fams)
     out.append(('fonts',pre,faces))
    continue
   if h_.startswith('http'):cur=None;out.append(('raw',chunk));continue
   if cur is None:cur=[h_];out.append(('seg',cur))
   else:cur.append(h_)
  elif chunk.lstrip().startswith('<style'):cur=None;out.append(('raw',chunk))
  else:out.append(('raw',chunk))
 faces_css=''
 html_out=''
 for o in out:
  if o[0] in('raw','held'):html_out+=o[1]
  elif o[0]=='fonts':html_out+='<!--bo-fonts-->'+o[1]+'<!--/bo-fonts-->';faces_css=o[2]
  else:
   body=emit_seg(o[1])
   if faces_css:body=minify(faces_css)+body;faces_css=''
   hsh=hashlib.md5(body.encode()).hexdigest()[:12];name=f'{hsh}.css'
   (BD/name).write_text(body);bundles[name]=len(body)
   html_out+=f'<link data-bo-css="" href="/assets/b/{name}" rel="stylesheet"/>'
 if faces_css:
  hsh=hashlib.md5(faces_css.encode()).hexdigest()[:12];(BD/f'{hsh}.css').write_text(minify(faces_css));html_out+=f'<link href="/assets/b/{hsh}.css" rel="stylesheet"/>'
 html_out=re.sub(r'<link\b[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*rel="preconnect"[^>]*>','',html_out)
 t=t[:hm.start()]+html_out+t[hm.end():]
 wr(p,t)
print(f'DIST: {len(pages)} pages, {len(bundles)} CSS bundles (avg {sum(bundles.values())//max(1,len(bundles))//1024} KiB)')
