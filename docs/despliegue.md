# Despliegue y PRs

- En local se abre con doble clic o como página estática (sin build).
- Producción: https://casilla.io (Cloudflare Workers Builds; también casilla.murcielagolambo.workers.dev).
- Alterna: https://ferhuca.github.io/Casilla/ (GitHub Pages, rama `main`, raíz).
- Ambos se despliegan solos con cada push a `main`. Estado: `gh api repos/FerHuCa/Casilla/commits/<sha>/check-runs`.
- Las ramas no se despliegan: en un PR el check «Workers Builds» de Cloudflare sale en falla y es normal (pasó en los PR #3 a #7). Solo cuenta el de `main`.
- Desde el sandbox no se puede abrir casilla.io (el proxy bloquea github.io, cdnjs y el dominio): confirmar en un navegador después de publicar.

Desde una sesión de Claude Code, `gh pr create` falla (GraphQL no está disponible): los PR se abren y fusionan con la API REST, por ejemplo `gh api repos/FerHuCa/Casilla/pulls --method POST --input pr.json` y `gh api repos/FerHuCa/Casilla/pulls/<n>/merge --method PUT -f merge_method=merge`. El clon del sandbox es de una sola rama: para que una rama nueva tenga seguimiento, agrega su refspec (`git config --add remote.origin.fetch '+refs/heads/<rama>:refs/remotes/origin/<rama>'`) antes del push.

Después de publicar en `main`, confirma los check runs. Los commits llevan la identidad noreply y los trailers de la sesión.
