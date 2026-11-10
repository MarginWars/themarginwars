from pathlib import Path
import os
from playwright.sync_api import sync_playwright
O=Path(os.environ.get('QA_OUT',str(Path(__file__).parent.parent/'site_qa/suite_1108')))
B=os.environ.get('SCREEN_BASE','http://localhost:8817');PRE=os.environ.get('SCREEN_PREFIX','')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for w in (375,1440):
  for f,name,sel in [('index.html','home_wire','.f-strip'),('about.html','about','main'),('advisory.html','route_brief','#route-brief'),('wire/index.html','wire','main'),('deal.html','deal','main')]:
   P=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');P.goto(B+'/'+f,wait_until='networkidle');P.evaluate('window.scrollTo(0,document.body.scrollHeight)');P.wait_for_timeout(400)
   P.add_style_tag(content='body>header{visibility:hidden!important}');P.locator(sel).screenshot(path=str(O/f'{PRE}{name}_{w}.png'));P.add_style_tag(content='body>header{visibility:visible!important}')
   if name=='about':P.evaluate('window.scrollTo(0,0)');P.screenshot(path=str(O/f'{PRE}about_first_{w}.png'));P.screenshot(path=str(O/f'{PRE}about_full_{w}.png'),full_page=True)
   if name=='wire':
    P.evaluate('window.scrollTo(0,0)');P.screenshot(path=str(O/f'{PRE}wire_first_{w}.png'));P.locator('.f-entry').first.scroll_into_view_if_needed();P.screenshot(path=str(O/f'{PRE}wire_reading_{w}.png'))
   if name=='about':
    P.add_style_tag(content='body>header{visibility:hidden!important}');P.locator('.pc').nth(1).screenshot(path=str(O/f'{PRE}anitha_{w}.png'))
   P.close()
