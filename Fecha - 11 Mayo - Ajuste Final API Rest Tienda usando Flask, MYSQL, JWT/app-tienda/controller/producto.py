from config.db import conexion
from model.producto import Producto

COLUMNAS = "producto_id, nombre_producto, descripcion, precio_unitario, stock, iva_porcentaje"


def get_productos():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM productos")
        registros = cursor.fetchall()
    productos = [Producto.from_row(registro) for registro in registros]
    con.close()
    return productos


def add_producto(producto):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(
            "INSERT INTO productos (nombre_producto, descripcion, precio_unitario, stock, iva_porcentaje) "
            "VALUES(%s, %s, %s, %s, %s)",
            (producto.nombre_producto, producto.descripcion, producto.precio_unitario,
             producto.stock, producto.iva_porcentaje),
        )
        producto_id = cursor.lastrowid
    con.commit()
    con.close()
    return producto_id


def get_producto(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM productos WHERE producto_id=%s", (id,))
        registro = cursor.fetchone()
    con.close()
    return Producto.from_row(registro) if registro else None


def delete_producto(id):
    con = conexion()
    with con.cursor() as cursor:
        filas = cursor.execute("DELETE FROM productos WHERE producto_id=%s", (id,))
    con.commit()
    con.close()
    return filas


def update_producto(id, producto):
    con = conexion()
    with con.cursor() as cursor:
        filas = cursor.execute(
            "UPDATE productos SET nombre_producto=%s, descripcion=%s, precio_unitario=%s, stock=%s, "
            "iva_porcentaje=%s WHERE producto_id=%s",
            (producto.nombre_producto, producto.descripcion, producto.precio_unitario,
             producto.stock, producto.iva_porcentaje, id),
        )
    con.commit()
    con.close()
    return filas
