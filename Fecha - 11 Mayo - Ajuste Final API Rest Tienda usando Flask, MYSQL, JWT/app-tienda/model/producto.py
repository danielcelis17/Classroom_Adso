from model.serializar import valor_json


class Producto:

    def __init__(self, nombre_producto, precio_unitario, producto_id=0, descripcion=None,
                 stock=0, iva_porcentaje=19):
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.stock = stock
        self.iva_porcentaje = iva_porcentaje

    @classmethod
    def from_row(cls, registro):
        producto_id, nombre_producto, descripcion, precio_unitario, stock, iva_porcentaje = registro
        return cls(nombre_producto, precio_unitario, producto_id, descripcion, stock, iva_porcentaje)

    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "nombre_producto": self.nombre_producto,
            "descripcion": self.descripcion,
            "precio_unitario": valor_json(self.precio_unitario),
            "stock": self.stock,
            "iva_porcentaje": valor_json(self.iva_porcentaje),
        }
