"""Cross-engine pixel-diff gate. usage: qa_diff.py SHOTS_DIR OUT_DIR [threshold_pct]
Compares the first screen (viewport height) and the full-page height of WebKit and Firefox against Chromium at the same width.
Pairs above the threshold get a side-by-side sheet in OUT_DIR for visual review."""
import sys,glob,os,json
from pathlib import Path
from PIL import Image,ImageChops
S,O=Path(sys.argv[1]),Path(sys.argv[2]);T=float(sys.argv[3]) if len(sys.argv)>3 else 4.0;O.mkdir(parents=True,exist_ok=True)
VH={'w375':812,'w390':844,'w768':1024,'w1440':900};res=[]
for ref in sorted(S.glob('chromium_*.png')):
 _,prof,base=ref.stem.split('_',2)
 if prof not in VH:continue
 a=Image.open(ref).convert('RGB')
 for eng in ('webkit','firefox'):
  q=S/f'{eng}_{prof}_{base}.png'
  if not q.exists():continue
  b=Image.open(q).convert('RGB');w=min(a.width,b.width);h=min(VH[prof],a.height,b.height)
  ca,cb=a.crop((0,0,w,h)),b.crop((0,0,w,h));d=ImageChops.difference(ca,cb).convert('L').point(lambda v:255 if v>48 else 0)
  pct=100*sum(1 for v in d.getdata() if v)/(w*h);hd=abs(a.height-b.height)/max(a.height,1)*100
  r={'route':base,'width':prof,'engine':eng,'first_screen_diff_pct':round(pct,2),'page_height_delta_pct':round(hd,2),'review':pct>T or hd>3}
  if r['review']:
   sh=Image.new('RGB',(w*3+20,h),'#ff00ff');sh.paste(ca,(0,0));sh.paste(cb,(w+10,0));sh.paste(d.convert('RGB'),(2*w+20,0))
   sc=min(1,1800/sh.width);sh=sh.resize((int(sh.width*sc),int(h*sc)));sh.save(O/f'{base}_{prof}_{eng}.jpg',quality=80)
  res.append(r)
(O/'diff.json').write_text(json.dumps(res,indent=1))
flag=[r for r in res if r['review']];print(len(res),'pairs;',len(flag),'flagged for visual review (threshold',T,'% first-screen, 3% page height)')
for r in sorted(flag,key=lambda r:-r['first_screen_diff_pct'])[:40]:print(r)
