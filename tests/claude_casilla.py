# Comentario con IA de partidas jugadas en Casilla (mockups 4a y 4b de Sam). Solo API simulada (route.fulfill).
# Reutiliza el arnés de claude_partidas.py. Capturas escritorio/movil-4a y 4b en docs/capturas/claude-partidas/.
import pathlib as _pl
exec(open(str(_pl.Path(__file__).resolve().parent/'claude_partidas.py')).read().split("for W in [1280, 390]:")[0])
PID='play:maestro-777'
SEED="""((a) => {
  const [sans, pid] = a;
  const g = new Chess(), fens = [g.fen()]; sans.forEach(s => { g.move(s); fens.push(g.fen()); });
  // W desde las blancas: el usuario (negras) pierde terreno en las jugadas 10, 16 y 18
  const W = fens.map((f, i) => i <= 9 ? -150 : i <= 15 ? 150 : 450);
  const best = fens.map(() => null); best[9] = 'c6a5'; best[15] = 'c6e7'; best[17] = 'e5d4';
  const pv = fens.map((f, i) => best[i] ? [best[i]] : []);
  const M = (ply, b, bSan, cat, drop) => { const c = new Chess(fens[ply-1]); const mv = c.move(sans[ply-1]);
    return {id:pid + '#' + ply, gid:pid, ply, fen:fens[ply-1], played:mv.san, playedUci:mv.from + mv.to, best:b, bestSan:bSan, drop, before:-20, cat, phase:'Apertura', date:1792000000, opp:'Gran Maestro', color:'b'}; };
  S.played = [{id:pid, src:'casilla', kind:'maestro', title:'Contra el maestro', opp:'Gran Maestro', user:'b', start:START_FEN, sans, res:'l', why:'abandono', end:1792000000}];
  S.analyses[pid] = {v:1, src:'maestro', acc:62, w:W, tags:{9:'??', 15:'?', 17:'?'}, cnt:{inacc:0, mistake:2, blunder:1}, deep:true, mt:400, best, pv,
    mistakes:[M(10, 'c6a5', 'Na5', 'Pieza colgada', 35), M(16, 'c6e7', 'Ne7', 'Error posicional', 24), M(18, 'e5d4', 'exd4', 'Error posicional', 22)]};
  S.analyses[pid].mistakes[0].exp = %EXP%;
  S.settings.claude = {on:false, key:'sk-ant-prueba', model:'claude-haiku-5-5', gameModel:'claude-haiku-5-5'};
  save(); return true; })""".replace('%EXP%', json.dumps(EXP))
