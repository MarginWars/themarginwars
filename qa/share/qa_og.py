import sys,json,pathlib
from html.parser import HTMLParser
from PIL import Image
D=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
GAMES=["daily","tracewire","leak","deal","quiz"]+[f"ep{i}" for i in range(1,10)]+["arcade"]
class P(HTMLParser):
    def __init__(s):super().__init__();s.m={};s.dup=[];s.canon=None;s.title=''
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='meta':
            k=a.get('property') or a.get('name')
            if k and (k.startswith('og:') or k.startswith('twitter:')):
                if k in s.m:s.dup.append(k)
                s.m[k]=a.get('content')
        if t=='link' and a.get('rel')=='canonical':s.canon=a.get('href')
res={};fails=[]
for g in GAMES:
    p=P();p.feed((D/f'{g}.html').read_text());m=p.m;f=[]
    need=['og:title','og:description','og:url','og:image','og:image:width','og:image:height','og:image:alt','og:type','twitter:card','twitter:title','twitter:description','twitter:image','twitter:image:alt']
    f+=[f'missing {k}' for k in need if not m.get(k)]
    if m.get('twitter:card')!='summary_large_image':f.append('card type')
    if m.get('og:url')!=p.canon:f.append('og:url != canonical')
    img=m.get('og:image','');
    if img!=f'https://themarginwars.com/assets/brand/og/{g}.png':f.append('og:image path')
    if m.get('twitter:image')!=img:f.append('twitter:image differs')
    loc=D/img.replace('https://themarginwars.com/','')
    if loc.exists():
        im=Image.open(loc);sz=loc.stat().st_size
        if im.size!=(1200,630):f.append(f'size {im.size}')
        if sz>5_000_000:f.append('too big')
    else:f.append('image file missing')
    if (m.get('og:image:width'),m.get('og:image:height'))!=('1200','630'):f.append('declared dims')
    if p.dup:f.append(f'duplicate {p.dup}')
    if len(m.get('og:title',''))>70:f.append('title long')
    res[g]={'og:title':m.get('og:title'),'og:description':m.get('og:description'),'og:image':img,'bytes':loc.stat().st_size if loc.exists() else 0,'fails':f}
    if f:fails.append((g,f))
json.dump(res,open('qa/og.json','w'),indent=1)
print('OG pages',len(GAMES),'fails',fails)
for g,r in res.items():print(f"{g:10} {r['og:title']!r:45} {r['bytes']//1024}KB")
