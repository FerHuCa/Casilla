# E2E contra los orígenes reales (necesita internet): sirve el sitio por http local, sin simular red
# (cdnjs, jsDelivr, Lichess y Chess.com reales), llena la memoria de puzzles y luego pasa a modo avión.
import os, sys, time, json, re, shutil, tempfile, threading, functools, http.server, pathlib
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
SITE=tempfile.mkdtemp(prefix='casilla-real-')
for n in os.listdir(ROOT):
    if n in ('tests','.git','docs'): continue
    s=ROOT/n; (shutil.copytree if s.is_dir() else shutil.copy)(s, os.path.join(SITE,n))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(H, directory=SITE))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL='http://127.0.0.1:%d/'%srv.server_address[1]
SHOTS=os.environ.get('CASILLA_SHOTS', str(ROOT/'tests/out/offline-ui'))+'/'; os.makedirs(SHOTS, exist_ok=True)
F=0; NET=[]
def check(n,c,x=''):
    global F; F+=not c; print('OK ' if c else 'FALLA ', n, x, flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':800})
    ST=[]; ctx.on('response', lambda r: ST.append((time.time(), r.status, r.url)) if '/api/puzzle/batch/' in r.url else None)
    ctx.on('request', lambda r: NET.append((time.time(), r.url)) if ('lichess.org' in r.url or 'chess.com' in r.url) else None)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(URL); pg.wait_for_function("navigator.serviceWorker.controller && Engine.ready && document.querySelector('#ver').textContent.startsWith('v')",timeout=180000)
    check('SW real instalado, pie con versión', True, pg.inner_text('#ver'))
    t0=time.time()
    while time.time()-t0<300 and pg.evaluate("PuzzleStore.count('lichess')")<200: pg.wait_for_timeout(5000)
    print('LOTES', [(round(t-t0), st, u.split('/batch/')[1]) for t,st,u in ST])
    r429=[t for t,st,u in ST if st==429]
    if r429:
        nxt=[t for t,st,u in ST if t>r429[0]]
        check('429 real de Lichess: el siguiente lote espera >= 60 s', not nxt or nxt[0]-r429[0]>=59, str([round(x-r429[0]) for x in nxt[:1]]))
    li=pg.evaluate("PuzzleStore.count('lichess')"); cc=pg.evaluate("PuzzleStore.count('chesscom')")
    print('GUARDADOS lichess',li,'chesscom',cc,'etapa',pg.evaluate("PuzzleStore.count('lichess',PLAN[planStage()].themes)"))
    check('Lichess real guarda (200 si el límite lo permite)', li>=50, str(li))
    check('Chess.com no se guarda', cc==0 and not [u for _,u in NET if 'pub/puzzle/random' in u])
    mb=pg.evaluate("PuzzleStore.req(PuzzleStore.tx('readonly').getAll()).then(a=>+(new Blob([JSON.stringify(a)]).size/1048576).toFixed(3))")
    print('MB_IDB_REAL',mb,'para',li+cc,'puzzles')
    bat=[t for t,u in NET if '/api/puzzle/batch/' in u]
    check('Lichess real en serie (>= 19 s entre lotes)', all(b2-a>=19 for a,b2 in zip(bat,bat[1:])), str(len(bat))+' lotes')
    ctx.set_offline(True); pg.wait_for_function("!Net.on",timeout=5000)
    pg.reload(); pg.wait_for_function("typeof Engine!=='undefined' && Engine.ready && PuzzleStore.db",timeout=60000)
    check('recarga en modo avión', pg.evaluate("!navigator.onLine"))
    pg.evaluate("App.puzzleSource='lichess'; switchTab('puzzles')"); pg.wait_for_timeout(1000*1)
    check('modo avión: Lichess guardado', pg.evaluate("App.session.p && App.session.p.src")=='lichess')
    dis=pg.evaluate("[...document.querySelectorAll('[data-seg=src] button')].filter(b=>b.disabled).map(b=>b.dataset.v)")
    check('modo avión: 5a solo desactiva lo no guardado', dis==['chesscom'], str(dis))
    for w in (1280,390):
        pg.set_viewport_size({'width':w,'height':800 if w>500 else 844}); pg.wait_for_timeout(1000*.5); pg.screenshot(path=SHOTS+'real-modo-avion-puzzles-%d.png'%w)
    pg.evaluate("App.setSession(new PuzzleSession(null,{plan:{kind:'pz',stage:planStage()}}))"); pg.wait_for_timeout(1000*.6)
    check('modo avión: Táctica de la etapa con guardado', pg.evaluate("!!App.session.p"))
    pg.evaluate("switchTab('ladder')"); pg.wait_for_timeout(1000*.5)
    check('modo avión: barra 1', pg.locator('#offBar').count()==1)
    n=len(NET); pg.wait_for_timeout(1000*3); check('modo avión: sin peticiones a Lichess/Chess.com', all('lichess' not in u and 'chess.com' not in u for _,u in NET[n:]))
    b.close()
print('FALLAS',F); sys.exit(1 if F else 0)
