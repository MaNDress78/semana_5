import json
import sqlite3
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from tienda.ofertas import (
    UMBRAL_STOCK,
    crear_esquema,
    crear_producto,
    maicol_and_opencode,
    registrar_venta,
)

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "pagina_web"
RUTA_BD = WEB_DIR / "tienda.db"

PRODUCTO_INICIAL = {
    "nombre": "Memoria RAM",
    "costo": 150.0,
    "precio_real": 200.0,
    "precio_oferta": 100.0,
    "stock": 20,
}


def conectar() -> sqlite3.Connection:
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


def asegurar_base_de_datos() -> None:
    RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
    conexion = conectar()
    try:
        crear_esquema(conexion)
        total = conexion.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
        if total == 0:
            crear_producto(conexion, **PRODUCTO_INICIAL)
    finally:
        conexion.close()


def estado(conexion: sqlite3.Connection) -> dict:
    fila = conexion.execute("SELECT * FROM productos ORDER BY id LIMIT 1").fetchone()
    producto = None
    if fila is not None:
        stock = fila["stock"]
        precio = fila["precio_oferta"] if stock > UMBRAL_STOCK else fila["precio_real"]
        descuento = round((fila["precio_real"] - precio) / fila["precio_real"] * 100, 2)
        producto = {
            "id": fila["id"],
            "nombre": fila["nombre"],
            "costo": fila["costo"],
            "precio_real": fila["precio_real"],
            "precio_oferta": fila["precio_oferta"],
            "stock": stock,
            "precio_actual": precio,
            "descuento_pct": descuento,
        }
    return {"producto": producto, "ventas": maicol_and_opencode(conexion)}


def reiniciar(con_ejemplo: bool) -> None:
    conexion = conectar()
    try:
        conexion.executescript("DROP TABLE IF EXISTS ventas; DROP TABLE IF EXISTS productos;")
        crear_esquema(conexion)
        producto_id = crear_producto(conexion, **PRODUCTO_INICIAL)
        if con_ejemplo:
            for i in range(20):
                registrar_venta(
                    conexion,
                    producto_id,
                    f"cliente{i + 1}",
                    f"2026-11-07 10:{i:02d}:00",
                )
    finally:
        conexion.close()


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def responder_json(self, datos: dict, estado_http: int = 200) -> None:
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(estado_http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def estado_actual(self) -> dict:
        conexion = conectar()
        try:
            return estado(conexion)
        finally:
            conexion.close()

    def do_GET(self) -> None:
        ruta = urlparse(self.path).path
        if ruta == "/api/estado":
            self.responder_json(self.estado_actual())
            return
        if ruta == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        ruta = urlparse(self.path).path
        try:
            if ruta == "/api/comprar":
                conexion = conectar()
                try:
                    fila = conexion.execute(
                        "SELECT id FROM productos ORDER BY id LIMIT 1"
                    ).fetchone()
                    if fila is None:
                        self.responder_json({"error": "No hay productos disponibles"}, 400)
                        return
                    registrar_venta(
                        conexion,
                        fila["id"],
                        "cliente-web",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                finally:
                    conexion.close()
                self.responder_json(self.estado_actual())
                return
            if ruta == "/api/ejemplo":
                reiniciar(con_ejemplo=True)
                self.responder_json(self.estado_actual())
                return
            if ruta == "/api/reiniciar":
                reiniciar(con_ejemplo=False)
                self.responder_json(self.estado_actual())
                return
            self.responder_json({"error": "Ruta no encontrada"}, 404)
        except ValueError as error:
            self.responder_json({"error": str(error)}, 400)

    def log_message(self, formato: str, *args) -> None:
        print(f"[servidor] {self.address_string()} - {formato % args}")


def main() -> None:
    asegurar_base_de_datos()
    servidor = ThreadingHTTPServer(("127.0.0.1", 8765), Manejador)
    print("Servidor listo en http://127.0.0.1:8765")
    print(f"Base de datos: {RUTA_BD}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
