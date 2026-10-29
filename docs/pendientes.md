# Pendientes conocidos

- **Cuentas de usuario con Firebase** (inicio de sesión con Google, base de datos para que amigos tengan su cuenta), manteniendo la sincronización por gist como alternativa. Se pospuso; hace falta el `firebaseConfig` del proyecto cuando se retome.
- No se pudo verificar casilla.io desde el sandbox (el proxy bloquea github.io, cdnjs y el dominio); confirmar en un navegador después de cada push.
- **IA con una clave real:** la lectura de capturas y las explicaciones solo se probaron con la API simulada (y una lectura manual de tres capturas de Chess.com). Falta probar de punta a punta en casilla.io y revisar el costo real contra `ANA_OPTIONS`.
- **Comentarios de partida con IA:** probar con la clave real en casilla.io (rama `feat/claude-partidas`): `usage` y costo real, que la segunda llamada lea la caché (`cache_read_input_tokens` > 0) y el mensaje real de una organización sin CORS. Ver `docs/claude-partidas.md`.
- **Links de Lichess:** no se confirmó que `lichess.org/game/export/{id}` responda a pedidos del navegador (el proxy bloquea Lichess). Si no responde, la app pide pegar el PGN.
- **Links de Chess.com con `?move=N`:** se ignora el número; falta confirmar cómo cuenta Chess.com las jugadas para abrir en esa posición.
- Las ramas `feat/maestro-analisis` y `feat/maestro-mejoras` ya están fusionadas en `main` y siguen en GitHub.


