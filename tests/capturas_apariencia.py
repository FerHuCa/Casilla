# Capturas de Apariencia (tablero y piezas por separado) a 1280 y 390 px en docs/capturas/apariencia/.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'run.py')).read().split("logs=[]")[0])
DEST=str(_HERE.parent/'docs'/'capturas'/'apariencia')+'/'; os.makedirs(DEST, exist_ok=True)
MOVES="['e4','e5','Nf3','Nc6','Bb5','a6','Ba4','Nf6','O-O','Be7']"
SIZES=[('1280',1280,1,800,1780),('390',390,2,844,2250)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for tag,w,sc,h,tall in SIZES:
        def page(height):
            ctx=b.new_context(viewport={'width':w,'height':height},device_scale_factor=sc); ctx.route('**/*',handle); pg=ctx.new_page()
            pg.on('pageerror',lambda e: print('PAGEERROR',e))
            pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000); return ctx,pg
        def look(pg, l): pg.evaluate("l=>{S.settings.look=l; save(); applyLook();}", l); pg.wait_for_timeout(600)
        def shot(pg, name, **k): pg.screenshot(path=DEST+name+'-'+tag+'.png', **k); print(name, tag)
        # Panel sin cambios y personalizado
        ctx,pg=page(tall)
        look(pg,{'preset':'clasico','mode':'oscuro'}); pg.evaluate("toggleLook(true)"); pg.wait_for_timeout(1200); shot(pg,'apariencia-sin-cambios')
        look(pg,{'preset':'clasico','mode':'oscuro','board':'nogal','pieces':'spatial'}); pg.evaluate("renderLook()"); pg.wait_for_timeout(800); shot(pg,'apariencia-personalizado')
        # Catálogo: el panel completo, de Tablero a Piezas
        pg.set_viewport_size({'width':w,'height':pg.evaluate("document.querySelector('#look').scrollHeight")+2}); pg.evaluate("renderLook(); document.querySelector('#look').scrollTop=0"); pg.wait_for_timeout(800)
        pg.locator('#look').screenshot(path=DEST+'catalogo-'+tag+'.png'); print('catalogo',tag)
        ctx.close()
        # Juego con mezcla (tablero Nogal + piezas Spatial en Maestro)
        ctx,pg=page(h)
        look(pg,{'preset':'clasico','mode':'oscuro','board':'nogal','pieces':'spatial'})
        pg.evaluate("switchTab('coach')"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{ %s.forEach(m=>App.game.move(m)); const h=App.game.history({verbose:true}); Board.last=h[h.length-1]; Board.render(); }"%MOVES); pg.wait_for_timeout(500)
        shot(pg,'juego-mezcla')
        # Arce y Veteado con selección y última jugada
        for bid in ('arce','veteado'):
            look(pg,{'preset':'clasico','mode':'oscuro','board':bid})
            pg.evaluate("()=>{ Board.sel='f3'; Board.render(); }"); pg.wait_for_timeout(700)
            shot(pg,'tablero-%s-resaltes'%bid)
            pg.evaluate("Board.sel=null; Board.render()")
        ctx.close()
    b.close()
