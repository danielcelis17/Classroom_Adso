from model.serializar import valor_json


class DetalleFactura:

    def __init__(self, producto_id, cantidad, detalle_id=0, factura_id=0, precio_venta=None,
                 subtotal_linea=None, nombre_producto=None):
        self.detalle_id = detalle_id
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.precio_venta = precio_venta
        self.subtotal_linea = subtotal_linea

    @classmethod
    def from_row(cls, registro):
        detalle_id, factura_id, producto_id, nombre_producto, cantidad, precio_venta, subtotal_linea = registro
        return cls(producto_id, cantidad, detalle_id, factura_id, precio_venta, subtotal_linea, nombre_producto)

    def to_dict(self):
        return {
            "detalle_id": self.detalle_id,
            "producto_id": self.producto_id,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "precio_venta": valor_json(self.precio_venta),
            "subtotal_linea": valor_json(self.subtotal_linea),
        }


class Factura:

    def __init__(self, cliente_id, factura_id=0, numero_factura=None, fecha_emision=None,
                 subtotal=None, total_iva=None, total_pagar=None, metodo_pago="Efectivo", detalles=None):
        self.factura_id = factura_id
        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision
        self.cliente_id = cliente_id
        self.subtotal = subtotal
        self.total_iva = total_iva
        self.total_pagar = total_pagar
        self.metodo_pago = metodo_pago
        self.detalles = detalles if detalles is not None else []

    @classmethod
    def from_row(cls, registro):
        (factura_id, numero_factura, fecha_emision, cliente_id,
         subtotal, total_iva, total_pagar, metodo_pago) = registro
        return cls(cliente_id, factura_id, numero_factura, fecha_emision,
                   subtotal, total_iva, total_pagar, metodo_pago)

    def to_dict(self, con_detalles=True):
        data = {
            "factura_id": self.factura_id,
            "numero_factura": self.numero_factura,
            "fecha_emision": valor_json(self.fecha_emision),
            "cliente_id": self.cliente_id,
            "subtotal": valor_json(self.subtotal),
            "total_iva": valor_json(self.total_iva),
            "total_pagar": valor_json(self.total_pagar),
            "metodo_pago": self.metodo_pago,
        }
        if con_detalles:
            data["detalles"] = [detalle.to_dict() for detalle in self.detalles]
        return data
