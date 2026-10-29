# Casilla: entrenamiento de ajedrez con Stockfish

Casilla es una app de ajedrez que corre completa en tu navegador, desde un solo archivo HTML. No necesitas instalar nada ni crear cuenta.

Juegas contra Stockfish por niveles o contra un maestro que se adapta a ti, resuelves puzzles y entrenas finales y aperturas. Al terminar cada partida recibes una evaluación con tus errores explicados a fondo. Si tienes cuenta en Chess.com, la app analiza tus partidas y te arma puzzles con tus propios errores.

**Úsala en línea:** https://casilla.io/

Dirección alternativa: https://ferhuca.github.io/Casilla/

## Qué necesitas

- Un navegador moderno: Chrome, Edge, Firefox o Safari, en computadora o celular.
- Conexión a internet la primera vez. La app descarga el motor Stockfish y la librería de ajedrez al abrirse, y los puzzles y partidas vienen de Lichess y Chess.com. Después funciona [sin conexión](#sin-conexión).
- Opcional: una clave de la API de Anthropic, si quieres que Claude escriba los comentarios del maestro.

## Cómo abrirla

- **En línea (recomendado):** entra a https://casilla.io/ y espera a que el indicador de arriba a la derecha diga **Motor listo**. Tarda unos segundos la primera vez.
- **Dirección alternativa:** https://ferhuca.github.io/Casilla/ tiene la misma versión. Algunas redes no logran conectarse con GitHub Pages; si una dirección no carga, usa la otra. Cada dirección guarda su propio progreso, así que conviene activar la [sincronización](#sincronizar-entre-computadora-y-celular) en la que uses.
- **En el celular:** abre el enlace en Safari (iPhone) o Chrome (Android) y usa **Añadir a pantalla de inicio** para tenerla como un ícono de app. La interfaz está adaptada a pantallas desde 360 px:
  - El tablero ocupa todo el ancho y los relojes quedan arriba y abajo de él.
  - Debajo del tablero aparecen el estado de la partida, el último comentario del maestro y sus avisos con los botones **Pensar otra vez** y **Jugarla igual**. Al terminar aparece **Ver evaluación**.
  - El resto del panel (lista de jugadas, explicaciones, opciones) queda más abajo; desliza para verlo. Los botones que muestran una línea en el tablero te regresan a él.
- **Sin publicar, en tu computadora:** descarga `index.html` de este repositorio, guárdalo en una carpeta fija y ábrelo con doble clic. En el celular este método no es confiable; usa el enlace.

### Sin conexión

Después de abrir casilla.io (o la dirección de GitHub Pages) una vez con internet, la app queda guardada en tu navegador y abre sin señal, por ejemplo en modo avión. Sin conexión puedes jugar contra el motor en la Escalera, analizar posiciones, revisar y analizar las partidas que ya cargaste en Partidas y resolver puzzles guardados. Con red, la app guarda en segundo plano 200 puzzles de Lichess en tu navegador (50 de ellos con los temas de tu etapa de la Ruta), sin ráfagas y respetando los límites de su API. Los de Chess.com no se guardan porque sus condiciones de uso no permiten copiar su contenido fuera de la caché temporal del navegador. Los que resuelves se borran y se reponen al volver la red. Sin conexión, Puzzles y la Táctica de la etapa usan esos guardados; solo se desactiva lo que no esté guardado (Chess.com siempre, y Lichess mientras no haya guardados). Lo demás que depende de internet no funciona hasta que vuelva la red: cargar partidas nuevas de Chess.com, la sincronización y los comentarios con IA. Un aviso arriba lo indica y la píldora dice «Sin conexión». El maestro sigue jugando con sus frases integradas y Claude vuelve solo al reconectar. Cuando hay una versión nueva, la app pregunta «Hay una versión nueva.» con **Actualizar** (recarga ya) y **Ahora no** (se aplica la próxima vez que abras Casilla). El pie de página muestra la versión instalada. El modo sin conexión no aplica si abres `index.html` con doble clic.

Para mover una pieza, arrástrala, o toca la pieza y luego la casilla de destino. Al coronar, elige la pieza en el selector que aparece sobre el tablero.

## Qué puedes hacer

La app tiene seis pestañas (Escalera, Maestro, Puzzles, Posiciones, Partidas y Progreso) y un botón de **Apariencia** arriba a la derecha.

### Escalera
Ocho niveles, desde Peón (~600 ELO) hasta Gran Maestro (2700+). Gana a un nivel sin ayudas para desbloquear el siguiente. Los ELO son aproximados: el motor se debilita limitando su nivel de habilidad y su profundidad de cálculo.

Antes de jugar eliges:
- **Color:** blancas, negras o al azar.
- **Ritmo:** sin reloj, 3+2, 5+0, 10+5, 15+10 o 30+20. Si se te acaba el tiempo pierdes, salvo que tu rival no tenga material para dar mate; en ese caso son tablas.
- **Con ayudas:** pistas, deshacer y barra de evaluación. Esas victorias no desbloquean niveles.
- **Barra de evaluación:** se muestra a un costado del tablero. Sin ayudas cuenta como ayuda, así que esa victoria tampoco desbloquea.
- **El maestro comenta la partida:** sin ayudas solo señala tus buenas jugadas y deja los errores para el final; con ayudas, además te avisa antes de un error grave.

### Maestro
Tu entrenador. Combina una ruta de estudio hasta 1500 con un rival que aprende de ti.

**Sesión de hoy.** Una lista corta de lo que toca hoy, en el orden en que conviene hacerlo:
1. **Repaso espaciado:** posiciones de tus propios errores que te tocan hoy.
2. **Táctica de la etapa:** puzzles de Lichess con los temas de tu etapa mezclados y sin decirte cuál es; el tema aparece al terminar, como en una partida real.
3. **Un final:** primero los pendientes de etapas anteriores; si ya los tienes todos, repasa el que completaste hace más tiempo.
4. En la versión **Completa** (unos 45 minutos) se suman **una partida lenta contra el maestro** con el modo y ritmo de tu etapa y **la revisión de sus errores**. La **Corta** dura unos 15 minutos.

Cada paso se marca solo al hacerlo. Al completar la sesión suma un día a tu racha. El día de estudio cambia a las 4 de la mañana.

**Ruta a 1500.** Cuatro etapas en el orden del Método Steps y del curso de finales de Silman:

| Etapa | Nivel | Táctica | Finales | Además |
|---|---|---|---|---|
| 1. Bases | hasta ~800 | Mate en 1, pieza colgada, mate del pasillo | Mate con dama y con torre | |
| 2. Táctica básica | 800 a 1100 | Ataque doble, clavada, enfilada, ataque descubierto, mate en 2 | Rey y peón, regla del cuadrado, oposición | Revisión de amenazas |
| 3. Calcular y defender | 1100 a 1300 | Desviación, atracción, eliminar al defensor, defensa, pieza atrapada, mate en 3 | Casillas clave, mate con dos alfiles | Amenazas; 2 errores o menos por partida |
| 4. Finales y plan | 1300 a 1500 | Finales de torres y de peones, jugada tranquila, zugzwang, jugada intermedia | Lucena y Philidor | Amenazas; 1 error o menos por partida |

La etapa se elige sola según tu nivel estimado, o la eliges tú. Cada etapa muestra lo que falta para dominarla: 80% al primer intento en sus puzzles (los de cada etapa tienen una dificultad fija), sus finales completados, 80% de amenazas vistas y los errores por partida contra el maestro. Es una guía: nada se bloquea.

**El rival:**
- **Estima tu nivel** con tus partidas de Chess.com, la escalera, tus puzzles y tus partidas serias contra él, y juega unos 100 puntos por encima. La pestaña muestra lo que sabe de ti: nivel estimado, errores más comunes y aperturas aprendidas.
- **Te juega tus aperturas:** en la apertura usa las jugadas que más te han puesto tus rivales en Chess.com.
- **Comenta los momentos clave:** buenas jugadas, la única jugada que salvaba la posición, tácticas encontradas y la entrada al final. Sus explicaciones se ajustan a tu nivel.
- **Partida guiada:** te avisa antes de un error grave ("Espera. Si juegas Nf6, tu rival tiene mate, empezando con Qxf7#"), señala amenazas y puedes pensar otra vez, pedir pistas o deshacer.
- **Partida de amenazas:** entrena el hábito que más puntos da por debajo de 1500: revisar jaques, capturas y amenazas del rival antes de mover. Antes de varias de tus jugadas el maestro pregunta qué amenaza tu rival; tocas tu pieza en peligro (o tu rey si hay mate) o pulsas **Nada directo**. A veces pregunta sin que haya nada, para que la pregunta no delate la respuesta. Después te enseña la amenaza con una flecha. Cuenta como amenaza una captura que te gana al menos dos puntos de material, un mate en una o un jaque con el que te gana material, como un ataque doble o una enfilada con jaque; en ese caso vale tocar tu rey o la pieza que se pierde. Todavía no reconoce ataques dobles sin jaque ni clavadas. Sin pistas ni deshacer, y no cuenta para tu rating con el maestro.
- **Partida seria:** sin ayudas. Los errores se repasan al final y el resultado cuenta para tu rating con el maestro.
- Los errores de cada partida se guardan en tus puzzles de **Mis errores**.

**Comentarios con IA (opcional):** sin configurar nada, el maestro comenta con frases armadas a partir de Stockfish. Si pegas tu propia clave de la API de Anthropic (Claude) en la pestaña Maestro, sección «Comentarios con IA (opcional)», la IA reescribe cada comentario en lenguaje natural. El comentario de una partida completa nunca se pide solo: lo pides con **Comentar partida con IA**. En la app se habla de «la IA» y «el motor», sin nombres de proveedor. Para conseguir la clave, ve a [Clave de IA](#clave-de-ia).
- Claude solo redacta. Las jugadas, las líneas y las evaluaciones siempre vienen de Stockfish.
- Hay dos modelos que eliges por separado: uno para comentar tus partidas y otro para el análisis con el Maestro y la lectura de capturas.
- Para comentar partidas se recomienda **Claude Haiku 5.5**, que cuesta menos de un centavo de dólar por partida. **Claude Sonnet 5.5** da explicaciones algo más finas y cuesta varias veces más.
- Para analizar posiciones y leer capturas eliges entre tres opciones. La primera vez que usas el análisis con IA aparece una tarjeta para elegir; mientras no elijas, se usa el modelo de comentarios. Costo aproximado en dólares por cada captura leída o explicación:
  - **Económico (Claude Haiku 5.5):** menos de 1 centavo. Puede equivocarse más al leer capturas.
  - **Equilibrado (Claude Sonnet 5.5):** de 2 a 4 centavos.
  - **Preciso (Claude Opus 5.5):** de 5 a 8 centavos. Recomendado si subes capturas.
  Son estimaciones con los precios de Anthropic; el costo real depende de cuánto piense el modelo.
- **Probar conexión** revisa los dos modelos.
- Cada persona que use la app necesita su propia clave. Puedes obtenerla en https://platform.claude.com/settings/keys
- **Gasto aproximado:** debajo de la clave, Maestro muestra cuántas partidas comentaste, cuántos ejercicios tuvieron pista, los tokens y un total aproximado en dólares. Se calcula en tu navegador con el uso que reporta la API y las tarifas guardadas en Casilla; no incluye otros dispositivos. El gasto real está en la consola de Anthropic (**Ver gasto real en la consola**, https://platform.claude.com/cost). **Reiniciar contador** lo pone en cero.

#### Clave de IA

1. Entra a https://platform.claude.com con tu cuenta (o la que te compartió quien administra la organización) y abre **API keys**.
2. Pulsa **Create key**, ponle un nombre (por ejemplo «Casilla, mi celular») y, si te deja, elige un workspace con límite de gasto y una fecha de vencimiento.
3. Copia la clave completa (empieza con `sk-ant-`). Solo se muestra una vez.
4. En Casilla, abre **Maestro**, baja a **Comentarios con IA (opcional)**, pégala en **Clave de la API** y pulsa **Probar conexión**.
5. La clave se queda solo en ese navegador: no se sincroniza ni va en los respaldos. Pégala en cada navegador donde quieras usar la IA.

Si **Probar conexión** o una partida dice que el servicio rechazó la clave (error 401), revisa que la copiaste completa o crea otra. Si dice que no dio permiso (error 403, o 401 por la configuración de la organización), la clave existe pero no puede usarse desde el navegador o para ese modelo: revísalo en la consola. Nunca compartas tu clave por correo ni en un grupo; si se filtra, revócala en la consola.

### Análisis con el Maestro
Abre cualquier posición o partida y pídele al Maestro que te la explique. Se llega desde **Posiciones > Importar**, desde **Analizar una posición** en la pestaña Maestro, desde **Maestro** al revisar una partida de Chess.com y desde cualquier botón **Analizar** de la app.

**Traer una posición (Posiciones > Importar):**
- **Desde una captura:** sube una captura de pantalla del tablero (de Chess.com, Lichess o un libro) o, en la computadora, pégala con Ctrl+V. La IA reconoce las piezas, qué bando está abajo y, si se ve, a quién le toca (por el texto de la pantalla o por la última jugada resaltada). Después se abre el editor con tu captura al lado. Necesita la IA activada.
- **Pegar FEN, PGN o link:** en Chess.com usa **Compartir** (en la app: **Opciones > Compartir partida**) y copia el link de la partida o descarga su PGN. Con un PGN o un link recorres toda la partida. La API pública de Chess.com no permite pedir una partida por su link, así que la app la busca en el archivo mensual de un jugador: si es tuya y ya cargaste tus partidas, se abre al instante; si no, te pide el usuario de uno de los dos jugadores.
- **Lichess:** pega el link de una partida (si termina en `/black`, el tablero se gira) o del tablero de análisis. Si Lichess no responde, la app te pide pegar el PGN.
- **Subir archivo PGN:** el que descargas en Compartir. Si el archivo trae varias partidas, se usa la primera.
- **Tus partidas recientes:** las últimas jugadas en Casilla o cargadas de Chess.com. Si ya están evaluadas, se abren justo después de tu primer error.
- **Armar a mano** o **Editar:** abre el editor de posición.

**Editor de posición:** elige una pieza debajo del tablero y toca la casilla; toca la misma pieza otra vez para quitarla o usa **Borrar**. Ajusta a quién le toca y los enroques. Las casillas marcadas en azul son las que la IA no pudo leer con seguridad. El editor avisa si falta un rey, hay un peón en la primera u octava fila o el bando que no mueve está en jaque, y no deja analizar hasta corregirlo.

**El análisis:** el motor muestra sus tres mejores líneas y la flecha de la mejor jugada. Puedes mover piezas de ambos colores para probar ideas; en una partida, una jugada distinta abre una variante y **Volver a la partida** regresa. Debajo, el Maestro tiene tres botones:
- **Explicar posición:** quién está mejor y por qué, la idea de la mejor jugada y el plan.
- **¿Por qué ...?:** por qué el motor prefiere su jugada y por qué las otras son peores.
- **¿Qué tal ...?:** evalúa la última jugada del tablero (tuya o de la partida): si fue buena, un error o un error grave, cuál es la respuesta del rival y qué era mejor.

Con la IA activada, el Maestro escribe en lenguaje natural y puedes hacerle **preguntas libres** sobre la posición. Antes de mencionar una jugada o variante que no viene en el análisis, la IA le pide al motor que la calcule, así que las líneas y evaluaciones siempre son del motor. Sin la IA, o sin conexión, explica con frases armadas a partir del motor y las preguntas libres no están disponibles. **Ver en el tablero** regresa a la posición de una explicación y muestra su flecha.

### Evaluación al final de cada partida
Al terminar una partida de la escalera, contra el maestro o desde una posición, Stockfish revisa todas las jugadas de ambos lados. Tarda de 20 a 30 segundos y mientras tanto puedes seguir en la pantalla de resultado. Si sales o empiezas otra partida, la evaluación no se pierde: sigue en segundo plano (se pausa mientras juegas) y te avisa cuando termina. Después, **Ver evaluación completa** muestra:
- **Resumen:** tu precisión y la de tu rival, tus errores graves, errores e imprecisiones, y una gráfica de la evaluación con tus errores marcados. Toca un punto para ir a ese momento.
- **Jugada a jugada:** con **Siguiente**, las flechas del teclado o tocando una jugada de la lista, recorres la partida una jugada a la vez. Cada jugada, tuya o de tu rival, trae su comentario: si fue la mejor, teoría, buena, imprecisión, error, error grave, oportunidad perdida o si permite mate; qué hizo (captura, jaque, ataque o amenaza nueva); cómo cambió la evaluación desde tu lado; y, si no fue la mejor, cuál era y por qué. En el celular el comentario aparece debajo del tablero.
- **Comentario de la IA:** arriba dice de dónde viene la partida (por ejemplo «Jugada en Casilla · Contra el maestro · fecha», con la apertura si se reconoce, o «Desde una posición»). Sin comentario muestra el **comentario del maestro (sin IA)**: cómo saliste de la apertura, el momento decisivo, oportunidades que no aprovechaste, tu precisión por fase y si apareció tu patrón de error más frecuente. Con tu clave, **Comentar partida con IA** funciona igual que en las partidas de Chess.com (resumen, un comentario por error, **Volver a comentar**, **Borrar comentario**) y deja **Repasar estos errores como puzzles** dentro del bloque. Nunca se pide solo.
- **Momentos clave, explicados a fondo:**
  1. Qué pasó.
  2. De dónde viene el error: una amenaza que ya existía, la pieza que defendía y moviste, una casilla atacada, el escudo de tu rey o una pieza que quedó pasiva.
  3. Lo que sigue después de tu jugada, comentado jugada por jugada.
  4. La mejor jugada y de dónde viene su idea: ataque doble, clavada, ataque descubierto, la casilla que había que defender o la pieza que tu rival dejó sin defensa con su jugada anterior.
  5. La línea del motor, comentada.
  6. Una lección para la próxima.

  Al abrir un momento, el tablero muestra la posición antes de esa jugada: la flecha roja es lo que se jugó y la verde, la mejor. Con **Siguiente** ves qué pasó después. Cada momento tiene botones para ver tu jugada y la mejor línea en el tablero, comentadas jugada por jugada.
- **Qué entrenar:** puzzles con estos mismos errores, el tema de Lichess relacionado o finales.

Las explicaciones detectan bien amenazas previas, piezas sin defensa, ataques dobles, clavadas y ataques descubiertos. En errores puramente posicionales son más generales: muestran la diferencia de evaluación y la línea del motor, pero no siempre pueden nombrar el plan.

### Puzzles
- **Lichess:** puzzles por tema (mate en 2, ataque doble, clavada, finales y más) ajustados a tu nivel.
- **Chess.com:** puzzles diarios de su archivo.
- **Mis errores:** posiciones de tus propias partidas donde fallaste, tanto de Chess.com como de las que juegas en Casilla. Al terminar cada uno ves qué jugaste en la partida, de dónde vino el error y la idea de la mejor jugada. Si el error es de una partida jugada aquí, **Ver la partida** abre su evaluación en ese momento. Con tu clave de IA, **Ver pista** muestra una pista escrita por la IA antes de resolver (cuenta como ayuda, igual que la pista del motor) (se anota como ayuda al terminar: no suma rating) y al terminar **Ver explicación de la IA** la pide; nunca se consulta sola. Si comentaste la partida con IA, la pista y la explicación ya están guardadas y no se vuelve a consultar. El ejercicio siempre se resuelve contra la mejor jugada del motor y sigue en el repaso espaciado.
- **Repaso:** tus errores con repaso espaciado. Si aciertas al primer intento, la posición vuelve en 1, 3, 7, 14 y 30 días; si fallas, vuelve al día siguiente. Entran hasta 10 errores nuevos por día, los más costosos primero. Cualquier puzzle de Mis errores cuenta para este calendario.
- **Combinado:** mezcla Lichess, Chess.com y tus errores.

El tema **Recomendado para ti** elige puzzles según tus errores más frecuentes. La app lleva tu rating de puzzles y tu racha; solo cuenta para el rating si lo resuelves al primer intento sin pedir pista.

### Posiciones
- **Finales:** diez finales clásicos contra Stockfish a máxima fuerza, cada uno con un objetivo: dar mate, ganar o entablar. Incluye la regla del cuadrado, las casillas clave, Lucena, Philidor y el mate de alfil y caballo. Los que forman parte de la ruta a 1500 indican su etapa.
- **Aperturas:** doce líneas principales, como la Italiana, la Española, la Siciliana Najdorf, la Caro-Kann y el Gambito de Dama. El rival juega la teoría y tú debes recordar tus jugadas; al terminar puedes seguir la partida contra el motor. También aparecen tus aperturas más jugadas en Chess.com.
- **De mis partidas:** tus errores más frecuentes agrupados por tipo. Puedes resolverlos como puzzle o volver a jugar desde esa posición.
- **Importar:** trae una posición o partida desde una captura, una FEN, un PGN (pegado o en archivo), un link de Chess.com o Lichess, o tus partidas recientes para analizarla con el Maestro o jugarla contra el motor. Ver [Análisis con el Maestro](#análisis-con-el-maestro).

### Partidas
**Jugadas en Casilla:** cada partida de la escalera, contra el maestro o desde una posición entra a esta lista cuando termina su evaluación, con el resultado, tu precisión y tus errores. Tócala para ver otra vez la evaluación completa, al instante y sin volver a calcularla. Sus errores ya están en tus puzzles de **Mis errores**.

**Chess.com:**
1. Escribe tu **nombre de usuario** de Chess.com, el que aparece en la URL de tu perfil, no tu nombre visible.
2. Elige cuántos meses cargar y pulsa **Cargar partidas**.
3. Pulsa **Analizar** para que Stockfish revise tus partidas. En modo Normal tarda unos 30 segundos por partida y puedes seguir usando la app mientras tanto.

No pide contraseña: solo lee tus datos públicos. Tus partidas en Chess.com ya son públicas por defecto, así que no tienes que cambiar nada.

Al abrir una partida ves cada jugada marcada como imprecisión, error o error grave, tu precisión aproximada y tus errores clasificados: pieza colgada, táctica no vista, mate no visto, permitió mate o error posicional. El botón **Evaluación a fondo** abre la misma evaluación completa que recibes al terminar una partida en la app.

**Comentario de la IA (opcional, con tu clave):** arriba de Momentos clave, **Comentar partida con IA** envía en una sola consulta la partida con las evaluaciones del motor y tus errores. La IA escribe un resumen y un comentario por cada error, con **Ver en el tablero** para ir a esa jugada. La IA solo redacta: las jugadas y evaluaciones son del motor, y el texto puede tener errores. Usa Sonnet 5.5 y cuesta menos de 5 centavos de dólar por partida; el costo aproximado de cada comentario aparece debajo. Puedes cancelar mientras escribe, **Volver a comentar** o **Borrar comentario**. El comentario se guarda con el análisis (se conserva si vuelves a analizar la partida) y se sincroniza; la clave no. **Borrar comentario** también se sincroniza: otro dispositivo con el comentario viejo no lo trae de vuelta. Si falta la clave, la clave no sirve o no hay conexión, el bloque lo dice y te lleva a la clave.

### Apariencia
El botón **Apariencia** abre un panel con 11 estilos completos. Cada uno combina tema, tablero, piezas, letra y estilo de botones, y el cambio se ve al instante:
- **Clásico** (por defecto): sobrio, tablero gris piedra y piezas clásicas. Tiene modo claro u oscuro.
- **Madera:** papel claro, tablero de madera, piezas Merida y letra de libro.
- **Pizarra:** oscuro y frío, tablero glaciar, piezas Minimal y letra moderna.
- **Cuero:** cálido y oscuro, tablero de nogal y piezas Celtic.
- **Club:** papel claro, tablero verde de torneo, piezas Chessnut y letra técnica.
- **Relieve:** botones que se hunden, paneles con profundidad y tablero con marco. Tiene modo claro u oscuro.
- **8 bits:** todo retro, con colores, letra, piezas y tablero pixel.
- **Arcade:** colores arcade con piezas Retro, sin letra pixel.
- **Medianoche:** azules profundos, tablero azul a juego, piezas Minimal y letra moderna.
- **Cacao:** cafés suaves, tablero cacao, piezas Merida y letra de libro.
- **Ciruela:** grises con tono violeta, tablero a juego y piezas clásicas.

Medianoche, Cacao y Ciruela salen de paletas de seis tonos: fondo, paneles, bordes, texto y botones usan solo esos tonos, y la última jugada se marca en dorado.

Debajo de los estilos puedes cambiar por separado el **Tablero** y las **Piezas**. La opción que trae el estilo lleva la marca «Del estilo».
- Tableros de color: Gris piedra, Madera, Nogal, Glaciar, Club, Arena, Oliva, Tinta, Coral, Contraste (pensado para quien ve poco contraste), Medianoche, Cacao y Ciruela. Texturas: Arce y Veteado. Retro: Arcade.
- Piezas clásicas: Clásicas, Merida, Celtic, Spatial y Fantasy. Modernas: Minimal, Chessnut, Shapes, Firi, Pirouetti y Letras. Retro: Pixel y Retro.

Si cambias el tablero o las piezas, el estilo queda marcado como «Personalizado» y aparece **Volver a [estilo]**, que quita solo esos cambios. La letra, los colores y el modo siguen viniendo del estilo. Elegir otro estilo descarta la personalización. Solo se descargan las piezas y la textura que usas (y las miniaturas al abrir el panel); quedan guardadas para usarlas sin conexión.

**Volver a Clásico** deja la apariencia por defecto. Si usabas una combinación propia en una versión anterior, la app elige el estilo más parecido y conserva tu tablero y tus piezas como personalización.

### Progreso
Tus niveles superados, la evolución de tu rating de puzzles, tus errores más comunes con una recomendación de qué entrenar, tus finales y aperturas repasados, tu avance en la ruta a 1500, la sincronización entre dispositivos y la opción de exportar o importar un respaldo.

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
  - Maestro, finales, aperturas, sesiones de la ruta, repaso espaciado y revisión de amenazas: se unen.
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
- **Lichess:** se piden puzzles de forma anónima y, si pegas el link de una partida, su PGN.
- **GitHub:** solo si activas la sincronización. Tu progreso se guarda en un gist secreto de tu cuenta.
- **Anthropic:** solo si activas Claude. Se envían las posiciones y los datos de Stockfish de cada comentario o análisis, tus preguntas al Maestro, las capturas que subes para leer y tu nivel estimado con tus errores más comunes. Si comentas una partida con IA, se envían sus jugadas con las evaluaciones del motor, el rival, el resultado y tus errores. Las capturas no se guardan en la app ni en los respaldos. La clave va directo de tu navegador a Anthropic.
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
- **La captura se leyó mal:** corrige las piezas en el editor antes de analizar; las casillas en azul son las dudosas. Ayuda una captura donde el tablero se vea completo y grande, sin flechas ni menús encima. Opus 5.5 lee mejor que Haiku.
- **No encuentra una partida por su link:** escribe el usuario del otro jugador o, más rápido, pega el PGN de la partida (está en **Compartir** de Chess.com).
- **La evaluación tarda:** es normal en partidas largas o en equipos lentos. Puedes salir y volver; si empiezas otra partida, la evaluación anterior se cancela.
- **Ves una versión vieja de la app:** con internet la app se actualiza sola al abrirla; si aun así ves la anterior, recarga forzando con Ctrl+Shift+R, o Cmd+Shift+R en Mac. En el celular, cierra la pestaña o el ícono de la pantalla de inicio y vuelve a abrirlo.
- **En el celular no ves el resultado o la explicación:** están en el panel debajo del tablero; desliza hacia abajo.

## Créditos

- Motor: [Stockfish](https://stockfishchess.org/) 19 (versión lite de un hilo), compilado para navegador por [stockfish.js](https://github.com/nmrugg/stockfish.js) (GPLv3). Si no carga, la app usa Stockfish 10 de [lichess-org/stockfish.js](https://github.com/lichess-org/stockfish.js) (GPLv3).
- Piezas, tomadas de [Lichess](https://github.com/lichess-org/lila):
  - Clásicas, de Colin M.L. Burnett (GPLv2+).
  - Merida, de Armando Hernández Marroquín (GPLv2+).
  - Celtic, de [Maurizio Monge](https://github.com/maurimo/chess-art) (MIT).
  - Minimal (MPChess), de [Maxime Chupin](https://github.com/chupinmaxime) (GPLv3+).
  - Chessnut, de [Alexis Luengas](https://github.com/LexLuengas/chessnut-pieces) (Apache 2.0).
  - Pixel, de therealqtpi (AGPLv3+).
  - Retro, de [RhosGFX](https://rhosgfx.itch.io/) (CC0).
  - Spatial y Fantasy, de [Maurizio Monge](https://github.com/maurimo/chess-art) (MIT).
  - Shapes, de [flugsio](https://github.com/flugsio/chess_shapes) ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).
  - Firi, de [James Faure](https://github.com/jfaure/Firi-pieceset) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
  - Pirouetti, de [pirouetti](https://lichess.org/@/pirouetti) (AGPLv3+).
  - Letras, de [usolando](https://lichess.org/@/usolando) (AGPLv3+).
  - Detalle de origen y licencias en [piece/LICENSE.md](piece/LICENSE.md).
- Texturas de tablero Arce y Veteado, de los autores de lila y [pirouetti](https://lichess.org/@/pirouetti) (AGPLv3+), tomadas de Lichess. Detalle en [board/LICENSE.md](board/LICENSE.md).
- Fuentes: Source Sans 3 y Source Serif 4 (Adobe), Manrope, Literata, IBM Plex Sans y Mono, incluidas en `fonts/` (SIL Open Font License).
- Fuentes pixel: Press Start 2P y Pixelify Sans, incluidas en `fonts/` (SIL Open Font License).
- Reglas de ajedrez: [chess.js](https://github.com/jhlywa/chess.js).
- Puzzles: API pública de [Lichess](https://lichess.org) y de [Chess.com](https://www.chess.com/news/view/published-data-api).
- Partidas: API pública de Chess.com.
- Comentarios opcionales: [API de Claude](https://platform.claude.com/docs/en/api/overview), de Anthropic.
- Sincronización opcional: [API de Gists de GitHub](https://docs.github.com/en/rest/gists).

Casilla no está afiliada a Chess.com, Lichess, Anthropic ni GitHub.

## Licencia

Casilla se distribuye bajo la licencia [GPL-3.0](LICENSE). Puedes usarla, estudiarla, modificarla y compartirla, siempre que tus versiones también se publiquen bajo GPL-3.0 y conserven los créditos. Los sets de piezas y el motor Stockfish mantienen sus propias licencias, indicadas en la sección de créditos.

Algunos archivos de terceros tienen otra licencia y la conservan:
- Piezas Pixel, Pirouetti y Letras, y las texturas Arce y Veteado, están bajo **AGPL-3.0 o posterior** ([texto](docs/licencias/AGPL-3.0.txt)). La GPL-3.0 (sección 13) permite combinarlas con Casilla; esos archivos mantienen la obligación de ofrecer el código fuente a quien use la app por red. El código fuente completo está en https://github.com/FerHuCa/Casilla, enlazado desde el pie de la app.
- Shapes (CC BY-SA 4.0) y Firi (CC BY 4.0) piden atribución, que va en el pie de la app y en esta página.
- Copia de `COPYING.md` de lila (commit 02284e0), de donde salen autores y licencias: [docs/licencias/COPYING-lila.md](docs/licencias/COPYING-lila.md).
