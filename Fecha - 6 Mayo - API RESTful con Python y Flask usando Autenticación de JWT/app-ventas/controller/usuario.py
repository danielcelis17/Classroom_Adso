from config.db import conexion
from model.usuario import Usuario

def add_usuario(usuario):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios (nombre, correo, username, password) VALUES(%s, %s, %s, %s)", (usuario.nombre, usuario.correo, usuario.username, usuario.password ))
    con.commit()
    con.close()

def login(username, password):
    con = conexion()
    with con.cursor() as cursor:
        # Columnas en el orden del constructor de Usuario
        cursor.execute("SELECT nombre, correo, username, password, id FROM usuarios WHERE username=%s AND password=%s", (username, password))
        registro = cursor.fetchone()
    con.close()
    if registro:
        return Usuario(*registro)
    return None
