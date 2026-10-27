# Pruebas

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
| `claude.py` | Conexión con Claude: encabezados, pensamiento por modelo (con Opus), los dos modelos en «Probar conexión», reintento y errores (API simulada) |
| `historial.py` | Partidas de Casilla en Partidas, evaluación en segundo plano, puzzles con sus errores, sync |
| `bar.py` | Barra de evaluación |
| `mobile.py` | Auditoría de móvil (desbordes, tamaños táctiles) |
| `sync.py` | Sincronización por gist |
| `offline.py` | Service worker por http: precache, modo avión a 390 px (`context.set_offline`), Escalera, Partidas y análisis sin red, respaldo Stockfish 10, IA apagada sin red y de vuelta, versión nueva que reemplaza a la vieja |
| `look.py`, `relieve.py`, `bits.py`, `migracion.py` | Apariencia por presets (incluye Medianoche, Cacao y Ciruela), estilo relieve y 8 bits, migración de preferencias |
| `motor.py` | Stockfish 19 por defecto y `?sf=10` (por http local) |
| `cfredirect.py` | Servidor que imita a Cloudflare (307 en `.html`) y jsDelivr con 403: instalación del SW y navegación sin red a `/`, `/index.html` y `/?x` |
| `offline_ui.py` | Avisos sin red 1, 2a, 2b, 5a, 5b, Táctica sin red, versión en el pie, aviso 3 Actualizar / Ahora no, 11 presets; capturas en `CASILLA_SHOTS` |
| `puzzle_store.py` | Memoria de puzzles en IndexedDB: 200 de Lichess, relleno en serie, 429, resueltos, Chess.com sin guardar, uso sin red y 5a |
| `e2e_real.py` | Orígenes reales (sin mocks): llena la memoria contra lichess.org y luego modo avión. Usa red real; no correr en bucle (429) |
| `apariencia_sets.py` | Tablero y piezas por separado: 12 SVG por set, solo se pide el set activo, Personalizado y «Volver a», cambio de estilo; por http, caché al usar, sin red y al actualizar |
| `apariencia_migracion.py` | `{preset, mode}`, formato nuevo con personalización e ids inexistentes, formato viejo; al abrir, respaldo y gist |
| `apariencia_contraste.py` | ΔE00 y contraste de última jugada y selección sobre cada tablero (umbral documentado en el archivo) |
| `capturas_apariencia.py` | Genera `docs/capturas/apariencia/` a 1280 y 390 |
| `exp.py` | Explicaciones de errores |
| `maestro_analisis.py` | Análisis con el Maestro: importar (captura con lectura simulada, FEN, PGN pegado o en archivo, links de Chess.com y Lichess, partidas recientes, posiciones imposibles al editor), editor, explicaciones sin IA (también en posiciones decididas), tarjeta de modelos, ciclo con herramientas de la IA (Opus sin `thinking`, Sonnet `between_tools`), cancelación al salir, errores de la IA sin nombres de proveedor y auditoría móvil a 390 |

Variables opcionales: `CASILLA_APP` (ruta del HTML, por defecto `../index.html`), `CASILLA_DEPS`, `CASILLA_OUT` (capturas, por defecto `tests/out/`). Revisa las capturas en escritorio y en móvil después de cambios visuales. 

Chequeo rápido de sintaxis del script:
```
python3 -c "import re;s=open('index.html').read();open('/tmp/c.js','w').write(re.findall(r'<script>([\s\S]*?)</script>',s)[-1])" && node --check /tmp/c.js
```

Si agregas o cambias una prueba, actualiza esta lista.

