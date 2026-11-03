# Guía: revisión de calidad con impeccable

## Qué es

`npx impeccable detect` busca patrones de interfaz de baja calidad, como palabras sueltas, bajo contraste, franjas laterales de color o halos con degradado. Es **gratis y local**. Úsalo como revisión de calidad **antes de cada entrega**.

## Cómo correrlo

```bash
# Escaneo estático del archivo
npx impeccable detect index.html

# Página renderizada (sirve Casilla en local primero; usa tu Chrome o Edge instalado)
# 8773 es solo un ejemplo: usa el puerto de tu servidor local, p. ej. 8773
npx impeccable detect http://localhost:8773/index.html

# Salida legible por máquina, para guardarla y comparar antes/después
npx impeccable detect --json . > imp-after.json

# Lista de reglas con su id y descripción
npx impeccable detect --list-rules
```

Corre los dos escaneos. Las reglas de bajo contraste y de texto diminuto solo se aplican al escanear la URL (la página renderizada), no el archivo.

Códigos de salida:

- `2`: hubo hallazgos.
- `1`: no pudo escanear.

## Cómo leer los resultados

Cada hallazgo trae `antipattern`, `name`, `description`, `severity` (`warning` o `advisory`), `category` (`slop` o `quality`), `file`, `snippet` y, en la versión renderizada, `selector`. Por ejemplo:

- `straggler` (advisory): queda una palabra sola en la última línea. Se corrige con `text-wrap: pretty`.
- `side-tab` (warning): un borde grueso en un solo lado de una tarjeta.
- `radial-halo` (warning): un halo de `radial-gradient` sobre un fondo oscuro.

Un resultado `[]` significa que no hay hallazgos. Guarda el JSON de antes y el de después y compáralos. En la prueba de Sam, la página renderizada pasó a `[]`, pero el escaneo estático siguió marcando un `radial-halo` (#c83228), que quedó fuera del alcance. No hace falta corregir todo; si un hallazgo no se toca, anótalo en el PR.

## Qué no hacer

- **No uses el modo live** (`/impeccable live`). Reescribe el código fuente desde el navegador y puede lanzar un agente con aprobaciones y sandbox desactivados.
- No sustituye los tests (`apariencia_contraste.py`, capturas) ni el QA de Tony.
