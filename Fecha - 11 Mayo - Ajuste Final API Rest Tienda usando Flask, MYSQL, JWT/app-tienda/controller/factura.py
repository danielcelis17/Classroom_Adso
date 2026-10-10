import uuid
from decimal import Decimal, ROUND_HALF_UP

from config.db import conexion
from model.factura import DetalleFactura, Factura

COLUMNAS = ("factura_id, numero_factura, fecha_emision, cliente_id, "
            "subtotal, total_iva, total_pagar, metodo_pago")

CENTAVOS = Decimal("0.01")


class FacturaError(Exception):
    """Error de negocio al facturar (cliente/producto inexistente, stock insuficiente)."""

    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status


def _get_detalles(cursor, factura_id):
    cursor.execute(
        "SELECT d.detalle_id, d.factura_id, d.producto_id, p.nombre_producto, d.cantidad, "
        "d.precio_venta, d.subtotal_linea "
        "FROM detalle_facturas d JOIN productos p ON p.producto_id = d.producto_id "
        "WHERE d.factura_id=%s ORDER BY d.detalle_id",
        (factura_id,),
    )
    return [DetalleFactura.from_row(registro) for registro in cursor.fetchall()]


def get_facturas():
    con = conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM facturas ORDER BY factura_id")
        registros = cursor.fetchall()
    facturas = [Factura.from_row(registro) for registro in registros]
    con.close()
    return facturas


def get_factura(id):
    con = conexion()
    with con.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM facturas WHERE factura_id=%s", (id,))
        registro = cursor.fetchone()
        factura = Factura.from_row(registro) if registro else None
        if factura:
            factura.detalles = _get_detalles(cursor, id)
    con.close()
    return factura


def add_factura(factura):
    """
    Crea la factura con sus detalles en una sola transacción:
    toma el precio y el IVA de cada producto, calcula subtotal, IVA y total,
    descuenta el stock y numera la factura como FAC-000123.
    Si algo falla no queda nada guardado.
    """
    con = conexion()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT 1 FROM clientes WHERE cliente_id=%s", (factura.cliente_id,))
            if cursor.fetchone() is None:
                raise FacturaError(f"El cliente {factura.cliente_id} no existe", 404)

            subtotal = Decimal("0")
            total_iva = Decimal("0")
            for detalle in factura.detalles:
                # FOR UPDATE bloquea la fila del producto hasta el commit, así dos ventas
                # simultáneas no pueden vender el mismo stock dos veces
                cursor.execute(
                    "SELECT nombre_producto, precio_unitario, stock, iva_porcentaje "
                    "FROM productos WHERE producto_id=%s FOR UPDATE",
                    (detalle.producto_id,),
                )
                producto = cursor.fetchone()
                if producto is None:
                    raise FacturaError(f"El producto {detalle.producto_id} no existe", 404)
                nombre, precio, stock, iva = producto
                if stock < detalle.cantidad:
                    raise FacturaError(
                        f"Stock insuficiente para '{nombre}': hay {stock}, se piden {detalle.cantidad}", 409)

                detalle.nombre_producto = nombre
                detalle.precio_venta = precio
                detalle.subtotal_linea = (precio * detalle.cantidad).quantize(CENTAVOS, ROUND_HALF_UP)
                subtotal += detalle.subtotal_linea
                total_iva += (detalle.subtotal_linea * iva / 100).quantize(CENTAVOS, ROUND_HALF_UP)

            factura.subtotal = subtotal
            factura.total_iva = total_iva
            factura.total_pagar = subtotal + total_iva

            # numero_factura es NOT NULL UNIQUE: se inserta uno temporal y luego se reemplaza por el id
            cursor.execute(
                "INSERT INTO facturas (numero_factura, cliente_id, subtotal, total_iva, total_pagar, metodo_pago) "
                "VALUES(%s, %s, %s, %s, %s, %s)",
                (uuid.uuid4().hex[:20], factura.cliente_id, factura.subtotal, factura.total_iva,
                 factura.total_pagar, factura.metodo_pago),
            )
            factura.factura_id = cursor.lastrowid
            factura.numero_factura = f"FAC-{factura.factura_id:06d}"
            cursor.execute("UPDATE facturas SET numero_factura=%s WHERE factura_id=%s",
                           (factura.numero_factura, factura.factura_id))

            for detalle in factura.detalles:
                cursor.execute(
                    "INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_venta, subtotal_linea) "
                    "VALUES(%s, %s, %s, %s, %s)",
                    (factura.factura_id, detalle.producto_id, detalle.cantidad,
                     detalle.precio_venta, detalle.subtotal_linea),
                )
                cursor.execute("UPDATE productos SET stock = stock - %s WHERE producto_id=%s",
                               (detalle.cantidad, detalle.producto_id))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
    return factura.factura_id


def delete_factura(id):
    """Anula la factura: devuelve el stock de sus productos y la borra (los detalles se borran en cascada)."""
    con = conexion()
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE productos p JOIN detalle_facturas d ON d.producto_id = p.producto_id "
                "SET p.stock = p.stock + d.cantidad WHERE d.factura_id=%s",
                (id,),
            )
            filas = cursor.execute("DELETE FROM facturas WHERE factura_id=%s", (id,))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
    return filas
