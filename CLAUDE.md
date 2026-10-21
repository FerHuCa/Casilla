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
| Constantes | `SF_BASE`, `TIERS` (8 niveles de la escalera), `ENDGAMES`, `OPENINGS`, `THEMES`, `CATS` |
| Utilidades | `winPct`, `fmtEval`, `parsePGN`, `buildGame`, `openingName` |
| Estado | `KEY` (`casilla.v1` en localStorage), `defaults()`, `S`, `save()` = `saveLocal()` + `Sync.dirty()` |
| Motor | `workerFromCode`, `handshake`, `Engine` (cola con prioridades: ui 3, coach 2, barra/eval/análisis 1, batch 0; trabajos con tag cancelables) |
| Tablero | `Board`, `EvalBar` |
| App y sesiones | `App` (`App.setSession`), `HomeSession`, `PlaySession`, `PuzzleSession`, `OpeningSession`, `AnalysisSession`, `ReviewSession`, `EvalSession` |
| Reloj | `TIME_CONTROLS`, `GameClock`, `Clocks` |
| Maestro | `playerModel`, `openingTree`, `threatScan`, `Coach`, `ClaudeAI` (opcional, con la API key del usuario) |
| Explicaciones | `rootCause`, `bestIdea`, `categorize`, `explanationHTML` |
| Evaluación post partida | `Evaluator`, `buildEvaluation`, `evalNarrative`, `deepMoment`, `evalGraph` |
| Chess.com y Lichess | `jsonp`, `Analyzer`, `lichessDifficulty`, `mistakePuzzle` |
| Pantallas de inicio | `renderLadderHome`, `renderCoachHome`, `renderGamesHome`, `renderPositionsHome`, `renderProgressHome`, `HOMES` |
| Apariencia | `LOOK`, `LOOK_DEFAULT`, `applyLook`, `renderLook` |
| Sincronización | `SYNC_FILE` (`casilla-progreso.json` en un gist), `canon`, `syncKey`, `mergeState`, `Sync` |
| Arranque | `boot()` |

Dependencias externas (por CDN, sin instalar nada):
- chess.js 0.10.3 y stockfish.js 10.0.2 desde cdnjs. Stockfish corre en un Web Worker creado desde un Blob; el loader WASM se parchea para apuntar al CDN y cae a asm.js si falla.
- Google Fonts (incluye Press Start 2P y Pixelify Sans para el estilo 8 bits).
- APIs: Chess.com PubAPI (con fallback JSONP), Lichess `/api/puzzle/next`, GitHub Gists (sync), Anthropic API (Maestro con Claude, opcional).

### Apariencia

Se controla con atributos en `<html>`: `data-theme`, `data-font`, `data-board`, `data-pieces`, `data-style` (plano, relieve, bits). Cada opción tiene su bloque CSS `html[data-...=valor]` y una entrada en `LOOK`. Para agregar una opción: CSS con variables + entrada en `LOOK` + crédito en el pie y en el README si trae piezas o fuentes de terceros. Las piezas van embebidas como SVG en data URIs.

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
| `evalt.py` | Evaluación al final de la partida |
| `bar.py` | Barra de evaluación |
| `mobile.py` | Auditoría de móvil (desbordes, tamaños táctiles) |
| `sync.py` | Sincronización por gist |
| `look.py`, `relieve.py`, `bits.py` | Apariencia, estilo relieve y 8 bits |
| `exp.py` | Explicaciones de errores |

Variables opcionales: `CASILLA_APP` (ruta del HTML, por defecto `../index.html`), `CASILLA_DEPS`, `CASILLA_OUT` (capturas, por defecto `tests/out/`). Revisa las capturas en escritorio y en móvil después de cambios visuales. Un `ERR_FAILED` en la consola por Google Fonts es esperado en el sandbox.

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
