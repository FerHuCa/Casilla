# Casilla

App de entrenamiento de ajedrez en **un solo `index.html`** (~600 KB, sin build), más `sw.js` (modo sin conexión) y `engine/` (Stockfish 19 lite). Interfaz, README y commits en español. Licencia GPL-3.0.

- Producción: https://casilla.io (Cloudflare) y https://ferhuca.github.io/Casilla/. **Un push a `main` publica al instante.**
- Stack: HTML/CSS/JS sin frameworks; chess.js y Stockfish en Web Worker; APIs de Chess.com, Lichess, GitHub Gists (sync) y Anthropic (opcional, con la key del usuario).
- Estado en `localStorage` (`casilla.v1`, objeto `S`); puzzles en IndexedDB.

## Propósito

Casilla ayuda a jugadores de habla hispana por debajo de 1500 a mejorar en ajedrez repasando sus propios errores, con explicaciones que siempre salen de Stockfish.

## Usuario principal

Una persona de habla hispana, por debajo de 1500 de nivel, que entrena desde el celular (pantallas desde 360 px). Si una decisión favorece a la computadora y perjudica al celular, gana el celular. El texto de la interfaz habla de «la IA» y «el motor», sin nombres de proveedor.

## Criterios de éxito

Se miden con datos que la app ya guarda y muestra en Progreso y Maestro. No agregues seguimiento nuevo solo para medirlos. Las metas son valores iniciales: el dueño las ajusta tras la primera semana de datos.

1. **Precisión en Mis errores:** porcentaje de puzzles de Mis errores resueltos al primer intento y sin pista. Meta inicial: 70% después de 4 semanas de uso.
2. **Sesiones de la Ruta completadas:** días con la Sesión de hoy completada entre los días en que se abrió la app. Meta inicial: 60%.
3. **Errores por partida seria contra el objetivo de la etapa:** promedio de errores en las últimas 5 partidas serias contra el maestro. Objetivo: 2 o menos en la etapa 3 y 1 o menos en la etapa 4. Las etapas 1 y 2 no tienen objetivo de errores por partida.

## No objetivos

Hasta que los tres criterios de éxito alcancen su meta:

- No se agregan temas, tableros ni sets de piezas nuevos.
- No se agregan frameworks ni paso de build.
- No se agrega nada que necesite un servidor propio o que cueste dinero (ver regla 5).

Un cambio que no mueva ningún criterio de éxito se discute con el dueño antes de empezar.

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

## Definición de hecho

Un cambio está hecho solo si cumple todo esto:

- Las pruebas pasan: `python3 run.py` y, si cambió el layout, `mobile.py`.
- `VERSION` en `sw.js` está subida si cambió `index.html` o algo precacheado.
- El README y los docs de abajo están al día con lo que cambió.
- La descripción de la rama o el PR dice **qué criterio de éxito mueve** (1, 2 o 3) y cómo se notaría en los datos. Si no mueve ninguno, el PR lo dice y espera el OK del dueño.
- Funciona en una pantalla de 360 px.

## Más detalle (léelo solo si lo necesitas)

- `docs/mapa-index.md`: dónde está cada cosa dentro de `index.html`.
- `docs/despliegue.md`: Cloudflare, Pages, check runs y cómo abrir PRs por API.
- `docs/offline-y-dependencias.md`: service worker, precache, CDNs, memoria de puzzles y Claude en el análisis.
- `docs/apariencia.md`: presets, tableros, piezas y contraste.
- `docs/pruebas.md`: qué cubre cada prueba de `tests/`.
- `docs/claude-partidas.md`: comentario de partida y ejercicios de tus errores con IA (`cx`, caché, gasto, errores de clave).
- `docs/pendientes.md`: pendientes conocidos.
