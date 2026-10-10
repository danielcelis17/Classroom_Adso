from model.serializar import valor_json


class Cliente:

    def __init__(self, numero_documento, nombre, apellido, cliente_id=0, tipo_documento="CC",
                 telefono=None, email=None, direccion=None, ciudad="Bogotá", fecha_registro=None):
        self.cliente_id = cliente_id
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.ciudad = ciudad
        self.fecha_registro = fecha_registro

    @classmethod
    def from_row(cls, registro):
        (cliente_id, tipo_documento, numero_documento, nombre, apellido,
         telefono, email, direccion, ciudad, fecha_registro) = registro
        return cls(numero_documento, nombre, apellido, cliente_id, tipo_documento,
                   telefono, email, direccion, ciudad, fecha_registro)

    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "fecha_registro": valor_json(self.fecha_registro),
        }
