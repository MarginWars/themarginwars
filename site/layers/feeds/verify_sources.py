import json,subprocess,concurrent.futures
from pathlib import Path
H=Path(__file__).parent
sources=json.loads((H/'source-registry.json').read_text())['sources']; (H/'sources').mkdir(exist_ok=True)
def check(kv):
 k,u=kv;p=H/'sources'/k
 r=subprocess.run(['curl','--location','--max-time','60','--silent','--show-error','--output',str(p),'--write-out','%{http_code}\t%{url_effective}',u],capture_output=True,text=True)
 result=dict(key=k,url=u,status=r.stdout,exit=r.returncode,bytes=p.stat().st_size if p.exists() else 0)
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(check,sources.items()))
(H/'source-checks.json').write_text(json.dumps(rows,indent=2))
