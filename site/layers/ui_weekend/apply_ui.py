"""Weekend UI layer (Nov 7 2026). Idempotent. Applies to site_calm/*.html."""
import re, pathlib, sys, shutil
for _f in ("wk.css","wk.js"): shutil.copy(pathlib.Path(__file__).parent/_f, pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "@MW_ROOT@/site_calm")/"assets"/_f)
D=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '@MW_ROOT@/site_calm')
TAG='<link rel="stylesheet" href="assets/wk.css"><script src="assets/wk.js" defer></script>'
SOON='Coming soon'
for f in sorted(D.glob('*.html')):
    s=o=f.read_text()
    if 'assets/wk.css' not in s: s=s.replace('</head>',TAG+'</head>',1)
    # single swappable logo component
    s=re.sub(r'<a class="brand" href="index.html">','<a class="brand" href="index.html" data-logo="current">',s)
    s=s.replace('content="width=device-width,initial-scale=1"','content="width=device-width,initial-scale=1,viewport-fit=cover"')
    n=f.name
    if n=='arcade.html':
        for k in range(2,10):
            s=re.sub(r'<li><a href=ep%d\.html>(.*?)<span class="es"[^>]*>.*?</span></a></li>'%k,
                     lambda m:'<li class="wk-soon"><span class="wk-off" aria-disabled="true">%s<span class="es">%s</span></span></li>'%(m.group(1),SOON),s,flags=re.S)
        s=re.sub(r'<a class="rt-hero" href="tracewire.html">(.*?)<span class="go">[^<]*</span></div>(.*?)</a>',
                 lambda m:'<div class="rt-hero wk-off" aria-disabled="true">%s<span class="go">%s</span></div>%s</div>'%(m.group(1),SOON,m.group(2)),s,flags=re.S)
    if n=='ep1.html':
        s=s.replace('<a class="btn" href="ep2.html">Episode 2: Close Quarters</a>','<span class="btn wk-off" aria-disabled="true">Episode 2: Close Quarters · %s</span>'%SOON)
    if re.fullmatch(r'ep[2-9]\.html|tracewire\.html',n):
        s=re.sub(r'<section class="gm[^"]*" data-game="[^"]*"[^>]*></section>','<section class="gm wk-soon-panel" aria-label="%s"><p class="wk-soon-k">%s</p></section>'%(SOON,SOON),s)
    if s!=o: f.write_text(s); print('updated',n)

# Nov 8: Australia & NZ terrain lane (split from APAC), UK Finance stop. Idempotent.
def _stop(j,t,b,k): return '<li class="tm-s" style="--j:%d" title="%s"><span class="tm-d" aria-hidden="true"></span><b>%s</b><i>%s</i></li>'%(j,t,b,k)
def _lane(n,label,stops):
    return ('<div class="tm-lane" tabindex="0" role="group" aria-label="%s"><p class="tm-r"><span>%s</span>%s</p><ol class="tm-stops"><span class="tm-line" aria-hidden="true"><i></i></span>%s</ol></div>'
            %(label,n,label,''.join(_stop(j,*x) for j,x in enumerate(stops))))
APAC=[('Central bank and payments regulator','RBI','central bank'),('Operates retail payment systems','NPCI','operator')]
ANZ=[('Real-time payments platform','NPP','rail'),('Business-initiated real-time account payments','PayTo','rail'),('Domestic debit card scheme','eftpos','scheme'),
     ('Central bank; Payments System Board','RBA','central bank'),('Corporate and financial services regulator','ASIC','regulator'),('Prudential regulator for banks','APRA','regulator'),
     ('AML/CTF regulator and financial intelligence unit','AUSTRAC','regulator'),('Australian Payments Network; industry self-regulatory body','AusPayNet','industry body'),
     ('Runs NPP and PayTo','Australian Payments Plus','operator'),('NZ; regulates Mastercard and Visa interchange','Commerce Commission','regulator'),
     ('Governs the rules for NZ core payment systems','Payments NZ','industry body'),('Bank acquirers in RBA least-cost routing reporting','ANZ · CBA · NAB · Westpac','acquirers')]
for f in sorted(D.glob('*.html')):
    s=o=f.read_text()
    if 'class="tm-lane"' not in s or 'aria-label="Australia &amp; NZ"' in s: continue
    s=re.sub(r'<div class="tm-lane" tabindex="0" role="group" aria-label="APAC">.*?</ol></div>',
             lambda m:_lane('05','APAC',APAC)+_lane('06','Australia &amp; NZ',ANZ),s,count=1,flags=re.S)
    s=s.replace('<p class="tm-r"><span>06</span>Global</p>','<p class="tm-r"><span>07</span>Global</p>')
    s=re.sub(r'(aria-label="UK / EU">.*?)(</ol></div>)',lambda m:m.group(1)+_stop(8,'UK banking and finance trade association','UK Finance','industry body')+m.group(2),s,count=1,flags=re.S)
    if s!=o: f.write_text(s); print('anz lane',f.name)
