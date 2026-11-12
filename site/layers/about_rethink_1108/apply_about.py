"""Full About layout. Idempotent. Run after tighten, before feeds. Approved content only."""
from pathlib import Path
from PIL import Image
import sys,shutil,os,json
from bs4 import BeautifulSoup
H=Path(__file__).parent; D=Path(sys.argv[1]) if len(sys.argv)>1 else H.parent/'site_calm'
Image.open(D/'assets/people/avi-portrait.webp').crop((50,0,270,220)).save(D/'assets/people/avi-hero.webp',quality=92)
p=D/'about.html'; s=BeautifulSoup(p.read_text(),'html.parser')
ppl=BeautifulSoup((H/'ppl_section.html').read_text(),'html.parser')
ppl.select_one('.ppl-h').decompose()
for top in ppl.select('.pc-top'): top.img.decompose()
for card in ppl.select('.pc'): card.select_one('.pc-sl').string='Field record'
ppl.section['class']=['ppl']; ppl.section['aria-labelledby']='field-title'
intro='''<section class="ab-hero"><div class="ab-intro"><p class="ab-k">The Margin Wars / About</p><h1>Avi &amp; Anitha</h1><p class="ab-eight">Eight years working side by side.</p><p class="ab-lede">One team, for anyone tired of hearing “negotiate the rate”.</p><a class="ab-link" href="#field-title">The field record ↓</a></div><div class="ab-portraits"><figure><img src="assets/people/avi-hero.webp" alt="Avi" width="320" height="320"><figcaption>Avi</figcaption></figure><figure><img src="assets/people/anitha-portrait.webp" alt="Anitha" width="320" height="320"><figcaption>Anitha</figcaption></figure></div></section>'''
body=intro+'<div class="ab-flow"><h2 id="field-title" class="ab-label">The field record</h2>'+str(ppl.section)+(H/'about_support.html').read_text()+'</div>'
mode=os.environ.get('ABOUT_PALETTE',json.loads((H/'palette_config.json').read_text())['mode'])
assert mode in ('original','status','technicolor')
if mode in ('status','technicolor'):
 support=BeautifulSoup((H/'about_support.html').read_text(),'html.parser')
 method=support.select_one('.bgs.team'); edu=support.select_one('.edu-s')
 watch=support.select_one('#watch'); conf=support.select_one('.split.flip')
 for ns in watch.select('.vframe noscript'):
  frame=ns.parent; ns.extract(); frame.insert_after(ns)
 stages=next(x for x in support.select('section') if x.find('h2',string=lambda t:t and 'made the case' in t))
 def band(cls,content): return '<div class="ab-band '+cls+'"><div class="ab-flow">'+content+'</div></div>'
 body=intro+band('ab-evidence','<h2 id="field-title" class="ab-label">The field record</h2>'+str(ppl.section))+band('ab-method',str(method)+str(edu))+band('ab-archive',str(stages)+str(watch))+band('ab-conf',str(conf))
for old in s.select('link[href="assets/about-palette.css"],link[href="assets/about-spectrum.css"]'): old.decompose()
s.body['class']=[c for c in s.body.get('class',[]) if c not in ('about-palette','about-spectrum')]
if mode in ('status','technicolor'):
 s.body['class'].append('about-palette')
 link=s.new_tag('link',rel='stylesheet',href='assets/about-palette.css');s.head.append(link)
 shutil.copy(H/'about-palette.css',D/'assets'/'about-palette.css')
if mode=='technicolor':
 s.body['class'].append('about-spectrum')
 link=s.new_tag('link',rel='stylesheet',href='assets/about-spectrum.css');s.head.append(link)
 shutil.copy(H/'about-spectrum.css',D/'assets'/'about-spectrum.css')
s.main.clear();s.main.append(BeautifulSoup(body,'html.parser'))
s.body['class']=list(set(s.body.get('class',[])+['about-clean']))
if not s.select_one('link[href="assets/about-clean.css"]'):
 l=s.new_tag('link',rel='stylesheet',href='assets/about-clean.css');s.head.append(l)
for f in ('ppl.css','about-clean.css'):shutil.copy(H/f,D/'assets'/f)
p.write_text(str(s)); print('Full About ->',p)
