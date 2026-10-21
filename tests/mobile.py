exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
import sys
W = int(sys.argv[1]) if len(sys.argv)>1 else 390
H = {390:844, 360:740}.get(W, 800)
TAG = sys.argv[2] if len(sys.argv)>2 else 'a'
D = OUT+'mob/'
os.makedirs(D, exist_ok=True)
AUDIT = r"""(()=>{
  const vw = innerWidth, out = {overflowX: document.documentElement.scrollWidth - vw};
  const wide = []; document.querySelectorAll('body *').forEach(el=>{ const r=el.getBoundingClientRect(); if(r.width>0 && r.right > vw+1 && getComputedStyle(el).position!=='fixed') wide.push((el.id?'#'+el.id:el.className||el.tagName)+':'+Math.round(r.right)); });
  out.wide = [...new Set(wide)].slice(0,6);
  const small = []; document.querySelectorAll('button, a, select, input, .stair, .game, summary').forEach(el=>{ const r=el.getBoundingClientRect(); if(r.width>0 && r.height>0 && r.height<36 && getComputedStyle(el).visibility!=='hidden') small.push((el.textContent||el.id||el.tagName).trim().slice(0,18)+':'+Math.round(r.height)); });
  out.smallTargets = small.length; out.smallEx = [...new Set(small)].slice(0,8);
  const fs = []; document.querySelectorAll('input, select, textarea').forEach(el=>{ const f=parseFloat(getComputedStyle(el).fontSize); if(f<16) fs.push((el.id||el.tagName)+':'+f); });
  out.iosZoomInputs = fs;
  const b = document.querySelector('.board-box').getBoundingClientRect(); out.board = [Math.round(b.left), Math.round(b.width), Math.round(vw - b.right)];
  return JSON.stringify(out);
})()"""
def shot(pg, name, full=True):
    pg.screenshot(path=D+f'{TAG}{W}_{name}.png', full_page=full)
    print(name, pg.evaluate(AUDIT))
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':W,'height':H}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.route('**/*',handle2); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(APP); pg.wait_for_function("Engine.ready",timeout=60000)
    pg.evaluate("S.settings.evalTime=200")
    shot(pg,'01_ladder')
    # partida con reloj, barra y maestro guiado
    pg.click('[data-seg=clock] button[data-v="300+0"]'); pg.check('#helps'); pg.check('#lbar'); pg.check('#lcoach')
    pg.click('#go'); time.sleep(1)
    pg.tap('.sq[data-sq="e2"]'); pg.tap('.sq[data-sq="e4"]'); pg.wait_for_function("App.game.history().length>=2",timeout=15000); time.sleep(1.5)
    shot(pg,'02_game', full=False); shot(pg,'02_game_full')
    pg.evaluate("""App.setSession(new PlaySession({fen:'r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 3 3', userColor:'b', tier:TIERS[3], tierIdx:3, helps:true, coach:{mode:'guide'}, title:'Prueba guiada'}))""")
    time.sleep(1.5); pg.tap('.sq[data-sq="g8"]'); pg.tap('.sq[data-sq="f6"]'); time.sleep(3)
    shot(pg,'03_warning', full=False)
    # promoción
    pg.evaluate("""App.setSession(new PlaySession({fen:'8/4P1k1/8/8/8/8/8/4K3 w - - 0 1', userColor:'w', tier:TIERS[0], tierIdx:0, helps:false, title:'Promo'}))"""); time.sleep(.6)
    pg.tap('.sq[data-sq="e7"]'); pg.tap('.sq[data-sq="e8"]'); time.sleep(.4)
    shot(pg,'04_promo', full=False)
    pg.tap('#promo button[data-p=q]'); time.sleep(.3)
    pg.click('.tab[data-tab=coach]'); time.sleep(.3); shot(pg,'05_coach')
    pg.click('.tab[data-tab=puzzles]'); pg.click('[data-seg=src] button[data-v=lichess]'); time.sleep(1.5); shot(pg,'06_puzzle')
    pg.click('.tab[data-tab=positions]'); time.sleep(.3); shot(pg,'07_positions')
    pg.click('.tab[data-tab=games]'); pg.fill('#user',U); pg.click('#load'); pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.5)
    shot(pg,'08_games')
    pg.click('.game[data-id] >> nth=2'); time.sleep(.6); shot(pg,'09_review')
    pg.click('#deep'); pg.wait_for_function("Evaluator.job && Evaluator.job.done", timeout=120000); time.sleep(.6)
    shot(pg,'10_eval', full=False); shot(pg,'10_eval_full')
    pg.click('.tab[data-tab=progress]'); time.sleep(.3); shot(pg,'11_progress')
    pg.click('#lookBtn'); time.sleep(.3); shot(pg,'12_look', full=False)
    b.close()
