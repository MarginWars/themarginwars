#!/usr/bin/env python3
"""Serve site/dist for the browser gates (default port 8817), like Pages: /x -> x.html, /dir/ -> dir/index.html, unknown -> 404.html."""
import http.server, os, sys
from pathlib import Path
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'site/dist').resolve()
PORT = int(sys.argv[2] if len(sys.argv) > 2 else 8817)
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a): pass
    def send_head(self):
        p = self.path.split('?')[0].split('#')[0]
        f = ROOT / p.lstrip('/')
        if not f.exists() and (ROOT / (p.lstrip('/') + '.html')).exists(): self.path = p + '.html'
        elif not f.exists():
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
            body = (ROOT / '404.html').read_bytes(); self.send_header('Content-Length', str(len(body))); self.end_headers()
            self.wfile.write(body); return None
        return super().send_head()
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
