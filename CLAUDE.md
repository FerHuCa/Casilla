# Casilla: notas para retomar el trabajo

Este archivo es para quien abra el repo en una sesión nueva (persona o Claude). Explica cómo está hecha la app, cómo probarla, cómo publicarla y qué reglas seguir. El README es para usuarios; este archivo es para desarrollo.

## Qué es

Casilla es una app de entrenamiento de ajedrez en **un solo archivo HTML** (`index.html`, unos 420 KB, sin build). Se abre local con doble clic o se sirve como página estática.

- Producción: https://casilla.io (Cloudflare Workers Builds, también en casilla.murcielagolambo.workers.dev)
- Alterna: https://ferhuca.github.io/Casilla/ (GitHub Pages, rama `main`, raíz)
- Ambos se despliegan solos al hacer push a `main`. Para ver el estado: `gh api repos/FerHuCa/Casilla/commits/<sha>/check-runs`
- Licencia GPL-3.0 (por Stockfish). Idioma de la interfaz y del README: español.

## Estructura de index.html

Todo vive en el mismo archivo: CSS arriba, HTML del layout y un solo `<script>` grande. Para ubicarte, busca estos símbolos (aparecen en este orden):

| Zona | Símbolos clave |
|---|---|
| Constantes | `SF_BASE`, `TIERS` (8 niveles de la escalera), `ENDGAMES`, `OPENINGS`, `THEMES`, `CATS`, `PLAN` (4 etapas de la ruta a 1500), `COACH_MODES` |
| Utilidades | `winPct`, `fmtEval`, `parsePGN`, `buildGame`, `openingName` |
| Estado | `KEY` (`casilla.v1` en localStorage), `defaults()`, `S`, `save()` = `saveLocal()` + `Sync.dirty()` |
| Motor | `workerFromCode`, `handshake`, `Engine` (cola con prioridades: ui 3, coach 2, barra/eval/análisis 1, batch 0; trabajos con tag cancelables) |
| Tablero | `Board`, `EvalBar` |
| App y sesiones | `App` (`App.setSession`), `HomeSession`, `PlaySession`, `PuzzleSession`, `OpeningSession`, `AnalysisSession`, `ReviewSession`, `EvalSession` |
| Reloj | `TIME_CONTROLS`, `GameClock`, `Clocks` |
| Maestro | `playerModel`, `openingTree`, `threatScan`, `Coach` (con `askThreat`/`answerThreat` en modo Amenazas), `ClaudeAI` (opcional, con la API key del usuario; `tune` ajusta pensamiento y esfuerzo por modelo, `readBoard` lee capturas, `converse` es el ciclo con herramientas) |
| Análisis con el Maestro | `linesFromInfo`, `sanLine`, `staticFacts`, `synthE` (estructura mínima para reutilizar `bestIdea` y `rootCause`), `localExplain`/`explainMove` (sin IA), `MAESTRO_TOOL` (`evaluar_jugadas`: la IA pide al motor que calcule), `maestroSystem`, `AnalysisSession` (posición suelta o partida con `main`, `ply` y variante en `vars`; caché de líneas por FEN) |
| Editor e importación | `positionProblems`, `castleRights`, `EditorSession` (paleta en `#controls`, `Board.onTap`), `prepImage`, `boardFromRead`, `readShot`, `READ_SYSTEM`/`READ_PROMPT`, `chessComLink`, `parseImport`, `findChessComGame`, `resolveImport`, `recentGames`, `openRecent`; pestaña Importar en `renderPositionsHome` (`App.posTab = 'importar'`, el valor viejo `fen` se acepta) |
| Revisión de amenazas | `threatsFor` (capturas, mate en una y jaques que ganan material con `checkWin`), `kingSquare`, `threatStats`; historial en `S.threats.hist`; `Board.onTap` recibe el toque mientras hay pregunta |
| Repaso espaciado | `DAY_START` (el día cambia a las 4), `dayKey`, `dueIn`, `srsQueue`, `srsRecord`, `srsStats`; tarjetas en `S.srs[idDelError]` |
| Ruta a 1500 | `planState`, `planDay`, `planStage`, `planSteps`, `planEndgame`, `planCheck`, `planStreak`, `stageChecks`, `planGo`, `planHTML`; datos en `S.plan` |
| Explicaciones | `rootCause`, `bestIdea`, `categorize`, `explanationHTML` |
| Evaluación post partida | `Evaluator` (varios trabajos, el más reciente primero, en pausa mientras se juega), `evalJobFor` (reabre sin recalcular), `buildEvaluation`, `saveEvaluation`, `evalNarrative`, `deepMoment`, `moveComment` (comentario de cada jugada), `evalGraph`, `EvalSession` |
| Historial de Casilla | `S.played` (partidas jugadas aquí, se guardan al terminar su evaluación), `openPlayed`, `playedHTML`; el análisis con `best` y `pv` vive en `S.analyses[gid]` |
| Chess.com y Lichess | `jsonp`, `Analyzer`, `lichessDifficulty`, `mistakePuzzle` |
| Pantallas de inicio | `renderLadderHome`, `renderCoachHome`, `renderGamesHome`, `renderPositionsHome`, `renderProgressHome`, `HOMES` |
| Apariencia | `LOOK`, `LOOK_GROUPS`, `PRESETS`, `withCustom`, `migrateLook`, `lookPref`, `lookFiles`, `applyLook`, `renderLook` |
| Sincronización | `SYNC_FILE` (`casilla-progreso.json` en un gist), `canon`, `syncKey`, `mergeState`, `Sync` |
| Arranque | `boot()`, `Offline` (registra `sw.js`) |

