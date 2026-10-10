class Usuario:

    def __init__(self, nombre, correo, username, password, id=0):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.username = username
        self.password = password

    @classmethod
    def from_row(cls, registro):
        id, nombre, correo, username, password = registro
        return cls(nombre, correo, username, password, id)

    def to_dict(self):
        # El password (hash) nunca se devuelve en las respuestas
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "username": self.username,
        }
