# Migración de la apariencia guardada a {preset, mode, board?, pieces?}.
# - {preset, mode} no cambia y se ve exactamente igual que antes (tabla fija con lo que mostraba cada estilo).
# - {preset, mode, board, pieces}: se conserva lo que difiere del estilo; ids inexistentes o iguales al estilo se quitan.
# - Formato viejo {theme, font, board, pieces, style}: el estilo sale de la regla de la sección 11 del spec B y,
#   si el tablero o las piezas no coinciden con ese estilo, quedan como personalización (se sigue viendo igual).
# - Las tres vías de entrada: localStorage al abrir, respaldo importado y datos del gist.
import os, tempfile, json as J
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'run.py')).read().split("logs=[]")[0])
F=0
def ck(ok,msg,extra=''):
    global F; F+=not ok; print('OK   ' if ok else 'FALLA ', msg, extra)
# Lo que mostraba cada estilo antes de este cambio: [theme, font, board, pieces, style]
SHOWN={
 ('clasico','oscuro'):['carbon','clasica','piedra','cburnett','plano'], ('clasico','claro'):['papel','clasica','piedra','cburnett','plano'],
 ('madera',None):['papel','libro','madera','merida','plano'], ('pizarra',None):['pizarra','moderna','glaciar','mpchess','plano'],
 ('cuero',None):['cuero','libro','nogal','celtic','plano'], ('club',None):['papel','tecnica','club','chessnut','plano'],
 ('relieve','oscuro'):['carbon','clasica','madera','cburnett','relieve'], ('relieve','claro'):['papel','clasica','madera','cburnett','relieve'],
 ('bits',None):['arcade','pixel','arcade','pixel','bits'], ('arcade',None):['arcade','tecnica','arcade','rhosgfx','plano'],
}
def shown(preset, mode, **over):
    v=list(SHOWN.get((preset,mode)) or SHOWN[(preset,None)]); idx={'board':2,'pieces':3}
    for k,x in over.items(): v[idx[k]]=x
    return v
D={'theme':'carbon','font':'clasica','board':'piedra','pieces':'cburnett','style':'plano'}
def o(**k): x=dict(D); x.update(k); return x
# (nombre, guardado, preferencia esperada, lo que se ve [theme, font, board, pieces, style])
CASES=[]
for (pr,m) in SHOWN:
    raw={'preset':pr,'mode':m or 'oscuro'}
    CASES.append(('{preset,mode} %s %s sin cambio'%(pr,m or ''), raw, dict(raw), shown(pr,m)))
