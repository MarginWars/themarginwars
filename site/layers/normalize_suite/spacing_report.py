import json,sys,glob
from collections import Counter,defaultdict
d={};[d.update(json.load(open(f))) for f in glob.glob(sys.argv[1]+'/spacing_*.json')]
W=[320,375,390,430,768,1024,1280,1440,1920];T=defaultdict(Counter);sel=defaultdict(Counter)
for k,v in d.items():
 f,w=k.split('|');w=int(w)
 T[w]['cases']+=1;T[w]['edge']+=v['edgeDev'];T[w]['intrusions']+=v['nIntr'];T[w]['rhythm']+=len(v['rhythm']);T[w]['heading_body']+=len(v['hb']);T[w]['overflow']+=v['overflow']
 for x in v['rhythm']:sel['rhythm'][x['sec']+' '+x['side']]+=1
 for x in v['intr']:sel['intr'][f+' '+x['el']]+=1
 for x in v['hb']:sel['hb'][f+' '+x['h']+' '+str(x['gap'])+'/'+str(x['want'])]+=1
 if v['edgeDev']:sel['edge'][f+' L%s R%s E%s'%(v['minL'],v['minR'],v['E'])]+=1
print('| width | cases | edge dev | edge intrusions | section rhythm | heading→body | overflow |\n|---|---|---|---|---|---|---|')
for w in W:t=T[w];print(f"| {w} | {t['cases']} | {t['edge']} | {t['intrusions']} | {t['rhythm']} | {t['heading_body']} | {t['overflow']} |")
if len(sys.argv)>2:
 for k,c in sel.items():print('\n##',k,len(c));[print(n,x) for x,n in c.most_common(int(sys.argv[2]))]