# == casos ==
for W in [1280, 390]:
    SENT.clear(); MODE['v']='ok'
    with sync_playwright() as p:
        b=p.chromium.launch(); mob = W == 390
        ctx=b.new_context(viewport={'width':W,'height':900 if not mob else 844}, device_scale_factor=1 if not mob else 2, is_mobile=mob, has_touch=mob)
        ctx.route('**/*',handle4); pg=ctx.new_page()
        pg.on('pageerror',lambda e: (print('PAGEERROR',e), fails.append('pageerror')))
        pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
        pg.evaluate(SEED, [SANS, PID]); tag=f'{W}'
        def shot(name):
            pg.add_style_tag(content='.side{max-height:none!important;overflow:visible!important;height:auto!important} main{height:auto!important;overflow:visible!important}')
            pg.screenshot(path=SHOTS+('escritorio' if W==1280 else 'movil')+'-'+name+'.png', full_page=True)
        def open_played():
            pg.evaluate("openPlayed(S.played[0])"); pg.wait_for_function("document.querySelector('#clbox') && document.querySelector('#clbox').innerText.length > 0",timeout=10000); time.sleep(.5)
        def box(): return pg.inner_text('#clbox')
        def wait_box(txt, t=8000): pg.wait_for_function(f"document.querySelector('#clbox') && document.querySelector('#clbox').innerText.includes({json.dumps(txt)})",timeout=t)
        open_played()
        c = box(); org = pg.evaluate("App.session.aiOrigin()")
        check(f'{tag} 4b: título y línea de origen', c.startswith('Comentario de la IA') and org.startswith('Jugada en Casilla · Contra el maestro · ') and org in c)
        check(f'{tag} 4b: sin apertura conocida, la línea no la inventa', org.count(' · ') == 2)
        check(f'{tag} 4b: comentario del maestro sin IA', 'Comentario del maestro (sin IA): ' in c)
        check(f'{tag} 4b: texto y botón', 'La IA puede escribir un comentario más completo a partir del análisis del motor. Usa tu clave; costo aproximado: menos de 1 centavo de dólar con Haiku 5.5.' in c and pg.locator('#clGo', has_text='Comentar partida con IA').count() == 1)
        GC=lambda: [x for x in SENT if 'Tarea: partida' in x[1]['messages'][0]['content']]
        check(f'{tag} 4b: sin comentario automático de la partida al abrir', len(GC()) == 0 and pg.locator('#narr').count() == 0 and pg.locator('#narrai').count() == 0)
        check(f'{tag} 4b: bloque arriba de Momentos clave', pg.evaluate("(()=>{ const b = document.querySelector('#clbox'), h = [...document.querySelectorAll('#side h3')].find(x => x.textContent==='Momentos clave'); return !!(b && h && (b.compareDocumentPosition(h) & Node.DOCUMENT_POSITION_FOLLOWING)); })()"))
        check(f'{tag} 4b: «Repasar estos errores» sigue en Qué entrenar', pg.locator('#trErr:visible').count() == 1 and pg.locator('#clTrain').count() == 0)
        # Captura con el modelo por defecto (Sonnet 5.5), como el mockup
        pg.evaluate("S.settings.claude.gameModel = 'claude-sonnet-5-5'; save(); GameAI.paint(S.played[0].id)"); time.sleep(.2)
        check(f'{tag} 4b: costo con Sonnet 5.5', 'menos de 5 centavos de dólar con Sonnet 5.5' in box())
        shot('4b-casilla-boton'); no_brand(pg, f'{tag} 4b')
        pg.evaluate("S.settings.claude.gameModel = 'claude-haiku-5-5'; save(); GameAI.paint(S.played[0].id)")
        # 4a: comentar
        pg.click('#clGo'); wait_box('Volver a comentar')
        h, body = GC()[-1]; user = body['messages'][0]['content']
        check(f'{tag} 4a: una sola llamada con la partida y sus errores', len(GC()) == 1 and 'Tarea: partida' in user and '"jugada": "5…Nxd5"' in user and 'Gran Maestro' in user and 'perdió' in user)
        c = box()
        check(f'{tag} 4a: resumen, errores, nota y botones', 'La partida se decidió en la apertura' in c and c.count('Ver en el tablero') == 3 and 'Escrito por IA a partir del análisis del motor' in c and 'Volver a comentar' in c and 'Borrar comentario' in c)
        check(f'{tag} 4a: línea de origen y sin el comentario local', org in c and 'Comentario del maestro (sin IA)' not in c)
        check(f'{tag} 4a: «Repasar estos errores como puzzles» dentro del bloque, sin repetir', pg.locator('#clbox #clTrain').count() == 1 and pg.locator('#trErr:visible').count() == 0)
        an = pg.evaluate(f"S.analyses[{json.dumps(PID)}]")
        check(f'{tag} 4a: se guarda en cx (partida y errores); exp intacto', len(an.get('cx',{}).get('summary',[])) == 2 and all(m.get('cx',{}).get('hint') for m in an['mistakes']) and an['mistakes'][0].get('exp') == EXP)
        shot('4a-casilla-comentario'); no_brand(pg, f'{tag} 4a')
        pg.click('[data-clgo="16"]'); time.sleep(.4)
        check(f'{tag} 4a: «Ver en el tablero» va a la jugada', pg.evaluate("App.session.ply") == 15 and pg.evaluate("App.session.open") == 15)
        # Recargar: sigue sin otra llamada
        pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000); open_played()
        check(f'{tag} recargar: el comentario sigue, sin otra llamada', 'Volver a comentar' in box() and len(GC()) == 1 and pg.locator('#clbox #clTrain').count() == 1)
        # Borrar: vuelve 4b y deja marca de borrado
        pg.evaluate("window.__R0 = JSON.parse(JSON.stringify(S))")
        pg.click('#clDel'); wait_box('Comentar partida con IA')
        check(f'{tag} borrar: vuelve al botón, «Repasar» regresa a Qué entrenar', 'Comentario del maestro (sin IA)' in box() and pg.locator('#trErr:visible').count() == 1)
        tb = pg.evaluate("(()=>{ const k = %s; const o = mergeState(JSON.parse(JSON.stringify(S)), window.__R0); return !o.analyses[k].cx && o.analyses[k].mistakes.every(m => !m.cx); })()" % json.dumps(PID))
        check(f'{tag} borrar sobrevive a la sincronización', tb)
        # Repasar desde el bloque
        pg.click('#clGo'); wait_box('Volver a comentar'); pg.click('#clTrain'); time.sleep(.6)
        check(f'{tag} 4a: «Repasar estos errores como puzzles» abre Mis errores', pg.evaluate("App.tab === 'puzzles' && App.puzzleSource === 'mine'"))
        if W == 1280:
            # Líneas de origen
            O = lambda d: pg.evaluate("(d => EvalSession.prototype.aiOrigin.call({job:{desc:d}}))(%s)" % json.dumps(d))
            FEN='8/8/8/4k3/8/8/4K3/4R3 w - - 0 1'
            check('origen: desde una posición sin título', O({'kind':'partida','startFen':FEN,'sans':[],'date':1792000000,'title':'Partida'}).startswith('Jugada en Casilla · Desde una posición · '))
            check('origen: desde una posición con título', O({'kind':'partida','startFen':FEN,'sans':[],'date':1792000000,'title':'Revancha de tu error'}).startswith('Jugada en Casilla · Revancha de tu error · '))
            check('origen: escalera (KIND_NAME)', O({'kind':'escalera','startFen':pg.evaluate('START_FEN'),'sans':['e4'],'date':1792000000,'title':'Nivel 4: Torre'}).startswith('Jugada en Casilla · Escalera · '))
            ol = pg.evaluate("OPENINGS.find(o => openingOf(o.line.split(' ')))")
            check('origen: con apertura conocida la agrega al final', O({'kind':'maestro','startFen':pg.evaluate('START_FEN'),'sans':ol['line'].split(' '),'date':1792000000}).endswith(' · ' + pg.evaluate("(l => openingOf(l.split(' ')))(%s)" % json.dumps(ol['line']))))
            check('origen: partida (KIND_NAME)', O({'kind':'partida','startFen':pg.evaluate('START_FEN'),'sans':['e4'],'date':1792000000,'title':'Partida'}).startswith('Jugada en Casilla · Partida · '))
            # Con la IA del Maestro activada tampoco se comenta la partida sola (los momentos del Maestro siguen igual)
            pg.evaluate("S.settings.claude.on = true; save(); openPlayed(S.played[0])"); time.sleep(1.5)
            check('IA del Maestro activada: abrir la evaluación no comenta la partida', len(GC()) == 2)
            pg.evaluate("S.settings.claude.on = false; save()")
            # Enlaces de la consola (QA 4)
            pg.click('.tab[data-tab=coach]'); time.sleep(.5)
            hrefs = pg.evaluate("[...document.querySelectorAll('#side a')].map(a => [a.textContent.trim(), a.href])")
            check('enlace «Ver gasto real en la consola» a platform.claude.com/cost', ['Ver gasto real en la consola', 'https://platform.claude.com/cost'] in hrefs)
            check('enlace «Obtener una clave» a platform.claude.com/settings/keys', ['Obtener una clave', 'https://platform.claude.com/settings/keys'] in hrefs)
            # Chess.com en EvalSession: comentario local, sin llamada automática
            n=len(SENT)
            pg.evaluate("(()=>{ const g = new Chess(); ['e4','e5','Nf3'].forEach(s => g.move(s)); App.setSession(new EvalSession({desc:{gid:'x', kind:'chesscom', sans:['e4','e5','Nf3'], startFen:START_FEN, user:'w', opp:'r'}, done:true, result:null, listeners:[]}, {})); })()"); time.sleep(.3)
            check('Chess.com en evaluación: sin llamada automática', len(SENT) == n)
        b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
