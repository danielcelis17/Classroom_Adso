class Pedido:
    def __init__(self, total, id_cliente, id_comercial, id=0, fecha=None):
        self.id = id
        self.total = total
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.id_comercial = id_comercial

    def to_dict(self):
        return {
            "id": self.id,
            "total": self.total,
            "fecha": str(self.fecha) if self.fecha else None,
            "id_cliente": self.id_cliente,
            "id_comercial": self.id_comercial,
        }
