import re,html,sys,pathlib
D=pathlib.Path(sys.argv[1])
def words(s):
    s=re.sub(r'(?s)<(script|style|svg|head).*?</\1>',' ',s); s=re.sub(r'<[^>]+>',' ',s)
    return len(html.unescape(s).split())
t=0
for f in sorted(D.glob('*.html')):
    n=words(f.read_text()); t+=n; print(f.name,n)
print('TOTAL',t)
