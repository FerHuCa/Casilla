# Avisos sin conexión (mockups 1, 2a, 2b, 3, 5a, 5b), Táctica de la etapa sin red, versión en el pie y
# actualización con Actualizar / Ahora no. Sirve el sitio por http con la red simulada (arnés de offline.py).
# Capturas a 1280 y 390 en CASILLA_SHOTS (por defecto tests/out/offline-ui/).
import os
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')
_src=open(os.path.join(os.path.dirname(__file__) or '.','offline.py')).read().split('with sync_playwright() as p:')[0]
exec(_src)
SHOTS=os.environ.get('CASILLA_SHOTS', OUT+'offline-ui')+'/'; os.makedirs(SHOTS, exist_ok=True)
SW0=open(os.path.join(SITE,'sw.js')).read(); VER=re.search(r"const VERSION = '([^']+)'",SW0).group(1)
def setver(v):
    open(os.path.join(SITE,'sw.js'),'w').write(re.sub(r"const VERSION = '[^']+'","const VERSION = '%s'"%v,SW0))
def ready(pg): pg.wait_for_function("navigator.serviceWorker.controller && Engine.ready && document.querySelector('#ver').textContent.startsWith('v')",timeout=90000)
def shot(pg, name, w):
    pg.set_viewport_size({'width':w,'height':800 if w>500 else 844}); time.sleep(.4)
    pg.screenshot(path=SHOTS+'%s-%d.png'%(name,w))
def handle3(route):
    u=route.request.url  # la memoria de puzzles se prueba en puzzle_store.py; aquí queda vacía
    if not OFF['v'] and ('/api/puzzle/batch/' in u or 'pub/puzzle/random' in u): return route.fulfill(status=503,headers={"Access-Control-Allow-Origin":"*"},body='')
    return handle2(route)
