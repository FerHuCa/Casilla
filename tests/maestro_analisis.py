exec(open('run.py').read().split("logs=[]")[0])
# Análisis con el Maestro: importar (captura, FEN, PGN, link de Chess.com, partidas recientes), editor de posición,
# explicaciones sin IA y con IA (API simulada, con el motor como herramienta) y auditoría móvil de las pantallas nuevas.
import re as _re
SENT=[]; CFG={'read':None, 'tool_moves':['Nf6'], 'answer':'Explicación IA de prueba.'}
CORS={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"*","Access-Control-Allow-Methods":"POST"}
def anth(route):
    if route.request.method=='OPTIONS': return route.fulfill(status=204,headers=CORS)
    body=json.loads(route.request.post_data); SENT.append(body)
    def ok(content, stop='end_turn'):
        return route.fulfill(status=200,headers=CORS,content_type='application/json',body=json.dumps({"content":content,"stop_reason":stop}))
    first=body['messages'][0]['content']
    if isinstance(first,list) and any(b.get('type')=='image' for b in first):
        return ok([{"type":"text","text":"Aquí está:\n"+json.dumps(CFG['read'])}])
    if body.get('tools'):
        last=body['messages'][-1]['content']
        if isinstance(last,list) and any(b.get('type')=='tool_result' for b in last):
            return ok([{"type":"text","text":CFG['answer']}])
        if body.get('tool_choice',{}).get('type')=='none':
            return ok([{"type":"text","text":CFG['answer']}])
        return ok([{"type":"thinking","thinking":"","signature":"sig"},{"type":"tool_use","id":"tu_1","name":"evaluar_jugadas","input":{"jugadas":CFG['tool_moves']}}], 'tool_use')
    return ok([{"type":"text","text":"listo"}])
def handle4(route):
    if 'api.anthropic.com' in route.request.url: return anth(route)
    return handle(route)
fails=[]
def check(name, cond):
    print(('OK   ' if cond else 'FALLA ') + name)
    if not cond: fails.append(name)
def side_text(pg):
    return pg.evaluate("document.querySelector('#side').innerText + ' ' + document.querySelector('.under').innerText")
def no_brand(pg, where):
    hits=_re.findall(r'(?i)claude|anthropic|stockfish', side_text(pg))
    check(f'sin menciones de Claude/Anthropic/Stockfish ({where})', not hits)
def wait_msg(pg, timeout=40000):
    pg.wait_for_function("App.session.msgs && App.session.msgs.length && !App.session.msgs[0].pending", timeout=timeout)
    return pg.evaluate("App.session.msgs[0]")
def ai_on(pg, on=True):
    pg.evaluate(f"S.settings.claude = {{on:{'true' if on else 'false'}, key:'sk-ant-prueba', model:'claude-haiku-5-5', anaModel:'claude-opus-5-5'}}")
def view(fen, bottom):
    # filas tal como se ven en la imagen, según qué bando está abajo
    rows=[]
    for r in fen.split()[0].split('/'):
        rows.append(''.join('.'*int(c) if c.isdigit() else c for c in r))
    if bottom=='b': rows=[r[::-1] for r in rows[::-1]]
    return rows
SHOT=str(_HERE.parent/'docs'/'capturas'/'390-partida.png')
FEN_IT='r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3'

