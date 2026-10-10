from config.db import conexion
from model.cliente import Cliente

COLUMNAS = ("cliente_id, tipo_documento, numero_documento, nombre, apellido, "
            "telefono, email, direccion, ciudad, fecha_registro")


def get_clientes():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM clientes")
        registros = cursor.fetchall()
    clientes = [Cliente.from_row(registro) for registro in registros]
    con.close()
    return clientes


def add_cliente(cliente):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(
            "INSERT INTO clientes (tipo_documento, numero_documento, nombre, apellido, telefono, email, direccion, ciudad) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (cliente.tipo_documento, cliente.numero_documento, cliente.nombre, cliente.apellido,
             cliente.telefono, cliente.email, cliente.direccion, cliente.ciudad),
        )
        cliente_id = cursor.lastrowid
    con.commit()
    con.close()
    return cliente_id


def get_cliente(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM clientes WHERE cliente_id=%s", (id,))
        registro = cursor.fetchone()
    con.close()
    return Cliente.from_row(registro) if registro else None


def delete_cliente(id):
    con = conexion()
    with con.cursor() as cursor:
        filas = cursor.execute("DELETE FROM clientes WHERE cliente_id=%s", (id,))
    con.commit()
    con.close()
    return filas


def update_cliente(id, cliente):
    con = conexion()
    with con.cursor() as cursor:
        filas = cursor.execute(
            "UPDATE clientes SET tipo_documento=%s, numero_documento=%s, nombre=%s, apellido=%s, "
            "telefono=%s, email=%s, direccion=%s, ciudad=%s WHERE cliente_id=%s",
            (cliente.tipo_documento, cliente.numero_documento, cliente.nombre, cliente.apellido,
             cliente.telefono, cliente.email, cliente.direccion, cliente.ciudad, id),
        )
    con.commit()
    con.close()
    return filas
