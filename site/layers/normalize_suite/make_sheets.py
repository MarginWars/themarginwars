import os
import json
from pathlib import Path
from PIL import Image,ImageDraw
H=Path(__file__).parent;O=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/suite_1108')));rs=json.loads((H/'routes.json').read_text())
for i in range(0,len(rs),5):
 batch=rs[i:i+5];sheet=Image.new('RGB',(1920,640*len(batch)),'#aaa');D=ImageDraw.Draw(sheet)
 for y,r in enumerate(batch):
  D.text((10,y*640+4),r['file'],fill='black')
  for x,(s,w) in enumerate((s,w) for s in ['default','expanded'] for w in [375,768,1280,1440]):
   im=Image.open(O/(r['file'].replace('/','_').replace('.html','')+f'_{w}_{s}.png'));im.thumbnail((234,595));sheet.paste(im,(x*240+(240-im.width)//2,y*640+40));D.text((x*240+5,y*640+23),f'{w} {s}',fill='black')
 sheet.save(O/f'sheet_{i//5:02}.jpg',quality=90)
print('Final contact sheets cover',len(rs),'routes, all four widths and both states')
