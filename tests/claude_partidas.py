exec(open('run.py').read().split("logs=[]")[0])
# Comentario de partida con IA y ejercicios de tus errores (mockups 1a-1f, 2a, 2b y 3). Todo con la API simulada:
# ninguna consulta sale a la red. Modos: ok, badkey (401 authentication_error), perm (403 permission_error),
# cors401 (401 sin authentication_error), cors (fetch falla: TypeError), hold (la respuesta tarda), nojson.
# Capturas en docs/capturas/claude-partidas/ a 1280 y 390 (CASILLA_SHOTS cambia la carpeta).
import re as _re
SHOTS=os.environ.get('CASILLA_SHOTS', str(_HERE.parent/'docs'/'capturas'/'claude-partidas'))+'/'
os.makedirs(SHOTS, exist_ok=True)
SENT=[]; MODE={'v':'ok'}; HELD=[]
CORS={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"*","Access-Control-Allow-Methods":"POST"}
GAME_JSON={"resumen":["La partida se decidió en la apertura. Con 4…d5 entraste en la línea más directa del Ng5, pero tras 5.exd5 recuperaste el peón con el caballo y dejaste f7 defendido solo por el rey.",
  "Después, 8…Ne7 en lugar de 8…Kd6 habría dejado una posición difícil pero jugable."],
  "errores":[{"id":"10","comentario":"El caballo en d5 queda atacado por el alfil de c4 y el punto f7 se queda sin ayuda. La línea habitual es 5…Na5: ataca al alfil y gana tiempo.","pista":"Antes de recuperar el peón, busca una jugada que ataque una pieza blanca y te dé tiempo."},
    {"id":"16","comentario":"Llevar el rey hacia el centro abre líneas para las piezas blancas. Ne7 cubría d5 y f5.","pista":"Tu rey está en peligro: busca una pieza que lo cubra."},
    {"id":"18","comentario":"El alfil se desarrolla, pero deja el centro a las blancas. Con exd4 abrías la columna e.","pista":"Mira qué peón blanco puedes capturar."}]}
def reply(body):
    user=body['messages'][0]['content']
    if 'Tarea: ejercicio' in user:
        return {"pista":"Busca una jugada que gane tiempo atacando una pieza.","explicacion":"La mejor según el motor ataca y gana tiempo; en la partida tu jugada dejó una pieza sin defensa."}
    return GAME_JSON
