exec(open('run.py').read().split("logs=[]")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':1000}); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e)); pg.on('console',lambda m: print('C',m.text) if m.type=='error' and 'ERR_FAILED' not in m.text else None)
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.4)
    pg.select_option('#bmt','250'); pg.click('#bgo'); pg.wait_for_function("Object.keys(S.analyses).length===3 && !Analyzer.running",timeout=120000)
    pg.click('.tab[data-tab=positions]'); pg.click('[data-seg=pt] button[data-v=mias]'); time.sleep(.3)
    for i in range(2):
        pg.click(f'[data-mz] >> nth={i}'); time.sleep(.5)
        if i==0:
            pg.click('text=Ver solución')
        else:
            sol=pg.evaluate("App.session.p.solution[0]"); pg.evaluate(f"App.session.onUserMove(uciObj('{sol}'))")
        pg.wait_for_function("App.session.p.exp",timeout=20000); time.sleep(.3)
        print(pg.inner_text('.explain')); print('-----')
        pg.screenshot(path=OUT+f'exp{i}.png')
        pg.click('#seeMine'); time.sleep(5); print('line',pg.evaluate("App.game.history().join(' ')")); pg.click('#seeBack')
        pg.click('.tab[data-tab=positions]'); pg.click('[data-seg=pt] button[data-v=mias]'); time.sleep(.3)
    print('persisted', pg.evaluate("errorProfile().all.filter(m=>m.exp).length"))
    b.close()
