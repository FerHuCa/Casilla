# Desborde horizontal a 390 px: en las pantallas principales el documento no se desplaza de lado
# (scrollWidth <= ancho de la ventana) y ningún elemento de main/header queda fuera de la pantalla
# (lo que un overflow:hidden recortaría sin que scrollWidth lo note, como la fila de Partidas).
# Reusa el arnés de claude_partidas.py: API simulada, ninguna llamada sale a la red.
import os
os.environ.setdefault('CASILLA_SHOTS', '/tmp/casilla-desborde')
exec(open('claude_partidas.py').read().split("for W in [1280, 390]:")[0])
CHECK = """(()=>{ const W = window.innerWidth, sw = document.documentElement.scrollWidth;
  const out = [...document.querySelectorAll('header *, main *')].filter(e => { const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && (r.right > W + 0.5 || r.left < -0.5) && getComputedStyle(e).position !== 'fixed'; })
    .slice(0, 4).map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).trim().split(/\\s+/).join('.') : '') + ' ' + Math.round(e.getBoundingClientRect().left) + '..' + Math.round(e.getBoundingClientRect().right));
  return {W, sw, out}; })()"""
def ok_width(pg, where):
    r = pg.evaluate(CHECK)
    check(f'390 sin desborde horizontal ({where}): scrollWidth {r["sw"]} <= {r["W"]}', r['sw'] <= r['W'])
    check(f'390 nada fuera de la pantalla ({where})', not r['out'])
    if r['out']: print('   ', r['out'])
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.route('**/*', handle4); pg = ctx.new_page()
    pg.on('pageerror', lambda e: (print('PAGEERROR', e), fails.append('pageerror')))
    pg.goto(APP); pg.wait_for_function("Engine.ready", timeout=60000)
    pg.evaluate(SETUP, SANS)
    pg.evaluate("S.settings.claude = {on:false, key:'sk-ant-prueba', model:'claude-haiku-5-5', gameModel:'claude-haiku-5-5'}; save()")
    for tab in ['ladder', 'coach', 'puzzles', 'positions', 'games', 'progress']:
        pg.click(f'.tab[data-tab={tab}]'); time.sleep(.5); ok_width(pg, tab)
    tabs = pg.evaluate("[...document.querySelectorAll('.tab')].map(t => { const r = t.getBoundingClientRect(); return [r.left, r.right, t.scrollWidth <= t.clientWidth + 1]; })")
    check('390 las 6 pestañas a la vista, sin corte', all(l >= 0 and r <= 390 and fit for l, r, fit in tabs))
    pg.evaluate("App.tab='games'; $$('.tab').forEach(b=>b.setAttribute('aria-selected', b.dataset.tab==='games')); App.setSession(new ReviewSession(S.games[0], 10))"); time.sleep(.4)
    pg.click('#clGo'); pg.wait_for_function("document.querySelector('#clbox').innerText.includes('Volver a comentar')", timeout=8000)
    ok_width(pg, 'partida con comentario de IA')
    pg.evaluate("App.puzzleSource='mine'"); pg.click('[data-pz="0"]')
    pg.wait_for_function("App.session.p && App.session.p.src==='mine'", timeout=8000); pg.click('#aiHint'); time.sleep(.3)
    ok_width(pg, 'Mis errores con pista')
    b.close()
print('\nRESULTADO:', 'todo bien' if not fails else 'fallas: ' + ', '.join(fails))