USAGE={"input_tokens":1200,"output_tokens":900,"cache_creation_input_tokens":1500,"cache_read_input_tokens":0}
def handle4(route):
    if 'api.anthropic.com' in route.request.url:
        if route.request.method=='OPTIONS': return route.fulfill(status=204,headers=CORS)
        body=json.loads(route.request.post_data); SENT.append((dict(route.request.headers), body))
        m=MODE['v']
        J=lambda st,o: route.fulfill(status=st,headers=CORS,content_type='application/json',body=json.dumps(o))
        if m=='badkey': return J(401,{"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}})
        if m=='perm': return J(403,{"type":"error","error":{"type":"permission_error","message":"Your API key does not have permission to use the specified resource."}})
        if m=='cors401': return J(401,{"type":"error","error":{"type":"invalid_request_error","message":"CORS requests are not allowed for this Organization because of the CORS settings."}})
        if m=='cors': return route.abort('failed')
        if m=='hold': HELD.append(route); return
        if m=='nojson': return J(200,{"content":[{"type":"text","text":"Lo siento, aquí va un comentario sin formato."}],"stop_reason":"end_turn","usage":USAGE})
        return J(200,{"content":[{"type":"text","text":"```json\n"+json.dumps(reply(body),ensure_ascii=False)+"\n```"}],"stop_reason":"end_turn","usage":USAGE})
    return handle(route)
fails=[]
def check(name, cond):
    print(('OK   ' if cond else 'FALLA ') + name)
    if not cond: fails.append(name)
SANS="e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Kd6 d4 Be7".split()
GID='https://www.chess.com/game/live/777'
SETUP="""(sans => {
  const g = new Chess(), fens = [g.fen()]; sans.forEach(s => { g.move(s); fens.push(g.fen()); });
  const w = fens.map((f, i) => i < 9 ? 20 : i < 15 ? 250 : 420);
  const M = (ply, best, bestSan, cat, drop) => { const c = new Chess(fens[ply-1]); const mv = c.move(sans[ply-1]);
    return {id:'%GID%#' + ply, gid:'%GID%', ply, fen:fens[ply-1], played:mv.san, playedUci:mv.from + mv.to, best, bestSan, drop, before:-20, cat, phase:'Apertura', date:1792000000, opp:'rodrigo_m', color:'b'}; };
  const pgn = '[Event "Live Chess"]\\n[White "rodrigo_m"]\\n[Black "fertest"]\\n[Result "1-0"]\\n[ECOUrl "https://www.chess.com/openings/Two-Knights-Defense-Fried-Liver-Attack"]\\n\\n' + g.pgn().replace(/\\[[^\\]]*\\]\\s*/g, '') + ' 1-0';
  S.username = 'fertest';
  S.games = [{id:'%GID%', pgn, white:'rodrigo_m', black:'fertest', wr:1312, br:1250, wres:'win', bres:'resigned', tc:'600+5', end:1792000000, eco:''}];
  S.analyses = {'%GID%':{v:1, acc:71, w, tags:{9:'??', 15:'?', 17:'?'}, cnt:{inacc:3, mistake:2, blunder:1},
    mistakes:[M(10, 'c6a5', 'Na5', 'Pieza colgada', 35), M(16, 'c6e7', 'Ne7', 'Error posicional', 24), M(18, 'e5d4', 'exd4', 'Error posicional', 22)], mt:400}};
  save(); return true; })""".replace('%GID%', GID)
def visible(pg):
    return pg.evaluate("""(()=>{ const c = document.body.cloneNode(true); c.querySelectorAll('footer,script,style').forEach(e=>e.remove());
      return c.innerText + ' ' + [...document.querySelectorAll('input,option,button,[title],[aria-label],[placeholder]')].filter(e => !e.closest('footer')).map(e => (e.tagName==='INPUT' && e.type!=='hidden' && e.type!=='password' ? e.value : '') + ' ' + (e.tagName==='OPTION' ? e.textContent : '') + ' ' + (e.title||'') + ' ' + (e.getAttribute('aria-label')||'') + ' ' + (e.placeholder||'')).join(' '); })()""")
def no_brand(pg, where):
    hits=_re.findall(r'(?i)claude|anthropic|stockfish', visible(pg))
    check(f'sin Claude/Anthropic/Stockfish visibles ({where})', not hits)
    if hits: print('   ', set(hits))
for W in [1280, 390]:
    SENT.clear(); MODE['v']='ok'
    with sync_playwright() as p:
        b=p.chromium.launch(); mob = W == 390
        ctx=b.new_context(viewport={'width':W,'height':900 if not mob else 844}, device_scale_factor=1 if not mob else 2, is_mobile=mob, has_touch=mob)
        ctx.route('**/*',handle4); pg=ctx.new_page()
        pg.on('pageerror',lambda e: (print('PAGEERROR',e), fails.append('pageerror')))
        pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
        pg.evaluate(SETUP, SANS); pg.evaluate("localStorage.removeItem('casilla.aiGasto')")
        tag=f'{W}'
        def shot(name):
            # Solo para la captura (como en el mock): el panel lateral se muestra completo
            pg.add_style_tag(content='.side{max-height:none!important;overflow:visible!important;height:auto!important} main{height:auto!important;overflow:visible!important}')
            pg.screenshot(path=SHOTS+('escritorio' if W==1280 else 'movil')+'-'+name+'.png', full_page=True)
        def open_game():
            pg.evaluate("App.tab='games'; $$('.tab').forEach(b=>b.setAttribute('aria-selected', b.dataset.tab==='games')); App.setSession(new ReviewSession(S.games[0], 10))"); time.sleep(.4)
        def box(): return pg.inner_text('#clbox')
        def wait_box(txt, t=8000): pg.wait_for_function(f"document.querySelector('#clbox') && document.querySelector('#clbox').innerText.includes({json.dumps(txt)})",timeout=t)
        open_game()
        check(f'{tag} botón de regreso dice «← Partidas»', pg.inner_text('#bk').strip() == '← Partidas')
        check(f'{tag} 1a: bloque arriba de Momentos clave', pg.evaluate("(()=>{ const b = document.querySelector('#clbox'), h = [...document.querySelectorAll('#side h3')].find(x => x.textContent==='Momentos clave'); return !!(b && h && (b.compareDocumentPosition(h) & Node.DOCUMENT_POSITION_FOLLOWING)); })()"))
        check(f'{tag} 1a: texto y botón', 'Comentar partida con IA' in box() and 'costo aproximado: menos de 5 centavos de dólar con Sonnet 5.5' in box())
        shot('1a-boton'); no_brand(pg, f'{tag} 1a')
        # 1d: sin clave
        pg.click('#clGo'); wait_box('Falta tu clave de IA')
        check(f'{tag} 1d: sin clave no consulta', len(SENT) == 0 and 'Ir a la clave' in box() and 'Cómo obtener una clave' in box())
        shot('1d-error-sin-key'); no_brand(pg, f'{tag} 1d')
        pg.click('#clKey'); time.sleep(.4)
        check(f'{tag} «Ir a la clave» lleva a Maestro, a la clave', pg.evaluate("App.tab==='coach' && document.activeElement && document.activeElement.id==='aikey'"))
        check(f'{tag} sección «Comentarios con IA (opcional)»', 'Comentarios con IA (opcional)' in pg.inner_text('#side'))
        no_brand(pg, f'{tag} Maestro sin clave')
        # Clave simulada; Haiku para comentar partidas en pruebas
        pg.evaluate("S.settings.claude = {on:false, key:'sk-ant-prueba', model:'claude-haiku-5-5', gameModel:'claude-haiku-5-5'}; save()")
        open_game()
        check(f'{tag} 1a con Haiku: costo menor', 'menos de 1 centavo de dólar con Haiku 5.5' in box())
        # 1b: cargando y cancelar
        MODE['v']='hold'; pg.click('#clGo'); wait_box('La IA está leyendo la partida')
        check(f'{tag} 1b: cargando', 'Suele tardar entre 10 y 20 segundos' in box() and pg.evaluate("document.querySelector('#clbox .cl-box').getAttribute('aria-busy')") == 'true')
        pg.click('#controls button:has-text("Siguiente")')
        time.sleep(.2); check(f'{tag} 1b: se puede seguir revisando la partida', 'La IA está leyendo' in box())
        shot('1b-cargando'); no_brand(pg, f'{tag} 1b')
        pg.click('#clCancel'); wait_box('Comentar partida con IA')
        for r in HELD:
            try: r.abort('aborted')
            except Exception: pass
        HELD.clear(); time.sleep(.3)
        check(f'{tag} cancelar vuelve al botón sin guardar', pg.evaluate(f"!S.analyses[{json.dumps(GID)}].cx"))
        # 1c: comentario
        MODE['v']='ok'; n0=len(SENT); pg.click('#clGo'); wait_box('Volver a comentar')
        h, body = SENT[-1]
        check(f'{tag} una sola llamada', len(SENT) == n0 + 1)
        check(f'{tag} encabezados de la API', h.get('x-api-key') == 'sk-ant-prueba' and h.get('anthropic-dangerous-direct-browser-access') == 'true')
        check(f'{tag} modelo de pruebas (Haiku)', body.get('model') == 'claude-haiku-5-5')
        sysb = body.get('system')
        check(f'{tag} prompt caching: cache_control en el bloque fijo', isinstance(sysb, list) and sysb[0].get('cache_control') == {'type':'ephemeral'} and len(sysb[0]['text']) > 2000)
        user = body['messages'][0]['content']
        check(f'{tag} envía PGN con evaluaciones y los errores', 'Tarea: partida' in user and '5... Nxd5 {' not in user and 'Nxd5 {' in user and '"jugada": "5…Nxd5"' in user and '"mejor_del_motor": "5…Na5"' in user and '[Result "1-0"]' in user)
        c = box()
        check(f'{tag} 1c: resumen y un comentario por error', 'La partida se decidió en la apertura' in c and c.count('Ver en el tablero') == 3 and '5…Nxd5' in c and '8…Kd6' in c and 'Error grave' in c)
        check(f'{tag} 1c: nota de autoría y costo aproximado', 'Escrito por IA a partir del análisis del motor; el texto puede tener errores.' in c and 'Costo aprox. de este comentario' in c)
        check(f'{tag} 1c: Volver a comentar y Borrar comentario', 'Volver a comentar' in c and 'Borrar comentario' in c)
        cx = pg.evaluate(f"S.analyses[{json.dumps(GID)}]")
        check(f'{tag} se guarda cx de la partida con usage', cx.get('cx',{}).get('usage',{}).get('cache_creation_input_tokens') == 1500 and cx['cx']['model'] == 'claude-haiku-5-5' and len(cx['cx']['summary']) == 2)
        check(f'{tag} se guarda m.cx con pista y texto; exp intacto', all(m.get('cx',{}).get('hint') and m['cx'].get('text') for m in cx['mistakes']) and all('exp' not in m for m in cx['mistakes']))
        shot('1c-comentario'); no_brand(pg, f'{tag} 1c')
        pg.click('[data-clgo="16"]'); time.sleep(.3)
        check(f'{tag} «Ver en el tablero» lleva a la jugada', pg.evaluate("App.session.ply") == 16)
        # Volver a comentar: mismo bloque fijo (la caché lo reutiliza)
        pg.click('#clAgain'); wait_box('Volver a comentar'); time.sleep(.2)
        check(f'{tag} Volver a comentar hace otra llamada con el mismo bloque fijo', len(SENT) == n0 + 2 and SENT[-1][1]['system'] == sysb)
        # Datos guardados: sincronización y respaldo
        st = pg.evaluate("(()=>{ const c = stripForSync(JSON.parse(JSON.stringify(S))); return {claude: !!(c.settings && c.settings.claude), cx: !!c.analyses[%s].cx}; })()" % json.dumps(GID))
        check(f'{tag} stripForSync quita la clave y conserva los comentarios', st['claude'] is False and st['cx'] is True)
        mg = pg.evaluate("(()=>{ const L = JSON.parse(JSON.stringify(S)), R = JSON.parse(JSON.stringify(S)); const k = %s; delete L.analyses[k].cx; L.analyses[k].mistakes.forEach(m => delete m.cx); const o = mergeState(L, R); return !!o.analyses[k].cx && o.analyses[k].mistakes.every(m => m.cx && m.cx.hint); })()" % json.dumps(GID))
        check(f'{tag} mergeState conserva cx del otro lado', mg)
        # 2a / 2b: Mis errores con la pista guardada
        pg.click('[data-pz="0"]'); pg.wait_for_function("App.session.p && App.session.p.src==='mine'",timeout=8000); time.sleep(.3)
        check(f'{tag} 2a: «Ver pista» antes de mostrarla', pg.locator('#aiHint').count() == 1 and 'Pista de la IA' not in pg.inner_text('#pzinfo'))
        check(f'{tag} sin la pista del motor repetida', pg.locator('#controls button', has_text=_re.compile('^Pista$')).count() == 0)
        pg.click('#aiHint'); time.sleep(.3)
        check(f'{tag} 2a: pista guardada, sin llamada nueva', 'Antes de recuperar el peón' in pg.inner_text('#pzinfo') and len(SENT) == n0 + 2)
        shot('2a-mis-errores-pista'); no_brand(pg, f'{tag} 2a')
        pg.evaluate("(()=>{ const s = App.session; s.onUserMove({from:'c6', to:'a5'}); })()")
        pg.wait_for_function("App.session.p && App.session.p.done",timeout=8000); time.sleep(.6)
        info = pg.inner_text('#pzinfo')
        check(f'{tag} 2b: se resuelve contra la jugada del motor y muestra la explicación', 'Explicación de la IA' in info and 'El caballo en d5 queda atacado' in info and 'la solución la valida el motor' in info)
        check(f'{tag} 2b: sigue en el repaso espaciado', pg.evaluate(f"!!S.srs[{json.dumps(GID+'#10')}]") and 'Entra al repaso espaciado' in info)
        shot('2b-mis-errores-explicacion'); no_brand(pg, f'{tag} 2b')
        # Ejercicio sin comentario previo: «Ver pista» consulta a la IA una vez y guarda m.cx
        pg.evaluate(f"(()=>{{ const m = S.analyses[{json.dumps(GID)}].mistakes[2]; delete m.cx; App.setSession(new PuzzleSession(mistakePuzzle(m))); }})()"); time.sleep(.5)
        n1=len(SENT); pg.click('#aiHint'); pg.wait_for_function("document.querySelector('#pzinfo').innerText.includes('Pista de la IA')",timeout=8000)
        eb = SENT[-1][1]
        check(f'{tag} ejercicio suelto: una llamada con el mismo bloque fijo', len(SENT) == n1 + 1 and 'Tarea: ejercicio' in eb['messages'][0]['content'] and eb['system'] == sysb)
        check(f'{tag} ejercicio suelto: guarda pista y explicación en m.cx', pg.evaluate(f"(()=>{{ const c = S.analyses[{json.dumps(GID)}].mistakes[2].cx; return !!(c && c.hint && c.text && c.model); }})()"))
        # 3: gasto aproximado en Maestro
        pg.click('.tab[data-tab=coach]'); time.sleep(.4)
        sp = pg.inner_text('#spend')
        g = pg.evaluate("AISpend.get()")
        check(f'{tag} 3: contador de gasto aproximado', 'Gasto aproximado en este navegador' in sp and g['games'] == 2 and g['ex'] == 1 and 'Total aproximado' in sp)
        exp_usd = 3 * (1200*0.10 + 1500*0.125 + 900*0.50) / 1e6
        check(f'{tag} 3: costo calculado con la tarifa de Haiku', abs(g['usd'] - exp_usd) < 1e-9)
        pg.evaluate("document.querySelector('#spend').scrollIntoView()"); shot('3-ajustes-gasto'); no_brand(pg, f'{tag} 3 Maestro')
        pg.click('#spendReset'); time.sleep(.3)
        check(f'{tag} reiniciar contador', pg.evaluate("AISpend.get().usd") == 0)
        # Borrar comentario
        open_game(); pg.click('#clDel'); wait_box('Comentar partida con IA')
        check(f'{tag} Borrar comentario quita cx y deja exp', pg.evaluate(f"(()=>{{ const a = S.analyses[{json.dumps(GID)}]; return !a.cx && a.mistakes.every(m => !m.cx); }})()"))
        # 1e: clave inválida (401 authentication_error)
        MODE['v']='badkey'; pg.click('#clGo'); wait_box('rechazó la clave')
        check(f'{tag} 1e: clave inválida', 'El servicio de IA rechazó la clave' in box() and 'error 401' in box() and 'Revisar la clave' in box() and 'Reintentar' in box())
        shot('1e-error-key-invalida'); no_brand(pg, f'{tag} 1e')
        # 403 permission_error y 401 sin authentication_error: mensaje distinto
        MODE['v']='perm'; pg.click('#clGo'); wait_box('no dio permiso')
        check(f'{tag} 403: mensaje de permiso, distinto de clave inválida', 'error 403' in box() and 'rechazó la clave' not in box())
        MODE['v']='cors401'; pg.click('#clGo'); wait_box('no dio permiso')
        check(f'{tag} 401 sin authentication_error (CORS de la organización): mensaje de permiso', 'error 401' in box() and 'desde el navegador' in box())
        # CORS bloqueado o red caída con conexión: TypeError
        MODE['v']='cors'; pg.click('#clGo'); wait_box('No se pudo conectar')
        check(f'{tag} fetch bloqueado (TypeError): no se confunde con clave inválida', 'rechazó la clave' not in box() and 'Reintentar' in box())
        # Respuesta sin JSON: no guarda nada
        MODE['v']='nojson'; pg.click('#clGo'); wait_box('formato inesperado')
        check(f'{tag} respuesta sin JSON: aviso y nada guardado', pg.evaluate(f"!S.analyses[{json.dumps(GID)}].cx"))
        # 1f: sin conexión
        ctx.set_offline(True); time.sleep(.5)
        check(f'{tag} 1f: sin conexión', 'Sin conexión' in box() and pg.evaluate("document.querySelector('#clGo').disabled") and 'Se activa al volver la conexión' in box())
        shot('1f-error-sin-conexion'); no_brand(pg, f'{tag} 1f')
        n2=len(SENT)
        ctx.set_offline(False); time.sleep(.5)
        check(f'{tag} al volver la red se puede comentar', pg.evaluate("!document.querySelector('#clGo').disabled") and len(SENT) == n2)
        MODE['v']='ok'; pg.click('#clGo'); wait_box('Volver a comentar')
        # Datos viejos sin cx y re-análisis: el comentario se conserva
        if W == 1280:
            kept = pg.evaluate("""(async () => { const r = S.games[0]; await Engine.whenReady(); const a = await Analyzer.analyzeGame(r, 60, null, 'ana'); return !!(a && a.cx && a.cx.summary.length); })()""")
            check('re-analizar conserva el comentario de la partida', kept)
            old = pg.evaluate("""(() => { const a = S.analyses[%s]; delete a.cx; a.mistakes.forEach(m => delete m.cx); App.setSession(new ReviewSession(S.games[0])); return document.querySelector('#clbox').innerText.includes('Comentar partida con IA'); })()""" % json.dumps(GID))
            check('datos sin cx abren igual', old)
        b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
