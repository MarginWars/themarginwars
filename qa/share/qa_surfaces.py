import sys,json
sys.path.insert(0,'.');from play import play
from qa_share import MJS
from playwright.sync_api import sync_playwright
P=[('dark390',{'viewport':{'width':390,'height':844},'color_scheme':'dark'}),('forced1440',{'viewport':{'width':1440,'height':900},'forced_colors':'active'}),
   ('reduced390',{'viewport':{'width':390,'height':844},'reduced_motion':'reduce'}),('zoom200',{'viewport':{'width':720,'height':450},'device_scale_factor':2}),
   ('phoneL844',{'viewport':{'width':844,'height':390},'has_touch':True,'is_mobile':True}),('d1920',{'viewport':{'width':1920,'height':1080}}),('d2560',{'viewport':{'width':2560,'height':1440}})]
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for g in ['daily','quiz','ep1','arcade']:
        for n,o in P:
            c=b.new_context(**o);pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));play(pg,g,'http://localhost:8871/')
            r=pg.evaluate(MJS);res[f'{g}|{n}']={'issues':r['issues'],'overflow':r['overflow'],'rows':r['rows'],'errors':errs}
            if g=='daily' and n in('forced1440','dark390'):
                m=pg.query_selector_all('.mws')[-1];m.screenshot(path=f'qa/surface_{g}_{n}.png')
            c.close()
    b.close()
json.dump(res,open('qa/surfaces.json','w'),indent=1)
print({k:v for k,v in res.items() if v['issues'] or v['overflow'] or v['errors']} or 'all surfaces clean', len(res),'cases')
