from config.db import conexion
from model.comercial import Comercial

def get_comerciales():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM comercial")
        registros = cursor.fetchall()
    con.close()
    return registros

def add_comercial(comercial):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO comercial (nombre, apellido1, apellido2, comision) VALUES(%s, %s, %s, %s)", (comercial.nombre, comercial.apellido1, comercial.apellido2, comercial.comision ))
    con.commit()
    con.close()

def get_comercial(id):
    con = conexion()
    with con.cursor() as cursor:
        # Columnas en el orden del constructor de Comercial (misma corrección que get_cliente)
        cursor.execute("SELECT nombre, apellido1, id, apellido2, comision FROM comercial WHERE id=%s", id)
        registro = cursor.fetchone()
        comercial=Comercial(*registro)
    con.close()
    return comercial

def delete_comercial(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM comercial WHERE id=%s", id)
    con.commit()
    con.close()

def update_comercial(id, comercial):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("UPDATE comercial SET nombre=%s, apellido1=%s, apellido2=%s, comision=%s WHERE id=%s", (comercial.nombre, comercial.apellido1, comercial.apellido2, comercial.comision, id ))
    con.commit()
    con.close()
