exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
# Evidencia (Progreso): prueba de 4 semanas calculada solo con S, sin red ni costo.
# Cubre datos viejos sin S.evid, empezar, cálculo semanal exacto con datos sembrados, avisos de muestra chica,
# errores que se repiten, exportar sin datos sensibles, marca de partida seria, conteo de puzzles,
# sincronización, recorte de días, reiniciar y el layout a 390 y 1280 sin desborde.
NET=[]
def handle_ev(route):
    u=route.request.url
    if not u.startswith('file://'): NET.append(u)
    return handle2(route)
fails=[]
def check(name, cond):
    print(('OK   ' if cond else 'FALLA ') + name)
    if not cond: fails.append(name)
AUDIT="(()=>document.documentElement.scrollWidth-innerWidth)()"

# Semilla: la prueba empezó hace 15 días (día 16: semanas 1 y 2 terminadas, la 3 en curso, la 4 pendiente)
SEED = """(() => {
  const st = dkAdd(dayKey(), -15), ms = n => dkDate(dkAdd(st, n)).getTime(), sec = n => Math.floor(ms(n) / 1000);
  S.evid = {start:st, startAt:1, days:{}};
  S.evid.days[dkAdd(st, 0)] = {o:1, pn:10, pk:6, mn:8, mk:4};
  S.evid.days[dkAdd(st, 2)] = {o:1, pn:4, pk:2, mn:2, mk:2};
  S.evid.days[dkAdd(st, 8)] = {o:1, pn:5, pk:5, mn:12, mk:9};
  S.plan = {len:'corta', stage:'auto', days:{}};
  S.plan.days[dkAdd(st, 0)] = {rev:3, pz:6, eg:true, game:null, rv:false, ok:true};
  S.plan.days[dkAdd(st, 1)] = {rev:3, pz:6, eg:true, game:null, rv:false, ok:true};
  S.plan.days[dkAdd(st, 8)] = {rev:1, pz:0, eg:false, game:null, rv:false, ok:false};
  const C = coachState();
  C.games = [
    {t:ms(9), vs:true, res:'w', acc:80, errors:1, ser:true},
    {t:ms(5), vs:true, res:'l', acc:50, errors:7},
    {t:ms(4), vs:true, res:'l', acc:40, errors:9, ser:false},
    {t:ms(3), vs:true, res:'d', acc:70, errors:2, ser:true},
    {t:ms(1), vs:true, res:'l', acc:60, errors:4, ser:true}];
  const mk = (gid, n, cats) => cats.map((c, i) => ({id:gid + '#' + i, gid, ply:i + 2, fen:'8/8/8/8/8/8/8/8 w - - 0 1', played:'e4', best:'e2e4', bestSan:'e4', drop:30, before:0, cat:c, phase:'Medio juego', date:sec(n), opp:'rivalsecreto', color:'w'}));
  S.played = [{id:'g1', src:'casilla', kind:'maestro', title:'', opp:'rivalsecreto', user:'w', start:START_FEN, sans:['e4'], res:'l', why:'', end:sec(1)},
              {id:'g3', src:'casilla', kind:'partida', title:'', opp:'rivalsecreto', user:'w', start:START_FEN, sans:['e4'], res:'l', why:'', end:sec(8)}];
  S.games = [{id:'https://www.chess.com/game/live/77', pgn:'1. e4 e5', white:'fertest', black:'rivalsecreto', end:sec(2)}];
  S.analyses = {
    g1:{v:1, src:'partida', acc:50, w:[], tags:{}, cnt:{}, mistakes:mk('g1', 1, ['Pieza colgada', 'Pieza colgada', 'Mate no visto'])},
    'https://www.chess.com/game/live/77':{v:1, src:'chesscom', acc:60, w:[], tags:{}, cnt:{}, mistakes:mk('cc', 2, ['Táctica no vista'])},
    ['coach:' + ms(3)]:{v:1, src:'coach', acc:70, w:[], tags:{}, cnt:{}, mistakes:[]},
    g3:{v:1, src:'partida', acc:55, w:[], tags:{}, cnt:{}, mistakes:mk('g3', 8, ['Pieza colgada'])},
    old:{v:1, src:'partida', acc:55, w:[], tags:{}, cnt:{}, mistakes:mk('old', -3, ['Pieza colgada'])}};
  save(); return st;
})()"""