AI="S.settings.claude={on:true,key:'sk-prueba',model:'claude-haiku-5-5'}; save()"
with sync_playwright() as p:
    b=p.chromium.launch()
    # Sin service worker (file://): el pie lo dice honestamente
    pg0=b.new_page(); pg0.route('**/*',handle); pg0.goto(APP); pg0.wait_for_function("document.querySelector('#ver').textContent.length>0",timeout=20000)
    check('pie sin SW', pg0.inner_text('#ver')=='Sin modo sin conexión.', pg0.inner_text('#ver')); pg0.close()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    ctx.route('**/*',handle3)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(URL); ready(pg)
    check('pie lee VERSION del SW activo', pg.inner_text('#ver')=='v'+VER, pg.inner_text('#ver'))
    check('pie usa GET_VERSION (no texto fijo)', pg.evaluate("Offline.readVer().then(()=>document.querySelector('#ver').textContent)")=='v'+VER)
    check('con red: sin barra ni píldora apagada', not pg.locator('#offBar').count() and 'off' not in pg.get_attribute('#pill','class'))
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=15000)
    pg.evaluate(AI)
    for w in (1280,390):
        pg.evaluate("switchTab('ladder')"); pg.evaluate("document.querySelector('footer').scrollIntoView()"); shot(pg,'pie',w)
    pg.evaluate("window.scrollTo(0,0)")
    # 1) Sin conexión: píldora y barra
    offline(ctx, True); pg.wait_for_function("!Net.on",timeout=5000)
    check('aviso 1: barra', pg.inner_text('#offBar').startswith('Sin conexión. Siguen funcionando el motor, el análisis, la Escalera y Partidas.'), pg.inner_text('#offBar'))
    check('píldora «Sin conexión»', pg.inner_text('#pillText')=='Sin conexión' and 'off' in pg.get_attribute('#pill','class'))
    for w in (1280,390): pg.evaluate("switchTab('ladder')"); shot(pg,'1-sin-conexion',w)
    # 2a) Maestro con IA configurada + Táctica de la etapa desactivada
    pg.click('.tab[data-tab=coach]'); time.sleep(.3)
    check('aviso 2a en Maestro', 'Comentarios de IA en pausa.' in pg.inner_text('#side .off-note'))
    tb=pg.locator('[data-step=pz]')
    check('Táctica de la etapa desactivada', tb.count()==1 and tb.is_disabled() and tb.get_attribute('title')=='Necesita conexión')
    check('nota de Táctica sin red', 'la Táctica de la etapa usa puzzles de Lichess' in pg.inner_text('#side'))
    for w in (1280,390): pg.evaluate("switchTab('coach')"); shot(pg,'2a-ia-pausa-maestro',w)
    for w in (1280,390):
        pg.evaluate("switchTab('coach')"); pg.evaluate("document.querySelector('[data-step=pz]').scrollIntoView({block:'center'})"); shot(pg,'tactica-sin-red',w)
    # 2b) Partida contra el maestro: tip sin comentario de IA
    pg.evaluate("window.scrollTo(0,0)"); pg.evaluate("switchTab('coach')"); pg.click('#cgo'); time.sleep(1.5)
    pg.wait_for_function("!document.querySelector('#tip').hidden",timeout=20000)
    check('aviso 2b en el tip', pg.inner_text('#tip')=='Sin comentario de IA: no hay conexión. La evaluación es del motor, en tu dispositivo.', pg.inner_text('#tip'))
    for w in (1280,390): pg.evaluate("document.querySelector('#tip').scrollIntoView({block:'center'})"); shot(pg,'2b-ia-pausa-evaluacion',w)
    # 5a) Puzzles
    pg.evaluate("App.puzzleSource='lichess'"); pg.evaluate("switchTab('puzzles')"); time.sleep(.6)
    dis=pg.evaluate("[...document.querySelectorAll('[data-seg=src] button')].filter(b=>b.disabled).map(b=>b.dataset.v)")
    check('5a: Combinado, Lichess y Chess.com desactivados', dis==['mix','lichess','chesscom'], str(dis))
    check('5a: nota y estado', 'Lichess y Chess.com no están disponibles' in pg.inner_text('#side') and pg.inner_text('#status')=='Sin conexión. Prueba con Repaso o Mis errores.')
    for w in (1280,390): pg.evaluate("window.scrollTo(0,0)"); shot(pg,'5a-puzzles-sin-red',w)
    # Táctica de la etapa abierta directo sin red no intenta Lichess
    pg.evaluate("App.setSession(new PuzzleSession(null,{plan:{kind:'pz',stage:0}}))"); time.sleep(.4)
    check('Táctica sin red no pide Lichess', pg.inner_text('#status')=='Sin conexión. Prueba con Repaso o Mis errores.')
    # 5b) Partidas
    pg.evaluate("switchTab('games')"); time.sleep(.3)
    check('5b: botón desactivado y nota', pg.locator('#load').is_disabled() and 'necesita conexión' in pg.inner_text('#side'))
    for w in (1280,390): pg.evaluate("switchTab('games')"); shot(pg,'5b-partidas-sin-red',w)
    # Cerrar la barra y vuelta de la red
    pg.click('#offBar .x'); check('Cerrar quita la barra', pg.locator('#offBar').count()==0)
    offline(ctx, False); pg.wait_for_function("Net.on",timeout=5000)
    check('con red vuelve todo', not pg.locator('#load').is_disabled() and 'off' not in pg.get_attribute('#pill','class') and pg.locator('#offBar').count()==0)
    # Todos los presets de Apariencia con la barra (escritorio)
    offline(ctx, True); pg.wait_for_function("!Net.on",timeout=5000)
    for pr in ['clasico','madera','pizarra','cuero','club','relieve','bits','arcade']:
        pg.evaluate("S.settings.look={preset:'%s',mode:'oscuro'};applyLook();switchTab('games')"%pr); time.sleep(.3)
        shot(pg,'temas/1-5b-%s'%pr,1280)
    pg.evaluate("S.settings.look={preset:'clasico',mode:'oscuro'};applyLook()")
    offline(ctx, False); pg.wait_for_function("Net.on",timeout=5000)
    # 3) Versión nueva: queda en espera y aparece el aviso; Actualizar la activa y recarga
    setver('prueba-a'); pg.evaluate("switchTab('ladder')"); pg.evaluate("Offline.reg.update()")
    pg.wait_for_selector('#upd',timeout=60000); time.sleep(1)
    check('3: SW nuevo en waiting, el viejo sigue', pg.evaluate("!!Offline.reg.waiting") and pg.inner_text('#ver')=='v'+VER)
    check('3: texto del aviso', pg.inner_text('#upd').replace('\n',' ').startswith('Hay una versión nueva.'))
    for w in (1280,390): shot(pg,'3-nueva-version',w)
    with pg.expect_navigation(timeout=30000): pg.click('#updGo')
    ready(pg); check('Actualizar: recarga con la versión nueva', pg.inner_text('#ver')=='vprueba-a', pg.inner_text('#ver'))
    check('Actualizar: cachés viejas borradas', wait_caches(pg,"k.length===1&&k[0]==='casilla-prueba-a'"))
    # Ahora no: se aplica en la siguiente apertura
    setver('prueba-b'); pg.evaluate("Offline.reg.update()"); pg.wait_for_selector('#upd',timeout=60000)
    pg.click('#updLater'); check('Ahora no: cierra el aviso y deja la marca', pg.locator('#upd').count()==0 and pg.evaluate("localStorage.getItem('casilla.updLater')")=='1')
    check('Ahora no: sigue la vieja en esta sesión', pg.inner_text('#ver')=='vprueba-a')
    other=ctx.new_page(); other.goto(URL)  # siguiente apertura (con la pestaña vieja aún abierta)
    pg.wait_for_function("document.querySelector('#ver').textContent==='vprueba-b'",timeout=60000)
    check('siguiente apertura: activa la nueva sin aviso', pg.locator('#upd').count()==0 and not pg.evaluate("localStorage.getItem('casilla.updLater')"))
    other.wait_for_function("document.querySelector('#ver').textContent==='vprueba-b'",timeout=60000)
    check('la otra pestaña también pasa a la nueva', True); other.close()
    # Sin marca pero sin pestañas: el navegador la activa al cerrar todas
    setver('prueba-c'); pg.evaluate("Offline.reg.update()"); pg.wait_for_selector('#upd',timeout=60000)
    pg.close(); time.sleep(1); pg=ctx.new_page(); pg.goto(URL)
    pg.wait_for_function("document.querySelector('#ver').textContent==='vprueba-c'",timeout=60000)
    check('sin pestañas abiertas: se activa sola', True, pg.inner_text('#ver'))
    # Sin red tras actualizar: sigue abriendo
    offline(ctx, True); pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000)
    check('sin red tras actualizar abre y muestra versión', pg.inner_text('#ver')=='vprueba-c')
    b.close()
srv.shutdown()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
