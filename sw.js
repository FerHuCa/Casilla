/* Casilla: service worker para usar la app sin conexión.
   - Precachea el sitio, las fuentes, el logo, los favicons, chess.js y los dos motores (Stockfish 19 lite alojado en engine/ y su respaldo, Stockfish 10).
   - No precachear 'index.html': Cloudflare lo redirige (307) a '/'. La shell se guarda como './'.
   - No usar jsDelivr para stockfish@19: responde 403 (paquete > 150 MB) y abortaba toda la instalación.
   - index.html (y la navegación) va con red primero: con internet siempre se sirve la versión nueva; sin red, la guardada.
   - El resto va con caché primero y se guarda lo que se baje después.
   - Al cambiar VERSION se crea una caché nueva, se activa sola (skipWaiting + clients.claim) y se borran las viejas.
   Sube VERSION en cada cambio de sw.js o de los archivos precacheados. */
const VERSION = '2026-10-22.2';
const CACHE = 'casilla-' + VERSION;
const SF10 = 'https://cdnjs.cloudflare.com/ajax/libs/stockfish.js/10.0.2/';
const LOCAL = [
  './', 'manifest.webmanifest',
  'engine/stockfish-19-lite-single.js', 'engine/stockfish-19-lite-single.wasm',
  'logo-claro.svg', 'logo-oscuro.svg', 'favicon.svg', 'favicon.ico',
  'favicon-16.png', 'favicon-32.png', 'favicon-48.png', 'apple-touch-icon-180.png', 'icon-512.png', 'icon-512-oscuro.png',
  'fonts/SourceSans3-latin.woff2', 'fonts/SourceSerif4-latin.woff2', 'fonts/Manrope-latin.woff2', 'fonts/Literata-latin.woff2',
  'fonts/IBMPlexSans-latin.woff2', 'fonts/IBMPlexMono-500-latin.woff2', 'fonts/IBMPlexMono-600-latin.woff2',
  'fonts/PressStart2P-latin.woff2', 'fonts/PixelifySans-latin.woff2'
];
const CDN = [
  'https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js',
  SF10 + 'stockfish.js', SF10 + 'stockfish.wasm.js', SF10 + 'stockfish.wasm'
];
const CDN_HOSTS = ['cdnjs.cloudflare.com'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(LOCAL.map(u => new Request(u, {cache:'reload'})));
    await c.addAll(CDN.map(u => new Request(u, {mode:'cors', credentials:'omit'})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith('casilla-') && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
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
    e.respondWith((async () => {
      const c = await caches.open(CACHE);
      try{
        const r = await fetch(req, {cache:'no-store'});
        if(r.ok) c.put(self.registration.scope, r.clone());
        return r;
      }catch(err){
        const hit = await c.match(self.registration.scope, {ignoreSearch:true});
        if(!hit) return Response.error();
        // Una respuesta con redirected=true no sirve para una navegación: se rearma limpia.
        return hit.redirected ? new Response(await hit.blob(), {status:200, headers:hit.headers}) : hit;
      }
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
