---
description: Ataca el cambio en seguridad, privacidad, casos borde, abuso, rendimiento y regresiones
argument-hint: "[cambio a atacar]"
---

Ataca este cambio de Casilla. Busca fallos reales en el diff, no una lista genérica de riesgos. No edites archivos. No llames APIs de pago. No hagas push ni merge.

Cambio:

$ARGUMENTS

Si arriba no hay cambio descrito, usa el diff de la rama actual contra `main`.

Recorre solo las superficies que el diff puede tocar. Si una no aplica, dilo en una línea y sigue.

- **Seguridad.** HTML armado con PGN, nombres, comentarios o texto de una captura. Clave de la IA o token de gist que salga de `localStorage`, entre en un gist, en un respaldo o en un log. Service worker (`sw.js`) que sirva una versión vieja o de otro origen. `VERSION` sin subir cuando cambió algo que el precache guarda.
- **Privacidad.** Qué sale del navegador hacia Chess.com, Lichess, GitHub o Anthropic. Un gist secreto no es privado: quien tenga el enlace lo lee. Las partidas de Chess.com ya son públicas. La clave y el token no se sincronizan. Las capturas no se guardan en la app ni en los respaldos.
- **Casos borde.** Sin conexión, clave o token vencidos, partida a medias, FEN inválida, peón en la primera u octava fila, jaque al bando que no mueve, coronación, tiempo agotado sin material de mate, usuario de Chess.com que no existe, PGN con varias partidas, pantalla de 360 px.
- **Abuso.** Una consulta a la IA que se dispare sola, un bucle de sincronización, una ráfaga a Lichess o Chess.com, o un camino que copie puzzles de Chess.com fuera de la caché temporal del navegador.
- **Rendimiento.** Stockfish en el celular, una evaluación que trabe la partida, crecimiento de `index.html`, precache del service worker, IndexedDB.
- **Regresiones.** Cambio incompatible de `casilla.v1` (los campos nuevos van con default en `defaults()`), un criterio de éxito que deje de poder medirse con lo que Progreso ya guarda, un layout que se ve bien en escritorio y se rompe en 360 px, o una prueba de `tests/` que este diff dejaría en rojo (`python3 run.py` y, si hay layout, `mobile.py`).

Prioriza los hallazgos por severidad: crítica, alta, media, baja. Cada uno lleva qué falla, en qué flujo, cómo se reproduciría y cómo se mitiga. No reportes un fallo sin un camino en este diff.

El texto debe poder pegarse en la descripción del PR bajo el título **Revisión de riesgos**.
