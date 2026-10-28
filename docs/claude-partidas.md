# Comentarios de partida y ejercicios de tus errores con IA

Rama `feat/claude-partidas`. Mockups aprobados el 28 oct 2026 (1a a 1f, 2a, 2b, 3 y móvil 1c), con los cambios de Fernando: pista detrás de «Ver pista», nota de autoría, gasto marcado «aproximado», «Volver a comentar» y «Borrar comentario», y ningún nombre de proveedor visible.

## Lo que ya funcionaba en main (7bda07f) para «Mis errores»

Confirmado en `index.html`:

- **Errores guardados:** `Analyzer.analyzeGame` (partidas de Chess.com) y `saveEvaluation` (partidas jugadas en Casilla) guardan en `S.analyses[gid].mistakes[]` cada error con caída de 20 % o más: `{id, gid, ply, fen, played, playedUci, best, bestSan, drop, before, cat, phase, date, opp, color}`.
- **Origen `mine`:** `mistakePuzzle(m)` convierte un error en puzzle con `solution:[m.best]` (la mejor del motor) y `pickMine()` elige por frecuencia de categoría, peso por caída y menos peso si ya se resolvió (`S.puzzles.seen`). `App.mineFocus` filtra por categorías (Ruta, Progreso, Posiciones). Combinado usa `mine` un 40 % de las veces.
- **Validación:** `PuzzleSession.onUserMove` acepta la mejor del motor y, en `mine`, también otra jugada si el motor la evalúa casi igual (`winPct` a 6 puntos o menos).
- **Repaso espaciado:** `score()` llama `srsRecord(m, win)` para todo puzzle `mine`; `srsQueue()` arma el Repaso (1, 1, 3, 7, 14, 30 días; 10 nuevos por día).
- **Explicación del motor:** al terminar, `explain()` pide `explainMistake(m)`, que calcula y guarda en `m.exp` `{refPv, bestPv, evP, evB}`; `explanationHTML(m, exp)` arma «Lo que pasó en tu partida», «La mejor jugada» y «La idea», con «Ver tu jugada» y «Ver la mejor línea». Re-evaluar conserva `exp` (`prevExp` en `saveEvaluation`) y la sincronización junta los `exp` de ambos lados.

## Lo que agregué

- **Comentario de partida (1a a 1f):** `GameAI` en `index.html`, después de `ClaudeAI`. El bloque `#clbox` va en `ReviewSession.renderSide` (partidas de Chess.com analizadas), arriba de Momentos clave. Una sola llamada (`GameAI.comment`) con PGN, evaluación tras cada jugada (`an.w`), y los errores con su etiqueta, tipo, categoría, fase, FEN, evaluación antes y después, mejor jugada del motor y, si existen en `m.exp`, las líneas. La IA solo redacta y responde JSON (`{resumen:[...], errores:[{id, comentario, pista}]}`); `GameAI.parse` tolera bloques de código, texto alrededor, comas finales y comillas tipográficas. Las jugadas del bloque (5…Nxd5) y su tipo salen del análisis, no de la IA. Cancelar usa un `AbortController`. Si sales de la partida la respuesta se guarda igual (ya se pagó) y el bloque se repinta al volver.
- **Modelo:** Sonnet 5.5 por defecto (`GameAI.model()`); `S.settings.claude.gameModel` lo cambia (sin control en la interfaz; las pruebas usan Haiku 5.5). No hace falta marcar «Usar IA para los comentarios»: basta la clave, porque comentar es una acción explícita.
- **Ejercicios (2a, 2b):** en el panel del puzzle `mine`, «Ver pista» muestra `m.cx.hint`. Si no hay, consulta a la IA una vez (`GameAI.exercise`, tarea «ejercicio») y guarda pista y explicación en `m.cx`. Ver la pista cuenta como ayuda, igual que la del motor. Con pista de la IA disponible se oculta el botón «Pista» del motor. Al terminar se muestra «Explicación de la IA» y la explicación del motor sigue debajo; si no hay explicación guardada y la IA está activada, se pide sola. La solución sigue siendo `m.best` y el SRS no cambia; se agregó la nota «Entra al repaso espaciado: volverá en N días». Con origen Mis errores, el botón dice «Siguiente error».
- **Prompt caching:** el bloque fijo `GameAI.SYSTEM` (unos 700 a 900 tokens según estimación, por encima del mínimo de 512 de los modelos 5.5) va en `system` como `[{type:'text', text, cache_control:{type:'ephemeral'}}]`; lo comparten la tarea de partida y la de ejercicio, y no lleva nada variable. Se verifica en `cache_creation_input_tokens` / `cache_read_input_tokens` de `usage`.
- **Gasto aproximado (3):** `AISpend` en `localStorage['casilla.aiGasto']` (fuera de `S`, no se sincroniza). `ClaudeAI.post` suma el `usage` de toda respuesta correcta con `AI_PRICES` (entrada, escritura de caché de 5 min, lectura de caché, salida; fuente en el comentario del código). Cada comentario guarda su costo en `cx.usd`.
- **Textos sin nombres de proveedor:** la sección de clave dice «Comentarios con IA (opcional)», las opciones de modelo «Haiku 5.5: …» y «Probar conexión» usa `aiModelName`. «← Mis partidas» pasó a «← Partidas» en la partida de Chess.com y en la evaluación de partidas de Casilla.

