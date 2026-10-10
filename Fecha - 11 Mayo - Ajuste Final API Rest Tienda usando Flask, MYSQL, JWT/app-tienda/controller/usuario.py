from werkzeug.security import check_password_hash, generate_password_hash

from config.db import conexion
from model.usuario import Usuario


def add_usuario(usuario):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, username, password) VALUES(%s, %s, %s, %s)",
            (usuario.nombre, usuario.correo, usuario.username, generate_password_hash(str(usuario.password))),
        )
    con.commit()
    con.close()


def get_usuario(username):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute("SELECT id, nombre, correo, username, password FROM usuarios WHERE username=%s", (username,))
        registro = cursor.fetchone()
    con.close()
    return Usuario.from_row(registro) if registro else None


def login(username, password):
    """Devuelve el usuario si el username existe y el password coincide con su hash; si no, None."""
    usuario = get_usuario(username)
    if usuario and check_password_hash(usuario.password, password):
        return usuario
    return None
