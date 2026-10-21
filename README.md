# Casilla: entrenamiento de ajedrez con Stockfish

Casilla es una app de ajedrez que corre completa en tu navegador, desde un solo archivo HTML. No necesitas instalar nada ni crear cuenta.

Juegas contra Stockfish por niveles o contra un maestro que se adapta a ti, resuelves puzzles y entrenas finales y aperturas. Al terminar cada partida recibes una evaluación con tus errores explicados a fondo. Si tienes cuenta en Chess.com, la app analiza tus partidas y te arma puzzles con tus propios errores.

**Úsala en línea:** https://casilla.io/

Dirección alternativa: https://ferhuca.github.io/Casilla/

## Qué necesitas

- Un navegador moderno: Chrome, Edge, Firefox o Safari, en computadora o celular.
- Conexión a internet. La app descarga el motor Stockfish y la librería de ajedrez al abrirse, y los puzzles y partidas vienen de Lichess y Chess.com.
- Opcional: una clave de la API de Anthropic, si quieres que Claude escriba los comentarios del maestro.

## Cómo abrirla

- **En línea (recomendado):** entra a https://casilla.io/ y espera a que el indicador de arriba a la derecha diga **Stockfish 10 listo**. Tarda unos segundos la primera vez.
- **Dirección alternativa:** https://ferhuca.github.io/Casilla/ tiene la misma versión. Algunas redes no logran conectarse con GitHub Pages; si una dirección no carga, usa la otra. Cada dirección guarda su propio progreso, así que conviene activar la [sincronización](#sincronizar-entre-computadora-y-celular) en la que uses.
- **En el celular:** abre el enlace en Safari (iPhone) o Chrome (Android) y usa **Añadir a pantalla de inicio** para tenerla como un ícono de app. La interfaz está adaptada a pantallas desde 360 px:
  - El tablero ocupa todo el ancho y los relojes quedan arriba y abajo de él.
  - Debajo del tablero aparecen el estado de la partida, el último comentario del maestro y sus avisos con los botones **Pensar otra vez** y **Jugarla igual**. Al terminar aparece **Ver evaluación**.
  - El resto del panel (lista de jugadas, explicaciones, opciones) queda más abajo; desliza para verlo. Los botones que muestran una línea en el tablero te regresan a él.
- **Sin publicar, en tu computadora:** descarga `index.html` de este repositorio, guárdalo en una carpeta fija y ábrelo con doble clic. En el celular este método no es confiable; usa el enlace.

Para mover una pieza, arrástrala, o toca la pieza y luego la casilla de destino. Al coronar, elige la pieza en el selector que aparece sobre el tablero.

## Qué puedes hacer

La app tiene seis pestañas (Escalera, Maestro, Puzzles, Posiciones, Mis partidas y Progreso) y un botón de **Apariencia** arriba a la derecha.

### Escalera
Ocho niveles, desde Peón (~600 ELO) hasta Gran Maestro (2700+). Gana a un nivel sin ayudas para desbloquear el siguiente. Los ELO son aproximados: el motor se debilita limitando su nivel de habilidad y su profundidad de cálculo.

Antes de jugar eliges:
- **Color:** blancas, negras o al azar.
- **Ritmo:** sin reloj, 3+2, 5+0, 10+5 o 15+10. Si se te acaba el tiempo pierdes, salvo que tu rival no tenga material para dar mate; en ese caso son tablas.
- **Con ayudas:** pistas, deshacer y barra de evaluación. Esas victorias no desbloquean niveles.
- **Barra de evaluación:** se muestra a un costado del tablero. Sin ayudas cuenta como ayuda, así que esa victoria tampoco desbloquea.
- **El maestro comenta la partida:** sin ayudas solo señala tus buenas jugadas y deja los errores para el final; con ayudas, además te avisa antes de un error grave.

### Maestro
Un rival que aprende de ti:
- **Estima tu nivel** con tus partidas de Chess.com, la escalera, tus puzzles y tus partidas serias contra él, y juega unos 100 puntos por encima. La pestaña muestra lo que sabe de ti: nivel estimado, errores más comunes y aperturas aprendidas.
- **Te juega tus aperturas:** en la apertura usa las jugadas que más te han puesto tus rivales en Chess.com.
- **Comenta los momentos clave:** buenas jugadas, la única jugada que salvaba la posición, tácticas encontradas y la entrada al final. Sus explicaciones se ajustan a tu nivel.
- **Partida guiada:** te avisa antes de un error grave ("Espera. Si juegas Nf6, tu rival tiene mate, empezando con Qxf7#"), señala amenazas y puedes pensar otra vez, pedir pistas o deshacer.
- **Partida seria:** sin ayudas. Los errores se repasan al final y el resultado cuenta para tu rating con el maestro.
- Los errores de cada partida se guardan en tus puzzles de **Mis errores**.