CASES+=[
 ('{preset,mode} de estilo sin modo guardado como claro', {'preset':'cuero','mode':'claro'}, {'preset':'cuero','mode':'claro'}, shown('cuero',None)),
 ('nuevo: tablero y piezas personalizados', {'preset':'clasico','mode':'oscuro','board':'nogal','pieces':'spatial'}, {'preset':'clasico','mode':'oscuro','board':'nogal','pieces':'spatial'}, shown('clasico','oscuro',board='nogal',pieces='spatial')),
 ('nuevo: textura y Letras en Madera', {'preset':'madera','mode':'oscuro','board':'veteado','pieces':'letter'}, {'preset':'madera','mode':'oscuro','board':'veteado','pieces':'letter'}, shown('madera',None,board='veteado',pieces='letter')),
 ('nuevo: solo piezas', {'preset':'relieve','mode':'claro','pieces':'firi'}, {'preset':'relieve','mode':'claro','pieces':'firi'}, shown('relieve','claro',pieces='firi')),
 ('nuevo: igual al estilo se quita', {'preset':'madera','mode':'oscuro','board':'madera','pieces':'merida'}, {'preset':'madera','mode':'oscuro'}, shown('madera',None)),
 ('nuevo: ids inexistentes se ignoran', {'preset':'cuero','mode':'oscuro','board':'lunar','pieces':'horsey'}, {'preset':'cuero','mode':'oscuro'}, shown('cuero',None)),
 ('nuevo: uno válido y otro inexistente', {'preset':'pizarra','mode':'oscuro','board':'contraste','pieces':'alpha'}, {'preset':'pizarra','mode':'oscuro','board':'contraste'}, shown('pizarra',None,board='contraste')),
 ('nuevo: tipos raros se ignoran', {'preset':'club','mode':'oscuro','board':7,'pieces':None,'x':1}, {'preset':'club','mode':'oscuro'}, shown('club',None)),
 ('nuevo: estilo inexistente = Clásico sin personalización', {'preset':'neon','mode':'claro','board':'arce'}, {'preset':'clasico','mode':'oscuro'}, shown('clasico','oscuro')),
 ('nuevo: modo inválido = oscuro', {'preset':'clasico','mode':'sepia','pieces':'shapes'}, {'preset':'clasico','mode':'oscuro','pieces':'shapes'}, shown('clasico','oscuro',pieces='shapes')),
 ('viejo: default', D, {'preset':'clasico','mode':'oscuro'}, shown('clasico','oscuro')),
 ('viejo: exacto Madera', o(theme='papel',font='libro',board='madera',pieces='merida'), {'preset':'madera','mode':'oscuro'}, shown('madera',None)),
 ('viejo: papel + nogal + merida = Madera con tablero Nogal', o(theme='papel',board='nogal',pieces='merida'), {'preset':'madera','mode':'oscuro','board':'nogal'}, shown('madera',None,board='nogal')),
 ('viejo: pizarra con piedra y cburnett = Clásico', o(theme='pizarra'), {'preset':'clasico','mode':'oscuro'}, shown('clasico','oscuro')),
 ('viejo: solo fuente pixel = 8 bits con tablero y piezas de antes', o(font='pixel'), {'preset':'bits','mode':'oscuro','board':'piedra','pieces':'cburnett'}, shown('bits',None,board='piedra',pieces='cburnett')),
 ('viejo: tablero arcade = Arcade con cburnett', o(board='arcade'), {'preset':'arcade','mode':'oscuro','pieces':'cburnett'}, shown('arcade',None,pieces='cburnett')),
 ('viejo: relieve en papel con club', o(theme='papel',board='club',style='relieve'), {'preset':'relieve','mode':'claro','board':'club'}, shown('relieve','claro',board='club')),
 ('viejo: empate Madera/Cuero = Clásico con madera y celtic', o(board='madera',pieces='celtic',font='moderna'), {'preset':'clasico','mode':'oscuro','board':'madera','pieces':'celtic'}, shown('clasico','oscuro',board='madera',pieces='celtic')),
 ('viejo: glaciar + mpchess = Pizarra', o(board='glaciar',pieces='mpchess'), {'preset':'pizarra','mode':'oscuro'}, shown('pizarra',None)),
 ('viejo: valores inválidos = Clásico', {'theme':'xx','board':'yy','pieces':'zz'}, {'preset':'clasico','mode':'oscuro'}, shown('clasico','oscuro')),
 ('viejo: solo theme', {'theme':'papel'}, {'preset':'clasico','mode':'claro'}, shown('clasico','claro')),
]
ATTRS="['theme','font','board','pieces','style'].map(k=>document.documentElement.dataset[k])"
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: ck(False,'PAGEERROR',str(e)))
    pg.goto(APP); pg.wait_for_function("typeof migrateLook==='function' && typeof S!=='undefined'")
    for name,raw,exp,see in CASES:
        r=pg.evaluate("raw=>{ S.settings.look=JSON.parse(JSON.stringify(raw)); migrateStoredLook(); applyLook(); return [S.settings.look, %s]; }"%ATTRS, raw)
        ck(r[0]==exp and r[1]==see, name, '-> %s %s'%(J.dumps(r[0]), r[1]))
    # Vía 1: localStorage al abrir (formato viejo con personalización y formato nuevo)
    def boot_with(look):
        pg.evaluate("l=>{ const st=JSON.parse(localStorage.getItem('casilla.v1')||'{}'); st.settings=st.settings||{}; st.settings.look=l; localStorage.setItem('casilla.v1',JSON.stringify(st)); }", look)
        pg.reload(); pg.wait_for_function("typeof S!=='undefined' && S.settings && document.documentElement.dataset.board")
        return pg.evaluate("[S.settings.look, %s]"%ATTRS)
    r=boot_with(o(theme='cuero',font='libro',board='glaciar',pieces='celtic'))
    ck(r==[{'preset':'cuero','mode':'oscuro','board':'glaciar'}, shown('cuero',None,board='glaciar')], 'al abrir: viejo Cuero con glaciar conserva el tablero', r)
    pg.evaluate("save()"); saved=pg.evaluate("JSON.parse(localStorage.getItem('casilla.v1')).settings.look")
    ck(saved=={'preset':'cuero','mode':'oscuro','board':'glaciar'}, 'al guardar se escribe el formato nuevo', saved)
    r=boot_with({'preset':'club','mode':'oscuro','board':'arce','pieces':'pirouetti'})
    ck(r==[{'preset':'club','mode':'oscuro','board':'arce','pieces':'pirouetti'}, shown('club',None,board='arce',pieces='pirouetti')], 'al abrir: formato nuevo se conserva', r)
    r=boot_with({'preset':'madera','mode':'oscuro'})
    ck(r==[{'preset':'madera','mode':'oscuro'}, shown('madera',None)], 'al abrir: {preset, mode} sin cambios', r)
    # Vía 2: respaldo importado
    fn=tempfile.mktemp(suffix='.json'); open(fn,'w').write(J.dumps({'settings':{'look':o(theme='papel',board='nogal',pieces='zz')}}))
    pg.evaluate("switchTab('progress')"); pg.wait_for_selector('#impf',state='attached')
    pg.set_input_files('#impf', fn); pg.wait_for_function("S.settings.look && S.settings.look.board==='nogal'",timeout=5000)
    r=pg.evaluate("[S.settings.look, %s]"%ATTRS)
    ck(r==[{'preset':'clasico','mode':'claro','board':'nogal'}, shown('clasico','claro',board='nogal')], 'respaldo viejo: pieza inexistente en el formato viejo se ignora, tablero se conserva', r)
    fn2=tempfile.mktemp(suffix='.json'); open(fn2,'w').write(J.dumps({'settings':{'look':{'preset':'pizarra','mode':'oscuro','pieces':'fantasy','board':'nada'}}}))
    pg.set_input_files('#impf', fn2); pg.wait_for_function("S.settings.look && S.settings.look.preset==='pizarra'",timeout=5000)
    r=pg.evaluate("[S.settings.look, %s]"%ATTRS)
    ck(r==[{'preset':'pizarra','mode':'oscuro','pieces':'fantasy'}, shown('pizarra',None,pieces='fantasy')], 'respaldo nuevo: se conserva lo válido', r)
    # Vía 3: datos que llegan del gist
    for raw,exp,see,name in [
        (o(theme='papel',font='tecnica',board='club',pieces='merida'), {'preset':'club','mode':'oscuro','pieces':'merida'}, shown('club',None,pieces='merida'), 'gist con formato viejo'),
        ({'preset':'bits','mode':'oscuro','board':'veteado'}, {'preset':'bits','mode':'oscuro','board':'veteado'}, shown('bits',None,board='veteado'), 'gist con formato nuevo'),
        ({'preset':'arcade','mode':'oscuro'}, {'preset':'arcade','mode':'oscuro'}, shown('arcade',None), 'gist con {preset, mode}')]:
        r=pg.evaluate("raw=>{ S.settings.look=raw; onRemoteApplied(false); return [S.settings.look, %s]; }"%ATTRS, raw)
        ck(r==[exp,see], name, r)
    b.close()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
