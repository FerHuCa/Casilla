exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
# Historial: las partidas jugadas en Casilla entran a Mis partidas cuando termina su evaluación,
# sus errores alimentan los puzzles y la evaluación se reabre sin recalcular.
def play(pg, moves, title):
    pg.evaluate("""App.setSession(new PlaySession({userColor:'w', tier:TIERS[7], tierIdx:7, ladder:false, helps:false, title:'%s', oppName:'Gran Maestro'}))""" % title)
    for mv in moves:
        pg.wait_for_function("!App.session.thinking && !App.session.over", timeout=20000)
        ok = pg.evaluate(f"(()=>{{ const m=uciObj('{mv}'); const legal=App.game.moves({{verbose:true}}).some(x=>x.from===m.from&&x.to===m.to); if(legal) App.session.onUserMove(m); return legal; }})()")
        time.sleep(.3)
        if not ok: break
    pg.wait_for_function("!App.session.thinking", timeout=20000)
    pg.click('text=Abandonar'); time.sleep(.4)
    return pg.evaluate("App.session.evalJob")
fails=[]
def check(name, cond):
    print(('OK   ' if cond else 'FALLA ') + name)
    if not cond: fails.append(name)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':950}); ctx.route('**/*',handle2); pg=ctx.new_page()
    pg.on('pageerror',lambda e: (print('PAGEERROR',e), fails.append('pageerror')))
    pg.on('console',lambda m: print('C',m.text) if m.type in ('error','warning') and 'ERR_FAILED' not in m.text else None)
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.evaluate("S.settings.evalTime=200")
    # 1) Una partida y, sin esperar la evaluación, otra: la primera no se pierde
    play(pg, ['e2e4','g1f3','f1c4','f3e5','e5f7','h1f1'], 'Prueba uno')
    gid1 = pg.evaluate("App.session.gid")
    play(pg, ['d2d4','c1f4','e2e3','f1d3','d1h5'], 'Prueba dos')
    gid2 = pg.evaluate("App.session.gid")
    pg.wait_for_function(f"S.analyses['{gid1}'] && S.analyses['{gid1}'].deep && S.analyses['{gid2}'] && S.analyses['{gid2}'].deep", timeout=180000)
    time.sleep(.5)
    ids = pg.evaluate("S.played.map(g=>g.id)")
    check('las dos partidas están en el historial', gid1 in ids and gid2 in ids)
    check('la más reciente va primero', ids[0] == gid2)
    a1 = pg.evaluate(f"(()=>{{const a=S.analyses['{gid1}'], r=S.played.find(g=>g.id==='{gid1}'); return {{w:a.w.length, best:a.best.length, pv:a.pv.length, sans:r.sans.length, res:r.res, title:r.title, opp:r.opp}}}})()")
    print('registro 1', a1)
    check('se guardan best y pv por posición', a1['w'] == a1['best'] == a1['pv'] == a1['sans'] + 1)
    check('resultado de abandono', a1['res'] == 'l')
    # 2) Mis partidas muestra la sección y abre la evaluación al instante
    pg.click('.tab[data-tab=games]'); time.sleep(.4)
    side = pg.inner_text('#side')
    check('sección Jugadas en Casilla', 'Jugadas en Casilla' in side and 'vs Gran Maestro' in side)
    print(side[:600])
    pg.screenshot(path=OUT+'h1_lista.png')
    pg.click(f'.game[data-pid="{gid1}"]'); time.sleep(.6)
    st = pg.evaluate("[App.session.constructor.name, App.session.job.done, !!App.session.job.cached]")
    check('abre la evaluación guardada sin recalcular', st == ['EvalSession', True, True])
    n = pg.evaluate("App.session.job.result.fens.length")
    pg.click('#controls >> text=Inicio'); time.sleep(.2)
    seq=[pg.evaluate("App.session.ply")]
    for k in range(n-1):
        pg.click('#controls >> text=Siguiente'); time.sleep(.15); seq.append(pg.evaluate("App.session.ply"))
    check('recorre todas las jugadas en orden', seq == list(range(n)))
    note = pg.inner_text('#mvnote')
    print('nota final:', note)
    check('cada jugada tiene comentario', pg.evaluate("(()=>{const E=App.session.job.result; return E.per.every((p,i)=>moveComment(E,i).text.length>10)})()"))
    pg.click('#ml [data-ply="2"]'); time.sleep(.2)
    check('clic en la lista de jugadas', pg.evaluate("App.session.ply") == 2)
    pg.screenshot(path=OUT+'h2_eval.png')
    # 3) Los errores de estas partidas alimentan los puzzles y llevan de regreso a la partida
    mine = pg.evaluate(f"errorProfile().all.filter(m=>m.gid==='{gid1}' || m.gid==='{gid2}').length")
    print('errores en puzzles', mine)
    check('errores de las partidas en Mis errores', mine > 0)
    if mine:
        pg.evaluate(f"(()=>{{const m=errorProfile().all.find(m=>m.gid==='{gid1}'||m.gid==='{gid2}'); App.tab='puzzles'; App.setSession(new PuzzleSession(mistakePuzzle(m)));}})()"); time.sleep(.6)
        check('botón Ver la partida en el puzzle', pg.locator('#pzGame').count() == 1)
        pg.click('#pzGame'); time.sleep(.6)
        st = pg.evaluate("[App.session.constructor.name, App.session.focus, App.session.ply]")
        print('desde el puzzle', st, pg.inner_text('#status'))
        check('abre la partida en el error', st[0] == 'EvalSession' and st[1] is not None and st[1] == st[2])
    # 4) Cambiar de usuario de Chess.com no borra lo jugado en Casilla
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.3)
    pg.evaluate("S.username='otro'"); pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.3)
    check('cambio de usuario conserva el historial de Casilla', pg.evaluate(f"S.played.length>=2 && !!S.analyses['{gid1}']"))
    # 5) Sincronización: se unen los historiales
    merged = pg.evaluate("""(()=>{ const R = JSON.parse(JSON.stringify(S)); R.played = [{id:'play:1', src:'casilla', kind:'partida', title:'Otra', opp:'X', user:'b', start:START_FEN, sans:['e4','e5'], res:'d', why:'', end:1}]; const L = JSON.parse(JSON.stringify(S)); const out = mergeState(L, R); return [out.played.length, L.played.length]; })()""")
    check('mergeState une el historial', merged[0] == merged[1] + 1)
    keep = pg.evaluate(f"""(()=>{{ const L = JSON.parse(JSON.stringify(S)), R = JSON.parse(JSON.stringify(S)); delete L.analyses['{gid1}'].best; delete L.analyses['{gid1}'].pv; return Array.isArray(mergeState(L, R).analyses['{gid1}'].best); }})()""")
    check('mergeState conserva las líneas guardadas', keep)
    # 6) Persiste al recargar
    pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000)
    check('el historial sobrevive a recargar', pg.evaluate(f"S.played.some(g=>g.id==='{gid1}')"))
    b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