with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':950}); ctx.route('**/*',handle4); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: (print('PAGEERROR',e), errs.append(str(e))))
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)

    # --- Importar sin IA ---
    pg.click('.tab[data-tab=positions]'); time.sleep(.3)
    pg.click('[data-seg=pt] button[data-v=importar]'); time.sleep(.3)
    check('pestaña Importar con captura, texto y partidas recientes', pg.is_visible('#shotin') or pg.query_selector('#shotin') is not None)
    check('sin IA, subir captura está desactivado y se ofrece armar a mano', pg.evaluate("document.querySelector('#shotin').disabled") and pg.is_visible('#byHand'))
    no_brand(pg,'importar')
    pg.fill('#fenin', 'esto no es nada'); pg.click('#fenAna'); time.sleep(.3)
    check('texto no reconocido se explica', 'No reconozco' in pg.inner_text('#fenerr'))
    pg.fill('#fenin', FEN_IT); pg.click('#fenAna'); time.sleep(.5)
    check('FEN abre el análisis', pg.evaluate("App.session instanceof AnalysisSession && App.game.fen()") == FEN_IT)
    pg.wait_for_function("document.querySelector('#lines') && document.querySelector('#lines').innerText.includes('Profundidad')", timeout=20000)
    pg.wait_for_function("App.session.cache[App.game.fen()]", timeout=20000)
    check('el botón de la mejor jugada lleva su nombre', pg.inner_text('#maBest').startswith('¿Por qué ') and not pg.evaluate("document.querySelector('#maBest').disabled"))
    check('sin jugada previa no se ofrece "¿Qué tal?"', pg.evaluate("document.querySelector('#maMine').hidden"))
    check('sin IA no hay campo de pregunta libre', pg.query_selector('#maQ') is None)
    pg.click('#maPos'); m=wait_msg(pg)
    print('  ', m['text'][:160]); print('  ', (m.get('line') or '')[:120])
    check('explicación sin IA: quién mueve, evaluación y mejor jugada', 'Mueven negras' in m['text'] and 'Según el motor' in m['text'] and 'la mejor es' in m['text'] and not m.get('ai'))
    check('la explicación trae la línea del motor y una flecha', (m.get('line') or '').startswith('Línea del motor') and len(m.get('arrows') or [])==1)
    pg.click('#maBest'); m=wait_msg(pg)
    check('por qué la mejor (sin IA)', 'la mejor es' in m['text'])
    # Jugada del usuario: Nd4 (casilla d4 está libre) y luego "¿Qué tal Nd4?"
    pg.click('.sq[data-sq="c6"]'); pg.click('.sq[data-sq="d4"]'); time.sleep(.3)
    check('después de mover aparece "¿Qué tal Nd4?"', pg.inner_text('#maMine') == '¿Qué tal Nd4?' and pg.is_visible('#maMine'))
    pg.click('#maMine'); m=wait_msg(pg, 60000)
    print('  ', m['text'][:200])
    check('evaluación de la jugada del usuario (sin IA)', 'Nd4' in m['text'] and (m.get('line') or '').startswith('Respuesta del rival'))
    check('mensajes previos ofrecen volver a su posición', pg.query_selector('#mafeed [data-show]') is not None)
    pg.click('#mafeed [data-show]'); time.sleep(.4)
    no_brand(pg,'análisis')

    # --- Con IA: herramientas del motor ---
    ai_on(pg); pg.evaluate("App.session.renderSide(); App.session.update()"); time.sleep(.3)
    check('con IA aparece la pregunta libre', pg.is_visible('#maQ'))
    pg.evaluate("App.session.go(0)"); time.sleep(.2)
    n=len(SENT); pg.click('#maPos'); m=wait_msg(pg, 60000)
    calls=SENT[n:]
    check('con IA: dos llamadas (herramienta y respuesta)', len(calls)==2)
    if len(calls)==2:
        c1,c2=calls
        check('modelo de análisis: Opus 5.5', c1['model']=='claude-opus-5-5')
        check('Opus: sin "thinking" y con esfuerzo bajo', 'thinking' not in c1 and c1.get('output_config')=={'effort':'low'} and c1['max_tokens']>=4000)
        check('se ofrece la herramienta evaluar_jugadas', c1['tools'][0]['name']=='evaluar_jugadas')
        u=c1['messages'][0]['content']
        check('los datos incluyen líneas, piezas y hechos', '"mejores_lineas"' in u and '"piezas"' in u and '"hechos"' in u and 'Explica esta posición' in u)
        check('el sistema pide no inventar y usar la herramienta', 'evaluar_jugadas' in c1['system'] and 'No inventes' in c1['system'])
        a=c2['messages'][1]; tr=c2['messages'][2]['content'][0]
        check('se devuelve el bloque de pensamiento sin cambios', a['role']=='assistant' and a['content'][0]=={"type":"thinking","thinking":"","signature":"sig"})
        res=json.loads(tr['content']); print('  ', res)
        check('la herramienta calcula con el motor', tr['type']=='tool_result' and tr['tool_use_id']=='tu_1' and 'evaluacion' in res and 'mejor_continuacion' in res and 'comparacion' in res)
    check('la respuesta de la IA se muestra con su etiqueta', m['text']=='Explicación IA de prueba.' and m.get('ai'))
    # Jugada ilegal pedida por la IA
    CFG['tool_moves']=['e4']; n=len(SENT); pg.click('#maBest'); m=wait_msg(pg, 60000)
    tr=SENT[n+1]['messages'][2]['content'][0] if len(SENT)>n+1 else {}
    res=json.loads(tr.get('content','{}'))
    check('jugada ilegal: error con jugadas legales', tr.get('is_error') and 'no es legal' in res.get('error','') and 'Nf6' in res.get('jugadas_legales',[]))
    CFG['tool_moves']=['Nf6']
    # Pregunta libre
    n=len(SENT); pg.fill('#maQ','¿Qué plan tengo aquí?'); pg.press('#maQ','Enter'); m=wait_msg(pg, 60000)
    check('pregunta libre: se muestra la pregunta y la respuesta', pg.evaluate("App.session.msgs[1].label")=='Tú' and m['text']=='Explicación IA de prueba.')
    check('la pregunta llega a la IA', any('¿Qué plan tengo aquí?' in c['messages'][0]['content'] for c in SENT[n:] if isinstance(c['messages'][0]['content'], str)))
    # Error de la IA: queda la explicación del motor
    ctx.unroute('**/*'); ctx.route('**/*', lambda r: r.fulfill(status=401,headers=CORS,content_type='application/json',body=json.dumps({"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}})) if 'api.anthropic.com' in r.request.url else handle4(r))
    pg.click('#maPos'); m=wait_msg(pg, 60000)
    check('si la IA falla, explica el motor y avisa', 'Mueven' in m['text'] and 'invalid x-api-key' in (m.get('note') or ''))
    ctx.unroute('**/*'); ctx.route('**/*',handle4)

    # --- Captura ---
    target='rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1'
    CFG['read']={"tablero":True,"abajo":"b","filas":view(target,'b'),"mueven":None,"ultima":[[1,2],[3,3]],"dudas":[[8,4]]}
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    check('con IA, subir captura está activo', not pg.evaluate("document.querySelector('#shotin').disabled"))
    n=len(SENT); pg.set_input_files('#shotin', SHOT)
    pg.wait_for_function("App.session instanceof EditorSession", timeout=20000); time.sleep(.3)
    req=SENT[n]; img=req['messages'][0]['content'][0]
    check('la captura va como imagen en base64', img['type']=='image' and img['source']['media_type']=='image/png' and len(img['source']['data'])>1000)
    check('lectura: Opus 5.5 con esfuerzo medio y sin apagar el pensamiento', req['model']=='claude-opus-5-5' and req.get('output_config')=={'effort':'medium'} and 'thinking' not in req)
    check('la imagen se achica al lado largo de 1568 px', pg.evaluate("(()=>{ const i=document.querySelector('.shot img'); return Math.max(i.naturalWidth,i.naturalHeight); })()")<=1568)
    print('  ', pg.evaluate("App.session.fen()"))
    check('la posición leída se convierte con negras abajo', pg.evaluate("App.session.fen()")==target)
    check('turno deducido de la última jugada resaltada', pg.evaluate("App.session.turn")=='b' and pg.evaluate("App.session.o.turnKnown"))
    check('tablero orientado como la captura', pg.evaluate("Board.orient")=='b')
    check('casilla dudosa marcada', pg.evaluate("Board.marks.e8")=='hint' and 'casillas marcadas' in pg.inner_text('#edprob'))
    check('se muestra la captura junto al editor', pg.is_visible('.shot img'))
    no_brand(pg,'editor')
    # Editar: poner y quitar piezas, rey que falta, enroques
    pg.click('[data-pc=Q]'); pg.click('.sq[data-sq="d4"]')
    check('poner una dama blanca en d4', pg.evaluate("App.session.b[4][3]")=='Q' and pg.evaluate("App.game.get('d4')")=={'type':'q','color':'w'})
    pg.click('.sq[data-sq="d4"]')
    check('tocarla otra vez la quita', pg.evaluate("App.session.b[4][3]") is None)
    pg.click('[data-pc=x]'); pg.click('.sq[data-sq="e1"]'); time.sleep(.2)
    check('sin rey blanco: aviso y botones desactivados', 'Falta el rey blanco' in pg.inner_text('#edprob') and pg.evaluate("document.querySelector('#edAna').disabled"))
    check('al quitar el rey se quitan sus enroques', pg.evaluate("App.session.castle")=='kq')
    pg.click('[data-pc=K]'); pg.click('.sq[data-sq="e1"]'); pg.check('[data-cs=K]'); time.sleep(.2)
    check('rey de vuelta y enroque corto marcado', pg.evaluate("App.session.castle")=='Kkq' and not pg.evaluate("document.querySelector('#edAna').disabled"))
    pg.click('[data-seg=edturn] button[data-v=w]'); time.sleep(.2)
    check('cambiar el turno', pg.evaluate("App.session.fen().split(' ')[1]")=='w')
    pg.click('[data-seg=edturn] button[data-v=b]')
    pg.fill('#edfen','8/8/8/8/8/8/8/8 w - - 0 1'); pg.click('#edFenGo'); time.sleep(.2)
    check('FEN vacía: faltan los reyes', 'Falta el rey blanco' in pg.inner_text('#edprob') and 'Falta el rey negro' in pg.inner_text('#edprob'))
    pg.click('#edStart'); time.sleep(.2)
    check('posición inicial en el editor', pg.evaluate("App.session.fen()")=='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    pg.fill('#edfen','4k3/8/8/8/8/8/8/4K2R w K - 0 1'); pg.click('#edFenGo'); pg.click('[data-seg=edturn] button[data-v=b]'); time.sleep(.2)
    check('posición válida con negras', 'válida' in pg.inner_text('#edprob'))
    pg.fill('#edfen','4k3/8/8/8/8/8/8/4K2R w K - 0 1'); pg.click('#edFenGo'); time.sleep(.2)
    pg.click('#edAna'); time.sleep(.4)
    check('del editor al análisis', pg.evaluate("App.session instanceof AnalysisSession && App.game.fen()")=='4k3/8/8/8/8/8/8/4K2R w K - 0 1')
    pg.click('#bk'); time.sleep(.3)
    check('volver del análisis al editor con la captura', pg.evaluate("App.session instanceof EditorSession") and pg.is_visible('.shot img'))
    # Captura sin tablero
    CFG['read']={"tablero":False}
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.set_input_files('#shotin', SHOT)
    pg.wait_for_function("document.querySelector('#shotst').textContent.includes('No encontré un tablero')", timeout=20000)
    check('imagen sin tablero se explica', True)
    # Filas mal formadas: se marcan como dudosas
    CFG['read']={"tablero":True,"abajo":"w","filas":["rnbqkbnr","pppppppp","8","8","4P3","8","PPPP1PPP","RNBQKBN"],"mueven":"b","ultima":None,"dudas":[]}
    pg.set_input_files('#shotin', SHOT); pg.wait_for_function("App.session instanceof EditorSession", timeout=20000)
    check('fila incompleta queda marcada como dudosa', pg.evaluate("Board.marks.h1")=='hint' and pg.evaluate("App.session.turn")=='b')

    # --- PGN ---
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.fill('#fenin', games[1]['pgn']); pg.click('#fenAna'); time.sleep(.5)
    n_main=pg.evaluate("App.session.main.length")
    check('PGN: abre al final de la partida', n_main==13 and pg.evaluate("App.session.ply")==13)
    check('PGN: título con los jugadores', 'fertest vs rival2' in pg.inner_text('#side h2'))
    pg.click('#controls button:has-text("Inicio")'); time.sleep(.2); pg.click('#controls button:has-text("Siguiente")'); time.sleep(.2)
    check('PGN: navegar la partida', pg.evaluate("App.session.ply")==1 and pg.inner_text('#maMine')=='¿Qué tal e4?')
    pg.click('.moves [data-ply="5"]'); time.sleep(.2)
    check('PGN: ir a una jugada de la lista', pg.evaluate("App.session.ply")==5)
    pg.click('.sq[data-sq="h7"]'); pg.click('.sq[data-sq="h6"]'); time.sleep(.2)
    check('jugada distinta abre una variante', pg.evaluate("App.session.vars.length")==1 and pg.query_selector('#controls button:has-text("Volver a la partida")') is not None and 'Variante' in pg.inner_text('#ml'))
    pg.click('#controls button:has-text("Volver a la partida")'); time.sleep(.2)
    check('volver a la partida', pg.evaluate("App.session.vars.length")==0 and pg.evaluate("App.session.ply")==5)
    pg.click('.sq[data-sq="g8"]'); pg.click('.sq[data-sq="f6"]'); time.sleep(.2)
    check('si la jugada coincide con la partida, sigue en ella', pg.evaluate("App.session.ply")==6 or pg.evaluate("App.session.vars.length")==1)

    # Archivo PGN con dos partidas (lo que descarga Compartir): se usa la primera
    import tempfile
    pf=os.path.join(tempfile.mkdtemp(), 'partida.pgn'); open(pf,'w').write('\ufeff'+games[1]['pgn']+'\n\n'+games[2]['pgn']+'\n')
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.set_input_files('#pgnin', pf); pg.wait_for_function("document.querySelector('#fenerr').textContent.includes('Cargué')", timeout=5000)
    check('subir PGN: carga la primera partida del archivo', 'partida.pgn (13 jugadas)' in pg.inner_text('#fenerr') and 'rival3' not in pg.input_value('#fenin'))
    pg.click('#fenAna'); time.sleep(.5)
    check('subir PGN: se analiza la partida', pg.evaluate("App.session instanceof AnalysisSession && App.session.main.length")==13)
    bad=os.path.join(tempfile.mkdtemp(), 'nada.txt'); open(bad,'w').write('hola')
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.set_input_files('#pgnin', bad); time.sleep(.4)
    check('subir un archivo sin partida se explica', 'no tiene una partida' in pg.inner_text('#fenerr'))

    # --- Link de Chess.com ---
    pg.evaluate("S.username=''; S.games=[]; App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.fill('#fenin', 'Mira esta partida https://www.chess.com/game/live/1001?move=3'); pg.click('#fenAna'); time.sleep(.5)
    check('link sin usuario: pide el usuario de un jugador', pg.is_visible('#linkUser') and 'escribe el usuario' in pg.inner_text('#fenerr'))
    pg.fill('#linkUser','fertest'); pg.click('#fenAna')
    pg.wait_for_function("App.session instanceof AnalysisSession", timeout=20000); time.sleep(.3)
    check('link encontrado en el archivo del jugador', pg.evaluate("App.session.main.length")==13 and 'fertest vs rival2' in pg.inner_text('#side h2'))
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.fill('#fenin', 'https://www.chess.com/game/live/999999'); pg.fill('#linkUser','fertest') if pg.is_visible('#linkUser') else None
    pg.evaluate("document.querySelector('#linkUserBox').hidden=false"); pg.fill('#linkUser','fertest'); pg.click('#fenAna')
    pg.wait_for_function("document.querySelector('#fenerr').textContent.includes('No la encontré')", timeout=20000)
    check('link que no está: se explica', True)
    pg.evaluate("loadChessCom('fertest', 1, ()=>{}).then(()=>{ S.username='fertest'; })"); time.sleep(1)
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.fill('#fenin', 'chess.com/game/live/1002'); pg.click('#fenAna'); time.sleep(.5)
    check('link de una partida ya cargada se abre directo', pg.evaluate("App.session instanceof AnalysisSession && App.session.main.length")==14)
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    pg.fill('#fenin', 'https://www.chess.com/analysis?fen=' + FEN_IT.replace(' ','%20')); pg.click('#fenAna'); time.sleep(.5)
    check('link de análisis con FEN', pg.evaluate("App.game.fen()")==FEN_IT)
    # Partidas recientes
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.3)
    check('partidas recientes listadas', len(pg.query_selector_all('[data-rg]'))==3)
    pg.click('[data-rg]'); time.sleep(.4)
    check('partida reciente abre el análisis', pg.evaluate("App.session instanceof AnalysisSession && App.session.main.length > 0"))

    # --- Revisión de partida y pestaña Maestro ---
    pg.evaluate("App.setSession(new ReviewSession(S.games[0], 4))"); time.sleep(.3)
    pg.click('#controls button:has-text("Maestro")'); time.sleep(.4)
    check('desde la revisión: análisis en la misma jugada', pg.evaluate("App.session instanceof AnalysisSession && App.session.ply")==4)
    pg.click('#bk'); time.sleep(.3)
    check('y regresa a la revisión', pg.evaluate("App.session instanceof ReviewSession"))
    pg.click('.tab[data-tab=coach]'); time.sleep(.3)
    check('ajuste del modelo de análisis con Opus por defecto', pg.evaluate("document.querySelector('#aimodel2').value")=='claude-opus-5-5')
    pg.select_option('#aimodel2','claude-sonnet-5-5')
    check('el modelo de análisis se guarda', pg.evaluate("S.settings.claude.anaModel")=='claude-sonnet-5-5' and pg.evaluate("S.settings.claude.model")=='claude-haiku-5-5')
    pg.click('#cana'); time.sleep(.3)
    check('la pestaña Maestro lleva a Importar', pg.evaluate("App.tab")=='positions' and pg.is_visible('#fenin'))
    check('la clave no queda en el respaldo', pg.evaluate("!stripForSync(JSON.parse(JSON.stringify(S))).settings.claude"))
    check('sin errores de página', not errs)
    b.close()

    # --- Móvil ---
    W=390; AUDIT=open('mobile.py').read().split('AUDIT = r"""')[1].split('"""')[0]
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':W,'height':844}, device_scale_factor=2, is_mobile=True, has_touch=True); ctx.route('**/*',handle4); pg=ctx.new_page()
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000); ai_on(pg)
    def audit(name):
        a=json.loads(pg.evaluate(AUDIT)); pg.screenshot(path=OUT+f'maestro{W}_{name}.png', full_page=True); print(' ', name, a)
        # La franja de pestañas se desplaza de lado a propósito; las casillas de verificación no hacen zoom en iOS
        check(f'móvil {name}: sin desborde horizontal', a['overflowX']<=0 and not [w for w in a['wide'] if not w.startswith('tab')])
        zoom=pg.evaluate("[...document.querySelectorAll('input:not([type=checkbox]):not([type=file]), select, textarea')].filter(e=>e.getBoundingClientRect().width>0 && parseFloat(getComputedStyle(e).fontSize)<16).map(e=>e.id||e.tagName)")
        check(f'móvil {name}: campos de texto sin zoom en iOS', not zoom)
        return a
    pg.evaluate("App.posTab='importar'; switchTab('positions')"); time.sleep(.4); audit('importar')
    CFG['read']={"tablero":True,"abajo":"w","filas":view(FEN_IT,'w'),"mueven":"b","ultima":None,"dudas":[[2,3]]}
    pg.set_input_files('#shotin', SHOT); pg.wait_for_function("App.session instanceof EditorSession", timeout=20000); time.sleep(.4)
    a=audit('editor')
    pal=pg.evaluate("[...document.querySelectorAll('.palette button')].map(b=>Math.round(b.getBoundingClientRect().height))")
    check('móvil: piezas de la paleta de al menos 40 px', min(pal)>=40)
    pg.tap('#edAna'); time.sleep(.5); pg.wait_for_function("App.session.cache[App.game.fen()]", timeout=20000)
    pg.tap('#maPos'); wait_msg(pg, 60000); time.sleep(.3); audit('analisis')
    b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
