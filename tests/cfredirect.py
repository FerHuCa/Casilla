# Reproduce el fallo de producción del PR #2 (casilla.io en Cloudflare): /index.html y *.html responden 307 a la ruta sin
# extensión, y jsDelivr da 403 a stockfish@19. Antes del arreglo el service worker no se instalaba y sin red salía
# «You're offline». Aquí se exige: instalación completa, nada precacheado con redirección y navegación sin red a /, /index.html y /?x.
import os
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')
src=open(os.path.join(os.path.dirname(__file__) or '.','offline.py')).read()
exec(src.split('with sync_playwright() as p:')[0].replace("    def end_headers(self):",
"""    def do_GET(self):
        p=self.path.split('?')[0]
        if p.endswith('.html'):
            self.send_response(307); self.send_header('Location', p[:-5].replace('/index','/') or '/'); self.end_headers(); return
        return super().do_GET()
    def end_headers(self):"""))
_h=handle
def handle(route):
    if 'cdn.jsdelivr.net/npm/stockfish@19' in route.request.url:
        return route.fulfill(status=403, body='Package size exceeded the configured limit of 150 MB.')
    return _h(route)
for f in ('sw.js','index.html'):
    check('sin jsDelivr para Stockfish 19 en '+f, 'cdn.jsdelivr.net/npm/stockfish' not in open(os.path.join(ROOT,f)).read())
import urllib.request
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a): return None
try: urllib.request.build_opener(NR).open(URL+'index.html'); code=200
except urllib.error.HTTPError as e: code=e.code
check('el servidor imita a Cloudflare (index.html → 307)', code==307)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    ctx.route('**/*',handle2)
    pg=ctx.new_page()
    pg.goto(URL)
    ok=True
    try: pg.wait_for_function("navigator.serviceWorker.controller && Engine.ready",timeout=90000)
    except Exception: ok=False
    check('service worker instalado y controlando', ok)
    wait_caches(pg, "k.length>0")
    ents=pg.evaluate("async()=>{const c=await caches.open((await caches.keys())[0]);const o=[];for(const r of await c.keys()){const m=await c.match(r);o.push([r.url,m.status,m.redirected])}return o}")
    check('ninguna entrada guardada con redirección', not [e for e in ents if e[2]], '%d entradas'%len(ents))
    check('Stockfish 19 en caché', any(e[0].endswith('engine/stockfish-19-lite-single.wasm') for e in ents))
    offline(ctx, True)
    for u in (URL, URL+'index.html', URL+'?source=pwa'):
        try:
            pg.goto(u); pg.wait_for_function("typeof Chess!=='undefined' && Engine.ready",timeout=60000); r=pg.evaluate("Engine.flavor")
        except Exception as e: r=None; print('   ',str(e).splitlines()[0])
        check('sin red abre '+u.replace(URL,'/'), r is not None, r or '')
    b.close()
print('FALLAS:',F); sys.exit(1 if F else 0)
