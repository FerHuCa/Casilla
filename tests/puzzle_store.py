# Memoria de puzzles sin conexión (IndexedDB): relleno en serie, límites, sustitución de resueltos,
# uso sin red y aviso 5a ajustado a lo guardado. Red de Lichess y Chess.com simulada.
import os, copy
os.environ.setdefault('PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS', '1')
_src=open(os.path.join(os.path.dirname(__file__) or '.','offline.py')).read().split('with sync_playwright() as p:')[0]
exec(_src)
SHOTS=os.environ.get('CASILLA_SHOTS', OUT+'offline-ui')+'/'; os.makedirs(SHOTS, exist_ok=True)
CALLS=[]; NID={'li':0,'cc':0}; MODE={'li429':0}
def batch(u):
    import urllib.parse as up
    q=up.parse_qs(up.urlparse(u).query); nb=int(q['nb'][0]); out=[]
    for _ in range(nb):
        NID['li']+=1; d=copy.deepcopy(LI); d['puzzle']['id']='t%04d'%NID['li']
        ang=u.split('/batch/')[1].split('?')[0]
        d['puzzle']['themes']=['middlegame',ang] if ang!='mix' else ['opening','mateIn4']; out.append(d)
    return {'puzzles':out}
def handle4(route):
    u=route.request.url; h={"Access-Control-Allow-Origin":"*"}
    if not OFF['v'] and '/api/puzzle/batch/' in u:
        CALLS.append(('li',time.time(),u))
        if MODE['li429']: MODE['li429']-=1; return route.fulfill(status=429,headers=h,body='')
        return route.fulfill(status=200,headers=h,content_type='application/json',body=json.dumps(batch(u)))
    if not OFF['v'] and 'pub/puzzle/random' in u:
        CALLS.append(('cc',time.time(),u)); NID['cc']+=1; d=dict(MOCK['/pub/puzzle/random']); d['publish_time']=NID['cc']
        return route.fulfill(status=200,headers=h,content_type='application/json',body=json.dumps(d))
    return handle2(route)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',handle4)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: print('PAGEERROR',e))
    MODE['li429']=1
    pg.goto(URL); pg.wait_for_function("navigator.serviceWorker.controller && PuzzleStore.db",timeout=90000)
    t0=time.time()
    while time.time()-t0<120 and not [c for c in CALLS if c[0]=='li']: time.sleep(.5)
    print('primer lote tras', round(time.time()-t0), 's', pg.evaluate('JSON.stringify({w:PuzzleStore.wait,r:PuzzleStore.running,on:Net.on,n:PuzzleStore.items.length})'))
    time.sleep(1); li1=[c for c in CALLS if c[0]=='li']
    w429=pg.evaluate("PuzzleStore.wait.lichess")/1000-li1[0][1]; li2=[c for c in li1[1:]]
    check('429 de Lichess: espera >= 60 s antes de reintentar Lichess', w429>=59 and (not li2 or li2[0][1]-li1[0][1]>=59), '%.0f s'%w429)
    pg.evaluate("PuzzleStore.wait.lichess=0; PuzzleStore.kick(0)")
    pg.wait_for_function("PuzzleStore.count('lichess')>=200",timeout=200000)
    li=[c for c in CALLS if c[0]=='li']; cc=[c for c in CALLS if c[0]=='cc']
    check('Lichess llega a 200 y no lo rebasa', pg.evaluate("PuzzleStore.count('lichess')")==200)
    check('Chess.com no se guarda (User Agreement)', not cc and pg.evaluate("PuzzleStore.count('chesscom')")==0)
    check('50 con temas de la etapa', pg.evaluate("PuzzleStore.count('lichess',PLAN[planStage()].themes)")>=50)
    check('lotes de Lichess de máx. 50', all('nb=' in c[2] and int(c[2].split('nb=')[1].split('&')[0])<=50 for c in li))
    gaps=[b2[1]-a[1] for a,b2 in zip(CALLS,CALLS[1:])]
    check('peticiones en serie, sin ráfagas (>= 19 s entre cada una)', min(gaps)>=19, '%.1f s'%min(gaps))
    check('persiste en IndexedDB', pg.evaluate("PuzzleStore.req(PuzzleStore.tx('readonly').count())")==200)
    mb=pg.evaluate("PuzzleStore.req(PuzzleStore.tx('readonly').getAll()).then(a=>+(new Blob([JSON.stringify(a)]).size/1048576).toFixed(3))")
    print('MB_IDB_200', mb)
    # Sin red
    offline(ctx, True); pg.wait_for_function("!Net.on",timeout=5000)
    pg.evaluate("App.puzzleSource='lichess'; switchTab('puzzles')"); time.sleep(.8)
    dis=pg.evaluate("[...document.querySelectorAll('[data-seg=src] button')].filter(b=>b.disabled).map(b=>b.dataset.v)")
    check('5a: con Lichess guardado solo se desactiva Chess.com', dis==['chesscom'], str(dis))
    check('5a: nota solo de Chess.com', 'Sin conexión: Chess.com no está disponible.' in pg.inner_text('#side') and 'Lichess y Chess.com' not in pg.inner_text('#side'))
    for w in (1280,390):
        pg.set_viewport_size({'width':w,'height':800 if w>500 else 844}); time.sleep(.4); pg.screenshot(path=SHOTS+'5a-con-guardados-%d.png'%w)
    pg.set_viewport_size({'width':1280,'height':800})
    pid=pg.evaluate("PuzzleSession && App.session.p && App.session.p.id")
    check('sin red Lichess usa un guardado', bool(pid) and pid.startswith('li:t'), str(pid))
    pg.evaluate("App.session.reveal()"); time.sleep(4)
    check('el resuelto se borra de la memoria', pg.evaluate("!PuzzleStore.items.some(x=>x.id===%r)"%pid) and pg.evaluate("PuzzleStore.req(PuzzleStore.tx('readonly').get(%r))"%pid) is None)
    pg.evaluate("App.puzzleSource='mix'; App.session.renderSide(); App.session.next()"); time.sleep(.6)
    check('sin red Combinado usa guardados de Lichess', pg.evaluate("App.session.p && App.session.p.src")=='lichess')
    # Táctica de la etapa con guardados de sus temas
    pg.evaluate("switchTab('coach')"); time.sleep(.4)
    tb=pg.locator('[data-step=pz]')
    if tb.count(): check('Táctica habilitada con guardados de la etapa', not tb.is_disabled())
    pg.evaluate("App.setSession(new PuzzleSession(null,{plan:{kind:'pz',stage:planStage()}}))"); time.sleep(.5)
    check('Táctica sin red usa guardado con tema de la etapa', pg.evaluate("!!App.session.p && App.session.p.themes.some(t=>PLAN[planStage()].themes.includes(t))"))
    # Vuelve la red: se repone lo resuelto
    n0=pg.evaluate("PuzzleStore.count('lichess')"); offline(ctx, False)
    pg.wait_for_function("Net.on",timeout=5000); pg.evaluate("PuzzleStore.wait={lichess:0}; PuzzleStore.kick(0)")
    pg.wait_for_function("PuzzleStore.count('lichess')>=200",timeout=60000)
    check('al volver la red se repone hasta 200', n0<200 and pg.evaluate("PuzzleStore.count('lichess')")==200)
    check('no vuelve a guardar el resuelto', pg.evaluate("!PuzzleStore.items.some(x=>x.id===%r)"%pid))
    b.close()
print('FALLAS', F); sys.exit(1 if F else 0)
