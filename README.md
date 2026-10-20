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
