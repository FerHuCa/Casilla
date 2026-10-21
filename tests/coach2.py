exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':900}); ctx.route('**/*',handle2); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e)); pg.on('console',lambda m: print('C',m.text) if m.type in ('error','warning') and 'ERR_FAILED' not in m.text else None)
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    # comentario sin ayudas: el error se guarda para el final
    pg.evaluate("""App.setSession(new PlaySession({fen:'r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 3 3', userColor:'b', tier:TIERS[3], tierIdx:3, helps:false, clock:'300+0', coach:{mode:'comment'}, title:'Prueba comentario'}))""")
    time.sleep(1.2)
    pg.evaluate("App.session.onUserMove({from:'g8',to:'f6'})"); time.sleep(4)
    print(feed(pg)); print('over', pg.evaluate("[App.session.over, App.session.result&&App.session.result.why]"))
    print('saved coach mistakes', pg.evaluate("Object.keys(S.analyses).filter(k=>k.startsWith('coach:')).map(k=>S.analyses[k].mistakes.length)"))
    pg.screenshot(path=OUT+'c6_comment.png')
    pg.click('.tab[data-tab=coach]'); pg.check('#aion'); pg.fill('#aikey','sk-ant-test'); pg.dispatch_event('#aikey','change'); pg.click('#aitest'); time.sleep(3)
    print('aitest:', pg.inner_text('#aist'), len(CL), [c[0].get(':method') or 'x' for c in CL])
    # puzzle de error guardado del maestro, sin enlace a chess.com
    pg.click('.tab[data-tab=puzzles]'); pg.click('[data-seg=src] button[data-v=mine]'); time.sleep(1.5)
    print('pz', pg.evaluate("[App.session.p && App.session.p.title, !!document.querySelector('#pzinfo a')]"))
    b.close()
