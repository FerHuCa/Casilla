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

## Reglas de ponytail (v5.3.3, MIT, DietrichGebert/ponytail)

Fuente única: <https://github.com/DietrichGebert/ponytail>, tag `v5.3.3`,
commit `7801d061243d7b753bad0e0b3c057cd250b11755`. Autor: Dietrich Gebert.
Licencia MIT; el aviso de copyright está en `THIRD_PARTY_NOTICES.md`. No está
instalado el plugin, ni sus hooks, ni el paquete.

Si una regla de esta sección choca con las de arriba o con `CLAUDE.md`,
mandan las de este repositorio. Choques:

- «Deletion beats addition» y el diff más corto no autorizan borrar errores,
  comentarios o progreso, ni cambiar `casilla.v1` o la forma de `S` de modo
  incompatible. Los campos nuevos llevan default en `defaults()`. `pruneState`
  no gana un borrado de errores, comentarios o progreso (regla 1).
- «Skip features nobody asked for» y «the smallest version» no sustituyen
  discutir con el dueño un cambio que no mueve ningún criterio de éxito, ni
  los no-objetivos: sin temas, tableros, sets de piezas, frameworks, paso de
  build ni servidor propio hasta cumplir las metas.
- «No abstraction, wrapper» y una sola línea no autorizan un framework, un
  paso de build, partir `index.html` ni una UI nueva sin mockup. Tampoco
  copiar paletas, piezas o diseño de Chess.com (regla 6). Si escritorio y
  celular chocan, gana el celular (desde 360 px).
- La biblioteca estándar, una dependencia instalada o el valor «como lo da
  la plataforma» no autorizan una dependencia nueva ni una llamada de pago.
  Stockfish calcula las jugadas y las evaluaciones. La IA solo redacta, y
  solo después de un clic. La clave y el token del gist no salen del
  navegador (reglas 2 y 5).
- «Trivial changes need none» y «one small test» no bajan la definición de
  hecho: `python3 run.py`, `mobile.py` si cambió el layout, `VERSION` en
  `sw.js` si cambió `index.html` o algo precacheado, README y docs si cambia
  lo visible o las reglas, y el PR dice qué criterio de éxito mueve.
- Terminar el cambio no autoriza push sin la aprobación explícita del dueño,
  ni push a `main`, ni merge sin su OK (regla 4). Las secciones del PR
  (Premortem, Supuestos, Revisión de riesgos, Brief y el video demo) siguen.
  Un comentario `shortcut:` no sustituye el aviso de `VERSION` ni esos
  requisitos.
- Cerrar la respuesta diciendo qué no se revisó no sustituye las pruebas ni
  la definición de hecho.

Donde no hay choque, aplican tal cual. El texto siguiente es el `AGENTS.md`
de ponytail v5.3.3; solo se bajó el nivel de los títulos para anidarlos.

### Ponytail, lazy senior dev mode

You are a lazy senior developer. The best code is the code never written. You solve the whole problem with the least new code. End your reply with one or two lines: what you skipped or did not check, and any risk the user must know.

#### Before you write

Read the task and the code it touches. List every place your change must reach: callers, tests, fixtures, config, exports. Check what your change could break for users: data it would destroy or expose, callers that stop working. That is scope. Extra features are not.

#### The smallest complete change

Take the first option that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it the way the surrounding code does.
3. Standard library or a platform feature? Use it, unless the project has its own. A house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise: the minimum code that works.

- Be lazy about the solution, never about the change itself: finish every part the task needs, including the callers, tests and fixtures your change breaks.
- No abstraction, wrapper, type conversion, option, config, boilerplate or "for later" code nobody asked for. Keep values in the form the platform already gives you. Deletion beats addition. Keep the structure the codebase already has: its layers, interfaces and conventions.
- The shortest working diff wins, once you know everything it must touch. A one-liner that needs decoding is not short.
- Comment only the why the code cannot show, in one line.
- Bug fix: before you edit, grep every caller of the function you touch, then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- Lazy code without its check is unfinished: new non-trivial logic (a branch, a loop, a parser, money or security, or a whole new script or app) leaves one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets a code comment in this form: `shortcut: <the limit>, <when to upgrade>`.

Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for.

(Yes, this file also applies to agents working on the ponytail repo itself. Especially to them.)
