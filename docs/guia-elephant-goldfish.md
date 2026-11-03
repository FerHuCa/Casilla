# Guía: revisión Elephant Goldfish (EGM)

## Qué es

Una revisión de **documentos de diseño** (planes), no de código ni de la interfaz visual. Varios revisores leen el documento, cada uno en un contexto aislado y sin historial, y lo contrastan con el código real. El resultado es un informe con acciones por prioridad (🔴 bloqueantes, 🟡 mayores, 🟢 menores); no modifica el plan ni ningún otro archivo. **No ve el mockup ni `tests/` si no se los das.**

En la revisión del plan del rediseño (3 nov 2026, `egm-review-plan.md`) se ejecutaron cinco etapas:

| Etapa | Revisores | Qué leen |
|---|---|---|
| 5. Zoom out inicial | `egm-zoom-out` | Plan completo |
| 6. Comprensión | `egm-comprehension` | Solo el plan, sin contexto |
| 7. Crítica | `egm-design`, `egm-structural`, `egm-style` | Parte de intención |
| 8. Zoom out intermedio | `egm-zoom-out` | Plan completo y lo hallado antes |
| 9. Preparación para implementar | `egm-implementation-readiness`, `egm-codebase-details`, `egm-style` | Parte de implementación |

Esa vez detectó que el plan describía un `index.html` distinto del real. Por ejemplo, poner `defer` en chess.js habría dejado la página en blanco.

## Cuándo usarla

Solo para cambios grandes o riesgosos, **no en cada PR**, y **antes** de escribir código. Por ejemplo:

- Dividir `index.html` en módulos o archivos.
- Cambios de seguridad de chess.js (SRI, vendorizarlo, el arranque) u otros de seguridad (CSP, `innerHTML`).
- Cambios en la sincronización entre dispositivos (gist, `casilla.v1`, presets).
- Más de ~200 líneas o varios módulos.

## Cuándo no

- Cambios chicos de CSS o de texto.
- Revisar código ya escrito o la interfaz: para eso están los tests, las capturas, el QA de Tony y `npx impeccable detect` (ver `guia-impeccable.md`).

## Cómo correrla

1. Clona el plugin (una sola vez):
   ```bash
   git clone https://github.com/google/elephant-goldfish-model /workspace/steve/egm
   ```
2. Revisa el uso de la suscripción. **Si está en 80% o más, no la corras.**
   ```bash
   /home/box/.local/bin/claude-usage
   ```
3. Abre la sesión con el plugin cargado solo para esa sesión, sin clave de pago:
   ```bash
   cd /workspace/steve/casilla && env -u ANTHROPIC_API_KEY /home/box/.local/bin/claude-max --plugin-dir /workspace/steve/egm
   ```
4. Dentro de la sesión, pide que redacte el documento de diseño del cambio y que lo pase por la revisión de cinco etapas de EGM.

Reglas:

- **Nunca uses `claude` a secas**, porque cobra por API.
- **No instales el plugin globalmente**; usa siempre `--plugin-dir`.
- Dale al revisor el contexto que necesita. Lo que no reciba quedará como "no verificado"; en la prueba faltaron `tests/`, `sw.js`, `manifest` y el mockup.
- Comprueba tú mismo en el código los hallazgos bloqueantes y los desacuerdos entre revisores. En la prueba, un revisor se equivocó y otro solo revisó una parte del archivo.

## Costo

- **US$0 de API** con `claude-max`.
- Gasta uso de la suscripción: en una corrida pasó **del 2% al 10%**. Por eso se revisa `claude-usage` antes (paso 2).
