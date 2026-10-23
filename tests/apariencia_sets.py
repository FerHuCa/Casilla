# Tablero y piezas por separado.
# A (file://): cada set nuevo carga sus 12 SVG desde piece/; solo se piden los del set activo (y las miniaturas
#   al abrir Apariencia); personalizar marca «Personalizado» y «Volver a [estilo]» lo quita; cambiar de estilo descarta.
# B (http con service worker): piece/ y board/ se guardan en la caché versionada al usarse, funcionan sin red,
#   un set no guardado cae al del estilo sin tocar lo guardado, y al actualizar la versión se conservan.
import os
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'run.py')).read().split("logs=[]")[0])
import time, shutil, tempfile, threading, functools, http.server, re
F=0
def ck(ok,msg,extra=''):
    global F; F+=not ok; print('OK   ' if ok else 'FALLA ', msg, extra)
SETS=['spatial','fantasy','shapes','firi','pirouetti','letter']
NAMES=['wK','wQ','wR','wB','wN','wP','bK','bQ','bR','bB','bN','bP']
LOADED="""s=>Promise.all(['wk','wq','wr','wb','wn','wp','bk','bq','br','bb','bn','bp'].map(c=>{
  const el=document.createElement('span'); el.className='pc p'+c; document.querySelector('#board').appendChild(el);
  const u=getComputedStyle(el).backgroundImage; el.remove(); const m=u.match(/url\\("?(.*?)"?\\)/);
  return new Promise(ok=>{ if(!m) return ok(null); const im=new Image(); im.onload=()=>ok([m[1],im.naturalWidth>0]); im.onerror=()=>ok([m[1],false]); im.src=m[1]; }); }))"""
