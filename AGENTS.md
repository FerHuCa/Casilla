# Agentes

Casilla es la app de ajedrez descrita en `CLAUDE.md` (un solo `index.html`, sin build). Lo de allí sigue vigente. Esta página añade la regla de los pull requests.

## Pull requests

Todo PR debe incluir en su descripción estas secciones:

- **Premortem**, generable con `/premortem`.
- **Supuestos**, generable con `/assumptions`.
- **Revisión de riesgos**, generable con `/redteam`.
- **Brief**, generable con `/brief`.

Además, todo PR lleva un **video demo** del cambio.

Nunca se hace push directo a `main`. Nada se mergea sin el OK explícito del dueño.

Los comandos están en `.claude/commands/`.
