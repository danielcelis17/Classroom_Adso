import os

import pymysql


def conexion():
    # Valores por defecto = los de la guía; en Docker se sobrescriben con variables de entorno.
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "tienda"),
        charset="utf8mb4",
    )