### Sin conexión (sw.js)

`sw.js` es el service worker. Solo se registra por http/https (`Offline.start()` en `boot()`), no en file://. En `install` precachea `LOCAL` (sitio, fuentes, logo, favicons, íconos) y `engine/` (Stockfish 19 lite .js/.wasm) y `CDN` (chess.js, Stockfish 10 .js/.wasm.js/.wasm). Estrategias: navegación e `index.html` con red primero (sin red, la copia guardada); lo demás del mismo origen y de cdnjs con caché primero, guardando lo nuevo; APIs (Chess.com, Lichess, Anthropic, GitHub) pasan directo. La clave de caché ignora hash y query (el worker de Stockfish 19 lleva la ruta del .wasm en el hash).

**Al cambiar sw.js o un archivo precacheado, sube `VERSION`** en sw.js: crea `casilla-<VERSION>` y `activate` borra las cachés `casilla-*` viejas. La versión nueva ya no hace `skipWaiting` sola: queda en espera y `Offline.prompt()` muestra el aviso 3 (`#upd`, «Hay una versión nueva.»). **Actualizar** manda `SKIP_WAITING` y recarga en `controllerchange` (`hadCtl` evita recargar en la primera instalación). **Ahora no** guarda `casilla.updLater` en localStorage y la siguiente apertura aplica la espera; el navegador también la activa cuando no quedan pestañas. El pie (`#ver`) pide `GET_VERSION` al SW activo por MessageChannel (respaldo: nombre de la caché `casilla-*`); sin SW dice «Sin modo sin conexión.». El registro usa `updateViaCache:'none'` y al volver la red (`online`) llama `reg.update()`. Si agregas una fuente, un ícono o cambias la versión de un CDN, agrégalo a `LOCAL`/`CDN`. `piece/` y `board/` no se precachean (`ON_USE`): se guardan al usarse y en `activate` se copian a la caché nueva antes de borrar la vieja.

Avisos sin red (mockups aprobados 1, 2a, 2b, 3, 5a, 5b, estilo B, solo tokens existentes): objeto `Net` (barra `#offBar`, píldora, notas). No agregues UI sin mockup aprobado.

