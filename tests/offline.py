# Modo sin conexión: service worker, precache, uso sin red en 390 px, IA apagada sin red y actualización de versión.
# Sirve una copia del sitio por http (el service worker no funciona en file://) y simula la red del CDN con el arnés de run.py.
import os
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')  # para que ctx.route vea las peticiones del service worker
exec(open(os.path.join(os.path.dirname(__file__) or '.','run.py')).read().split('logs=[]')[0])
import time, shutil, tempfile, threading, functools, http.server, re
ROOT=_HERE.parent
SITE=tempfile.mkdtemp(prefix='casilla-site-')
for n in os.listdir(ROOT):
    if n in ('tests','.git','docs'): continue
    s=ROOT/n; (shutil.copytree if s.is_dir() else shutil.copy)(s, os.path.join(SITE,n))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def end_headers(self): self.send_header('Cache-Control','no-cache'); super().end_headers()
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(H, directory=SITE))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL='http://127.0.0.1:%d/'%srv.server_address[1]
F=0
def check(name, cond, extra=''):
    global F; F+=not cond; print('OK ' if cond else 'FALLA ', name, extra)
OFF={'v':False}
def handle2(route):
    if OFF['v']: return route.abort('internetdisconnected')
    u=route.request.url
    if 'api.anthropic.com' in u: return route.fulfill(status=200,headers={"Access-Control-Allow-Origin":"*"},content_type='application/json',body='{"content":[{"type":"text","text":"ok"}]}')
    if u.startswith(URL): return route.continue_()
    return handle(route)
def wait_caches(pg, cond, secs=60):
    for _ in range(secs*4):
        if pg.evaluate("caches.keys().then(k=>!!(%s))"%cond): return True
        time.sleep(.25)
    return False
