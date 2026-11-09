---
description: Ejecuta la tarea en silencio y entrega solo el resultado y un resumen breve
argument-hint: "[tarea]"
---

Modo silencioso. Ejecuta esta tarea en el repo de Casilla.

Tarea:

$ARGUMENTS

Conducta de este turno:

- Haz el trabajo. No narres el plan, no comentes cada paso y no ofrezcas alternativas que no se pidieron.
- No hagas preguntas salvo un bloqueo real: falta un dato sin el cual el resultado saldría mal, o la acción choca con una regla fija. Esas reglas son: no hacer push directo a `main`, no mergear sin el OK explícito del dueño, no llamar APIs de pago sin aprobación, no cambiar `casilla.v1` de forma incompatible, y no sacar del navegador la clave de la IA ni el token del gist.
- Si hay bloqueo, dilo en una frase y detente. No improvises alrededor de la regla.
- Sigue `CLAUDE.md` y `AGENTS.md`. Interfaz, commits y textos de la app van en español. Si escritorio y celular chocan, gana el celular (desde 360 px).
- Al terminar, entrega solo dos cosas:
  1. El resultado pedido.
  2. Un resumen breve: qué quedó hecho, qué archivos cambiaron y si hace falta una decisión del dueño.