with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':900}, accept_downloads=True); ctx.route('**/*',handle_ev); pg=ctx.new_page()
    pg.on('pageerror',lambda e: (print('PAGEERROR',e), fails.append('pageerror')))
    pg.on('dialog', lambda d: d.accept())
    # 0) Datos de una versión anterior, sin S.evid
    pg.goto(APP); pg.evaluate("localStorage.setItem('casilla.v1', JSON.stringify({username:'', ladder:{unlocked:1, rec:{}}, puzzles:{rating:1200, hist:[], solved:0, failed:0, streak:0, best:0, seen:{}}, games:[], played:[], analyses:{}, endgames:{}, openings:{}, settings:{movetime:400}}))")
    pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000)
    check('datos viejos abren con S.evid por defecto', pg.evaluate("!!(S.evid && S.evid.days && S.evid.start === null)"))
    check('abrir la app marca el día', pg.evaluate("S.evid.days[dayKey()] && S.evid.days[dayKey()].o === 1"))
    # 1) Sin empezar, y nada sale a la red al abrir Progreso
    NET.clear()
    pg.click('.tab[data-tab=progress]'); time.sleep(.3)
    txt = pg.inner_text('#side')
    check('Evidencia sin empezar', 'Evidencia' in txt and pg.is_visible('#evStart'))
    check('Evidencia queda antes de Sincronizar', txt.index('Evidencia') < txt.index('Sincronizar entre dispositivos'))
    pg.click('#evStart'); time.sleep(.3)
    check('empezar fija el inicio hoy', pg.evaluate("S.evid.start === dayKey() && S.evid.startAt > 0"))
    txt = pg.inner_text('#evid')
    check('día 1 de 28', 'día 1 de 28' in txt)
    check('semana 4 pendiente con fecha', 'Pendiente' in txt and 'desde el' in txt)
    check('sin avisos en la semana en curso', 'aún no es confiable' not in txt)
    check('Evidencia no usa la red', NET == [])
    # 2) Cálculo exacto con datos sembrados
    st = pg.evaluate(SEED)
    s = pg.evaluate("evidStats()")
    W = s['W']
    print('semanas', [(w['w'], w['state'], w['mn'], w['mk'], w['sg'], w['se'], w['op'], w['ok'], w['ag'], w['hung'], w['tac'], w['mate']) for w in W])
    check('día 16 y estados de las semanas', s['day'] == 16 and [w['state'] for w in W] == ['done', 'done', 'cur', 'pend'])
    check('puzzles por semana', (W[0]['pn'], W[0]['pk'], W[0]['mn'], W[0]['mk']) == (14, 8, 10, 6) and (W[1]['mn'], W[1]['mk']) == (12, 9))
    check('solo cuentan las partidas serias', (W[0]['sg'], W[0]['se']) == (2, 6) and (W[1]['sg'], W[1]['se']) == (1, 1))
    check('Ruta: días abiertos y completos', (W[0]['op'], W[0]['ok']) == (3, 2) and (W[1]['op'], W[1]['ok']) == (1, 0))
    check('errores por tipo y partidas analizadas', (W[0]['ag'], W[0]['hung'], W[0]['tac'], W[0]['mate']) == (3, 2, 1, 1) and (W[1]['ag'], W[1]['hung']) == (1, 1))
    check('lo anterior al inicio no cuenta', sum(w['ag'] for w in W) == 4)
    pg.click('.tab[data-tab=ladder]'); pg.click('.tab[data-tab=progress]'); time.sleep(.3)
    txt = pg.inner_text('#evid')
    check('porcentajes en pantalla', '60%' in txt and '75%' in txt)
    check('errores por partida seria en pantalla', '3.0' in txt and '1.0' in txt)
    check('Ruta en pantalla', '2 de 3' in txt and '0 de 1' in txt)
    check('aviso de pocas partidas serias', 'Semana 1: solo 2 partidas serias' in txt and 'Semana 2: solo 1 partida seria' in txt)
    check('sin aviso de puzzles con 10 o más', 'puzzles de Mis errores' not in txt)
    check('errores que se repiten: semana 1 contra la 2', 'Semana 1 contra la semana 2' in txt and '0.7 → 1.0' in txt and 'sube' in txt and 'baja' in txt)
    check('todos los puzzles por semana', 'semana 1 57%' in txt and 'semana 2 100%' in txt)
    check('objetivo de la etapa', ('tu etapa:' in txt) or ('sin objetivo en tu etapa' in txt))
    # 3) Exportar: solo números y fechas
    with pg.expect_download() as dl: pg.click('#evExp')
    path = dl.value.path(); raw = open(path).read(); data = json.loads(raw)
    check('archivo con nombre de evidencia', dl.value.suggested_filename.startswith('casilla-evidencia-'))
    check('4 semanas y 16 días', len(data['semanas']) == 4 and len(data['dias']) == 16 and data['inicio'] == st)
    check('semana 1 exportada', data['semanas'][0]['misErrores'] == {'total':10, 'primerIntento':6} and data['semanas'][0]['partidasSerias'] == {'partidas':2, 'errores':6})
    low = raw.lower()
    check('sin datos sensibles en el archivo', not any(w in low for w in ['fen', 'pgn', 'rivalsecreto', 'fertest', 'chess.com', 'sk-ant', 'token', '"e4"']))
    # 4) La partida seria queda marcada; la guiada no
    r = pg.evaluate("""(() => { const out = [];
      for(const serious of [true, false]){
        const c = Object.assign(Object.create(Coach.prototype), {moveEvals:[], vs:true, prof:{top:[]}, ses:{gid:'cx' + serious, oppName:'M', user:'w', o:{}}, deferred:[], say(){}, guide:false, quiz:false, qa:{}});
        try{ c._finish({res:'w', serious}); }catch(e){ return 'error: ' + e.message; }
        out.push(coachState().games[0].ser);
      } return out; })()""")
    check('marca ser en partidas contra el maestro', r == [True, False])
    # 5) Cada puzzle suma al día
    before = pg.evaluate("Object.assign({}, S.evid.days[dayKey()])")
    pg.evaluate("PuzzleSession.prototype.score.call({p:{src:'mine', rating:1200, id:'me:x'}, opt:{}}, true)")
    pg.evaluate("PuzzleSession.prototype.score.call({p:{src:'lichess', rating:1200, id:'li:x'}, opt:{}}, false)")
    after = pg.evaluate("S.evid.days[dayKey()]")
    check('puzzle de Mis errores y de Lichess cuentan', (after['pn'] - before.get('pn', 0), after['pk'] - before.get('pk', 0), after['mn'] - before.get('mn', 0), after['mk'] - before.get('mk', 0)) == (2, 1, 1, 1))
    # 6) Sincronización: manda la prueba más reciente y por día el conteo mayor
    m = pg.evaluate("""(() => { const L = JSON.parse(JSON.stringify(S)), R = defaults();
      L.evid = {start:'2026-10-01', startAt:5, days:{'2026-10-01':{o:1, pn:3, pk:1, mn:0, mk:0}}};
      R.evid = {start:'2026-10-03', startAt:9, days:{'2026-10-01':{o:1, pn:5, pk:0, mn:2, mk:2}, '2026-10-02':{o:1, pn:1, pk:1, mn:0, mk:0}}};
      const o = mergeState(L, R); return [o.evid.start, o.evid.days['2026-10-01'], Object.keys(o.evid.days).length, mergeState(L, defaults()).evid.start]; })()""")
    check('sync: inicio más reciente', m[0] == '2026-10-03')
    check('sync: conteo mayor por día', m[1] == {'o':1, 'pn':5, 'pk':1, 'mn':2, 'mk':2} and m[2] == 2)
    check('sync con un dispositivo nuevo conserva la prueba', m[3] == '2026-10-01')
    # 7) Recorte: últimos 60 días, más los 28 de la prueba aunque sean viejos
    k = pg.evaluate("""(() => { const E = {start:dkAdd(dayKey(), -100), days:{}};
      for(let i = 0; i < 120; i++) E.days[dkAdd(dayKey(), -i)] = {o:1};
      evidPrune(E); const ks = Object.keys(E.days); return [ks.length, !!E.days[dkAdd(dayKey(), -100)], !!E.days[dkAdd(dayKey(), -73)], !!E.days[dkAdd(dayKey(), -72)], !!E.days[dkAdd(dayKey(), -101)]]; })()""")
    check('recorte conserva la prueba', k == [88, True, True, False, False])
    # 8) Respaldo viejo sin evid: abre con el valor por defecto
    check('respaldo viejo', pg.evaluate("(() => { const o = Object.assign(defaults(), {username:'x'}); return !!(o.evid && o.evid.days); })()"))
    # 9) Capturas y desborde a 1280 y 390
    pg.click('.tab[data-tab=ladder]'); pg.click('.tab[data-tab=progress]'); time.sleep(.3)
    pg.locator('#evid').screenshot(path=OUT+'ev_1280.png')
    pg.set_viewport_size({'width':390,'height':844}); time.sleep(.4)
    pg.click('.tab[data-tab=ladder]'); pg.click('.tab[data-tab=progress]'); time.sleep(.3)
    check('sin desborde a 390', pg.evaluate(AUDIT) <= 0)
    pg.locator('#evid').scroll_into_view_if_needed(); pg.screenshot(path=OUT+'ev_390.png', full_page=True)
    btn = pg.evaluate("(() => { const b = document.querySelector('#evExp').getBoundingClientRect(); return b.height; })()")
    check('botones con tamaño táctil', btn >= 40)
    # 10) Reiniciar: vuelve a sin empezar y no borra nada más
    n_an = pg.evaluate("Object.keys(S.analyses).length")
    pg.click('#evReset'); time.sleep(.3)
    check('reiniciar quita la prueba', pg.evaluate("S.evid.start === null") and pg.is_visible('#evStart'))
    check('reiniciar no borra el progreso', pg.evaluate("Object.keys(S.analyses).length") == n_an and pg.evaluate("Object.keys(S.evid.days).length") > 0)
    b.close()
print('\nFALLAS:', fails if fails else 'ninguna')
sys.exit(1 if fails else 0)