def offline(ctx, v): OFF['v']=v; ctx.set_offline(v)
SIZE_JS="""async()=>{let n=0,b=0;const keys=await caches.keys();for(const k of keys){const c=await caches.open(k);for(const r of await c.keys()){const x=await c.match(r);b+=(await x.blob()).size;n++}}
 const e=await navigator.storage.estimate();return {keys,n,mb:+(b/1048576).toFixed(2),usageMb:+(e.usage/1048576).toFixed(2)}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    ctx.route('**/*',handle2)
    pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e))
    # 1) Primera visita con internet: precache
    pg.goto(URL)
    pg.wait_for_function("navigator.serviceWorker.controller && Engine.ready",timeout=90000)
    wait_caches(pg, "k.length>0")
    need=['engine/stockfish-19-lite-single.wasm','fonts/PressStart2P-latin.woff2','logo-claro.svg','favicon.ico','apple-touch-icon-180.png','chess.min.js','stockfish-19-lite-single.wasm','stockfish-19-lite-single.js','10.0.2/stockfish.wasm','10.0.2/stockfish.js','10.0.2/stockfish.wasm.js']
    urls=pg.evaluate("async()=>{const c=await caches.open((await caches.keys())[0]);return (await c.keys()).map(r=>r.url)}")
    miss=[n for n in need if not any(u.endswith(n) for u in urls)]+([] if URL in urls else ['./ (shell)'])
    check('precache completo', not miss, '%d archivos%s'%(len(urls), (' faltan '+str(miss)) if miss else ''))
    sz=pg.evaluate(SIZE_JS); print('   caché:',sz)
    # Datos de Partidas con red (luego se usan sin red)
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load')
    pg.wait_for_function("S.games.length===3",timeout=15000)
    pg.evaluate("S.settings.claude={on:true,key:'sk-prueba',model:'claude-haiku-5-5'}; save()")
    check('IA lista con red', pg.evaluate("ClaudeAI.ready()"))
    # 2) Modo avión: recargar sin red
    offline(ctx, True)
    pg.reload(); pg.wait_for_function("typeof Chess!=='undefined' && Engine.ready",timeout=60000)
    check('abre sin red con chess.js y motor', True, pg.evaluate("Engine.flavor"))
    check('motor sin red es Stockfish 19 lite', pg.evaluate("Engine.flavor")=='WASM 19 lite')
    check('navigator.onLine es false', pg.evaluate("navigator.onLine")==False)
    check('IA apagada sin red', pg.evaluate("ClaudeAI.ready()")==False)
    # Escalera: jugar contra el motor
    pg.click('.tab[data-tab=ladder]'); pg.click('#go'); time.sleep(.5)
    pg.evaluate("App.session.onUserMove({from:'e2',to:'e4'})")
    pg.wait_for_function("App.game.history().length>=2",timeout=20000)
    check('Escalera: el motor responde sin red', True, pg.evaluate("App.game.history().join(' ')"))
    pg.screenshot(path=OUT+'offline_escalera_390.png')
    # Partidas + análisis sin red
    pg.click('.tab[data-tab=games]'); time.sleep(.5)
    check('Partidas guardadas visibles sin red', pg.evaluate("S.games.length")==3 and pg.locator('.game[data-id]').count()>=3)
    pg.select_option('#bmt','250'); pg.click('#bgo')
    pg.wait_for_function("Object.keys(S.analyses).length===3 && !Analyzer.running",timeout=180000)
    check('análisis de partidas sin red', True, '%d analizadas'%pg.evaluate("Object.keys(S.analyses).length"))
    r=pg.evaluate("Engine.run('r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 2 4',{depth:10,tag:'t'}).then(r=>r.best)")
    check('análisis de posición sin red (mate Qxf7)', r=='h5f7', r)
    pg.screenshot(path=OUT+'offline_partidas_390.png')
    # Stockfish 10 de respaldo sin red
    pg.goto(URL+'?sf=10'); pg.wait_for_function("Engine.ready",timeout=60000)
    check('respaldo Stockfish 10 sin red', pg.evaluate("Engine.flavor")=='WASM', pg.evaluate("Engine.flavor"))
    # 3) Vuelve la red: la IA regresa sola
    pg.goto(URL); pg.wait_for_function("Engine.ready",timeout=60000)
    offline(ctx, False); pg.wait_for_function("navigator.onLine===true",timeout=5000)
    check('IA vuelve sola al reconectar', pg.evaluate("ClaudeAI.ready()"))
    offline(ctx, True); pg.wait_for_function("navigator.onLine===false",timeout=5000)
    check('IA se apaga sola al perder la red (sin recargar)', pg.evaluate("ClaudeAI.ready()")==False)
    offline(ctx, False)
    # 4) Versión nueva reemplaza a la vieja
    old=pg.evaluate("caches.keys()")
    sw=open(os.path.join(SITE,'sw.js')).read(); sw=re.sub(r"const VERSION = '[^']+'","const VERSION = 'prueba-nueva'",sw); open(os.path.join(SITE,'sw.js'),'w').write(sw)
    ih=open(os.path.join(SITE,'index.html')).read().replace('</body>','<meta name="casilla-prueba" content="v2"></body>',1); open(os.path.join(SITE,'index.html'),'w').write(ih)
    pg.evaluate("Offline.reg.update()")
    pg.wait_for_selector('#upd', timeout=60000)  # aviso 3: ya no se activa sola
    check('versión nueva queda en espera', pg.evaluate("!!Offline.reg.waiting"))
    with pg.expect_navigation(timeout=30000): pg.click('#updGo')
    ok=wait_caches(pg, "k.length===1&&k[0]==='casilla-prueba-nueva'")
    check('caché nueva activa y viejas borradas', ok, '%s -> %s'%(old, pg.evaluate("caches.keys()")))
    pg.wait_for_load_state('load'); pg.wait_for_timeout(1500)  # deja terminar la recarga de controllerchange
    try: pg.reload()
    except Exception: pg.wait_for_load_state('load')
    pg.wait_for_function("Engine.ready",timeout=60000)
    check('index.html nuevo con red (red primero)', pg.evaluate("!!document.querySelector('meta[name=casilla-prueba]')"))
    offline(ctx, True); pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000)
    check('sin red se sirve la versión nueva', pg.evaluate("!!document.querySelector('meta[name=casilla-prueba]')"))
    sz2=pg.evaluate(SIZE_JS); print('   caché tras actualizar:',sz2)
    b.close()
srv.shutdown()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