**Comentarios con Claude (opcional):** sin configurar nada, el maestro comenta con frases armadas a partir de Stockfish. Si pegas tu propia clave de la API de Anthropic en la pestaña Maestro, Claude reescribe cada comentario y la evaluación final en lenguaje natural.
- Claude solo redacta. Las jugadas, las líneas y las evaluaciones siempre vienen de Stockfish.
- Recomendado: **Claude Haiku 5.5**, que cuesta menos de un centavo de dólar por partida. **Claude Sonnet 5.5** da explicaciones algo más finas y cuesta varias veces más.
- Cada persona que use la app necesita su propia clave. Puedes obtenerla en https://console.anthropic.com/settings/keys

### Evaluación al final de cada partida
Al terminar una partida de la escalera, contra el maestro o desde una posición, Stockfish revisa todas las jugadas de ambos lados. Tarda de 20 a 30 segundos y mientras tanto puedes seguir en la pantalla de resultado. Después, **Ver evaluación completa** muestra:
- **Resumen:** tu precisión y la de tu rival, tus errores graves, errores e imprecisiones, y una gráfica de la evaluación con tus errores marcados. Toca un punto para ir a ese momento.
- **Comentario del maestro:** cómo saliste de la apertura, el momento decisivo, oportunidades que no aprovechaste, tu precisión por fase y si apareció tu patrón de error más frecuente.
- **Momentos clave, explicados a fondo:**
  1. Qué pasó.
  2. De dónde viene el error: una amenaza que ya existía, la pieza que defendía y moviste, una casilla atacada, el escudo de tu rey o una pieza que quedó pasiva.
  3. Lo que sigue después de tu jugada, comentado jugada por jugada.
  4. La mejor jugada y de dónde viene su idea: ataque doble, clavada, ataque descubierto, la casilla que había que defender o la pieza que tu rival dejó sin defensa con su jugada anterior.
  5. La línea del motor, comentada.
  6. Una lección para la próxima.

  Cada momento tiene botones para ver tu jugada y la mejor línea en el tablero.
- **Qué entrenar:** puzzles con estos mismos errores, el tema de Lichess relacionado o finales.

Las explicaciones detectan bien amenazas previas, piezas sin defensa, ataques dobles, clavadas y ataques descubiertos. En errores puramente posicionales son más generales: muestran la diferencia de evaluación y la línea del motor, pero no siempre pueden nombrar el plan.

### Puzzles
- **Lichess:** puzzles por tema (mate en 2, ataque doble, clavada, finales y más) ajustados a tu nivel.
- **Chess.com:** puzzles diarios de su archivo.
- **Mis errores:** posiciones de tus propias partidas donde fallaste. Al terminar cada uno ves qué jugaste en la partida, de dónde vino el error y la idea de la mejor jugada.
- **Combinado:** mezcla las tres fuentes.

El tema **Recomendado para ti** elige puzzles según tus errores más frecuentes. La app lleva tu rating de puzzles y tu racha; solo cuenta para el rating si lo resuelves al primer intento sin pedir pista.

### Posiciones
- **Finales:** ocho finales clásicos contra Stockfish a máxima fuerza, cada uno con un objetivo: dar mate, ganar o entablar. Incluye Lucena, Philidor y el mate de alfil y caballo.
- **Aperturas:** doce líneas principales, como la Italiana, la Española, la Siciliana Najdorf, la Caro-Kann y el Gambito de Dama. El rival juega la teoría y tú debes recordar tus jugadas; al terminar puedes seguir la partida contra el motor. También aparecen tus aperturas más jugadas en Chess.com.
- **De mis partidas:** tus errores más frecuentes agrupados por tipo. Puedes resolverlos como puzzle o volver a jugar desde esa posición.
- **FEN:** pega cualquier posición para jugarla o analizarla.

### Mis partidas (Chess.com)
1. Escribe tu **nombre de usuario** de Chess.com, el que aparece en la URL de tu perfil, no tu nombre visible.
2. Elige cuántos meses cargar y pulsa **Cargar partidas**.
3. Pulsa **Analizar** para que Stockfish revise tus partidas. En modo Normal tarda unos 30 segundos por partida y puedes seguir usando la app mientras tanto.

No pide contraseña: solo lee tus datos públicos. Tus partidas en Chess.com ya son públicas por defecto, así que no tienes que cambiar nada.

