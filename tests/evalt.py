exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':950}); ctx.route('**/*',handle2); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e)); pg.on('console',lambda m: print('C',m.text) if m.type in ('error','warning') and 'ERR_FAILED' not in m.text else None)
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.evaluate("S.settings.evalTime=250")
    # 1) partida de la escalera: el usuario juega la trampa Blackburne con blancas contra un rival que la conoce
    pg.evaluate("""App.setSession(new PlaySession({userColor:'w', tier:TIERS[7], tierIdx:7, ladder:false, helps:false, title:'Prueba evaluación', oppName:'Gran Maestro'}))""")
    for mv in ['e2e4','g1f3','f1c4','f3e5','e5f7','h1f1']:
        pg.wait_for_function("!App.session.thinking && !App.session.over", timeout=20000)
        ok = pg.evaluate(f"(()=>{{ const m=uciObj('{mv}'); const legal=App.game.moves({{verbose:true}}).some(x=>x.from===m.from&&x.to===m.to); if(legal) App.session.onUserMove(m); return legal; }})()")
        time.sleep(.3)
        if not ok:
            break
    pg.wait_for_function("!App.session.thinking", timeout=20000)
    print('hist', pg.evaluate("App.game.history().join(' ')"))
    pg.click('text=Abandonar'); time.sleep(.5)
    print('evbox', pg.inner_text('#evbox')[:120])
    pg.wait_for_function("Evaluator.job && Evaluator.job.done", timeout=120000); time.sleep(.3)
    print('evbox done', pg.inner_text('#evbox'))
    pg.click('#evgo'); time.sleep(.8)
    print('==== side ====\n' + pg.inner_text('#side')[:6000])
    pg.screenshot(path=OUT+'e1.png', full_page=False)
    pg.click('.moment >> nth=0 >> [data-mine]'); time.sleep(3); pg.screenshot(path=OUT+'e2.png')
    print('saved', pg.evaluate("Object.entries(S.analyses).map(([k,a])=>k.slice(0,6)+':'+a.mistakes.length+':'+!!a.deep)"))
    # 2) evaluación a fondo de una partida de Chess.com
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.4)
    pg.click('.game[data-id] >> nth=2'); time.sleep(.5); pg.click('#deep'); pg.wait_for_function("Evaluator.job && Evaluator.job.done", timeout=120000); time.sleep(.5)
    print('==== chess.com ====\n' + pg.inner_text('#side')[:3000])
    pg.screenshot(path=OUT+'e3.png')
    b.close()
