# Comentarios con IA: guía de uso

Guía para quien usa Casilla. Aquí se habla de «la IA» y de «el motor», igual que en la app. El detalle técnico está en [claude-partidas.md](claude-partidas.md).

## Nada se cobra sin un clic

La IA ya no comenta las partidas por su cuenta. Abrir una partida, una evaluación o un ejercicio no hace ninguna consulta. Solo se consulta a la IA, y solo cuesta, cuando pulsas uno de estos botones:

- **Comentar partida con IA**
- **Volver a comentar**
- **Ver pista** (en Mis errores, si la pista no estaba guardada)
- **Ver explicación de la IA** (en Mis errores, si la explicación no estaba guardada)

El comentario final que antes se escribía solo al terminar la evaluación se quitó. Sin pulsar nada ves el **comentario del maestro (sin IA)**, que se arma en tu navegador y no cuesta.

## Comentar una partida

1. Abre una partida: una de Chess.com analizada (en Partidas) o una jugada en Casilla (su evaluación completa).
2. Pulsa **Comentar partida con IA**. Se envía en una sola consulta la partida con las evaluaciones del motor y tus errores.
3. La IA escribe un resumen y un comentario por cada error, con **Ver en el tablero** para ir a esa jugada. Puedes **Cancelar** mientras escribe.

La IA solo redacta: las jugadas, las líneas y las evaluaciones son del motor, y el texto puede tener errores. Debajo del comentario aparece su costo aproximado.

### Chess.com y partidas jugadas en Casilla funcionan igual

- **Chess.com:** el bloque va arriba de Momentos clave.
- **Jugadas en Casilla** (Escalera, contra el maestro o desde una posición): el bloque va en la evaluación, en lugar del comentario del maestro. Arriba dice de dónde viene la partida, por ejemplo «Jugada en Casilla · Contra el maestro · fecha», con la apertura si se reconoce. Con el comentario hecho, **Repasar estos errores como puzzles** queda dentro del bloque.

En los dos casos es el mismo botón, el mismo resumen con un comentario por error, y los mismos **Volver a comentar** y **Borrar comentario**.

## Se guarda: recargar no vuelve a cobrar

- El comentario de la partida y las pistas y explicaciones de sus errores se guardan con el análisis.
- Al recargar la página o volver a abrir la partida se muestran los guardados, sin otra consulta.
- Si vuelves a analizar la partida, el comentario se conserva.
- Si sales de la partida mientras la IA escribe, la respuesta se guarda igual (ya se pagó) y aparece al volver.
- Solo **Volver a comentar** hace una consulta nueva y vuelve a cobrar.
- Los comentarios se sincronizan entre tus dispositivos; la clave no.

## Borrar comentario

**Borrar comentario** quita el comentario de la partida y también las pistas y explicaciones de la IA de sus errores. El borrado se sincroniza: otro dispositivo que todavía tenga el comentario viejo no lo trae de vuelta. Si después comentas otra vez, el comentario nuevo sí se sincroniza.

## Mis errores: «Ver pista» y «Ver explicación de la IA»

En los puzzles de **Mis errores**, con tu clave:

- **Ver pista** muestra una pista escrita por la IA antes de resolver. Cuenta como ayuda, igual que la pista del motor, y se anota al terminar (ya no aparece el aviso de rating antes de resolver).
- Al terminar, **Ver explicación de la IA** pide la explicación. Nunca se pide sola. La explicación del motor sigue debajo.
- Si ya comentaste esa partida con IA, la pista y la explicación ya están guardadas: se muestran sin otra consulta.
- El ejercicio siempre se resuelve contra la mejor jugada del motor y sigue en el repaso espaciado.

## Tu clave y lo que gastas

- **Cada persona pone su propia clave**, en su navegador: pestaña **Maestro**, sección **Comentarios con IA (opcional)**. Pasos en [Clave de IA](../README.md#clave-de-ia).
- La clave se queda solo en ese navegador: no se sincroniza ni va en los respaldos. Pégala en cada navegador donde quieras usar la IA.
- **Gasto aproximado:** debajo de la clave, Maestro muestra las partidas comentadas, los ejercicios con pista, los tokens y un total aproximado en dólares. Se calcula en tu navegador; no incluye otros dispositivos. **Reiniciar contador** lo pone en cero.
- **El gasto real** se ve en la consola de tu cuenta de IA: **Ver gasto real en la consola**, https://platform.claude.com/cost.

## Si algo falla

Si falta la clave, la clave no sirve, el servicio no dio permiso o no hay conexión, el bloque lo dice y te lleva a la clave. Con **Reintentar** lo vuelves a intentar.
