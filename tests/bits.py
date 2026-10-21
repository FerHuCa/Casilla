exec(open("coach.py").read().split("with sync_playwright() as p:")[0])
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h,tag) in [(1400,900,'d'),(390,844,'m')]:
        ctx=b.new_context(viewport={'width':w,'height':h}, device_scale_factor=1 if w>500 else 2, is_mobile=w<500, has_touch=w<500); ctx.route('**/*',handle2); pg=ctx.new_page()
        pg.on('pageerror',lambda e: print('PAGEERROR',e))
        pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
        for th,bd in [('arcade','arcade')]:
            pg.evaluate(f"S.settings.look={{theme:'{th}',font:'pixel',board:'{bd}',pieces:'pixel',style:'bits'}}; saveLocal(); applyLook(); switchTab('ladder')")
            time.sleep(.3); pg.screenshot(path=OUT+f'b8_{tag}_{th}_home.png')
        pg.click('[data-seg=clock] button[data-v="300+0"]'); pg.click('#go'); time.sleep(.5)
        pg.evaluate("App.session.onUserMove({from:'e2',to:'e4'})"); pg.wait_for_function("App.game.history().length>=2",timeout=10000); time.sleep(.5)
        pg.screenshot(path=OUT+f'b8_{tag}_game.png')
        pg.click('#lookBtn'); time.sleep(.3); pg.screenshot(path=OUT+f'b8_{tag}_look.png')
        ctx.close()
    b.close()
