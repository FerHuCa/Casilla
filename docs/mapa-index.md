# Mapa de index.html

Todo vive en `index.html`: CSS arriba, HTML del layout y un solo `<script>`. Busca estos símbolos (aparecen en este orden):

| Zona | Símbolos clave |
|---|---|
| Constantes | `SF_BASE`, `TIERS` (8 niveles de la escalera), `ENDGAMES`, `OPENINGS`, `THEMES`, `CATS`, `PLAN` (4 etapas de la ruta a 1500), `COACH_MODES` |
| Utilidades | `winPct`, `fmtEval`, `parsePGN`, `buildGame`, `openingName` |
| Estado | `KEY` (`casilla.v1` en localStorage), `defaults()`, `S`, `save()` = `saveLocal()` + `Sync.dirty()` |
| Motor | `workerFromCode`, `handshake`, `Engine` (cola con prioridades: ui 3, coach y Maestro del análisis 2, barra/eval/análisis 1, batch 0; trabajos con tag cancelables: `ui`, `coach`, `bar`, `ana`, `maestro`, `batch`) |
| Tablero | `Board`, `EvalBar` |
| App y sesiones | `App` (`App.setSession`), `HomeSession`, `PlaySession`, `PuzzleSession`, `OpeningSession`, `AnalysisSession`, `ReviewSession`, `EvalSession` |
| Reloj | `TIME_CONTROLS`, `GameClock`, `Clocks` |
| Maestro | `playerModel`, `openingTree`, `threatScan`, `Coach` (con `askThreat`/`answerThreat` en modo Amenazas), `ANA_OPTIONS`, `modelPickHTML`/`bindModelPick`, `ClaudeAI` (opcional, con la API key del usuario; `tune` ajusta pensamiento y esfuerzo por modelo, `readBoard` lee capturas, `converse` es el ciclo con herramientas, `friendly` y `clean` para la interfaz, `errorKind` clasifica fallas), `AI_PRICES`/`usageCost`/`AISpend` (gasto aproximado en `casilla.aiGasto`), `spendHTML`, `GameAI` (comentario de partida y pista/explicación de errores en `cx`; ver `docs/claude-partidas.md`), `goToAIKey` |
| Análisis con el Maestro | `linesFromInfo`, `sanLine`, `staticFacts`, `synthE` (estructura mínima para reutilizar `bestIdea` y `rootCause`), `ideaCtx` (contexto para `bestIdea`), `altText` (segunda línea, con mates), `localExplain`/`explainMove` (sin IA), `compareToBest` (comparación de la herramienta), `MAESTRO_TOOL` (`evaluar_jugadas`: la IA pide al motor que calcule), `maestroSystem`, `AnalysisSession` (posición suelta o partida con `main`, `ply` y variante en `vars`; caché de líneas por FEN; en el celular la última respuesta va también en `#tip` con `renderTip`) |
| Editor e importación | `positionProblems`, `castleRights`, `cleanCastle`, `EditorSession` (paleta en `#controls` en el celular y en `#edpal` del panel en la computadora; `Board.onTap`), `prepImage`, `boardFromRead`, `readShot`, `READ_SYSTEM`/`READ_PROMPT`, `firstGame` (primera partida de un PGN), `chessComLink`, `lichessLink`, `lichessGame` (exportar una partida de Lichess; sin respuesta pide pegar el PGN), `parseImport`, `findChessComGame`, `resolveImport`, `recentGames`, `openRecent`; pestaña Importar en `renderPositionsHome` (`App.posTab = 'importar'`, el valor viejo `fen` se acepta) |
| Revisión de amenazas | `threatsFor` (capturas, mate en una y jaques que ganan material con `checkWin`), `kingSquare`, `threatStats`; historial en `S.threats.hist`; `Board.onTap` recibe el toque mientras hay pregunta |
| Repaso espaciado | `DAY_START` (el día cambia a las 4), `dayKey`, `dueIn`, `srsQueue`, `srsRecord`, `srsStats`; tarjetas en `S.srs[idDelError]` |
| Ruta a 1500 | `planState`, `planDay`, `planStage`, `planSteps`, `planEndgame`, `planCheck`, `planStreak`, `stageChecks`, `planGo`, `planHTML`; datos en `S.plan` |
| Evidencia (Progreso) | `EVID_WEEKS`, `EVID_FIELDS`, `evidState`, `dkDate`/`dkAdd`/`dkDiff` (aritmética de `dayKey`), `evidPrune` (60 días más los 28 de la prueba), `evidTouch` (marca el día al abrir y al volver), `evidPuzzle` (desde `PuzzleSession.score`), `evidStats` (4 semanas desde `S.evid.start`), `evidHTML`, `evidExport` (solo números y fechas), `bindEvid`; datos en `S.evid` y `ser` en `S.coach.games` (partida seria) |
| Explicaciones | `rootCause`, `bestIdea` (acepta `ctx.quiet` y `ctx.noOpening` para el análisis de posiciones sueltas), `categorize`, `explanationHTML` |
| Evaluación post partida | `Evaluator` (varios trabajos, el más reciente primero, en pausa mientras se juega), `evalJobFor` (reabre sin recalcular), `buildEvaluation`, `saveEvaluation`, `evalNarrative`, `deepMoment`, `moveComment` (comentario de cada jugada), `evalGraph`, `EvalSession` |
| Historial de Casilla | `S.played` (partidas jugadas aquí, se guardan al terminar su evaluación), `openPlayed`, `playedHTML`; el análisis con `best` y `pv` vive en `S.analyses[gid]` |
| Chess.com y Lichess | `jsonp`, `chessComJSON` (reintenta 429 hasta 3 veces), `Analyzer`, `lichessDifficulty`, `mistakePuzzle` |
| Pantallas de inicio | `renderLadderHome`, `renderCoachHome`, `renderGamesHome`, `renderPositionsHome`, `renderProgressHome`, `HOMES` |
| Apariencia | `LOOK`, `LOOK_GROUPS`, `PRESETS`, `withCustom`, `migrateLook`, `lookPref`, `lookFiles`, `applyLook`, `renderLook` |
| Sincronización | `SYNC_FILE` (`casilla-progreso.json` en un gist), `canon`, `syncKey`, `mergeState`, `Sync` |
| Arranque | `boot()`, `Offline` (registra `sw.js`) |

Los campos nuevos entran con valor por defecto en `defaults()` y se fusionan al cargar. Los datos de versiones viejas deben seguir abriendo.
