from config.db import conexion
from model.cliente import Cliente

def get_clientes():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM cliente")
        registros = cursor.fetchall()
        user_objects = [Cliente(*registro) for registro in registros]
    con.close()
    return registros

def add_cliente(cliente):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO cliente (nombre, apellido1, apellido2, ciudad, categoria) VALUES(%s, %s, %s, %s, %s)", (cliente.nombre, cliente.apellido1, cliente.apellido2, cliente.ciudad, cliente.categoria ))
    con.commit()
    con.close()

def get_cliente(id):
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        # Corrección a la guía: con "SELECT *" la fila llega como (id, nombre, apellido1, ...)
        # y Cliente(*registro) ponía el id en nombre. Se piden las columnas en el orden del constructor.
        cursor.execute("SELECT nombre, apellido1, id, apellido2, ciudad, categoria FROM cliente WHERE id=%s", id)
        registro = cursor.fetchone()
        cliente=Cliente(*registro)
    con.close()
    return cliente

def delete_cliente(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM cliente WHERE id=%s", id)
    con.commit()
    con.close()

def update_cliente(id, cliente):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("UPDATE cliente SET nombre=%s, apellido1=%s, apellido2=%s, ciudad=%s, categoria=%s WHERE id=%s", (cliente.nombre, cliente.apellido1, cliente.apellido2, cliente.ciudad, cliente.categoria, id ))
    con.commit()
    con.close()