def pieces_of(reqs): return sorted({re.search(r'/piece/([^/]+)/',u).group(1) for u in reqs if '/piece/' in u})
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- A ----------
    REQ=[]; ctx=b.new_context(viewport={'width':1280,'height':900}); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('request', lambda r: REQ.append(r.url)); pg.on('pageerror',lambda e: ck(False,'PAGEERROR',str(e)))
    pg.goto(APP); pg.wait_for_function("document.querySelectorAll('#board .pc').length===32",timeout=30000); time.sleep(.5)
    ck(not [u for u in REQ if '/piece/' in u or '/board/' in u], 'Clásico no pide nada de piece/ ni board/')
    for s in SETS:
        REQ.clear()
        pg.evaluate("s=>{S.settings.look={preset:'clasico',mode:'oscuro',pieces:s}; applyLook();}", s); time.sleep(.4)
        r=pg.evaluate(LOADED, s)
        ok=all(x and x[1] for x in r) and sorted(x[0].split('/piece/')[1] for x in r)==sorted(s+'/'+n+'.svg' for n in NAMES)
        ck(ok, '%s: 12 SVG cargados desde piece/%s/'%(s,s))
        files={u.split('/piece/')[1] for u in REQ if '/piece/' in u}
        ck(pieces_of(REQ)==[s] and files=={s+'/'+n+'.svg' for n in NAMES}, '%s: solo se piden sus 12 archivos'%s, pieces_of(REQ))
    for bid,f in [('arce','maple.jpg'),('veteado','wood4.jpg')]:
        REQ.clear(); pg.evaluate("id=>{S.settings.look={preset:'clasico',mode:'oscuro',board:id}; applyLook();}", bid); time.sleep(.4)
        bg=pg.evaluate("getComputedStyle(document.querySelector('#board')).backgroundImage")
        ck(f in bg and [u.split('/board/')[1] for u in REQ if '/board/' in u]==[f] and not pieces_of(REQ), '%s: solo se pide board/%s'%(bid,f))
    # Panel: miniaturas solo al abrir
    pg.evaluate("S.settings.look={preset:'clasico',mode:'oscuro'}; save(); applyLook()"); pg.reload()
    pg.wait_for_function("document.querySelectorAll('#board .pc').length===32"); REQ.clear(); time.sleep(.4)
    ck(not [u for u in REQ if '/piece/' in u or '/board/' in u], 'tras recargar con Clásico no se pide ningún set')
    pg.click('#lookBtn'); time.sleep(.8)
    ck(pieces_of(REQ)==sorted(SETS) and any('/board/' in u for u in REQ), 'al abrir Apariencia se cargan las miniaturas', pieces_of(REQ))
    ck(pg.locator('#look .lk-custom').count()==0 and pg.locator('#lookUndo').count()==0, 'sin personalizar no hay tarjeta ni «Volver a»')
    ck(pg.locator('.lk-opt[data-k=board]').count()==13 and pg.locator('.lk-opt[data-k=pieces]').count()==13, '13 tableros y 13 sets de piezas')
    subs=pg.evaluate("[...document.querySelectorAll('#look .lk-sub')].map(x=>x.textContent)")
    ck(subs==['Modo','Colores','Texturas','Retro','Clásicas','Modernas','Retro'], 'grupos del mock', subs)
    marks=pg.evaluate("[...document.querySelectorAll('.lk-opt')].filter(b=>b.querySelector('.d')).map(b=>b.dataset.k+':'+b.dataset.v+':'+b.querySelector('.d').textContent)")
    ck(marks==['board:piedra:Del estilo','pieces:cburnett:Del estilo'], 'marca «Del estilo» en las opciones del estilo', marks)
    pg.click('.lk-opt[data-k=board][data-v=nogal]'); pg.click('.lk-opt[data-k=pieces][data-v=spatial]')
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"clasico","mode":"oscuro","board":"nogal","pieces":"spatial"}', 'se guarda {preset, mode, board, pieces}')
    ck(pg.evaluate("[document.documentElement.dataset.board,document.documentElement.dataset.pieces]")==['nogal','spatial'], 'se aplica al tablero')
    ck(pg.inner_text('.preset[aria-checked=true] .tag')=='Personalizado', 'el estilo queda marcado «Personalizado»')
    ck(pg.inner_text('.lk-custom b')=='Clásico, personalizado' and 'Tablero Nogal y piezas Spatial.' in pg.inner_text('.lk-custom'), 'resumen de la personalización', pg.inner_text('.lk-custom'))
    ck(pg.inner_text('#lookUndo')=='Volver a Clásico' and pg.inner_text('#lookReset')=='Volver a Clásico', 'botones «Volver a Clásico»')
    pg.click('[data-m=claro]'); ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"clasico","mode":"claro","board":"nogal","pieces":"spatial"}', 'cambiar el modo conserva la personalización')
    pg.click('#lookUndo')
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"clasico","mode":"claro"}' and pg.evaluate("[document.documentElement.dataset.board,document.documentElement.dataset.pieces]")==['piedra','cburnett'], '«Volver a Clásico» restaura el estilo y conserva el modo')
    ck(pg.locator('#lookUndo').count()==0 and pg.locator('.preset .tag').count()==0, 'desaparecen la tarjeta y la marca')
    # en otro estilo
    pg.click('.preset[data-p=cuero]'); pg.click('.lk-opt[data-k=pieces][data-v=firi]')
    ck(pg.inner_text('.lk-custom b')=='Cuero, personalizado' and 'Piezas Firi.' in pg.inner_text('.lk-custom') and pg.inner_text('#lookUndo')=='Volver a Cuero', 'solo piezas: «Piezas Firi.» y «Volver a Cuero»', pg.inner_text('.lk-custom'))
    pg.click('.lk-opt[data-k=pieces][data-v=celtic]')
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"cuero","mode":"claro"}', 'elegir la opción del estilo quita la personalización')
    pg.click('.lk-opt[data-k=board][data-v=veteado]'); pg.click('.lk-opt[data-k=pieces][data-v=letter]')
    pg.click('.preset[data-p=pizarra]')
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"pizarra","mode":"claro"}' and pg.evaluate("[document.documentElement.dataset.board,document.documentElement.dataset.pieces]")==['glaciar','mpchess'], 'cambiar de estilo descarta la personalización')
    pg.click('.lk-opt[data-k=board][data-v=contraste]'); pg.click('#lookReset')
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"clasico","mode":"claro"}', '«Volver a Clásico» de abajo también descarta')
    # teclado en las opciones
    pg.focus('.lk-opt[data-k=board][aria-checked=true]'); pg.keyboard.press('ArrowRight')
    ck(pg.evaluate("[S.settings.look.board, document.activeElement.dataset.v]")==['madera','madera'], 'flecha derecha elige el tablero siguiente')
    pg.keyboard.press('End'); ck(pg.evaluate("S.settings.look.board")=='arcade', 'Fin va al último tablero')
    pg.evaluate("S.settings.look={preset:'clasico',mode:'oscuro',board:'arce',pieces:'shapes'}; save()"); pg.reload()
    pg.wait_for_function("document.querySelectorAll('#board .pc').length===32")
    ck(pg.evaluate("[document.documentElement.dataset.board,document.documentElement.dataset.pieces]")==['arce','shapes'], 'la personalización se conserva al recargar')
    ctx.close()
    # ---------- B ----------
    ROOT=_HERE.parent; SITE=tempfile.mkdtemp(prefix='casilla-sets-')
    for n in os.listdir(ROOT):
        if n in ('tests','.git','docs'): continue
        s_=ROOT/n; (shutil.copytree if s_.is_dir() else shutil.copy)(s_, os.path.join(SITE,n))
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a): pass
        def end_headers(self): self.send_header('Cache-Control','no-cache'); super().end_headers()
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(H, directory=SITE))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    URL='http://127.0.0.1:%d/'%srv.server_address[1]; OFF={'v':False}
    def handle2(route):
        if OFF['v']: return route.abort('internetdisconnected')
        if route.request.url.startswith(URL): return route.continue_()
        return handle(route)
    def offline(c,v): OFF['v']=v; c.set_offline(v)
    CK="async()=>{const out=[];for(const k of await caches.keys()){const c=await caches.open(k);for(const r of await c.keys()) if(/\\/(piece|board)\\//.test(r.url)) out.push(k+' '+r.url.match(/(piece|board)\\/.*/)[0])}return out.sort()}"
    ctx=b.new_context(viewport={'width':390,'height':844}); ctx.route('**/*',handle2); pg=ctx.new_page()
    pg.on('pageerror',lambda e: ck(False,'PAGEERROR',str(e)))
    pg.goto(URL); pg.wait_for_function("navigator.serviceWorker.controller && Engine.ready",timeout=90000)
    for _ in range(240):
        if pg.evaluate("caches.keys().then(k=>k.length===1)"): break
        time.sleep(.25)
    ver=pg.evaluate("caches.keys().then(k=>k[0])")
    ck(pg.evaluate(CK)==[], 'precache sin piece/ ni board/ (el set y el tablero por defecto van embebidos)', ver)
    pg.evaluate("S.settings.look={preset:'clasico',mode:'oscuro',board:'arce',pieces:'spatial'}; save(); applyLook()")
    pg.evaluate(LOADED, 'spatial'); time.sleep(1)
    got=pg.evaluate(CK)
    ck(sorted(got)==sorted([ver+' piece/spatial/'+n+'.svg' for n in NAMES]+[ver+' board/maple.jpg']), 'al usarlos se guardan en la caché versionada (12 SVG + maple.jpg)', '%d archivos'%len(got))
    offline(ctx,True); pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000); time.sleep(1)
    r=pg.evaluate(LOADED,'spatial')
    ck(all(x and x[1] and '/piece/spatial/' in x[0] for x in r) and pg.evaluate("[document.documentElement.dataset.board,document.documentElement.dataset.pieces]")==['arce','spatial'], 'sin red: Spatial y Arce siguen desde la caché')
    pg.evaluate("S.settings.look={preset:'cuero',mode:'oscuro',board:'veteado',pieces:'pirouetti'}; save(); applyLook()")
    pg.wait_for_function("document.documentElement.dataset.pieces==='celtic' && document.documentElement.dataset.board==='nogal'",timeout=10000)
    ck(pg.evaluate("JSON.stringify(S.settings.look)")=='{"preset":"cuero","mode":"oscuro","board":"veteado","pieces":"pirouetti"}', 'sin red y sin caché: se ve el tablero y las piezas del estilo, sin perder la elección')
    offline(ctx,False)
    pg.evaluate("S.settings.look={preset:'clasico',mode:'oscuro',board:'arce',pieces:'spatial'}; save(); applyLook()")
    # versión nueva: lo usado pasa a la caché nueva
    sw=open(os.path.join(SITE,'sw.js')).read(); open(os.path.join(SITE,'sw.js'),'w').write(re.sub(r"const VERSION = '[^']+'","const VERSION = 'prueba-sets'",sw))
    pg.evaluate("Offline.reg.update()"); pg.wait_for_function("!!Offline.reg.waiting",timeout=60000)
    pg.evaluate("Offline.reg.waiting.postMessage({type:'SKIP_WAITING'})")
    for _ in range(240):
        try:
            if pg.evaluate("caches.keys().then(k=>k.length===1&&k[0]==='casilla-prueba-sets')"): break
        except Exception: pass
        time.sleep(.25)
    time.sleep(1.5)
    got=pg.evaluate(CK)
    ck(sorted(got)==sorted(['casilla-prueba-sets piece/spatial/'+n+'.svg' for n in NAMES]+['casilla-prueba-sets board/maple.jpg']), 'al actualizar, piece/ y board/ pasan a la caché nueva y se borra la vieja', '%d archivos'%len(got))
    offline(ctx,True); pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000); time.sleep(.8)
    r=pg.evaluate(LOADED,'spatial')
    ck(all(x and x[1] for x in r) and pg.evaluate("document.documentElement.dataset.pieces")=='spatial', 'sin red tras actualizar: el set activo sigue')
    b.close(); srv.shutdown()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
