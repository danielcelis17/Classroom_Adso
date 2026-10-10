class Usuario:
    def __init__(self, nombre, correo, username, password, id=0):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "username": self.username,
        }
