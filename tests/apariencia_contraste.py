# Resaltes visibles en cada tablero: mide con Playwright el color renderizado de una casilla vacía
# sin resaltar y con resalte (última jugada y selección), en casilla clara y oscura, sobre todos los tableros
# de LOOK.board (colores, texturas y Contraste). Compara la misma casilla antes y después (así sirve para texturas).
#
# Métrica: CIEDE2000 (ΔE00) entre los colores medios del centro de la casilla (50 %), en sRGB D65, y razón de
# contraste WCAG entre ambos colores (luminancia relativa).
# Umbral para los tableros nuevos (Arena, Oliva, Tinta, Coral, Contraste, Arce, Veteado): ΔE00 >= 8 y contraste >= 1.05.
#   Referencia: ΔE00 ~2.3 es la diferencia apenas perceptible y a partir de ~5 se nota de un vistazo; 8 deja margen
#   para pantallas peores y luz ambiente. El contraste >= 1.05 evita resaltes que solo cambian de tono con la misma
#   luminancia (poco visibles con daltonismo).
# Tableros aprobados antes de este cambio (Gris piedra, Madera, Nogal, Glaciar, Club, Arcade): no se cambia su diseño;
#   se exige solo ΔE00 >= 3 como piso contra regresiones. Hoy el más débil es Club, selección en casilla oscura (~3.4),
#   y Madera y Nogal en última jugada sobre casilla clara (~6); se reportan para decidir aparte.
import os, io, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'run.py')).read().split("logs=[]")[0])
from PIL import Image
MIN_DE=8.0; MIN_CR=1.05; MIN_DE_OLD=3.0
F=0
def ck(ok,msg):
    global F; F+=not ok; print('OK   ' if ok else 'FALLA ', msg)
def lin(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lab(rgb):
    r,g,b=[lin(x) for x in rgb]
    X=(0.4124*r+0.3576*g+0.1805*b)/0.95047; Y=(0.2126*r+0.7152*g+0.0722*b); Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return (116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z)))
def de2000(c1,c2):
    L1,a1,b1=c1; L2,a2,b2=c2
    C1=math.hypot(a1,b1); C2=math.hypot(a2,b2); Cb=(C1+C2)/2
    G=0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7)))
    a1p=(1+G)*a1; a2p=(1+G)*a2; C1p=math.hypot(a1p,b1); C2p=math.hypot(a2p,b2)
    h1p=math.degrees(math.atan2(b1,a1p))%360; h2p=math.degrees(math.atan2(b2,a2p))%360
    dLp=L2-L1; dCp=C2p-C1p
    dhp=0 if C1p*C2p==0 else (h2p-h1p if abs(h2p-h1p)<=180 else (h2p-h1p-360 if h2p-h1p>180 else h2p-h1p+360))
    dHp=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dhp/2))
    Lbp=(L1+L2)/2; Cbp=(C1p+C2p)/2
    hbp=h1p+h2p if C1p*C2p==0 else ((h1p+h2p)/2 if abs(h1p-h2p)<=180 else ((h1p+h2p+360)/2 if h1p+h2p<360 else (h1p+h2p-360)/2))
    T=1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))+0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63))
    dth=30*math.exp(-((hbp-275)/25)**2); RC=2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    SL=1+0.015*(Lbp-50)**2/math.sqrt(20+(Lbp-50)**2); SC=1+0.045*Cbp; SH=1+0.015*Cbp*T; RT=-math.sin(math.radians(2*dth))*RC
    return math.sqrt((dLp/SL)**2+(dCp/SC)**2+(dHp/SH)**2+RT*(dCp/SC)*(dHp/SH))
def lum(rgb): r,g,b=[lin(x) for x in rgb]; return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b): la,lb=sorted([lum(a),lum(b)]); return (lb+0.05)/(la+0.05)
def mean(pg, sq):
    bb=pg.locator(f'#board [data-sq={sq}]').bounding_box(); w=bb['width']
    clip={'x':bb['x']+w*.25,'y':bb['y']+w*.25,'width':w*.5,'height':w*.5}
    im=Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); px=list(im.get_flattened_data() if hasattr(im,'get_flattened_data') else im.getdata()); n=len(px)
    return tuple(sum(p[i] for p in px)/n for i in range(3))
# Casillas vacías de la posición inicial: c3 y e3 oscuras, d3 y f3 claras. La última jugada marca c3 y d3.
CASES=[('última jugada','c3','oscura'),('última jugada','d3','clara'),('selección','e3','oscura'),('selección','f3','clara')]
SET={'última jugada':"s=>{Board.last={from:'c3',to:'d3'}; Board.render();}", 'selección':"s=>{Board.sel=s; Board.render();}"}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1280,'height':900}); ctx.route('**/*',handle); pg=ctx.new_page()
    pg.on('pageerror',lambda e: print('PAGEERROR',e))
    pg.goto(APP); pg.wait_for_function("typeof Board!=='undefined' && document.querySelectorAll('#board [data-sq]').length===64",timeout=30000)
    boards=pg.evaluate("LOOK.board.map(o=>[o[0],o[1],!!o[4]])")
    old=['piedra','madera','nogal','glaciar','club','arcade']
    mins={'aprobados antes':99,'nuevos':99}
    for bid,name,tex in boards:
        pg.evaluate("id=>{S.settings.look={preset:'clasico',mode:'oscuro',board:id}; applyLook(); Board.last=null; Board.sel=null; Board.render();}", bid)
        if tex: pg.wait_for_function("id=>{const u=getComputedStyle(document.querySelector('#board')).backgroundImage; if(!u.includes('board/')) return false; const im=new Image(); im.src=u.slice(5,-2); return im.complete && im.naturalWidth>0}", arg=bid, timeout=10000)
        pg.wait_for_timeout(150)
        base={sq:mean(pg,sq) for _,sq,_ in CASES}
        grp='aprobados antes' if bid in old else 'nuevos'
        for label,sq,tone in CASES:
            pg.evaluate(SET[label], sq); pg.wait_for_timeout(80)
            after=mean(pg,sq); d=de2000(lab(base[sq]),lab(after)); c=cr(base[sq],after); mins[grp]=min(mins[grp],d)
            ok=(d>=MIN_DE and c>=MIN_CR) if grp=='nuevos' else d>=MIN_DE_OLD
            ck(ok, '%-11s %-14s %s (%s): ΔE00 %.1f, contraste %.2f'%(name,label,sq,tone,d,c))
            pg.evaluate("()=>{Board.last=null; Board.sel=null; Board.render();}")
        if bid in ('arce','veteado','contraste'):
            pg.evaluate("()=>{Board.last={from:'c3',to:'d3'}; Board.sel='e3'; Board.render();}"); pg.wait_for_timeout(80)
            pg.locator('#board').screenshot(path=OUT+'contraste_%s.png'%bid)
    print('ΔE00 mínimo por grupo: %s (umbral nuevos %.1f, aprobados antes %.1f)'%({k:round(v,1) for k,v in mins.items()}, MIN_DE, MIN_DE_OLD))
    b.close()
print('RESULTADO: todo bien' if not F else 'RESULTADO: %d fallas'%F); raise SystemExit(F)
