exec(open('coach.py').read().split("with sync_playwright() as p:")[0])
import re
GIST = {}   # almacén simulado de gists
TOKEN = 'ghp_test123'
CALLS = []
def gh(route):
    req = route.request; url = req.url; m = req.method
    h = {"Access-Control-Allow-Origin":"*", "Access-Control-Allow-Headers":"*", "Access-Control-Allow-Methods":"GET,POST,PATCH"}
    if m == 'OPTIONS': return route.fulfill(status=204, headers=h)
    if 'gist.githubusercontent.com' in url:
        gid = url.split('/')[-2]; return route.fulfill(status=200, headers=h, body=GIST[gid]['content'])
    auth = req.headers.get('authorization','')
    CALLS.append(m + ' ' + url.split('api.github.com')[1])
    if auth != 'Bearer ' + TOKEN: return route.fulfill(status=401, headers=h, content_type='application/json', body='{"message":"Bad credentials"}')
    path = url.split('api.github.com')[1].split('?')[0]
    def gj(gid):
        g = GIST[gid]; c = g['content']; trunc = len(c) > 1000000
        return {"id":gid, "html_url":"https://gist.github.com/"+gid, "files":{g['name']:{"filename":g['name'], "content": None if trunc else c, "truncated":trunc, "raw_url":"https://gist.githubusercontent.com/u/"+gid+"/raw"}}}
    if path == '/gists' and m == 'GET':
        return route.fulfill(status=200, headers=h, content_type='application/json', body=json.dumps([{"id":k,"html_url":"https://gist.github.com/"+k,"files":{v['name']:{"filename":v['name']}}} for k,v in GIST.items()]))
    if path == '/gists' and m == 'POST':
        d = json.loads(req.post_data); name = list(d['files'].keys())[0]; gid = 'g%d' % (len(GIST)+1)
        GIST[gid] = {'name':name, 'content':d['files'][name]['content'], 'public':d['public']}
        return route.fulfill(status=201, headers=h, content_type='application/json', body=json.dumps(gj(gid)))
    mm = re.match(r'/gists/(\w+)$', path)
    if mm and mm.group(1) in GIST:
        gid = mm.group(1)
        if m == 'PATCH':
            d = json.loads(req.post_data); GIST[gid]['content'] = d['files'][GIST[gid]['name']]['content']
        return route.fulfill(status=200, headers=h, content_type='application/json', body=json.dumps(gj(gid)))
    return route.fulfill(status=404, headers=h, body='{}')
def handle3(route):
    if 'github.com' in route.request.url or 'githubusercontent' in route.request.url: return gh(route)
    return handle2(route)
def connect(pg, tok):
    pg.click('.tab[data-tab=progress]'); time.sleep(.3)
    pg.fill('#syncTok', tok); pg.click('#syncGo')
    pg.wait_for_function("Sync.state==='ok' || Sync.state==='err'", timeout=15000); time.sleep(.3)
with sync_playwright() as p:
    b = p.chromium.launch()
    A = b.new_context(viewport={'width':1400,'height':900}); A.route('**/*', handle3); pa = A.new_page()
    B = b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True); B.route('**/*', handle3); pb = B.new_page()
    for pg in (pa, pb): pg.on('pageerror', lambda e: print('PAGEERROR', e))
    pa.goto(APP); pa.wait_for_function("Engine.ready", timeout=60000)
    # A: progreso inicial
    pa.evaluate("S.username='fertest'; S.ladder.unlocked=3; S.ladder.rec={0:{w:1,d:0,l:0},1:{w:1,d:0,l:1}}; S.puzzles.rating=1350; S.puzzles.hist=[{t:1000,r:1350,ok:true,src:'lichess'}]; S.puzzles.solved=5; S.settings.look={theme:'papel',font:'libro',board:'madera',pieces:'merida'}; S.settings.claude={on:true,key:'sk-ant-SECRETO',model:'claude-haiku-5-5'}; S.endgames={kq:{done:true,at:1}}; saveLocal(); applyLook();")
    # token malo primero
    connect(pa, 'malo'); print('A token malo ->', pa.evaluate("[Sync.state, Sync.error]"))
    connect(pa, TOKEN); print('A conectado ->', pa.evaluate("[Sync.state, S.settings.sync.gistId]"), 'gists:', list(GIST.keys()), 'public:', GIST['g1']['public'])
    raw = GIST['g1']['content']; print('payload enc:', json.loads(raw)['enc'], 'bytes:', len(raw), 'contiene clave?', 'SECRETO' in raw, 'contiene token?', TOKEN in raw)
    pa.screenshot(path=OUT+'s1_progress.png')
    # B: dispositivo nuevo
    pb.goto(APP); pb.wait_for_function("Engine.ready", timeout=60000)
    connect(pb, TOKEN)
    print('B tras conectar ->', pb.evaluate("JSON.stringify({u:S.username, lad:S.ladder.unlocked, pr:S.puzzles.rating, look:S.settings.look, claude:!!S.settings.claude, eg:Object.keys(S.endgames)})"), 'theme attr', pb.evaluate("document.documentElement.dataset.theme"))
    # B gana un nivel y resuelve un puzzle
    pb.evaluate("S.ladder.unlocked=4; S.ladder.rec[2]={w:1,d:0,l:0}; S.puzzles.hist.push({t:2000,r:1380,ok:true,src:'mine'}); S.puzzles.rating=1380; S.puzzles.solved=6; save();")
    print('B estado tras cambio ->', pb.evaluate("Sync.state"), pb.inner_text('#syncInd') if pb.is_visible('#syncInd') else '(indicador oculto en móvil chico)')
    pb.evaluate("Sync.now()"); pb.wait_for_function("Sync.state==='ok'", timeout=15000)
    # A al mismo tiempo jugó otra cosa sin sincronizar
    pa.evaluate("S.openings={itaw:{reps:2,clean:1}}; S.coach={rating:1420,rec:{w:1,d:0,l:0},serious:1,games:[{t:3000,vs:true,res:'w',acc:80,errors:1}]}; saveLocal();")
    pa.evaluate("Sync.now()"); pa.wait_for_function("Sync.state==='ok'", timeout=15000); time.sleep(.3)
    print('A combinado ->', pa.evaluate("JSON.stringify({lad:S.ladder.unlocked, rec2:S.ladder.rec[2], pr:S.puzzles.rating, hist:S.puzzles.hist.length, solved:S.puzzles.solved, op:S.openings, coach:S.coach.rating, key:S.settings.claude.key.slice(0,6)})"))
    pb.evaluate("Sync.now()"); pb.wait_for_function("Sync.state==='ok'", timeout=15000)
    print('B combinado ->', pb.evaluate("JSON.stringify({lad:S.ladder.unlocked, pr:S.puzzles.rating, op:S.openings, coach:S.coach&&S.coach.rating})"))
    # el respaldo exportado no lleva token
    print('respaldo sin token/clave:', pa.evaluate("(()=>{ const c=JSON.parse(JSON.stringify(S)); c.settings.claude.key=''; delete c.settings.sync; return !JSON.stringify(c).includes('ghp_') && !JSON.stringify(c).includes('SECRETO'); })()"))
    pb.screenshot(path=OUT+'s2_mobile.png', full_page=True)
    print('llamadas:', len(CALLS), CALLS[:12])
    b.close()