Memoria de puzzles (`PuzzleStore`): IndexedDB `casilla-puzzles`, aparte de la caché del SW. Objetivo 200 de Lichess (`/api/puzzle/batch/{angle}`, 50 con temas de la etapa; puzzles CC0 según database.lichess.org). Chess.com no se guarda: su User Agreement (chess.com/legal/user-agreement, sección 4.C) prohíbe descargar o copiar información salvo la caché temporal del navegador. Relleno en serie con red, 20 s entre peticiones, 429 de Lichess espera 60 s y duplica (máx. 1 h). `done(id)` borra el resuelto y lo anota en `casilla.pzSolved` (últimos 500) para no volver a guardarlo. Más de 14 días se renuevan (20 por pasada). Sin red, `PuzzleSession.fromStore()` sirve guardados y el 5a (`offPzNote`) solo desactiva fuentes sin guardados.

IA sin red: `ClaudeAI.ready()` exige `navigator.onLine`, así que sin red la IA se comporta como apagada (frases integradas) y vuelve sola. No hay UI nueva para esto todavía (pendiente de mockup). Caché medida: unos 4.7 MB en 27 archivos (`navigator.storage.estimate` reporta unos 7.4 MB en Chromium). Pruebas en `offline.py` y `cfredirect.py`.

Reglas del precache (aprendidas en producción): Cloudflare responde 307 en `/index.html` y `*.html`, así que nunca precachear URLs `.html`; la shell se guarda como `./` (el scope). Stockfish 19 lite vive en `engine/` porque jsDelivr da 403 a `stockfish@19` (paquete > 150 MB) y un solo 403 aborta `cache.addAll` y deja la app sin service worker. Antes de publicar, pide con `curl -sI` cada URL del precache en producción.

Dependencias externas (por CDN, sin instalar nada):
- chess.js 0.10.3 desde cdnjs. Stockfish 19 lite de un hilo (npm `stockfish` 19.0.1) alojado en `engine/` (GPL-3.0; jsDelivr da 403 a ese paquete), en un Web Worker creado desde un Blob; la ruta del .wasm va en el hash del worker. Si falla, cae a stockfish.js 10.0.2 de cdnjs (WASM y luego asm.js). `?sf=10` fuerza el 10.
- Todas las fuentes van autoalojadas en `fonts/` (OFL). Las de los presets no Clásicos se declaran con @font-face y el navegador solo las baja cuando se usan. Ya no se usa Google Fonts.
- APIs: Chess.com PubAPI (con fallback JSONP), Lichess `/api/puzzle/next`, GitHub Gists (sync), Anthropic API (Maestro con Claude, opcional).

### Claude en el análisis

- Dos modelos: `model` (comentarios en partida, por defecto Haiku 5.5) y `anaModel` (análisis y capturas, por defecto Opus 5.5). Ambos viven en `S.settings.claude`, que nunca se sincroniza.
- Opus 5.5 rechaza `thinking: disabled` y `between_tools`: se manda sin `thinking`, con `output_config.effort` bajo y `max_tokens` con espacio para pensar. Haiku usa `disabled` y Sonnet `between_tools`. Opus y Sonnet rechazan `tool_choice` forzado; al llegar al límite de consultas se manda `tool_choice: none`.
- En el ciclo con herramientas, el contenido de la respuesta (incluidos los bloques de pensamiento) se devuelve sin cambios.
- La captura se lee como cuadrícula tal como se ve (filas de arriba a abajo) más qué bando está abajo; `boardFromRead` la convierte a casillas. La lectura puede fallar: el editor siempre se abre para revisar.
- La API pública de Chess.com no da partidas por número: `findChessComGame` recorre el archivo mensual de un jugador del más nuevo al más viejo y corta cuando los números de partidas en vivo del mes ya son menores.
- Las capturas no se guardan en `S`.

### Apariencia

