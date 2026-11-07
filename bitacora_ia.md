# Bitácora de uso de IA

Proyecto: Tienda de componentes (Memoria RAM en oferta)
Estudiante: Maicol Ramos Betancourt
Funcionalidad: HU-[xx] Cuando quedan 10 unidades, el precio sube al 100 % del valor real
Asistente usado: OpenCode en modo agente, con OpenRouter como proveedor (API key); modelos: Big Pickle, Claude Sonnet 5.5 y DeepSeek 4.2.

## Entradas

### Entrada 1

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Pedí una página web extremadamente sencilla, con la RAM para comprar en la mitad superior y la lista de ganancias en la inferior, siguiendo el formato del contexto (`evidencia_del_trabajo`), sin crear todavía la base de datos y respondiendo antes todas las dudas del asistente. El asistente preguntó si el botón debía funcionar, dónde guardar la página, qué datos de ejemplo usar y qué estilo visual.
- **Decisión:** Aceptada con cambios
- **Por qué:** La estructura propuesta (un solo `index.html`, estilo minimalista claro, datos de ejemplo del contexto) me sirvió tal cual. Lo que cambié fue mi plan inicial: pensaba entregar una página con datos quemados, pero preferí hacer algo simple y a la vez funcional, así que pedí que el botón «Comprar» quedara preparado para conectarse a la base de datos.
- **Verificación:** Abrí la página y revisé que la mitad superior mostrara la RAM (oferta $100, precio real $200, 50 % de descuento) y que la inferior tuviera la tabla con producto, hora de venta, ganancia y descuento, como en el ejemplo del contexto.
- **Commit relacionado:** [pendiente: hash o mensaje]

### Entrada 2

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** «Procede con la creación de la base de datos para la página». El asistente creó `tienda/ofertas.py` (con `crear_esquema`, `crear_producto`, `registrar_venta` y `maicol_and_opencode`), `crear_base_de_datos.py`, `servidor.py` con una API local y conectó la página a SQLite.
- **Decisión:** Aceptada
- **Por qué:** Cumple el contrato del contexto: solo librería estándar, firma sin cambios y tablas `productos` y `ventas`. Además, deja funcional lo que antes era solo visual.
- **Verificación:** Ejecuté las pruebas del documento contra esta implementación (ver entrada 4) y revisé que la base `tienda.db` se creara con la RAM (costo 150, precio real 200, oferta 100, stock 20).
- **Commit relacionado:** [pendiente: hash o mensaje]

### Entrada 3

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** «Abre la página web». El asistente inició `python3 servidor.py`; como el puerto 8000 estaba ocupado, usó el 8765.
- **Decisión:** Aceptada
- **Por qué:** El cambio de puerto no afecta el contrato ni el comportamiento de la página, solo la dirección local.
- **Verificación:** El servidor respondió HTTP 200 y la página cargó en `http://127.0.0.1:8765`.
- **Commit relacionado:** [pendiente: hash o mensaje]

### Entrada 4

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** «Corre las pruebas que hay en el documento, pregunta si no te cuadra algo». El asistente ejecutó las 9 pruebas con pytest en el entorno `.venv`.
- **Decisión:** Aceptada
- **Por qué:** Las pruebas son la referencia del contrato (casos normales, de límite y de error) y las escribí antes de la implementación, así que no se modificó ninguna.
- **Verificación:** `.venv/bin/python -m pytest -v` dio `9 passed`.
- **Commit relacionado:** [pendiente: hash o mensaje]

### Entrada 5

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Regla del umbral generada por el asistente: mientras queden más de 10 unidades se vende a $100 (ganancia -$50, 50 %); con 10 o menos se vende a $200 (ganancia +$50, 0 %). El objetivo de negocio es endeudarse con las 10 primeras unidades para atraer tráfico y recuperarse con las 10 últimas, de modo que se atrae tráfico sin perder dinero.
- **Decisión:** Aceptada
- **Por qué:** Con esa regla las 20 ventas del ejemplo dan 10 × (-50) + 10 × (+50) = 0, es decir, punto de equilibrio. Eso es justo lo que pide la historia de usuario.
- **Verificación:** Las pruebas de límite (11 unidades sigue en oferta, 10 unidades sube a precio real, stock inicial igual al umbral) pasan, y la suma de la ganancia en la tabla de las 20 ventas de ejemplo da 0.
- **Commit relacionado:** [pendiente: hash o mensaje]

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 4 |
| Aceptadas con cambios | 1 |
| Rechazadas | 0 |

## Errores que atraparon las pruebas

En la ejecución registrada, las 9 pruebas pasaron a la primera, así que no hay un fallo real que documentar. [Pendiente: si durante el desarrollo falló alguna prueba, describir cuál, por qué falló y cómo se corrigió.]

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más al montar de una sola vez la página, la base de datos SQLite y el servidor a partir del contrato, algo que a mano me habría tomado bastante más. Cambié mi plan inicial de entregar una página con datos quemados porque preferí algo simple pero funcional. Las pruebas escritas antes del código fueron la guía: las de límite (11, 10 y stock inicial igual al umbral) confirman la regla de negocio de endeudarse con las 10 primeras unidades y recuperarse con las 10 últimas. En esta ejecución no encontraron ningún fallo, y no quiero presentarlo como si lo hubieran hecho. En la próxima funcionalidad haría los commits de pruebas en rojo, en verde y de refactor desde el principio, y agregaría una prueba para el supuesto de que no todo se venda a la misma persona, que hoy no está cubierto.
