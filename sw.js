/* Casilla: service worker para usar la app sin conexión.
   - Precachea solo archivos del mismo origen: el sitio, las fuentes, el logo, los favicons, chess.js (lib/) y Stockfish 19 lite (engine/).
     Ningún CDN entra al precache: si un CDN falla o está bloqueado, la instalación no se cae.
   - El respaldo, Stockfish 10 (cdnjs), se guarda solo si se llega a usar y se conserva entre versiones.
   - No precachear 'index.html': Cloudflare lo redirige (307) a '/'. La shell se guarda como './'.
   - No usar jsDelivr para stockfish@19: responde 403 (paquete > 150 MB) y abortaba toda la instalación.
   - index.html (y la navegación) sale de la caché al instante y se revalida en segundo plano (ETag): abrir la app no espera a la red.
     Lo que baje se guarda para la siguiente apertura. Sin copia guardada (primera visita) va a la red.
   - El resto va con caché primero y se guarda lo que se baje después.
   - Al cambiar VERSION se crea una caché nueva y el SW nuevo queda en espera (waiting), sin skipWaiting automático.
     La página muestra el aviso «Hay una versión nueva.»: Actualizar manda SKIP_WAITING y aquí se llama skipWaiting().
     Con «Ahora no» se activa en la siguiente apertura (index.html) o cuando ya no quedan pestañas abiertas.
     Al activarse: clients.claim y se borran las cachés viejas.
   - GET_VERSION responde la VERSION por el puerto del MessageChannel (la usa el pie).
   - Piezas (piece/) y texturas (board/) no se precachean: se guardan al usarlas (caché primero, como el resto).
     Solo el set por defecto (Clásicas) va embebido en index.html y el tablero por defecto son colores, así que no hay archivo que precachear.
     Al activarse una versión nueva, lo ya guardado de piece/ y board/ pasa a la caché nueva antes de borrar la vieja,
     para que el set activo siga sin red tras actualizar.
   Sube VERSION en cada cambio de sw.js o de los archivos precacheados. */
const VERSION = '2026-11-09.1';
const CACHE = 'casilla-' + VERSION;
const SF10 = 'https://cdnjs.cloudflare.com/ajax/libs/stockfish.js/10.0.2/';
const LOCAL = [
  './', 'manifest.webmanifest', 'lib/chess.js',
  'engine/stockfish-19-lite-single.js', 'engine/stockfish-19-lite-single.wasm',
  'logo-claro.svg', 'logo-oscuro.svg', 'favicon.svg', 'favicon.ico',
  'favicon-16.png', 'favicon-32.png', 'favicon-48.png', 'apple-touch-icon-180.png', 'icon-512.png', 'icon-512-oscuro.png',
  'fonts/SourceSans3-latin.woff2', 'fonts/SourceSerif4-latin.woff2', 'fonts/Manrope-latin.woff2', 'fonts/Literata-latin.woff2',
  'fonts/IBMPlexSans-latin.woff2', 'fonts/IBMPlexMono-500-latin.woff2', 'fonts/IBMPlexMono-600-latin.woff2',
  'fonts/PressStart2P-latin.woff2', 'fonts/PixelifySans-latin.woff2'
];
const CDN_HOSTS = ['cdnjs.cloudflare.com'];
const ON_USE = ['piece/', 'board/']; // se guardan al usarlos y se conservan entre versiones

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(LOCAL.map(u => new Request(u, {cache:'reload'})));
    // Sin skipWaiting: la primera instalación se activa sola (no hay SW previo); una actualización espera al aviso 3.
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys(), old = keys.filter(k => k.startsWith('casilla-') && k !== CACHE);
    const c = await caches.open(CACHE), base = self.registration.scope;
    for(const k of old){
      const o = await caches.open(k);
      for(const req of await o.keys()){
        if(!(ON_USE.some(d => req.url.startsWith(base + d)) || req.url.startsWith(SF10)) || await c.match(req)) continue;
        const r = await o.match(req); if(r) await c.put(req, r);
      }
    }
    await Promise.all(old.map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', e => {
  const t = e.data && e.data.type;
  if(t === 'SKIP_WAITING') self.skipWaiting();
  else if(t === 'GET_VERSION'){
    const msg = {type:'VERSION', version:VERSION};
    if(e.ports && e.ports[0]) e.ports[0].postMessage(msg); else if(e.source) e.source.postMessage(msg);
  }
});

function isIndex(req, url){
  return req.mode === 'navigate' || (url.origin === self.location.origin && /\/(index\.html)?$/.test(url.pathname));
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if(req.method !== 'GET') return;
  const url = new URL(req.url);
  const same = url.origin === self.location.origin;
  if(!same && !CDN_HOSTS.includes(url.hostname)) return; // APIs (Chess.com, Lichess, Claude, GitHub) van directo a la red
  const key = url.origin + url.pathname; // sin hash ni query (el worker de Stockfish 19 lleva la ruta del .wasm en el hash)
  if(same && isIndex(req, url)){
    const shell = self.registration.scope;
    const cache = caches.open(CACHE);
    const stored = cache.then(c => c.match(shell, {ignoreSearch:true}));
    // Revalidación: con ETag casi siempre es un 304 barato. Lo nuevo queda guardado para la siguiente apertura.
    const fresh = (async () => {
      const r = await fetch(req, {cache:'no-cache'});
      await stored; // primero se lee la copia que se va a servir, luego se reemplaza
      if(r.ok) await (await cache).put(shell, r.clone());
      return r;
    })();
    e.waitUntil(fresh.catch(() => {}));
    e.respondWith((async () => {
      const hit = await stored;
      if(!hit){ try{ return await fresh; }catch(err){ return Response.error(); } }
      // Una respuesta con redirected=true no sirve para una navegación: se rearma limpia.
      return hit.redirected ? new Response(await hit.blob(), {status:200, headers:hit.headers}) : hit;
    })());
    return;
  }
  e.respondWith((async () => {
    const c = await caches.open(CACHE);
    const hit = await c.match(key);
    if(hit) return hit;
    const r = await fetch(req);
    if(r.ok && (r.type === 'basic' || r.type === 'cors')) c.put(key, r.clone());
    return r;
  })());
});
