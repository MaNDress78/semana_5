import sqlite3
from pathlib import Path

from tienda.ofertas import crear_esquema, crear_producto

BASE_DIR = Path(__file__).resolve().parent
RUTA_BD = BASE_DIR / "pagina_web" / "tienda.db"

PRODUCTO_INICIAL = {
    "nombre": "Memoria RAM",
    "costo": 150.0,
    "precio_real": 200.0,
    "precio_oferta": 100.0,
    "stock": 20,
}


def main() -> None:
    RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(RUTA_BD)
    try:
        crear_esquema(conexion)
        conexion.execute("DELETE FROM ventas")
        conexion.execute("DELETE FROM productos")
        conexion.commit()
        crear_producto(conexion, **PRODUCTO_INICIAL)
    finally:
        conexion.close()
    print(f"Base de datos creada en: {RUTA_BD}")


if __name__ == "__main__":
    main()