Al abrir una partida ves cada jugada marcada como imprecisión, error o error grave, tu precisión aproximada y tus errores clasificados: pieza colgada, táctica no vista, mate no visto, permitió mate o error posicional. El botón **Evaluación a fondo** abre la misma evaluación completa que recibes al terminar una partida en la app.

### Apariencia
El botón **Apariencia** abre un panel para personalizar la app. Los cambios se ven al instante:
- **Estilo:** Plano (el original); Relieve, con botones que se hunden al presionarlos, paneles con profundidad, tablero con marco y piezas con sombra; u 8 bits, con bordes gruesos y sombras sólidas de videojuego retro.
- **Tema:** Carbón, Papel (claro), Pizarra, Cuero o Arcade.
- **Fuente:** Clásica, Moderna, Libro, Técnica o Pixel.
- **Tablero:** Gris piedra, Madera, Nogal, Glaciar, Club o Arcade.
- **Piezas:** Clásicas, Merida, Celtic, Minimal, Chessnut, Pixel o Retro.

El botón **Todo en 8 bits** aplica de un toque el estilo, tema, fuente, tablero y piezas retro.

### Progreso
Tus niveles superados, la evolución de tu rating de puzzles, tus errores más comunes con una recomendación de qué entrenar, tus finales y aperturas repasados, la sincronización entre dispositivos y la opción de exportar o importar un respaldo.

## Sincronizar entre computadora y celular

Casilla puede guardar tu progreso en un **gist secreto de tu cuenta de GitHub** para usar el mismo progreso en todos tus dispositivos. No hay servidor de por medio: la app habla directo con GitHub.

