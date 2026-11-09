---
description: Resume el cambio para alguien no técnico y deja clara la decisión que hace falta
argument-hint: "[cambio]"
---

Escribe un brief corto, en español llano, para alguien que no lee código. No uses jerga de implementación salvo el nombre de una pestaña que la persona ya ve (Escalera, Maestro, Puzzles, Posiciones, Partidas, Progreso). No edites archivos. No llames APIs de pago. No hagas push ni merge.

Cambio:

$ARGUMENTS

Si arriba no hay cambio descrito, usa el diff de la rama actual contra `main`.

Usa solo estas secciones, en este orden, con frases cortas:

- **Qué cambia.** Qué va a notar quien usa Casilla, sobre todo en el celular. Si la pantalla no cambia, dilo en la primera frase.
- **Por qué.** Qué problema de entrenamiento resuelve. Relaciónalo con la precisión en Mis errores, con completar la sesión de la Ruta, o con los errores por partida seria. Si no mueve ninguno de esos tres, dilo.
- **Riesgo.** El peor efecto realista para quien entrena: perder progreso, que se cobre una consulta a la IA, que se filtre la clave o el token, o que el celular quede inutilizable. Una o dos frases.
- **Cómo probarlo.** Pasos que una persona puede hacer en la app (en casilla.io o abriendo `index.html`), y nombra la prueba automática que corresponde: `python3 run.py` y, si el cambio toca el layout, `mobile.py`. Si no hay nada que probar en la pantalla, dilo.
- **Decisión.** Qué tiene que decir el dueño: aprobar, pedir un cambio o no mergear. Recuerda que un push a `main` publica al instante y que nada se mergea sin su OK explícito.

El texto debe poder pegarse en la descripción del PR bajo el título **Brief**.
