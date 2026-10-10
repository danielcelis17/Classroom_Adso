from config.db import conexion
from model.pedido import Pedido

def get_pedidos():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM pedido")
        registros = cursor.fetchall()
    con.close()
    return registros

def add_pedido(pedido):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO pedido (total, fecha, id_cliente, id_comercial) VALUES(%s, %s, %s, %s)", (pedido.total, pedido.fecha, pedido.id_cliente, pedido.id_comercial ))
    con.commit()
    con.close()

def get_pedido(id):
    con = conexion()
    with con.cursor() as cursor:
        # Columnas en el orden del constructor de Pedido (misma corrección que get_cliente)
        cursor.execute("SELECT total, id_cliente, id_comercial, id, fecha FROM pedido WHERE id=%s", id)
        registro = cursor.fetchone()
        pedido=Pedido(*registro)
    con.close()
    return pedido

def delete_pedido(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM pedido WHERE id=%s", id)
    con.commit()
    con.close()

def update_pedido(id, pedido):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("UPDATE pedido SET total=%s, fecha=%s, id_cliente=%s, id_comercial=%s WHERE id=%s", (pedido.total, pedido.fecha, pedido.id_cliente, pedido.id_comercial, id ))
    con.commit()
    con.close()
