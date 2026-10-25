exec(open('run.py').read().split("logs=[]")[0])
# Conexión con Claude: lo que se envía a la API y cómo se manejan sus respuestas (API simulada)
SENT=[]; MODE={'v':'ok'}
def handle3(route):
    if 'api.anthropic.com' in route.request.url:
        cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"*","Access-Control-Allow-Methods":"POST"}
        if route.request.method=='OPTIONS': return route.fulfill(status=204,headers=cors)
        body=json.loads(route.request.post_data); SENT.append((dict(route.request.headers), body))
        m=MODE['v']
        if m=='reject' and 'thinking' in body:
            return route.fulfill(status=400,headers=cors,content_type='application/json',body=json.dumps({"type":"error","error":{"type":"invalid_request_error","message":"thinking: this setting is not supported"}}))
        if m=='badkey':
            return route.fulfill(status=401,headers=cors,content_type='application/json',body=json.dumps({"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}}))
        if m=='onlythink':
            return route.fulfill(status=200,headers=cors,content_type='application/json',body=json.dumps({"content":[{"type":"thinking","thinking":"","signature":"x"}],"stop_reason":"max_tokens"}))
        return route.fulfill(status=200,headers=cors,content_type='application/json',body=json.dumps({"content":[{"type":"thinking","thinking":"","signature":"x"},{"type":"text","text":"listo"}],"stop_reason":"end_turn"}))
    return handle(route)
fails=[]
def check(name, cond):
    print(('OK   ' if cond else 'FALLA ') + name)
    if not cond: fails.append(name)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':950}); ctx.route('**/*',handle3); pg=ctx.new_page()
    pg.on('pageerror',lambda e: (print('PAGEERROR',e), fails.append('pageerror')))
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.click('.tab[data-tab=coach]'); time.sleep(.4)
    pg.check('#aion'); pg.fill('#aikey','sk-ant-prueba'); pg.select_option('#aimodel','claude-haiku-5-5')
    # El modelo de análisis igual al de comentarios: la prueba hace una sola llamada
    check('modelo de análisis por defecto: Opus 5.5', pg.evaluate("document.querySelector('#aimodel2').value") == 'claude-opus-5-5')
    pg.select_option('#aimodel2','claude-haiku-5-5')
    def test():
        n=len(SENT); pg.click('#aitest'); pg.wait_for_function("!document.querySelector('#aist').textContent.includes('Probando')",timeout=10000); time.sleep(.2)
        return pg.inner_text('#aist'), SENT[n:]
    out, calls = test(); h, body = calls[-1]
    print(' ', out)
    check('Haiku: conexión correcta y muestra la respuesta', 'Conexión correcta' in out and 'listo' in out)
    check('Haiku: sin pensamiento previo', body.get('thinking') == {'type':'disabled'})
    check('Haiku: encabezados de la API', h.get('x-api-key') == 'sk-ant-prueba' and h.get('anthropic-version') == '2023-06-01' and h.get('anthropic-dangerous-direct-browser-access') == 'true')
    check('modelo enviado', body.get('model') == 'claude-haiku-5-5')
    pg.select_option('#aimodel','claude-sonnet-5-5'); pg.select_option('#aimodel2','claude-sonnet-5-5'); out, calls = test(); h, body = calls[-1]
    check('Sonnet: conexión correcta', 'Conexión correcta con claude-sonnet-5-5' in out)
    check('Sonnet: between_tools', body.get('thinking') == {'type':'between_tools'})
    # Opus 5.5 para análisis: la prueba revisa los dos modelos; Opus no acepta apagar el pensamiento
    pg.select_option('#aimodel2','claude-opus-5-5'); out, calls = test()
    print(' ', out)
    ob = [c[1] for c in calls if c[1]['model'] == 'claude-opus-5-5']
    check('prueba ambos modelos si son distintos', len(calls) == 2 and 'claude-opus-5-5 también responde' in out)
    check('Opus: sin "thinking", esfuerzo bajo y espacio para pensar', ob and 'thinking' not in ob[0] and ob[0].get('output_config') == {'effort':'low'} and ob[0]['max_tokens'] >= 4000)
    pg.select_option('#aimodel2','claude-sonnet-5-5')
    MODE['v']='reject'; out, calls = test()
    print(' ', out, [c[1].get('thinking') for c in calls], [c[1]['max_tokens'] for c in calls])
    check('si rechaza el ajuste, reintenta sin él y con más espacio', len(calls) == 2 and 'thinking' not in calls[1][1] and calls[1][1]['max_tokens'] >= 2048 and 'Conexión correcta' in out)
    MODE['v']='onlythink'; out, _ = test()
    print(' ', out)
    check('respuesta sin texto se reporta como error', 'No se pudo conectar' in out and 'espacio' in out)
    MODE['v']='badkey'; out, _ = test()
    print(' ', out)
    check('clave inválida se reporta', 'No se pudo conectar: invalid x-api-key' in out)
    check('la clave no queda en el respaldo', pg.evaluate("(()=>{ const c = JSON.parse(JSON.stringify(S)); return !!(stripForSync(c).settings.claude); })()") is False)
    # Opción B: Claude, Anthropic y Stockfish solo aparecen en los ajustes de IA (y Stockfish en el crédito del pie)
    import re as _re
    for tab in ['ladder','puzzles','positions','games','progress','coach']:
        pg.click(f'.tab[data-tab={tab}]'); time.sleep(.4)
        txt=pg.evaluate("""(()=>{ const c = document.body.cloneNode(true); c.querySelectorAll('footer,script,style,#look').forEach(e=>e.remove());
          const side = c.querySelector('#side'); if(side){ const h = [...side.querySelectorAll('h3')].find(x => /Comentarios con Claude/.test(x.textContent)); if(h){ let n = h; while(n){ const nx = n.nextSibling; n.remove(); n = nx; } } }
          return c.innerText; })()""")
        hits=_re.findall(r'(?i)claude|anthropic|stockfish', txt)
        check(f'sin menciones de Claude/Anthropic/Stockfish fuera de los ajustes de IA ({tab})', not hits)
    check('crédito de Stockfish en el pie', 'Stockfish' in pg.inner_text('footer') and 'GPL' in pg.inner_text('footer'))
    b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
