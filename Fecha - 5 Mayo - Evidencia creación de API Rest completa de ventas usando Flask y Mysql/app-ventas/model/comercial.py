class Comercial:
    def __init__(self, nombre, apellido1, id=0, apellido2=None, comision=0):
        self.id = id
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.comision = comision

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido1": self.apellido1,
            "apellido2": self.apellido2,
            "comision": self.comision,
        }
