import sys,json
sys.path.insert(0,'.');from play import play
from playwright.sync_api import sync_playwright
AXE=open('/tmp/axe/node_modules/axe-core/axe.min.js').read();res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for g in ['daily','leak','deal','quiz','ep1','ep2','tracewire','arcade']:
        for w in (390,1440):
            for site,url in (('share','http://localhost:8872/' if g in ('ep2','tracewire') else 'http://localhost:8871/'),):
                c=b.new_context(viewport={'width':w,'height':900},reduced_motion='reduce');pg=c.new_page();play(pg,g,url)
                pg.add_script_tag(content=AXE)
                r=pg.evaluate("async()=>{const r=await axe.run(document,{resultTypes:['violations']});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes.map(n=>n.target.join(' ')).slice(0,4)}))}")
                inm=[v for v in r if any('mws' in t for t in v['t'])]
                res[f'{g}|{w}']={'all':r,'in_share':inm};c.close()
        print(g,[(v['id'],v['impact'],v['n']) for v in res[f'{g}|390']['all']],'share-scope:',[v['id'] for v in res[f'{g}|390']['in_share']],flush=True)
    b.close()
json.dump(res,open('qa/axe.json','w'),indent=1)
