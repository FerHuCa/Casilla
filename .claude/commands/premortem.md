---
description: Imagina que el cambio fracasó en 6 a 12 meses y lista causas, señales tempranas y mitigaciones
argument-hint: "[cambio o feature]"
---

Haz un premortem de este cambio de Casilla. No edites archivos. No llames APIs de pago (nada de Anthropic ni OpenAI). No hagas push ni merge.

Cambio:

$ARGUMENTS

Si arriba no hay cambio descrito, usa el diff de la rama actual contra `main`.

Contexto que no puedes ignorar:

- Casilla es un solo `index.html`, sin build, más `sw.js` y Stockfish en un Web Worker. Un push a `main` publica al instante en casilla.io y en GitHub Pages.
- Quien entrena es una persona de habla hispana, por debajo de 1500, casi siempre desde el celular (pantallas desde 360 px). Si escritorio y celular chocan, gana el celular.
- El progreso vive en `localStorage` (`casilla.v1`, objeto `S`) y los puzzles en IndexedDB. La sincronización opcional sube a un gist. La clave de la IA y el token del gist no salen del navegador (`stripForSync`) ni van en los respaldos.
- Stockfish calcula jugadas y evaluaciones. La IA, si la persona pegó su clave, solo redacta, y solo después de un clic. Nada se consulta solo.
- Los criterios de éxito ya medidos en Progreso son tres: precisión en Mis errores, sesiones de la Ruta completadas y errores por partida seria. No inventes métricas nuevas.

Imagina que pasaron de 6 a 12 meses y este cambio fracasó: quien entrena dejó de usarlo, perdió progreso, entrenó peor, o el dueño tuvo que revertirlo en producción.

Responde en español. Ordena las causas de más probable a menos probable. Para cada una escribe:

1. **Causa.** Qué salió mal, atado a este diff y a este stack. Nada genérico que serviría para cualquier app.
2. **Señal temprana.** Qué se vería en las primeras semanas: en Progreso, en una partida, en `python3 run.py`, en `mobile.py` si el cambio toca el layout, o al abrir la app en 360 px. Sin telemetría nueva.
3. **Mitigación.** Qué habría que dejar resuelto antes de mergear.

Cierra con las causas que bloquearían el merge si siguen abiertas, y di si el cambio mueve el criterio 1, el 2, el 3 o ninguno.

El texto debe poder pegarse en la descripción del PR bajo el título **Premortem**.