El usuario elige uno de 8 presets (`PRESETS`) y, aparte, puede cambiar Tablero y Piezas (`LOOK_GROUPS` arma los grupos del panel). En `S.settings.look` se guarda `{preset, mode, board?, pieces?}`; `board` y `pieces` solo existen si difieren del preset y si el id está en `LOOK` (`withCustom`). `mode` (claro u oscuro) aplica solo a Clásico y Relieve. Elegir otro preset o «Volver a [preset]» descarta la personalización. El formato viejo `{theme, font, board, pieces, style}` pasa por `migrateLook` al cargar, al importar un respaldo y al recibir datos del gist: el preset sale de la regla de la spec B, sección 11 (`migratePreset`), y tablero/piezas distintos quedan como personalización (pruebas en `migracion.py` y `apariencia_migracion.py`).

Las piezas nuevas (Spatial, Fantasy, Shapes, Firi, Pirouetti, Letras) viven en `piece/<set>/{w,b}{K,Q,R,B,N,P}.svg` y las texturas (Arce, Veteado) en `board/`; el CSS las pide solo con `html[data-pieces=...]`/`html[data-board=...]` activos o con las miniaturas `.pz-<set>-xx` del panel. `applyLook` precarga los archivos del set activo y, si alguno falla (sin red y sin caché), usa el del preset sin tocar lo guardado. Licencias en `piece/LICENSE.md`, `board/LICENSE.md` y `docs/licencias/`. Los resaltes usan `--hlLast`/`--hlSel` (por defecto los de siempre; más marcados en los tableros nuevos, medidos en `apariencia_contraste.py`). `applyLook` traduce el preset a atributos en `<html>`: `data-theme`, `data-font`, `data-board`, `data-pieces`, `data-style` (plano, relieve, bits). Cada opción tiene su bloque CSS `html[data-...=valor]` y una entrada en `LOOK`. Para agregar una opción: CSS con variables + entrada en `LOOK` + crédito en el pie y en el README si trae piezas o fuentes de terceros. Las piezas van embebidas como SVG en data URIs.

## Reglas que no se rompen

1. **Compatibilidad con datos guardados.** Nunca cambies la clave `casilla.v1` ni la forma de `S` de modo incompatible. Campos nuevos se agregan con valor por defecto en `defaults()` y se fusionan al cargar. Los datos de versiones viejas deben seguir abriendo.
2. **Secretos.** La API key de Claude y el token del gist se quedan solo en el navegador del usuario. Nunca se suben al gist, al repo ni a exportaciones (`stripForSync`).
3. **Commits** con la identidad noreply de GitHub, nunca con el correo personal:
   ```
   git -c user.name=FerHuCa -c user.email=250413865+FerHuCa@users.noreply.github.com commit ...
   ```
4. **Push solo con aprobación explícita** del dueño en cada ocasión (publica en casilla.io al instante).
5. **No copiar** paletas, piezas ni diseño protegidos de Chess.com. Inspirarse está bien; calcar, no.
6. **Sin guiones largos (em dash)** en textos del README, la interfaz y los mensajes.
7. Mensajes de commit en español, en imperativo ("Agregar...", "Corregir...").

## Cómo probar

Las pruebas están en `tests/` y usan Playwright (Python) con toda la red simulada: CDN, Chess.com, Lichess, Claude y GitHub responden con datos falsos, así que corren sin internet.

```
cd tests
npm install                 # baja chess.js y stockfish.js para servirlos en lugar del CDN
pip install playwright      # si no está; en el sandbox de Claude ya viene Chromium
python3 run.py              # flujo general: escalera, puzzles, partidas, posiciones, progreso
```

Otras pruebas (todas se basan en el arnés de `run.py` y `coach.py`):

