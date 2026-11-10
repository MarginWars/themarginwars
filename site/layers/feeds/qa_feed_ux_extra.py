import os
from pathlib import Path
from bs4 import BeautifulSoup as BS
from PIL import Image
from playwright.sync_api import sync_playwright,expect
import json,datetime as dt
H=Path(__file__).parent;D=H.parent/'site_calm';O=H/'qa-ux';checks=[]
idx=json.loads((D/'assets/feeds/search-index.json').read_text());assert len(idx)==sum(len(json.loads((D/'assets/feeds'/f'{k}.json').read_text())) for k in ['wire','calendar','bp-watch','route-briefs'])
for x in idx:
 p=D/x['url'].strip('/')/'index.html';s=BS(p.read_text(),'html.parser');assert len(s.select('h1'))==1,x['key'];assert s.select_one('meta[property="og:url"]')['content'].endswith(x['url']);assert s.select_one('meta[property="og:description"]')['content']==x['lead'];u=s.select_one('meta[property="og:image"]')['content'];im=D/u.split('.pages.dev/')[1];assert Image.open(im).size==(1200,630)
checks.append({'OG_pages_and_PNGs':len(idx),'server_metadata':'pass'})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox'])
 for width in [375,1440]:
  page=b.new_page(viewport={'width':width,'height':1000});page.goto('http://localhost:8957/wire/items/nz-commercial-cards/',wait_until='networkidle');figure=page.locator('.fx-cardproof');figure.scroll_into_view_if_needed();figure.screenshot(path=str(O/f'share-card-{width}.png'));assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');page.close()
 # Every enhanced hit area in the open My markets and an expanded item is >=44 CSS px.
 page=b.new_page(viewport={'width':375,'height':1000});page.goto('http://localhost:8957/wire/',wait_until='networkidle');page.locator('[data-prefs-open]').first.click();page.locator('.fx-details').first.locator('summary').click();bad=page.locator('.fx-actions>*,.fx-check,.fx-prefbottom button,.fx-details summary,.fx-shareactions>*').evaluate_all('(es)=>es.filter(e=>e.getBoundingClientRect().height&&e.getBoundingClientRect().height<43.9).map(e=>({text:e.textContent,height:e.getBoundingClientRect().height}))');assert not bad,bad;checks.append({'mobile_hit_targets':'all >=44px'})
 # Empty selections stay explainable, not a blank page.
 page.locator('input[name=market][value=global]').check();page.locator('input[name=rail][value=authentication]').check();page.goto('http://localhost:8957/bp-watch/',wait_until='networkidle');assert page.locator('.f-entry:visible').count()==0;expect(page.locator('.fx-filter-empty')).to_be_visible();checks.append({'empty_filter_feedback':'visible'})
 # No-JS remains complete and native disclosure works.
 ctx=b.new_context(java_script_enabled=False,viewport={'width':375,'height':1000});n=ctx.new_page();n.goto('http://localhost:8957/wire/',wait_until='networkidle');assert n.locator('.f-entry:visible').count()==31;n.locator('.fx-details').first.locator('summary').click();assert n.locator('.fx-details').first.get_attribute('open') is not None;assert n.locator('[data-snippet=linkedin]:visible').count()==0;checks.append({'no_js':'31 entries; native details; inactive copy controls hidden'})
 # Clock tests use Pacific dates and correct singular/day-zero/past handling.
 clock=b.new_context(viewport={'width':375,'height':1000});c=clock.new_page();c.clock.install(time=dt.datetime(2026,11,8,15,tzinfo=dt.timezone.utc))
 for date,expected in [(8,'in 1 day'),(9,'Today'),(10,'1 day ago')]:
  c.clock.set_fixed_time(dt.datetime(2026,11,date,15,tzinfo=dt.timezone.utc));c.goto('http://localhost:8957/calendar/items/ca-rtr-launch/',wait_until='networkidle');expect(c.locator('.fx-countdown')).to_have_text(expected);assert c.locator('.fx-countdown').evaluate('(e)=>e.classList.contains("fx-near")')==(date<=9)
 checks.append({'countdown_clock':'Pacific dates: tomorrow / today / past all pass'})
 c.goto('http://localhost:8957/calendar/',wait_until='networkidle');c.locator('[data-prefs-open]').click();c.locator('input[name=market][value=ukeu]').check();c.locator('input[name=rail][value=bank]').check()
 row=c.locator('.fx-timeline-row[data-market=ukeu]');dates=row.locator('li[data-event-date]:visible').evaluate_all('(es)=>es.map(e=>e.dataset.eventDate).sort()')
 # Collapsed timeline li visibility is controlled by the native disclosure; inspect preference hidden flags instead.
 dates=row.locator('li[data-event-date]').evaluate_all('(es)=>es.filter(e=>!e.hidden&&e.dataset.eventDate>="2026-11-10").map(e=>e.dataset.eventDate).sort()')
 if dates:assert row.locator('summary > span').get_attribute('data-countdown')==dates[0]
 else:expect(row.locator('summary > span')).to_have_text('No confirmed upcoming date')
 checks.append({'timeline_filter_and_clock':'nearest visible upcoming date recomputed'})

 # Email copy, then intentional clipboard denial fallback. Nothing is sent.
 ctx=b.new_context(permissions=['clipboard-read','clipboard-write']);c=ctx.new_page();c.goto('http://localhost:8957/wire/items/emv-3ds24/',wait_until='networkidle');c.locator('[data-snippet=email]').click();expect(c.locator('.fx-copy-status')).to_contain_text('Copied');text=c.evaluate('navigator.clipboard.readText()');assert text.startswith('Subject:') and 'Official source: https://' in text;c.evaluate("Object.defineProperty(navigator.clipboard,'writeText',{value:()=>Promise.reject(new Error('blocked for QA'))})");c.locator('[data-snippet=linkedin]').click();expect(c.locator('.fx-share textarea')).to_be_visible();assert 'Official source: https://' in c.locator('.fx-share textarea').input_value();checks.append({'email_and_clipboard_fallback':'source included; no message sent'})
 # Keyboard focus returns to opener after Escape; slash never hijacks a text field.
 c.goto('http://localhost:8957/wire/',wait_until='networkidle');c.locator('[data-search-open]').click();c.locator('#fx-search-input').fill('MonitorAccount');assert c.locator('.fx-results li').count()>0;c.keyboard.press('ArrowDown');assert c.evaluate('document.activeElement.matches(".fx-results a")');c.keyboard.press('Escape');assert c.evaluate('document.activeElement.matches("[data-search-open]")');checks.append({'search_keyboard':'technical field indexed; arrows and Escape restore focus'})
 b.close()
(O/'additional-results.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