**Configurarlo (una vez por dispositivo):**
1. Abre [este enlace para crear un token](https://github.com/settings/tokens/new?scopes=gist&description=Casilla). Ya viene con el permiso **gist** marcado, que es el único que necesita. Elige una fecha de vencimiento y pulsa **Generate token**.
2. En Casilla, ve a **Progreso → Sincronizar entre dispositivos**, pega el token y pulsa **Conectar y sincronizar**.
3. En tu otro dispositivo haz lo mismo, con el mismo token o con uno nuevo. La app encuentra el gist sola y combina los dos progresos.

**Cómo funciona:**
- **Cuándo sincroniza:** al abrir la app y al volver a ella; unos segundos después de cada cambio sube lo nuevo. También puedes pulsar **Sincronizar ahora**. El indicador del encabezado muestra el estado.
- **Combina, no sobrescribe:**
  - Escalera: se queda el nivel más alto.
  - Partidas y análisis: se suman.
  - Puzzles: el historial se une y el rating toma el más reciente.
  - Maestro, finales y aperturas: se unen.
- **Ajustes:** en un dispositivo nuevo se copian tu apariencia y preferencias. Después, cada dispositivo conserva las suyas.
- **Tamaño:** el progreso se comprime antes de subirse, así que ocupa poco aunque tengas cientos de partidas.

**Lo que conviene saber:**
- **El token y tu clave de Claude nunca se suben.** Se quedan en el navegador de cada dispositivo y tampoco van en los respaldos.
- **Un gist secreto no es privado:** no aparece en búsquedas ni en tu perfil, pero quien tenga su enlace exacto puede verlo. Contiene tu progreso y tus partidas de Chess.com, que ya son públicas.
- **Cuando el token caduque,** la app te avisa y te deja pegar uno nuevo sin perder nada.
- **Desconectar un dispositivo** solo borra el token de ese navegador. El gist y tu progreso se quedan.
- **Si juegas en dos dispositivos a la vez sin conexión,** algunos contadores, como las victorias por nivel, pueden quedar con el número mayor de los dos en lugar de la suma.

## Dónde se guarda tu progreso

Todo se guarda en el navegador donde abres la app, no en el archivo ni en ningún servidor. Eso incluye tus niveles, puzzles, partidas y análisis, tu historial con el maestro, tu apariencia y, si la usas, tu clave de Claude. Se conserva aunque cierres el navegador o apagues la computadora.

Lo pierdes si:
- Abres la app en otro navegador u otro dispositivo. La computadora y el celular tienen progresos separados.
- Borras los datos de navegación (cookies y datos de sitios).
- Usas una ventana privada o de incógnito.
- Usas la versión local y mueves el archivo de carpeta (puede pasar en Firefox).

Tampoco se guarda una partida que dejes a medias: solo se registran las terminadas.

Para evitar todo esto, activa la [sincronización](#sincronizar-entre-computadora-y-celular).

**Consejo:** en Progreso usa **Exportar respaldo** de vez en cuando, sobre todo después de analizar muchas partidas. Con **Importar respaldo** recuperas todo en otro navegador o equipo, por ejemplo para pasar tu análisis de la computadora al celular. Por seguridad, el respaldo no incluye tu clave de Claude; vuelve a pegarla en cada navegador.

## Privacidad

- **Chess.com:** la app solo lee la API pública con tu nombre de usuario. No pide contraseña ni puede modificar nada en tu cuenta.
- **Lichess:** se piden puzzles de forma anónima.
- **GitHub:** solo si activas la sincronización. Tu progreso se guarda en un gist secreto de tu cuenta.
- **Anthropic:** solo si activas Claude. Se envían las posiciones y los datos de Stockfish de cada comentario, junto con tu nivel estimado y tus errores más comunes. La clave va directo de tu navegador a Anthropic.
- Nada más sale de tu navegador. Cada persona que abre la app empieza de cero y nadie ve el progreso de otros.

## Si algo no funciona

- **"This site can't be reached" o ERR_CONNECTION_ABORTED:** tu red no logra conectarse con esa dirección. Abre la otra dirección (casilla.io o GitHub Pages) o cambia entre Wi-Fi y datos móviles.
- **"Stockfish no cargó":** revisa tu conexión a internet y recarga la página.
- **"No encontré ese usuario en Chess.com":** revisa que sea el nombre de usuario exacto. Puedes comprobarlo abriendo `https://api.chess.com/pub/player/TUUSUARIO/games/archives` en el navegador: si ves una lista de meses, la app te puede leer.
- **No aparecen tus partidas de hoy:** Chess.com actualiza sus datos públicos cada 12 a 24 horas.
- **Faltan algunas partidas:** la app solo carga ajedrez estándar; omite Chess960, bughouse y otras variantes.
- **Los puzzles no cargan:** Lichess o Chess.com pueden estar temporalmente sin respuesta. Prueba otra fuente o pulsa Reintentar.
- **La sincronización falla:** en Progreso aparece el motivo. Lo más común es un token vencido o sin permiso **gist**; crea uno nuevo con el enlace de arriba y pégalo en **Nuevo token de GitHub**.
- **Claude no responde:** en la pestaña Maestro pulsa **Probar conexión**; el mensaje dice el motivo. Lo más común es una clave mal copiada o una cuenta de Anthropic sin saldo. Mientras tanto, el maestro sigue comentando con sus frases integradas.
- **La evaluación tarda:** es normal en partidas largas o en equipos lentos. Puedes salir y volver; si empiezas otra partida, la evaluación anterior se cancela.
- **Ves una versión vieja de la app:** recarga forzando con Ctrl+Shift+R, o Cmd+Shift+R en Mac. En el celular, cierra la pestaña o el ícono de la pantalla de inicio y vuelve a abrirlo.
- **En el celular no ves el resultado o la explicación:** están en el panel debajo del tablero; desliza hacia abajo.

## Créditos

- Motor: [Stockfish](https://stockfishchess.org/) 10, compilado para navegador por [stockfish.js](https://github.com/lichess-org/stockfish.js) (GPLv3).
- Piezas, tomadas de [Lichess](https://github.com/lichess-org/lila):
  - Clásicas, de Colin M.L. Burnett (GPLv2+).
  - Merida, de Armando Hernández Marroquín (GPLv2+).
  - Celtic, de [Maurizio Monge](https://github.com/maurimo/chess-art) (MIT).
  - Minimal (MPChess), de [Maxime Chupin](https://github.com/chupinmaxime) (GPLv3+).
  - Chessnut, de [Alexis Luengas](https://github.com/LexLuengas/chessnut-pieces) (Apache 2.0).
  - Pixel, de therealqtpi (AGPLv3+).
  - Retro, de [RhosGFX](https://rhosgfx.itch.io/) (CC0).
- Fuentes pixel: Press Start 2P y Pixelify Sans, de Google Fonts (SIL Open Font License).
- Reglas de ajedrez: [chess.js](https://github.com/jhlywa/chess.js).
- Puzzles: API pública de [Lichess](https://lichess.org) y de [Chess.com](https://www.chess.com/news/view/published-data-api).
- Partidas: API pública de Chess.com.
- Comentarios opcionales: [API de Claude](https://platform.claude.com/docs/en/api/overview), de Anthropic.
- Sincronización opcional: [API de Gists de GitHub](https://docs.github.com/en/rest/gists).

Casilla no está afiliada a Chess.com, Lichess, Anthropic ni GitHub.

## Licencia

Casilla se distribuye bajo la licencia [GPL-3.0](LICENSE). Puedes usarla, estudiarla, modificarla y compartirla, siempre que tus versiones también se publiquen bajo GPL-3.0 y conserven los créditos. Los sets de piezas y el motor Stockfish mantienen sus propias licencias, indicadas en la sección de créditos.
