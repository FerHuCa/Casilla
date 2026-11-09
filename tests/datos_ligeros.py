# Datos guardados más ligeros sin cambiar la forma de S: PGN de Chess.com sin relojes ni cabeceras que no se usan,
# análisis de partidas que ya no están sin las líneas del motor, lo mismo al combinar con otro dispositivo, y la huella
# de sincronización (syncKey) igual para un estado y su copia por JSON.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'run.py')).read().split('logs=[]')[0])
F=0
def check(name, cond, extra=''):
    global F; F+=not cond; print('OK ' if cond else 'FALLA ', name, extra)
FAT='[Event "Live Chess"]\\n[Site "Chess.com"]\\n[White "rival1"]\\n[Black "fertest"]\\n[Result "1-0"]\\n[ECOUrl "https://www.chess.com/openings/Italian-Game"]\\n[Link "https://www.chess.com/game/live/1"]\\n\\n1. e4 {[%clk 0:04:59.1]} 1... e5 {[%clk 0:04:58]} 2. Bc4 {[%clk 0:04:50]} 2... Nc6 {[%clk 0:04:40]} 3. Qh5 {[%clk 0:04:30]} 3... Nf6 {[%clk 0:04:20]} 4. Qxf7# {[%clk 0:04:10]} 1-0'
SEED="""()=>{
  const fat='%s';
  const mk=id=>({v:1, acc:70, deep:true, w:[20,30,10,-40], tags:{1:'??'}, cnt:{inacc:0,mistake:0,blunder:1}, best:['e2e4',null,'g1f3',null], pv:[['e2e4','e7e5'],[],['g1f3'],[]],
    mistakes:[{id:id+'#2', gid:id, ply:2, fen:'x', played:'e5', best:'c7c5', bestSan:'c5', drop:31, before:0, cat:'Error posicional', phase:'Apertura', date:1790000000, opp:'rival1', color:'b', exp:'explicación guardada', cx:{hint:'pista', text:'texto', model:'m', at:5}}]});
  const st=defaults(); st.username='fertest';
  // de la más reciente a la más vieja, como las guarda la app
  st.games=[{id:'https://www.chess.com/game/live/2', pgn:fat, white:'rival1', black:'fertest', wr:1400, br:1450, wres:'win', bres:'checkmated', tc:'blitz', end:1790000001, eco:'https://www.chess.com/openings/Italian-Game'},
            {id:'https://www.chess.com/game/live/1', pgn:fat, white:'rival1', black:'fertest', wr:1400, br:1450, wres:'win', bres:'checkmated', tc:'blitz', end:1790000000, eco:''}];
  st.analyses={'https://www.chess.com/game/live/1':mk('https://www.chess.com/game/live/1'), 'https://www.chess.com/game/live/999':mk('https://www.chess.com/game/live/999'), 'coach:1790000000000':{v:1, src:'coach', acc:80, w:[], tags:{}, cnt:{inacc:0,mistake:0,blunder:0}, mistakes:[]}};
  st.srs={'https://www.chess.com/game/live/999#2':{last:1, n:1}};
  localStorage.setItem('casilla.v1', JSON.stringify(st)); return fat.length }"""%FAT
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':900}); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: check('PAGEERROR', False, str(e)))
    pg.goto(APP); pg.wait_for_function("typeof S!=='undefined'")
    n=pg.evaluate(SEED); pg.reload(); pg.wait_for_function("typeof S!=='undefined' && S.games.length===2")
    g=pg.evaluate("S.games.map(g=>g.pgn)")
    check('al abrir, el PGN queda sin relojes ni cabeceras de más', all('{' not in x and '[Event' not in x and '[Link' not in x for x in g), '%d -> %d caracteres'%(n, len(g[1])))
    check('conserva Result y, sin eco, ECOUrl', '[Result "1-0"]' in g[0] and 'ECOUrl' in g[1] and 'ECOUrl' not in g[0])
    check('las jugadas son las mismas', pg.evaluate("S.games.every(g=>buildGame(g.pgn).moves.map(m=>m.san).join(' ')==='e4 e5 Bc4 Nc6 Qh5 Nf6 Qxf7#')"))
    check('la apertura se sigue leyendo', pg.evaluate("S.games.map(openingName).join('|')")=='Italian Game|Italian Game')
    check('quedó guardado en localStorage', pg.evaluate("!JSON.parse(localStorage.getItem('casilla.v1')).games.some(g=>g.pgn.includes('clk'))"))
    a=pg.evaluate("[S.analyses['https://www.chess.com/game/live/1'], S.analyses['https://www.chess.com/game/live/999'], S.analyses['coach:1790000000000']]")
    check('el análisis de una partida que sigue en la lista no cambia', a[0]['w']==[20,30,10,-40] and len(a[0]['best'])==4 and len(a[0]['pv'])==4)
    check('el de una partida que ya no está pierde solo las líneas del motor', a[1]['w']==[] and 'best' not in a[1] and 'pv' not in a[1])
    m=a[1]['mistakes'][0]
    check('y conserva errores, marcas, explicación y comentario con IA', len(a[1]['mistakes'])==1 and m['exp']=='explicación guardada' and m['cx']['text']=='texto' and a[1]['tags']=={'1':'??'} and a[1]['acc']==70 and a[1]['deep']==True)
    check('los análisis del maestro (coach:) no se tocan', a[2]['src']=='coach' and a[2]['acc']==80)
    check('Mis errores sigue contando los dos', pg.evaluate("errorProfile().total")==2)
    check('el repaso espaciado no se toca', pg.evaluate("Object.keys(S.srs).length")==1)
    check('abrir de nuevo no cambia nada (idempotente)', pg.evaluate("pruneState(S)")==False)
    # Combinar con un dispositivo que todavía tiene los datos pesados
    r=pg.evaluate("""()=>{ const fat='%s'; const R=JSON.parse(JSON.stringify(S));
      R.games=R.games.map(g=>Object.assign({}, g, {pgn:fat})); R.analyses['https://www.chess.com/game/live/999'].best=['e2e4']; R.analyses['https://www.chess.com/game/live/999'].pv=[['e2e4']]; R.analyses['https://www.chess.com/game/live/999'].w=[1,2];
      const out=mergeState(S, R); return {fat:out.games.some(g=>isFatPGN(g.pgn)), orphan:out.analyses['https://www.chess.com/game/live/999'], same:syncKey(out)===syncKey(S), remoteDiff:syncKey(R)!==syncKey(out)} }"""%FAT)
    check('al combinar con datos pesados el resultado queda ligero', r['fat']==False and r['orphan']['w']==[] and 'best' not in r['orphan'])
    check('y es igual al estado local (no hay nada que aplicar) pero distinto al remoto (se sube la versión ligera)', r['same'] and r['remoteDiff'])
    # Huella de sincronización
    k=pg.evaluate("""()=>{ const c=JSON.parse(JSON.stringify(S)); const viejo=st=>{ const x=JSON.parse(JSON.stringify(st)); if(x.settings){ delete x.settings.sync; delete x.settings.claude; } delete x.meta; return canon(x) };
      S.settings.sync={token:'t'}; S.settings.claude={key:'k'}; const withSecrets=syncKey(S); delete S.settings.sync; delete S.settings.claude;
      const hole={a:[1,undefined,3]};
      return {clone:syncKey(S)===syncKey(c), old:syncKey(S)===viejo(S), secrets:withSecrets===syncKey(S), noSecret:!withSecrets.includes('"token"')&&!withSecrets.includes('"key"'), hole:canon(hole)===canon(JSON.parse(JSON.stringify(hole)))} }""")
    check('syncKey: igual para el estado y su copia por JSON, e igual a la huella anterior', k['clone'] and k['old'])
    check('syncKey: ignora la clave de IA y el token, y no los incluye', k['secrets'] and k['noSecret'])
    check('canon: un hueco en un arreglo cuenta como null', k['hole'])
    # Al cargar de Chess.com se guarda ya ligero
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_function("typeof S!=='undefined'")
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=15000)
    check('las partidas nuevas de Chess.com se guardan ligeras', pg.evaluate("!S.games.some(g=>isFatPGN(g.pgn)) && S.games.every(g=>buildGame(g.pgn).moves.length>=7)"))
    b.close()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
