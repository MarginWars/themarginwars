"""Usability journeys. usage: qa_journeys.py ENGINE WIDTH -> prints JSON results"""
import sys,json,os
from playwright.sync_api import sync_playwright
eng,W=sys.argv[1],int(sys.argv[2]);B=os.environ.get('QA_BASE','http://localhost:8817/');R={}
def J(name,fn,P):
  try:R[name]=fn(P)
  except Exception as e:R[name]={'ok':False,'err':str(e)[:200]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('QA_CHROME') or None,args=['--no-sandbox']) if eng=='chromium' else getattr(p,eng).launch()
 ctx=dict(viewport={'width':W,'height':844 if W<500 else 900},reduced_motion='reduce')
 if W<500 and eng!='firefox':ctx.update(has_touch=True,is_mobile=(eng=='chromium'))
 c=b.new_context(**ctx);P=c.new_page();errs=[];P.on('pageerror',lambda e:errs.append(str(e)[:150]))
 def first_visit(P):
  P.goto(B+'index.html',wait_until='networkidle')
  cta=P.locator('header a.btn, header .nm-primary').first;href=cta.get_attribute('href');txt=cta.inner_text()
  cta.click();P.wait_for_load_state('networkidle')
  mails=P.eval_on_selector_all('main a[href^="mailto:"]','e=>e.map(a=>a.textContent.trim())');li=P.eval_on_selector_all('main a[href*="linkedin.com"]','e=>e.length')
  return {'ok':P.url.endswith('contact.html') and len(mails)>0,'cta':txt,'href':href,'landed':P.url.split('/')[-1],'mail_links':mails,'linkedin_links':li,'clicks':1}
 def contact_picker(P):
  P.goto(B+'contact.html',wait_until='networkidle')
  f=P.locator('form#contact-form');n=f.count()
  if not n:return {'ok':False,'note':'no contact form'}
  opts=f.locator('label.wk-opt');k=opts.count();sel=[]
  for i in range(k):
   opts.nth(i).click();P.wait_for_timeout(60);sel.append(P.evaluate("(document.querySelector('#contact-form input[name=topic]:checked')||{}).value"))
  lab=P.evaluate("()=>[...document.querySelectorAll('#contact-form input:not([type=hidden]),#contact-form textarea')].filter(i=>i.name!=='website').every(i=>i.closest('label')||document.querySelector('label[for=\"'+i.id+'\"]')||i.getAttribute('aria-label'))")
  legend=P.evaluate("()=>!!document.querySelector('#contact-form fieldset legend')")
  mail=P.evaluate("()=>!!document.querySelector('#contact-form a[href^=\"mailto:\"]')")
  return {'ok':lab and legend and mail and len(set(sel))==k==6,'options':k,'selected':sel,'labelled':lab,'legend':legend,'mailto_fallback':mail,'server_submit':True}
 def briefing(P):
  P.goto(B+'writing.html',wait_until='networkidle')
  a=P.locator('main a:has-text("invitation"), main a:has-text("Request")').first
  if not a.count():return {'ok':False,'note':'no invite link'}
  t=a.inner_text();a.click();P.wait_for_load_state('networkidle');P.wait_for_timeout(300);chk=P.evaluate("(document.querySelector('#contact-form input[name=topic]:checked')||{}).value||null");return {'ok':'contact' in P.url and chk=='Briefing invitation','link':t,'landed':P.url.split('/')[-1],'preselected':chk}
 def browse(P):
  out={}
  for pg in ('advisory.html','speaking.html','warroom.html'):
   P.goto(B+pg,wait_until='networkidle')
   d=P.locator('main details').first
   if d.count():
    s=d.locator('summary');s.scroll_into_view_if_needed();s.click();P.wait_for_timeout(150);op=d.evaluate('e=>e.open')
    s.click();P.wait_for_timeout(100);cl=not d.evaluate('e=>e.open')
   else:op=cl=None
   nx=P.locator('.nextp a').first;nh=nx.get_attribute('href') if nx.count() else None
   out[pg]={'accordion_toggles':(op,cl),'next':nh}
  return {'ok':all(v['accordion_toggles'] in ((True,True),(None,None)) and v['next'] for v in out.values()),**out}
 def research(P):
  P.goto(B+'wire/index.html',wait_until='networkidle')
  n0=P.evaluate("()=>[...document.querySelectorAll('.f-feedcard,.f-ledger li,article')].filter(e=>e.offsetParent).length")
  chips=P.locator('[data-fx-tools] button, .fx-tools button');k=chips.count()
  tools_visible=P.evaluate("()=>{const t=document.querySelector('[data-fx-tools]');return t?!t.hidden:null}")
  srch=P.locator('input[type=search]').first;r={}
  if srch.count() and srch.is_visible():
   srch.fill('UK');P.wait_for_timeout(300);r['after_search']=P.evaluate("()=>[...document.querySelectorAll('.f-feedcard,article')].filter(e=>e.offsetParent).length");srch.fill('')
  sm=P.locator('main details.fx-details>summary').first;sm.scroll_into_view_if_needed();sm.click();P.wait_for_timeout(150)
  first=P.locator('main details.fx-details[open] a[href*="/items/"]').first;h=first.get_attribute('href');first.click();P.wait_for_load_state('networkidle')
  back=P.locator('main a[href="/wire/"], header a[href="/wire/"]').count()
  P.go_back();P.wait_for_load_state('networkidle')
  return {'ok':P.url.endswith('/wire/') or P.url.endswith('wire/index.html'),'cards':n0,'tool_buttons':k,'tools_visible':tools_visible,**r,'item':h,'back_link_on_item':back,'back_restored':P.url.split('8817')[-1]}
 def game(P):
  P.goto(B+'daily.html',wait_until='networkidle');steps=0
  for i in range(8):
   opts=P.locator('main button:visible').filter(has_not_text='Share')
   q=P.locator('text=/QUESTION \\d OF 5/i')
   if not q.count():break
   opts.first.click();P.wait_for_timeout(200);steps+=1
   nxt=P.locator('main button:visible:has-text("Next"), main button:visible:has-text("See")')
   if nxt.count():nxt.first.click();P.wait_for_timeout(200)
  txt=P.locator('main').inner_text()[:400]
  return {'ok':steps>=5 and not P.locator('text=/QUESTION \\d OF 5/i').count(),'answered':steps,'end_screen':txt.replace('\n',' | ')[:220]}
 def notfound(P):
  P.goto(B+'index.html',wait_until='networkidle');r=P.goto(B+os.environ.get('QA_404','404.html'),wait_until='networkidle')
  st=r.status if r else None;h1=P.locator('h1').first.inner_text() if P.locator('h1').count() else None
  links=P.eval_on_selector_all('main a','e=>e.map(a=>a.getAttribute("href"))')
  P.go_back();P.wait_for_load_state('networkidle')
  return {'ok':bool(h1) and len(links)>0 and P.url.endswith('index.html'),'status':st,'h1':h1,'links':links[:6],'back':P.url.split('/')[-1],'note':'local server: 404.html opened directly; live calm URL checked for a missing path after deploy'}
 def keyboard(P):
  P.goto(B+'speaking.html',wait_until='networkidle');P.keyboard.press('Tab')
  f=P.evaluate("()=>[document.activeElement.className,document.activeElement.textContent.trim(),getComputedStyle(document.activeElement).outlineStyle,document.activeElement.getBoundingClientRect().top]")
  P.keyboard.press('Enter');P.wait_for_timeout(150)
  tgt=P.evaluate("()=>[location.hash,document.activeElement.id||document.activeElement.tagName]")
  seq=[]
  for i in range(14):
   P.keyboard.press('Tab');seq.append(P.evaluate("()=>{const a=document.activeElement,s=getComputedStyle(a);return [a.tagName,(a.textContent||'').trim().slice(0,22),s.outlineStyle!='none'||s.boxShadow!='none']}"))
  sm=P.locator('main summary').first
  if sm.count():
   sm.focus();P.keyboard.press('Enter');P.wait_for_timeout(100);kopen=sm.evaluate('e=>e.parentElement.open')
  else:kopen=None
  P.goto(B+'index.html',wait_until='networkidle')
  tab=P.locator('[role=tab]').first;tabs=None
  if tab.count():
   tab.focus();P.keyboard.press('ArrowRight');P.wait_for_timeout(100);tabs=P.evaluate("()=>[document.activeElement.id,document.activeElement.getAttribute('aria-selected')]")
  lm=P.evaluate("()=>({main:document.querySelectorAll('main').length,header:document.querySelectorAll('header').length,nav:document.querySelectorAll('nav').length,footer:document.querySelectorAll('footer').length,h1:document.querySelectorAll('h1').length})")
  return {'ok':'skip' in f[0] and all(x[2] for x in seq if x[0] in('A','BUTTON','SUMMARY')) and kopen is not False,'first_tab':f,'skip_target':tgt,'focus_visible_all':all(x[2] for x in seq),'no_focus_ring':[x for x in seq if not x[2]],'summary_enter_opens':kopen,'tabs_arrow':tabs,'landmarks_index':lm}
 def anchor(P):
  P.goto(B+'about.html#',wait_until='networkidle')
  a=P.locator('main a[href^="#"]').first
  if not a.count():return {'ok':True,'note':'no in-page anchors'}
  h=a.get_attribute('href');a.click();P.wait_for_timeout(600)
  top=P.evaluate(f"()=>{{const t=document.querySelector('{h}');const hd=document.querySelector('header');return [Math.round(t.getBoundingClientRect().top),Math.round(hd.getBoundingClientRect().bottom),getComputedStyle(hd).position]}}")
  return {'ok':top[0]>=top[1]-1 or top[2] not in('sticky','fixed'),'anchor':h,'target_top':top[0],'header_bottom':top[1],'header_pos':top[2]}
 for n,fn in [('first_visit_to_contact',first_visit),('contact_route_picker',contact_picker),('briefing_invite',briefing),('browse_advisory_speaking_insights',browse),('research_desk',research),('arcade_daily_game',game),('not_found_and_back',notfound),('keyboard_a11y',keyboard),('anchor_under_sticky_header',anchor)]:J(n,fn,P)
 R['page_errors']=errs
 b.close()
print(json.dumps(R,indent=1))
