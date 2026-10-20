# Casilla: entrenamiento de ajedrez con Stockfish

Casilla es una app de ajedrez que corre completa en tu navegador desde un solo archivo HTML. No necesitas instalar nada ni crear cuenta. Juegas contra Stockfish por niveles, resuelves puzzles, entrenas finales y aperturas, y si tienes cuenta en Chess.com, analiza tus partidas y te arma puzzles con tus propios errores.

**Úsala en línea:** https://ferhuca.github.io/Casilla/

## Qué necesitas

- Un navegador moderno: Chrome, Edge, Firefox o Safari, en computadora o celular.
- Conexión a internet. La app descarga el motor Stockfish y la librería de ajedrez al abrirse, y los puzzles y partidas vienen de Lichess y Chess.com.

## Cómo abrirla

**En línea (recomendado):** entra a https://ferhuca.github.io/Casilla/ y espera a que el indicador de arriba a la derecha diga **Stockfish 10 listo**. Tarda unos segundos la primera vez.

**En el celular:** abre el enlace en Safari (iPhone) o Chrome (Android) y usa **Añadir a pantalla de inicio** para tenerla como un ícono de app. Puedes arrastrar las piezas o tocar la pieza y luego la casilla de destino.

**Sin publicar, en tu computadora:** descarga `index.html` de este repositorio, guárdalo en una carpeta fija y ábrelo con doble clic. En celular este método no es confiable, usa el enlace.

Para mover piezas, arrástralas o haz clic en la pieza y luego en la casilla de destino.

## Qué puedes hacer

### Escalera
Ocho niveles, desde Peón (~600 ELO) hasta Gran Maestro (2700+). Gana a un nivel para desbloquear el siguiente. Puedes elegir blancas, negras o al azar.

Si activas **Con ayudas** tienes pistas, deshacer y barra de evaluación, pero esas victorias no desbloquean niveles.

Los ELO son aproximados: el motor se debilita limitando su nivel de habilidad y su profundidad de cálculo.

Puedes jugar sin reloj o con ritmo 3+2, 5+0, 10+5 o 15+10. Si se te acaba el tiempo pierdes, salvo que tu rival no tenga material para dar mate.

Si activas **El maestro comenta la partida**, sin ayudas solo señala tus buenas jugadas y deja los errores para el resumen final; con ayudas, además te avisa antes de un error grave.

**Barra de evaluación:** puedes mostrarla a un costado del tablero desde la pantalla de inicio o con el botón **Mostrar barra** durante la partida. Se actualiza después de cada jugada con Stockfish a máxima fuerza y se gira junto con el tablero. En la escalera sin ayudas cuenta como ayuda: esa victoria no desbloquea niveles.

### Maestro
Un rival que aprende de ti:
- **Estima tu nivel** con tus partidas de Chess.com, la escalera, tus puzzles y tus partidas serias contra él, y juega unos 100 puntos por encima.
- **Te juega tus aperturas:** en la apertura usa las jugadas que más te han puesto tus rivales en Chess.com.
- **Comenta los momentos clave:** buenas jugadas, la única jugada buena, tácticas encontradas, la entrada al final y un resumen al terminar. Sus explicaciones se ajustan a tu nivel.
- **Partida guiada:** te avisa antes de un error grave ("Espera. Si juegas Nf6, tu rival tiene mate") y puedes pensar otra vez, pedir pistas o deshacer.
- **Partida seria:** sin ayudas; los errores se repasan al final y el resultado cuenta para tu rating con el maestro.
- Los errores de cada partida se guardan en tus puzzles de **Mis errores**.

**Comentarios con Claude (opcional):** sin configurar nada, el maestro comenta con frases armadas a partir de Stockfish. Si pegas tu propia clave de la API de Anthropic, Claude reescribe cada comentario en lenguaje natural. La clave se guarda solo en tu navegador, se envía directo a Anthropic y no se incluye en los respaldos. Cada persona que use la app necesita su propia clave.

### Evaluación al final de cada partida
Al terminar una partida de la escalera, contra el maestro o desde una posición, Stockfish revisa todas las jugadas de ambos lados. Mientras tanto puedes seguir en la pantalla de resultado. Luego **Ver evaluación completa** muestra:
- Tu precisión y la de tu rival, tus errores graves, errores e imprecisiones, y una gráfica de la evaluación con tus errores marcados.
- **Comentario del maestro:** cómo saliste de la apertura, el momento decisivo, oportunidades que no aprovechaste, precisión por fase y si apareció tu patrón de error más frecuente.
- **Momentos clave**, explicados a fondo:
  - Qué pasó.
  - De dónde viene el error: una amenaza que ya existía, la pieza que defendía y moviste, una casilla atacada, el escudo de tu rey o una pieza que quedó pasiva.
  - La línea que sigue, con cada jugada comentada.
  - La mejor jugada y de dónde viene su idea: ataque doble, clavada, ataque descubierto, la casilla que había que defender o la pieza que tu rival dejó sin defensa con su jugada anterior.
  - Una lección para la próxima.
- **Qué entrenar:** puzzles con estos errores, el tema de Lichess relacionado o finales.

En **Mis partidas**, el botón **Evaluación a fondo** hace lo mismo con cualquier partida de Chess.com.

