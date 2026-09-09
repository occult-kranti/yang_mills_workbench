#!/usr/bin/env python3
"""Preview the built GitHub project site at its actual URL prefix."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import argparse
import json
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
def make_server(port=8002):
    docs=ROOT/'docs'
    prefix=json.loads((docs/'build-manifest.json').read_text())['base']
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(docs),**kwargs)
        def send_head(self):
            path=urlsplit(self.path).path
            if path=='/':
                self.send_response(302);self.send_header('Location',prefix);self.end_headers();return None
            if not path.startswith(prefix):self.send_error(404);return None
            self.path='/'+self.path[len(prefix):]
            return super().send_head()
        def log_message(self,*args):pass
    return ThreadingHTTPServer(('127.0.0.1',port),Handler),prefix

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8002);a=p.parse_args()
    if not 1<=a.port<=65535:p.error('port must be between 1 and 65535')
    server,prefix=make_server(a.port)
    print(f'Serving static Pages preview at http://127.0.0.1:{a.port}{prefix}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
