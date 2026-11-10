"""Final static-suite layer; run after feeds. No content or event-handler changes."""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil,json,os
H=Path(__file__).parent;D=H.parent/'site_calm';asset='assets/suite.css';routes=[]
for f in sorted(D.rglob('*.html')):
 s=BeautifulSoup(f.read_text(),'html.parser')
 if not s.body or not s.head:continue
 s.body['class']=sorted(set(s.body.get('class',[])+['nm']))
 for old in s.select('link[data-suite]'):old.decompose()
 l=s.new_tag('link',rel='stylesheet',href='/'+asset);l['data-suite']='';s.head.append(l)
 for old in s.select('script[data-polish]'):old.decompose()
 if os.environ.get('SUITE_POLISH','1')!='0':
  sc=s.new_tag('script',src='/assets/polish.js');sc['defer']='';sc['data-polish']='';s.body.append(sc)
 if os.environ.get('SUITE_POLISH','1')!='0':
  # Polish a11y: landmark for the research preview status strip; tabpanels on a permitted element; no skipped heading level before the first h2
  for old in s.select('meta[data-polish]'):old.decompose()
  for nm,cv in (('color-scheme','light'),('theme-color','#FFFFFF')):
   if not s.head.find('meta',attrs={'name':nm}):m=s.new_tag('meta');m['name']=nm;m['content']=cv;m['data-polish']='';s.head.append(m)
  mn=s.find('main')
  if mn and mn.get('id') and not mn.get('tabindex'):mn['tabindex']='-1'
  for fp in s.select('.f-preview'):
   if not fp.find_parent(['main','header','footer','nav','aside']) and not fp.get('role'):fp['role']='region';fp['aria-label']='Preview status'
  for tp in s.select('article[role=tabpanel]'):tp.name='section'
  hs=s.find_all(['h1','h2','h3','h4'])
  if hs and hs[0].name=='h1':
   for h in hs[1:]:
    if h.name=='h2':break
    if h.name=='h3' and not h.get('aria-level'):h['role']='heading';h['aria-level']='2'
 for a in s.select('a[href]'):
  classes=[c for c in a.get('class',[]) if c not in ('nm-inline','nm-primary')]
  if not a.find(['img','svg','div','h1','h2','h3','h4','p','figure','ul','ol']) and not any(c in classes for c in ['brand','f-brand','skip','f-skip','gc','rd']):classes.append('nm-inline')
  if ('btn' in classes and 'alt' not in classes) or 'rb-cta' in classes:classes.append('nm-primary')
  if os.environ.get('SUITE_POLISH','1')!='0':
   classes=[c for c in classes if c!='nm-intext']
   par=a.parent
   if 'nm-inline' in classes and 'btn' not in classes and par and par.name in ('p','span','aside','li','dd','small','figcaption','blockquote','td','em','b','strong') and any(isinstance(n,str) and n.strip() and n.strip() not in ('·','|','/') for n in par.children):classes.append('nm-intext')
  if classes:a['class']=classes
 f.write_text(str(s))
 rel=str(f.relative_to(D));family=rel.split('/')[0] if '/' in rel else ('games' if f.stem in ['arcade','daily','deal','leak','quiz','tracewire'] or f.stem.startswith('ep') else 'core')
 routes.append({'file':rel,'route':'/'+('' if rel=='index.html' else rel[:-10] if rel.endswith('index.html') else rel[:-5]),'family':family,'controls':len(s.select('button,input,select,summary')),'links':len(s.select('a[href]'))})
(D/asset).write_text((H/'suite.css').read_text()+('\n'+(H/'relief.css').read_text() if os.environ.get('SUITE_RELIEF','1')!='0' else '')+('\n'+(H/'balance.css').read_text() if os.environ.get('SUITE_BALANCE','1')!='0' else '')+'\n'+(H/'spacing.css').read_text()+('\n'+(H/'roles.css').read_text() if os.environ.get('SUITE_ROLES','1')!='0' else '')+('\n'+(H/'band.css').read_text() if os.environ.get('SUITE_BAND','1')!='0' else '')+('\n'+(H/'polish_cycle.css').read_text()+'\n'+(H/'polish.css').read_text() if os.environ.get('SUITE_POLISH','1')!='0' else ''))
if os.environ.get('SUITE_POLISH','1')!='0':(D/'assets/polish.js').write_text((H/'polish.js').read_text())
(H/'routes.json').write_text(json.dumps(routes,indent=2))
(H/'ROUTES.md').write_text('# Actual HTML route inventory\n\n'+ '\n'.join('- '+x['route']+' (`'+x['file']+'`) — '+x['family'] for x in routes)+'\n')
# The server assistant's old snapshot still contained the removed CV/colleague copy.
# Derive its factual payload ONLY from the same approved, public HTML; never private notes.
knowledge=[]
for name in ('index','about','advisory','speaking','writing','contact'):
    page=BeautifulSoup((D/(name+'.html')).read_text(),'html.parser').select_one('main')
    for el in page.select('script,style,template'):el.decompose()
    text='\n'.join(t.strip() for t in page.stripped_strings)
    knowledge.append('=== PAGE: '+name+' ===\n'+text)
kp=H.parent/'review_deploy/functions/api/_knowledge.js'
kp.write_text('export default '+json.dumps('\n\n'.join(knowledge))+';\n')
print('Normalized',len(routes),'HTML routes; assistant knowledge refreshed from public HTML')
# Polish a11y: game panels render h3 straight after the page h1 (axe heading-order). Expose them as level 2, idempotently.
if os.environ.get('SUITE_POLISH','1')!='0':
 g=D/'assets/games.js';gt=g.read_text();ng=gt.replace("<h3 aria-level=\"2\"","<h3").replace("<h3","<h3 aria-level=\"2\"")
 if ng!=gt:g.write_text(ng)
