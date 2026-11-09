---
description: Lista los supuestos del cambio, cómo validar cada uno y qué pasa si es falso
argument-hint: "[cambio]"
---

Saca a la luz los supuestos de este cambio de Casilla. No edites archivos. No llames APIs de pago. No hagas push ni merge.

Cambio:

$ARGUMENTS

Si arriba no hay cambio descrito, usa el diff de la rama actual contra `main` y, si existe, el texto del PR.

Separa dos listas:

- **Explícitos.** Lo que el cambio o el PR afirma en voz alta.
- **Implícitos.** Lo que el código da por cierto sin decirlo.

Cuando el diff los toque, mira en especial estos supuestos de Casilla: `casilla.v1` sigue siendo compatible y los campos nuevos tienen default en `defaults()`; Stockfish calcula y la IA solo redacta, y solo tras un clic; el celular desde 360 px es el cliente principal; no hay servidor propio; el service worker y `VERSION` siguen alineados con lo precacheado; la clave y el token no viajan; Lichess, Chess.com, GitHub y Anthropic pueden fallar o estar ausentes.

Para cada supuesto escribe:

1. El supuesto, en una frase.
2. **Cómo validarlo** con lo que ya existe: el diff, `python3 run.py`, `mobile.py` si hay layout, una prueba manual en 360 px, o un dato que Progreso ya muestra. No propongas telemetría nueva ni una llamada de pago.
3. **Si es falso:** a quién afecta y si el merge debería esperar.

Marca los supuestos que, de fallar, rompen progreso guardado, filtran un secreto o publican en `main` sin red de seguridad.

El texto debe poder pegarse en la descripción del PR bajo el título **Supuestos**.