## Datos

- `m.cx = {hint, text, model, at}` por error y `S.analyses[gid].cx = {summary:[...], model, at, usage, usd}` por partida. Opcionales: sin `cx` todo funciona como antes. `exp` no cambia.
- Límites: hasta 3 párrafos de 900 caracteres en el resumen, 700 por comentario, 300 por pista y 900 por explicación (`clipText`).
- Se conservan al re-analizar (`Analyzer.analyzeGame` y `saveEvaluation`) y `mergeState` toma el `cx` más reciente de cada lado. «Borrar comentario» quita `cx` de la partida y de sus errores (también pistas de ejercicios). Si otro dispositivo aún tiene el comentario, la sincronización lo trae de vuelta.
- `stripForSync` sigue quitando `settings.claude`; los comentarios sí se sincronizan.

## Qué se puede distinguir de un error (prioridad 6)

`ClaudeAI.errorKind(e)`:

| Lo que ve el navegador | Estado |
|---|---|
| `navigator.onLine` es false (antes de llamar o al fallar) | Sin conexión (1f), «Reintentar» se activa al volver la red |
| `fetch` lanza `TypeError` sin status, con red | «No se pudo conectar con el servicio de IA». No se puede saber si fue CORS, la red o una extensión: el navegador oculta la respuesta |
| 401 con `error.type` `authentication_error` | Clave inválida (1e) |
| 401 o 403 con otro tipo o mensaje (`permission_error`, organización con CORS deshabilitado si la respuesta se puede leer) | «El servicio de IA no dio permiso», con el número de error |
| `AbortError` | Cancelado, vuelve al botón |
| Respuesta sin el JSON pedido | «La IA respondió en un formato inesperado», no se guarda nada |
| Otros (429, 5xx, sin saldo) | Motivo de `ClaudeAI.friendly` y «Reintentar» |

Según una fuente secundaria (Simon Willison, ago 2024), las organizaciones que no permiten CORS responden 401; si esa respuesta trae los encabezados CORS la vemos como «no dio permiso», y si no los trae, como `TypeError`. Falta confirmarlo con una clave real.

## Pruebas

`tests/claude_partidas.py`, con la API simulada (`route.fulfill`, nada sale a la red) a 1280 y 390: modos ok, cargando (respuesta retenida) y cancelar, sin clave, 401 `authentication_error`, 403 `permission_error`, 401 de CORS de la organización, `TypeError` (route.abort), sin red (`context.set_offline`), respuesta sin JSON, `cache_control` en el cuerpo, mismo bloque fijo en todas las llamadas, cx guardado, stripForSync, mergeState, re-análisis, datos sin cx, pista y explicación en Mis errores, SRS, contador de gasto y que no se vea «Claude», «Anthropic» ni «Stockfish» fuera del pie. Capturas en `docs/capturas/claude-partidas/`.

## Pendiente

- Probar con una clave real (costo y `usage` reales, que la caché sí se lea en la segunda llamada, mensaje real de CORS de organización).
- El bloque solo está en las partidas de Chess.com (`ReviewSession`), como en el mockup. Las partidas jugadas en Casilla abren `EvalSession`, que ya tiene su comentario final con IA; agregar el bloque ahí necesita mockup.
- El panel del puzzle conserva su diseño actual (rating, origen, tema) y agrega los bloques del mockup; no se cambió el encabezado «Mis errores» del 2a.