### Puzzles
- **Lichess:** puzzles por tema (mate en 2, ataque doble, clavada, finales y más) ajustados a tu nivel.
- **Chess.com:** puzzles diarios de su archivo.
- **Mis errores:** posiciones de tus propias partidas donde fallaste. Requiere analizar partidas primero.
- **Combinado:** mezcla las tres fuentes.

La app lleva tu rating de puzzles y tu racha. Solo cuenta para el rating si lo resuelves al primer intento sin pedir pista.

### Posiciones
- **Finales:** ocho finales clásicos contra Stockfish a máxima fuerza, cada uno con un objetivo (dar mate, ganar o entablar). Incluye Lucena, Philidor y el mate de alfil y caballo.
- **Aperturas:** doce líneas principales (Italiana, Española, Siciliana Najdorf, Caro-Kann, Gambito de Dama y otras). El rival juega la teoría y tú debes recordar tus jugadas. Al terminar puedes seguir la partida contra el motor.
- **De mis partidas:** tus errores más frecuentes agrupados por tipo. Puedes resolverlos como puzzle o volver a jugar desde esa posición.
- **FEN:** pega cualquier posición para jugarla o analizarla.

### Mis partidas (Chess.com)
1. Escribe tu **nombre de usuario** de Chess.com (el que aparece en la URL de tu perfil, no tu nombre visible).
2. Elige cuántos meses cargar y pulsa **Cargar partidas**.
3. Pulsa **Analizar** para que Stockfish revise tus partidas. En modo Normal tarda unos 30 segundos por partida y puedes seguir usando la app mientras tanto.

No pide contraseña: solo lee tus datos públicos. Tus partidas en Chess.com ya son públicas por defecto, no tienes que cambiar nada.

Al terminar verás tu precisión aproximada por partida, tus jugadas marcadas como imprecisión, error o error grave, y tus errores clasificados en: pieza colgada, táctica no vista, mate no visto, permitió mate o error posicional.

### Apariencia
El botón **Apariencia**, arriba a la derecha, abre un panel para personalizar la app. Los cambios se ven al instante:
- **Tema:** Carbón, Papel (claro), Pizarra o Cuero.
- **Fuente:** Clásica, Moderna, Libro o Técnica.
- **Tablero:** Gris piedra, Madera, Nogal, Glaciar o Club.
- **Piezas:** Clásicas, Merida, Celtic, Minimal o Chessnut.

### Progreso
Resumen de tus niveles superados, la evolución de tu rating de puzzles, tus errores más comunes con una recomendación de qué entrenar, y la opción de exportar o importar un respaldo.

## Dónde se guarda tu progreso

Todo se guarda en el navegador donde abres el archivo, no en el archivo mismo ni en ningún servidor. Se conserva aunque cierres el navegador o apagues la computadora.

Lo pierdes si:
- Abres la app en otro navegador u otro dispositivo (computadora y celular tienen progresos separados).
- Borras los datos de navegación (cookies y datos de sitios).
- Usas una ventana privada o de incógnito.
- Usas la versión local y mueves el archivo de carpeta (puede pasar en Firefox).

También se pierde una partida que dejes a medias: solo se registran las terminadas.

**Consejo:** en Progreso usa **Exportar respaldo** de vez en cuando, sobre todo después de analizar muchas partidas. Con **Importar respaldo** recuperas todo en otro navegador o equipo, por ejemplo para pasar tu análisis de la computadora al celular.

## Si algo no funciona

- **"Stockfish no cargó":** revisa tu conexión a internet y recarga la página.
- **"No encontré ese usuario en Chess.com":** revisa que sea el nombre de usuario exacto. Puedes comprobarlo abriendo `https://api.chess.com/pub/player/TUUSUARIO/games/archives` en el navegador: si ves una lista de meses, la app te puede leer.
- **No aparecen tus partidas de hoy:** Chess.com actualiza sus datos públicos cada 12 a 24 horas.
- **Faltan algunas partidas:** la app solo carga ajedrez estándar; omite Chess960, bughouse y otras variantes.
- **Los puzzles no cargan:** Lichess o Chess.com pueden estar temporalmente sin respuesta. Prueba otra fuente o pulsa Reintentar.

## Créditos

- Motor: [Stockfish](https://stockfishchess.org/) 10 compilado para navegador por [stockfish.js](https://github.com/lichess-org/stockfish.js) (licencia GPLv3).
- Piezas: Clásicas de Colin M.L. Burnett (GPLv2+), Merida de Armando Hernández Marroquín (GPLv2+), Celtic de [Maurizio Monge](https://github.com/maurimo/chess-art) (MIT), Minimal (MPChess) de [Maxime Chupin](https://github.com/chupinmaxime) (GPLv3+) y Chessnut de [Alexis Luengas](https://github.com/LexLuengas/chessnut-pieces) (Apache 2.0), tomadas de [Lichess](https://github.com/lichess-org/lila).
- Reglas de ajedrez: [chess.js](https://github.com/jhlywa/chess.js).
- Puzzles: API pública de [Lichess](https://lichess.org) y de [Chess.com](https://www.chess.com/news/view/published-data-api).
- Partidas: API pública de Chess.com.

Casilla no está afiliada a Chess.com ni a Lichess.

## Licencia

Casilla se distribuye bajo la licencia [GPL-3.0](LICENSE). Puedes usarla, estudiarla, modificarla y compartirla, siempre que tus versiones también se publiquen bajo GPL-3.0 y conserven los créditos. Los sets de piezas y el motor Stockfish mantienen sus propias licencias, indicadas en la sección de créditos.
