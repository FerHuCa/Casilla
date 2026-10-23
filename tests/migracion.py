exec(open('run.py').read().split("logs=[]")[0])
F=0
D={'theme':'carbon','font':'clasica','board':'piedra','pieces':'cburnett','style':'plano'}
def o(**k): x=dict(D); x.update(k); return x
CASES=[
 ('default de hoy (ejemplo de la spec)', D, ('clasico','oscuro')),
 ('papel + nogal + merida (ejemplo)', o(theme='papel',board='nogal',pieces='merida'), ('madera',None)),
 ('pizarra + piedra + cburnett (ejemplo)', o(theme='pizarra'), ('clasico','oscuro')),
 ('papel exacto = Clásico claro', o(theme='papel'), ('clasico','claro')),
 ('exacto Madera', o(theme='papel',font='libro',board='madera',pieces='merida'), ('madera',None)),
 ('exacto Relieve oscuro', o(board='madera',style='relieve'), ('relieve','oscuro')),
 ('exacto 8 bits (Todo en 8 bits)', {'theme':'arcade','font':'pixel','board':'arcade','pieces':'pixel','style':'bits'}, ('bits',None)),
 ('exacto Arcade', {'theme':'arcade','font':'tecnica','board':'arcade','pieces':'rhosgfx','style':'plano'}, ('arcade',None)),
 ('regla 2: solo fuente pixel', o(font='pixel'), ('bits',None)),
 ('regla 2: piezas pixel con tema arcade', o(theme='arcade',pieces='pixel'), ('bits',None)),
 ('regla 2: estilo bits gana a relieve y arcade', o(theme='arcade',style='bits'), ('bits',None)),
 ('regla 3: tablero arcade', o(board='arcade'), ('arcade',None)),
 ('regla 3: piezas Retro con relieve', o(pieces='rhosgfx',style='relieve'), ('arcade',None)),
 ('regla 4: relieve en papel = claro', o(theme='papel',board='club',style='relieve'), ('relieve','claro')),
 ('regla 4: relieve en cuero = oscuro', o(theme='cuero',style='relieve'), ('relieve','oscuro')),
 ('regla 5: tablero glaciar + piezas mpchess = Pizarra', o(board='glaciar',pieces='mpchess'), ('pizarra',None)),
 ('regla 5: tema cuero + celtic = Cuero', o(theme='cuero',pieces='celtic'), ('cuero',None)),
 ('regla 5: empate Madera/Cuero = Clásico', o(theme='carbon',board='madera',pieces='celtic',font='moderna'), ('clasico','oscuro')),
 ('regla 5: empate con papel = Clásico claro', o(theme='papel',board='nogal',pieces='mpchess',font='moderna'), ('clasico','claro')),
 ('valores inválidos = defaults', {'theme':'xx','board':'yy'}, ('clasico','oscuro')),
]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(APP); pg.wait_for_function("typeof migrateLook==='function'")
    for name,old,exp in CASES:
        if old is None: continue
        r=pg.evaluate("o=>migrateLook(o)", old)
        # El estilo sale de la regla de la sección 11; tablero y piezas quedan como personalización solo si difieren del estilo
        pb=pg.evaluate("([id,o])=>{const p=presetById(id), l=Object.assign({},LOOK_DEFAULT,o); const c={}; for(const k of ['board','pieces']) if(l[k]!==p[k] && lookOpt(k,l[k])) c[k]=l[k]; return c;}", [exp[0], old])
        ok=r['preset']==exp[0] and (exp[1] is None or r['mode']==exp[1]) and {k:v for k,v in r.items() if k not in ('preset','mode')}==pb
        F+=not ok; print('OK   ' if ok else 'FALLA ', name, '->', r)
    # migración al cargar desde casilla.v1 y reemplazo del formato viejo al guardar
    pg.evaluate("""()=>{ const st=JSON.parse(localStorage.getItem('casilla.v1')||'{}'); st.settings=st.settings||{}; st.settings.look={theme:'papel',font:'clasica',board:'nogal',pieces:'merida',style:'plano'}; localStorage.setItem('casilla.v1',JSON.stringify(st)); }""")
    pg.reload(); pg.wait_for_function("typeof S!=='undefined' && S.settings")
    time.sleep(.5)
    r=pg.evaluate("[document.documentElement.dataset.theme, document.documentElement.dataset.board, JSON.stringify(S.settings.look)]")
    ok=r==['papel','nogal','{"preset":"madera","mode":"oscuro","board":"nogal"}']; F+=not ok; print('OK   ' if ok else 'FALLA ','migra al cargar (conserva el tablero Nogal como personalización)', r)
    pg.evaluate("save()"); saved=pg.evaluate("JSON.parse(localStorage.getItem('casilla.v1')).settings.look")
    ok=saved=={'preset':'madera','mode':'oscuro','board':'nogal'}; F+=not ok; print('OK   ' if ok else 'FALLA ','el formato viejo se reemplaza al guardar', saved)
    # respaldo importado pasa por la misma función
    import tempfile, json as J
    fn=tempfile.mktemp(suffix='.json'); open(fn,'w').write(J.dumps({'settings':{'look':{'theme':'arcade','font':'pixel','board':'arcade','pieces':'pixel','style':'bits'}}}))
    pg.evaluate("switchTab('progress')"); time.sleep(.5)
    pg.set_input_files('#impf', fn); time.sleep(.6)
    r=pg.evaluate("[S.settings.look.preset, document.documentElement.dataset.style]")
    ok=r==['bits','bits']; F+=not ok; print('OK   ' if ok else 'FALLA ','respaldo importado se migra', r)
    b.close()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
