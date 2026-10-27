# Sin conexión, dependencias e IA

## Sin conexión (sw.js)

`sw.js` es el service worker. Solo se registra por http/https (`Offline.start()` en `boot()`), no en file://. En `install` precachea `LOCAL` (sitio, fuentes, logo, favicons, íconos) y `engine/` (Stockfish 19 lite .js/.wasm) y `CDN` (chess.js, Stockfish 10 .js/.wasm.js/.wasm). Estrategias: navegación e `index.html` con red primero (sin red, la copia guardada); lo demás del mismo origen y de cdnjs con caché primero, guardando lo nuevo; APIs (Chess.com, Lichess, Anthropic, GitHub) pasan directo. La clave de caché ignora hash y query (el worker de Stockfish 19 lleva la ruta del .wasm en el hash).

**Al cambiar sw.js o un archivo precacheado, sube `VERSION`** en sw.js (una vez por publicación): crea `casilla-<VERSION>` y `activate` borra las cachés `casilla-*` viejas. La versión nueva ya no hace `skipWaiting` sola: queda en espera y `Offline.prompt()` muestra el aviso 3 (`#upd`, «Hay una versión nueva.»). **Actualizar** manda `SKIP_WAITING` y recarga en `controllerchange` (`hadCtl` evita recargar en la primera instalación). **Ahora no** guarda `casilla.updLater` en localStorage y la siguiente apertura aplica la espera; el navegador también la activa cuando no quedan pestañas. El pie (`#ver`) pide `GET_VERSION` al SW activo por MessageChannel (respaldo: nombre de la caché `casilla-*`); sin SW dice «Sin modo sin conexión.». El registro usa `updateViaCache:'none'` y al volver la red (`online`) llama `reg.update()`. Si agregas una fuente, un ícono o cambias la versión de un CDN, agrégalo a `LOCAL`/`CDN`. `piece/` y `board/` no se precachean (`ON_USE`): se guardan al usarse y en `activate` se copian a la caché nueva antes de borrar la vieja.

Avisos sin red (mockups aprobados 1, 2a, 2b, 3, 5a, 5b, estilo B, solo tokens existentes): objeto `Net` (barra `#offBar`, píldora, notas). No agregues UI sin mockup aprobado.

Memoria de puzzles (`PuzzleStore`): IndexedDB `casilla-puzzles`, aparte de la caché del SW. Objetivo 200 de Lichess (`/api/puzzle/batch/{angle}`, 50 con temas de la etapa; puzzles CC0 según database.lichess.org). Chess.com no se guarda: su User Agreement (chess.com/legal/user-agreement, sección 4.C) prohíbe descargar o copiar información salvo la caché temporal del navegador. Relleno en serie con red, 20 s entre peticiones, 429 de Lichess espera 60 s y duplica (máx. 1 h). `done(id)` borra el resuelto y lo anota en `casilla.pzSolved` (últimos 500) para no volver a guardarlo. Más de 14 días se renuevan (20 por pasada). Sin red, `PuzzleSession.fromStore()` sirve guardados y el 5a (`offPzNote`) solo desactiva fuentes sin guardados.

IA sin red: `ClaudeAI.ready()` exige `navigator.onLine`, así que sin red la IA se comporta como apagada (frases integradas) y vuelve sola. No hay aviso propio para esto (pendiente de mockup); el análisis e Importar solo cambian su nota de texto (preguntas libres y lectura de capturas necesitan conexión). Caché medida: unos 4.7 MB en 27 archivos (`navigator.storage.estimate` reporta unos 7.4 MB en Chromium). Pruebas en `offline.py` y `cfredirect.py`.

Reglas del precache (aprendidas en producción): Cloudflare responde 307 en `/index.html` y `*.html`, así que nunca precachear URLs `.html`; la shell se guarda como `./` (el scope). Stockfish 19 lite vive en `engine/` porque jsDelivr da 403 a `stockfish@19` (paquete > 150 MB) y un solo 403 aborta `cache.addAll` y deja la app sin service worker. Antes de publicar, pide con `curl -sI` cada URL del precache en producción.

Dependencias externas (por CDN, sin instalar nada):
- chess.js 0.10.3 desde cdnjs. Stockfish 19 lite de un hilo (npm `stockfish` 19.0.1) alojado en `engine/` (GPL-3.0; jsDelivr da 403 a ese paquete), en un Web Worker creado desde un Blob; la ruta del .wasm va en el hash del worker. Si falla, cae a stockfish.js 10.0.2 de cdnjs (WASM y luego asm.js). `?sf=10` fuerza el 10.
- Todas las fuentes van autoalojadas en `fonts/` (OFL). Las de los presets no Clásicos se declaran con @font-face y el navegador solo las baja cuando se usan. Ya no se usa Google Fonts.
- APIs: Chess.com PubAPI (partidas por archivo mensual y puzzle diario, con fallback JSONP), Lichess (`/api/puzzle/next`, `/api/puzzle/batch/{angle}`, `/api/puzzle/daily` y `/game/export/{id}` para importar links), GitHub Gists (sync), Anthropic API (Maestro con Claude, opcional).

## Claude en el análisis

- Dos modelos: `model` (comentarios en partida, por defecto Haiku 5.5) y `anaModel` (análisis y capturas). `anaModel` no tiene valor por defecto: `ClaudeAI.anaModel()` usa el de comentarios hasta que la persona elige en la tarjeta `modelPickHTML` (opciones y costos en `ANA_OPTIONS`) o en el ajuste. Ambos viven en `S.settings.claude`, que nunca se sincroniza. Si cambian los precios de Anthropic, actualiza los costos de `ANA_OPTIONS` y del README.
- Opus 5.5 rechaza `thinking: disabled` y `between_tools`: se manda sin `thinking`, con `output_config.effort` bajo y `max_tokens` con espacio para pensar. Haiku usa `disabled` y Sonnet `between_tools`. Opus y Sonnet rechazan `tool_choice` forzado; al llegar al límite de consultas se manda `tool_choice: none`.
- En el ciclo con herramientas, el contenido de la respuesta (incluidos los bloques de pensamiento) se devuelve sin cambios.
- `AnalysisSession.alive()` y un `AbortController` (`this.ctl`) cortan el ciclo al salir de la pantalla: no más consultas pagadas ni mensajes en otra sesión. Lo que depende de la posición se toma al pulsar el botón, no después de calcular.
- En la interfaz los errores de la IA pasan por `ClaudeAI.friendly` (sin nombres de proveedor ni modelo); el mensaje original queda en `ClaudeAI.lastError`, que se muestra en los ajustes. `ClaudeAI.clean` quita Markdown y guiones largos de las respuestas.
- Importar valida con `positionProblems` y limpia enroques con `cleanCastle`: una posición imposible abre el editor en lugar del análisis.
- La captura se lee como cuadrícula tal como se ve (filas de arriba a abajo) más qué bando está abajo; `boardFromRead` la convierte a casillas. La lectura puede fallar: el editor siempre se abre para revisar.
- La API pública de Chess.com no da partidas por número: `findChessComGame` recorre el archivo mensual de un jugador del más nuevo al más viejo y corta cuando los números de partidas en vivo del mes ya son menores.
- Las capturas no se guardan en `S`.

