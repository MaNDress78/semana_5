import sqlite3

UMBRAL_STOCK = 10


def crear_esquema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            costo REAL NOT NULL,
            precio_real REAL NOT NULL,
            precio_oferta REAL NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            comprador TEXT NOT NULL,
            hora_venta TEXT NOT NULL,
            precio REAL NOT NULL,
            costo REAL NOT NULL,
            descuento_pct REAL NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        );
        """
    )
    conn.commit()


def crear_producto(
    conn: sqlite3.Connection,
    nombre: str,
    costo: float,
    precio_real: float,
    precio_oferta: float,
    stock: int,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO productos (nombre, costo, precio_real, precio_oferta, stock)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre, costo, precio_real, precio_oferta, stock),
    )
    conn.commit()
    return int(cursor.lastrowid)


def registrar_venta(
    conn: sqlite3.Connection,
    producto_id: int,
    comprador: str,
    hora_venta: str,
) -> None:
    fila = conn.execute(
        "SELECT costo, precio_real, precio_oferta, stock FROM productos WHERE id = ?",
        (producto_id,),
    ).fetchone()

    if fila is None:
        raise ValueError("El producto no existe")

    costo, precio_real, precio_oferta, stock = fila

    if stock <= 0:
        raise ValueError("No hay stock disponible")

    precio = precio_oferta if stock > UMBRAL_STOCK else precio_real
    descuento_pct = round((precio_real - precio) / precio_real * 100, 2)

    conn.execute(
        """
        INSERT INTO ventas (producto_id, comprador, hora_venta, precio, costo, descuento_pct)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (producto_id, comprador, hora_venta, precio, costo, descuento_pct),
    )
    conn.execute(
        "UPDATE productos SET stock = stock - 1 WHERE id = ?",
        (producto_id,),
    )
    conn.commit()


def maicol_and_opencode(conn: sqlite3.Connection) -> list[dict]:
    filas = conn.execute(
        """
        SELECT p.nombre, v.hora_venta, v.precio - v.costo AS ganancia, v.descuento_pct
        FROM ventas AS v
        JOIN productos AS p ON p.id = v.producto_id
        ORDER BY v.hora_venta ASC
        """
    ).fetchall()

    return [
        {
            "nombre": nombre,
            "hora_venta": hora_venta,
            "ganancia": float(ganancia),
            "descuento_pct": float(descuento_pct),
        }
        for nombre, hora_venta, ganancia, descuento_pct in filas
    ]
