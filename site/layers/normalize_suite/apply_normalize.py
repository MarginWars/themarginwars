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
 for a in s.select('a[href]'):
  classes=[c for c in a.get('class',[]) if c not in ('nm-inline','nm-primary')]
  if not a.find(['img','svg','div','h1','h2','h3','h4','p','figure','ul','ol']) and not any(c in classes for c in ['brand','f-brand','skip','f-skip','gc','rd']):classes.append('nm-inline')
  if ('btn' in classes and 'alt' not in classes) or 'rb-cta' in classes:classes.append('nm-primary')
  if classes:a['class']=classes
 f.write_text(str(s))
 rel=str(f.relative_to(D));family=rel.split('/')[0] if '/' in rel else ('games' if f.stem in ['arcade','daily','deal','leak','quiz','tracewire'] or f.stem.startswith('ep') else 'core')
 routes.append({'file':rel,'route':'/'+('' if rel=='index.html' else rel[:-10] if rel.endswith('index.html') else rel[:-5]),'family':family,'controls':len(s.select('button,input,select,summary')),'links':len(s.select('a[href]'))})
(D/asset).write_text((H/'suite.css').read_text()+('\n'+(H/'relief.css').read_text() if os.environ.get('SUITE_RELIEF','1')!='0' else '')+('\n'+(H/'balance.css').read_text() if os.environ.get('SUITE_BALANCE','1')!='0' else '')+'\n'+(H/'spacing.css').read_text()+('\n'+(H/'roles.css').read_text() if os.environ.get('SUITE_ROLES','1')!='0' else '')+('\n'+(H/'band.css').read_text() if os.environ.get('SUITE_BAND','1')!='0' else ''))
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
