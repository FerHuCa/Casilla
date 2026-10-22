import json, sys, time
from playwright.sync_api import sync_playwright
import os, pathlib
_HERE=pathlib.Path(__file__).resolve().parent if '__file__' in globals() else pathlib.Path.cwd()
DEPS=os.environ.get('CASILLA_DEPS', str(_HERE/'node_modules'))+'/'
APP='file://'+os.environ.get('CASILLA_APP', str(_HERE.parent/'index.html'))
OUT=os.environ.get('CASILLA_OUT', str(_HERE/'out'))+'/'
os.makedirs(OUT, exist_ok=True)
U='fertest'
def pgn(w,b,res,moves,wres,bres):
    return {"pgn":f'[Event "Live Chess"]\n[Site "Chess.com"]\n[White "{w}"]\n[Black "{b}"]\n[Result "{res}"]\n[ECOUrl "https://www.chess.com/openings/Italian-Game-2...Nc6-3.Bc4"]\n\n{moves} {res}',
            "white":{"username":w,"rating":1400,"result":wres},"black":{"username":b,"rating":1450,"result":bres}}
g1=pgn('rival1',U,'1-0','1. e4 {[%clk 0:04:59.1]} 1... e5 {[%clk 0:04:58]} 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#','win','checkmated')
g2=pgn(U,'rival2','1-0','1. e4 e5 2. Nf3 d6 3. Bc4 Bg4 4. Nc3 g6 5. Nxe5 Bxd1 6. Bxf7+ Ke7 7. Nd5#','win','checkmated')
g3=pgn(U,'rival3','0-1','1. e4 e5 2. Nf3 Nc6 3. Bc4 Nd4 4. Nxe5 Qg5 5. Nxf7 Qxg2 6. Rf1 Qxe4+ 7. Be2 Nf3#','checkmated','win')
games=[]
for i,g in enumerate([g1,g2,g3]):
    g.update({"url":f"https://www.chess.com/game/live/{1000+i}","time_class":"blitz","rules":"chess","end_time":1790000000+i*1000})
    games.append(g)
MOCK={
 '/pub/player/fertest/games/archives':{"archives":["https://api.chess.com/pub/player/fertest/games/2026/10"]},
 '/pub/player/fertest/games/2026/10':{"games":games},
 '/pub/puzzle/random':{"title":"Pasillo","url":"https://www.chess.com/daily-chess-puzzle/x","publish_time":1,"fen":"6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1","pgn":'[FEN "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1"]\r\n\r\n1. Ra8# *'},
}
LI={"game":{"id":"g","pgn":"e4 e5 Nf3 Nc6 Bc4 Nd4 Nxe5"},"puzzle":{"id":"abc12","rating":1500,"initialPly":6,"solution":["d8g5","e5f7","g5g2","h1f1","g2e4","c4e2","d4f3"],"themes":["opening","mateIn4"]}}
def handle(route):
    url=route.request.url
    h={"Access-Control-Allow-Origin":"*"}
    if 'cdnjs.cloudflare.com' in url:
        if 'chess.min.js' in url: return route.fulfill(path=DEPS+'chess.js/chess.js',headers=h,content_type='text/javascript')
        f=url.split('/')[-1]
        ct='application/wasm' if f.endswith('.wasm') else 'text/javascript'
        return route.fulfill(path=DEPS+'stockfish.js/'+f,headers=h,content_type=ct)
    if 'cdn.jsdelivr.net/npm/stockfish@' in url:
        f=url.split('#')[0].split('/')[-1]
        return route.fulfill(path=DEPS+'stockfish/bin/'+f,headers={"Access-Control-Allow-Origin":"*"},content_type='application/wasm' if f.endswith('.wasm') else 'text/javascript')
    if 'fonts.g' in url: return route.abort()
    if 'api.chess.com' in url:
        p=url.split('api.chess.com')[1].split('?')[0]
        if p in MOCK: return route.fulfill(status=200,headers=h,content_type='application/json',body=json.dumps(MOCK[p]))
        return route.fulfill(status=404,headers=h,body='{}')
    if 'lichess.org' in url:
        return route.fulfill(status=200,headers=h,content_type='application/json',body=json.dumps(LI))
    return route.continue_()