| Archivo | Qué cubre |
|---|---|
| `coach.py`, `coach2.py` | Maestro: comentarios, adaptación, jugar contra él |
| `ruta.py` | Ruta a 1500: sesión del día, táctica de la etapa con tema oculto, repaso espaciado, modo Amenazas, finales nuevos, sync y datos viejos |
| `evalt.py` | Evaluación al final de la partida |
| `evalnav.py` | Recorrer la evaluación jugada por jugada: orden, comentarios y que nada regrese el tablero solo |
| `claude.py` | Conexión con Claude: encabezados, pensamiento apagado por modelo, reintento y errores (API simulada) |
| `historial.py` | Partidas de Casilla en Partidas, evaluación en segundo plano, puzzles con sus errores, sync |
| `bar.py` | Barra de evaluación |
| `mobile.py` | Auditoría de móvil (desbordes, tamaños táctiles) |
| `sync.py` | Sincronización por gist |
| `offline.py` | Service worker por http: precache, modo avión a 390 px (`context.set_offline`), Escalera, Partidas y análisis sin red, respaldo Stockfish 10, IA apagada sin red y de vuelta, versión nueva que reemplaza a la vieja |
| `look.py`, `relieve.py`, `bits.py`, `migracion.py` | Apariencia por presets, estilo relieve y 8 bits, migración de preferencias |
| `motor.py` | Stockfish 19 por defecto y `?sf=10` (por http local) |
| `cfredirect.py` | Servidor que imita a Cloudflare (307 en `.html`) y jsDelivr con 403: instalación del SW y navegación sin red a `/`, `/index.html` y `/?x` |
| `offline_ui.py` | Avisos sin red 1, 2a, 2b, 5a, 5b, Táctica sin red, versión en el pie, aviso 3 Actualizar / Ahora no, 8 presets; capturas en `CASILLA_SHOTS` |
| `puzzle_store.py` | Memoria de puzzles en IndexedDB: 200 de Lichess, relleno en serie, 429, resueltos, Chess.com sin guardar, uso sin red y 5a |
| `e2e_real.py` | Orígenes reales (sin mocks): llena la memoria contra lichess.org y luego modo avión. Usa red real; no correr en bucle (429) |
| `apariencia_sets.py` | Tablero y piezas por separado: 12 SVG por set, solo se pide el set activo, Personalizado y «Volver a», cambio de estilo; por http, caché al usar, sin red y al actualizar |
| `apariencia_migracion.py` | `{preset, mode}`, formato nuevo con personalización e ids inexistentes, formato viejo; al abrir, respaldo y gist |
| `apariencia_contraste.py` | ΔE00 y contraste de última jugada y selección sobre cada tablero (umbral documentado en el archivo) |
| `capturas_apariencia.py` | Genera `docs/capturas/apariencia/` a 1280 y 390 |
| `exp.py` | Explicaciones de errores |
| `maestro_analisis.py` | Análisis con el Maestro: importar (captura con lectura simulada, FEN, PGN, link de Chess.com, partidas recientes), editor, explicaciones sin IA, ciclo con herramientas de la IA (Opus sin `thinking`), errores de la IA y auditoría móvil a 390 |

Variables opcionales: `CASILLA_APP` (ruta del HTML, por defecto `../index.html`), `CASILLA_DEPS`, `CASILLA_OUT` (capturas, por defecto `tests/out/`). Revisa las capturas en escritorio y en móvil después de cambios visuales. 

Chequeo rápido de sintaxis del script:
```
python3 -c "import re;s=open('index.html').read();open('/tmp/c.js','w').write(re.findall(r'<script>([\s\S]*?)</script>',s)[-1])" && node --check /tmp/c.js
```

## Flujo para un cambio

1. Editar `index.html` directamente.
2. Probar con `tests/` (al menos `run.py` y la prueba del área tocada, más `mobile.py` si cambió el layout).
3. Actualizar el README si cambia algo visible para el usuario.
4. Commit con la identidad noreply y los trailers de la sesión.
5. Preguntar antes de `git push origin main`. Después, confirmar los check runs.

## Pendientes conocidos

- **Cuentas de usuario con Firebase** (inicio de sesión con Google, base de datos para que amigos tengan su cuenta), manteniendo la sincronización por gist como alternativa. Se pospuso; hace falta el `firebaseConfig` del proyecto cuando se retome.
- No se pudo verificar casilla.io desde el sandbox (el proxy bloquea github.io, cdnjs y el dominio); confirmar en un navegador después de cada push.
