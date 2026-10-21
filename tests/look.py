exec(open('run.py').read().split("logs=[]")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':900}); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.click('#lookBtn'); time.sleep(.3); pg.screenshot(path=OUT+'look0.png')
    combos=[('papel','libro','madera','merida'),('pizarra','moderna','glaciar','celtic'),('cuero','tecnica','nogal','chessnut'),('carbon','clasica','club','mpchess')]
    for i,(t,f,bd,pc) in enumerate(combos):
        for k,v in (('theme',t),('font',f),('board',bd),('pieces',pc)):
            pg.click(f'.opt[data-k={k}][data-v={v}]')
        time.sleep(.2); pg.screenshot(path=OUT+f'look{i+1}.png')
        pg.keyboard.press('Escape'); time.sleep(.2)
        pg.click('#go'); time.sleep(.3)
        pg.evaluate("App.session.onUserMove({from:'e2',to:'e4'})"); pg.wait_for_function("App.game.history().length>=2",timeout=10000)
        pg.screenshot(path=OUT+f'lookg{i+1}.png')
        pg.click('.tab[data-tab=ladder]'); pg.click('#lookBtn'); time.sleep(.2)
    print(pg.evaluate("JSON.stringify(S.settings.look)"))
    pg.reload(); pg.wait_for_function("Engine.ready",timeout=60000)
    print('after reload', pg.evaluate("[document.documentElement.dataset.theme,document.documentElement.dataset.pieces]"))
    m=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); m.route('**/*',handle); mp=m.new_page(); mp.goto(APP); time.sleep(1.5); mp.click('#lookBtn'); time.sleep(.3); mp.screenshot(path=OUT+'look_mobile.png')
    b.close()
