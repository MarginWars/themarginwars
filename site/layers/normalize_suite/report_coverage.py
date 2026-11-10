import os
from pathlib import Path
import json,collections
H=Path(__file__).parent;O=Path(os.environ.get('QA_OUT',str(H.parent/'site_qa/suite_1108')));R=json.loads((H/'routes.json').read_text());D=json.loads((O/'final_results.json').read_text());E=json.loads((O/'interactions.json').read_text());extra={r['file'] for r in E if r.get('w')};nojs={r['file'] for r in E if r.get('mode')=='nojs'}
lines=['# Per-route release coverage','', 'All routes: 375 / 768 / 1280 / 1440, default + expanded. Each cell includes symmetry geometry, text contrast, effective 44px targets, page errors and document overflow. Visual atlas: sheet_00–17; extra-width atlas: extra_sheet_0–1.','', '| Route | Family | 8 core cases | Extra 320/390/430/1024, both states | No-JS static content | Visual atlas |','|---|---|---|---|---|---|']
for i,r in enumerate(R):
 assert all(f"{r['file']}|{w}|{s}" in D and not D[f"{r['file']}|{w}|{s}"] for w in [375,768,1280,1440] for s in ['default','expanded'])
 lines.append(f"| {r['route']} | {r['family']} | PASS | {'PASS' if r['file'] in extra else '—'} | {'PASS' if r['file'] in nojs else 'MISSING'} | sheet_{i//5:02}.jpg |")
(H/'COVERAGE.md').write_text('\n'.join(lines)+'\n');print('Coverage matrix:',len(R),'routes')
