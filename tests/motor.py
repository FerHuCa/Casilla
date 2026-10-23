exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__) or '.','run.py')).read().split('logs=[]')[0])
import time, threading, functools, http.server
# Por http: Stockfish 19 vive en engine/ (mismo origen) y un worker no puede importScripts de file://.
class _H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
_srv=http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(_H, directory=str(_HERE.parent)))
threading.Thread(target=_srv.serve_forever, daemon=True).start()
APP='http://127.0.0.1:%d/index.html'%_srv.server_address[1]
F=0
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':900}); ctx.route('**/*',handle); pg=ctx.new_page()
    for q,exp in [('', 'WASM 19 lite'), ('?sf=10', 'WASM')]:
        pg.goto(APP+q); pg.wait_for_function("Engine.ready",timeout=60000)
        fl=pg.evaluate("Engine.flavor"); ok=fl==exp; F+=not ok
        print('OK ' if ok else 'FALLA ', 'motor', q or '(defecto)', fl)
        r=pg.evaluate("""()=>new Promise(res=>{const w=Engine.w;const old=w.onmessage;w.onmessage=e=>{if(String(e.data).startsWith('bestmove')){w.onmessage=old;res(String(e.data))}};w.postMessage('position startpos');w.postMessage('go depth 8');})""")
        ok=r.startswith('bestmove ') and len(r.split()[1])>=4; F+=not ok
        print('OK ' if ok else 'FALLA ', 'jugada', r)
    b.close()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
