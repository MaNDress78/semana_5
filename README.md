# Tienda de componentes — Memoria RAM en oferta

**Integrantes:** Maicol Ramos Betancourt y Eduardo Tovar Roa.

Proyecto de la semana 5: primera funcionalidad con pruebas y bitácora de IA.
Incluye una página web sencilla que muestra una Memoria RAM en oferta y la
lista de ganancias de sus ventas, respaldada por una base de datos SQLite.

## Funcionalidad de la semana 5

### Historia de usuario

**HU-05 — Precio según stock bajo**

Como dueña de una página que vende componentes en descuento, quiero que
cuando queden solo 10 unidades de un producto el precio suba al 100 % de su
valor real, para atraer tráfico con las primeras ventas sin perder dinero.

### Criterio de aceptación

- Dado un producto con costo 150, precio real 200, precio de oferta 100 y
  stock inicial 20.
- Mientras el stock sea mayor a 10, la unidad se vende a 100: ganancia -50 y
  descuento 50 %.
- Cuando el stock sea 10 o menos (antes de registrar la venta), la unidad se
  vende a 200: ganancia +50 y descuento 0 %.
- Cada venta queda registrada con su hora y se refleja en el reporte.
- Si el producto no existe o no hay stock, la operación falla con `ValueError`
  y no registra la venta.

### Contrato de la función

Módulo: `codigo/tienda/ofertas.py`

| Firma | Recibe | Devuelve |
|---|---|---|
| `crear_esquema(conn: sqlite3.Connection) -> None` | Conexión SQLite | `None` (crea las tablas `productos` y `ventas`) |
| `crear_producto(conn, nombre: str, costo: float, precio_real: float, precio_oferta: float, stock: int) -> int` | Conexión y datos del producto | `id` del producto creado |
| `registrar_venta(conn, producto_id: int, comprador: str, hora_venta: str) -> None` | Conexión, producto, comprador y hora | `None` (calcula el precio y descuenta stock) |
| `maicol_and_opencode(conn) -> list[dict]` | Conexión SQLite | Lista de filas con `nombre`, `hora_venta`, `ganancia` y `descuento_pct` |

**Supuestos y límites**

- Solo se usa la librería estándar de Python (`sqlite3`).
- El umbral es fijo: `UMBRAL_STOCK = 10`.
- El precio se decide con el stock que hay **antes** de registrar la venta.
- Con exactamente 10 unidades en stock la venta ya sale a precio real.
- El reporte se ordena por `hora_venta` ascendente.
- Un producto inexistente o sin stock lanza `ValueError` y no registra nada.
- No se valida que todos los compradores sean distintos.

**Ejemplos de entrada y salida**

1. Primera venta con stock 20:
   ```json
   {
     "nombre": "Memoria RAM",
     "hora_venta": "2026-11-07 10:00:00",
     "ganancia": -50.0,
     "descuento_pct": 50.0
   }
   ```

2. Venta número 11 (quedan 10 unidades antes de vender):
   ```json
   {
     "nombre": "Memoria RAM",
     "hora_venta": "2026-11-07 10:10:00",
     "ganancia": 50.0,
     "descuento_pct": 0.0
   }
   ```

3. Sin ventas registradas:
   ```json
   []
   ```

4. Vender un producto con `producto_id` inexistente:
   ```text
   ValueError: El producto no existe
   ```

## Cómo ejecutar las pruebas

```bash
cd codigo
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -v
```

Resultado esperado: `9 passed`.

Las pruebas están en `codigo/tests/test_ofertas.py` y cubren casos normales,
casos límite y casos de error.

## Cómo ejecutar la página

```bash
cd codigo
python3 servidor.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:8765
```

El servidor crea la base de datos automáticamente en
`codigo/pagina_web/tienda.db` si todavía no existe. La página permite comprar,
cargar las 20 ventas de ejemplo y reiniciar la demostración.

## Estructura del repositorio

```text
trabajo_semana_5/
├── README.md
├── bitacora_ia.md
├── pruebas_base_de_datos.txt
├── evidencia_del_trabajo
├── Tarea_Semana_5.pdf
└── codigo/
    ├── pytest.ini
    ├── crear_base_de_datos.py
    ├── servidor.py
    ├── tienda/
    │   ├── __init__.py
    │   └── ofertas.py
    ├── tests/
    │   └── test_ofertas.py
    └── pagina_web/
        ├── index.html
        └── tienda.db   (se genera al ejecutar el servidor)
```

## Uso de IA

Las decisiones, la verificación y las reflexiones sobre el uso del asistente
están documentadas en `bitacora_ia.md`.