logs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1400,'height':900})
    ctx.route('**/*',handle)
    pg=ctx.new_page()
    pg.on('console',lambda m: logs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)))
    pg.goto(APP)
    pg.wait_for_function("document.querySelector('#pillText').textContent.includes('listo') || document.querySelector('#pill').classList.contains('err')",timeout=60000)
    print('pill:',pg.inner_text('#pillText'))
    pg.screenshot(path=OUT+'1_ladder.png')
    # openings legality
    print(pg.evaluate("""OPENINGS.map(o=>{const g=new Chess();const bad=o.line.split(' ').find(m=>!g.move(m,{sloppy:true}));return o.id+':'+(bad||'ok')}).join(' ')"""))
    # endgames eval
    res="skip" if True else pg.evaluate("""(async()=>{const out=[];for(const e of ENDGAMES){const r=await Engine.run(e.fen,{depth:22,movetime:6000,tag:'t'});const v=(e.fen.split(' ')[1]==='w'?1:-1)*cpEq(r.score);out.push(e.id+' '+e.goal+' white:'+fmtEval(v)+' d'+r.depth+' best '+r.best)}return out.join('\\n')})()""")
    print(res)
    # ladder game via real clicks
    pg.click('#go')
    time.sleep(0.5)
    def sqbox(sq): return pg.locator(f'.sq[data-sq="{sq}"]').bounding_box()
    a=sqbox('e2'); c=sqbox('e4')
    pg.mouse.move(a['x']+a['width']/2,a['y']+a['height']/2); pg.mouse.down(); pg.mouse.move(c['x']+30,c['y']+30,steps=6); pg.mouse.up()
    pg.wait_for_function("App.game.history().length>=2",timeout=10000)
    print('ladder hist',pg.evaluate("App.game.history().join(' ')"))
    # click-click
    pg.click('.sq[data-sq="g1"]'); pg.click('.sq[data-sq="f3"]')
    pg.wait_for_function("App.game.history().length>=4",timeout=10000)
    print('ladder hist',pg.evaluate("App.game.history().join(' ')"))
    pg.screenshot(path=OUT+'2_game.png')
    # puzzles lichess
    pg.click('.tab[data-tab=puzzles]')
    pg.click('[data-seg=src] button[data-v=lichess]')
    pg.wait_for_function("App.session.p && App.session.p.src==='lichess'",timeout=10000)
    print('puzzle fen',pg.evaluate("App.game.fen()"),'turn',pg.evaluate("App.game.turn()"))
    for mv in ['d8g5','g5g2','g2e4','d4f3']:
        pg.evaluate(f"App.session.onUserMove(uciObj('{mv}'))"); time.sleep(0.8)
    print('puzzle done',pg.evaluate("[App.session.p.done,App.session.p.failed,S.puzzles.rating]"), pg.inner_text('#status'))
    pg.screenshot(path=OUT+'3_puzzle.png')
    pg.click('[data-seg=src] button[data-v=chesscom]')
    pg.wait_for_function("App.session.p && App.session.p.src==='chesscom'",timeout=10000)
    pg.evaluate("App.session.onUserMove({from:'a2',to:'a4'})"); time.sleep(1)
    print('wrong ->',pg.evaluate("[App.session.p.failed, App.game.fen()]"))
    pg.evaluate("App.session.onUserMove(uciObj('a1a8'))"); time.sleep(0.5)
    print('cc puzzle',pg.evaluate("[App.session.p.done,S.puzzles.rating]"))
    # games
    pg.click('.tab[data-tab=games]')
    pg.fill('#user',U); pg.click('#load')
    pg.wait_for_function("S.games.length===3",timeout=10000); time.sleep(.5)
    pg.select_option('#bmt','250')
    pg.click('#bgo')
    pg.wait_for_function("Object.keys(S.analyses).length===3 && !Analyzer.running",timeout=120000)
    print(pg.evaluate("JSON.stringify(Object.values(S.analyses).map(a=>({acc:a.acc,cnt:a.cnt,tags:a.tags,m:a.mistakes.map(m=>[m.played,m.bestSan,m.cat,m.phase,m.drop])})))"))
    time.sleep(.5); pg.screenshot(path=OUT+'4_games.png')
    pg.click('.game[data-id] >> nth=2'); time.sleep(.6)
    pg.click('[data-go] >> nth=0'); time.sleep(.4)
    pg.screenshot(path=OUT+'5_review.png')
    pg.click('.tab[data-tab=positions]'); pg.click('[data-seg=pt] button[data-v=mias]'); time.sleep(.3)
    pg.screenshot(path=OUT+'6_mias.png')
    pg.click('[data-mz] >> nth=0'); time.sleep(.5)
    print('mine puzzle',pg.evaluate("[App.session.p.src, App.session.p.solution, App.game.fen()]"))
    # endgame session
    pg.click('.tab[data-tab=positions]'); pg.click('[data-seg=pt] button[data-v=finales]'); time.sleep(.2)
    pg.click('[data-eg=kp6]'); time.sleep(.3)
    for mv in ['e6d6','e5e6','e6e7']:
        pg.evaluate(f"App.session.onUserMove(uciObj('{mv}'))")
        pg.wait_for_function("!App.session.thinking",timeout=15000); time.sleep(.3)
        print(' eg',pg.evaluate("[App.game.fen(), App.session.userEval, App.session.over]"))
    pg.screenshot(path=OUT+'7_endgame.png')
    pg.click('.tab[data-tab=progress]'); time.sleep(.3); pg.screenshot(path=OUT+'8_progress.png')
    pg.click('.tab[data-tab=positions]'); pg.click('[data-seg=pt] button[data-v=aperturas]'); pg.click('[data-op=naj][data-side=b]'); time.sleep(1)
    pg.evaluate("App.session.onUserMove({from:'c7',to:'c5'})"); time.sleep(1)
    pg.evaluate("App.session.onUserMove({from:'e7',to:'e5'})"); time.sleep(1)
    print('opening',pg.evaluate("App.game.history().join(' ')"), pg.inner_text('#status'))
    pg.screenshot(path=OUT+'9_opening.png')
    m=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); m.route('**/*',handle); mp=m.new_page(); mp.goto(APP); time.sleep(2); mp.screenshot(path=OUT+'10_mobile.png',full_page=True)
    b.close()
print('\n'.join(logs[:30]))
