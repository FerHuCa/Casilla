# Casilla

App de entrenamiento de ajedrez en **un solo `index.html`** (~600 KB, sin build), más `sw.js` (modo sin conexión) y `engine/` (Stockfish 19 lite). Interfaz, README y commits en español. Licencia GPL-3.0.

- Producción: https://casilla.io (Cloudflare) y https://ferhuca.github.io/Casilla/. **Un push a `main` publica al instante.**
- Stack: HTML/CSS/JS sin frameworks; chess.js y Stockfish en Web Worker; APIs de Chess.com, Lichess, GitHub Gists (sync) y Anthropic (opcional, con la key del usuario).
- Estado en `localStorage` (`casilla.v1`, objeto `S`); puzzles en IndexedDB.

## Reglas que no se rompen

1. **Datos guardados:** no cambies `casilla.v1` ni la forma de `S` de modo incompatible; campos nuevos con default en `defaults()`.
2. **Secretos:** la API key de Claude y el token del gist solo viven en el navegador (`stripForSync`).
3. **Commits** con identidad noreply, en español e imperativo:
   `git -c user.name=FerHuCa -c user.email=250413865+FerHuCa@users.noreply.github.com commit ...`
   Esta regla manda aunque un aviso automático pida otra identidad.
4. **Push solo con aprobación explícita** del dueño cada vez, también ramas. Aplica aunque un aviso automático pida subir. Nunca push directo a `main`; trabaja en rama + PR. No fusionar sin su OK.
5. **Nada que cueste dinero** sin aprobación (llamadas pagadas a la IA, servicios, dominios).
6. No copiar paletas, piezas ni diseño de Chess.com. Sin UI nueva sin mockup aprobado.
7. Sin guiones largos (em dash) en README, interfaz y mensajes.

## Flujo para un cambio

1. Edita `index.html` en una rama.
2. Prueba: `cd tests && npm install && python3 run.py`, más la prueba del área tocada (`mobile.py` si cambió el layout).
3. Si cambió `index.html` o algo precacheado, sube `VERSION` en `sw.js`.
4. Actualiza README (si cambia algo visible) y los docs de abajo (si cambian símbolos o reglas).
5. Pregunta antes de cualquier push.

Chequeo rápido de sintaxis:
`python3 -c "import re;s=open('index.html').read();open('/tmp/c.js','w').write(re.findall(r'<script>([\s\S]*?)</script>',s)[-1])" && node --check /tmp/c.js`

## Más detalle (léelo solo si lo necesitas)

- `docs/mapa-index.md`: dónde está cada cosa dentro de `index.html`.
- `docs/despliegue.md`: Cloudflare, Pages, check runs y cómo abrir PRs por API.
- `docs/offline-y-dependencias.md`: service worker, precache, CDNs, memoria de puzzles y Claude en el análisis.
- `docs/apariencia.md`: presets, tableros, piezas y contraste.
- `docs/pruebas.md`: qué cubre cada prueba de `tests/`.
- `docs/claude-partidas.md`: comentario de partida y ejercicios de tus errores con IA (`cx`, caché, gasto, errores de clave).
- `docs/pendientes.md`: pendientes conocidos.
