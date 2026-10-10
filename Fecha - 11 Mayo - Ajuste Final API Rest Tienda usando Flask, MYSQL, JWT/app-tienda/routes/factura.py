from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required
from model.factura import DetalleFactura, Factura
from routes.validacion import leer_json, validar_numero, validar_opcion
import controller.factura as factura_control

factura_bp = Blueprint('factura_bp', __name__)

METODOS_PAGO = ("Efectivo", "Tarjeta", "Transferencia", "Nequi/Daviplata")


def leer_factura():
    """
    Body: {"cliente_id": 1, "metodo_pago": "Efectivo", "detalles": [{"producto_id": 1, "cantidad": 2}, ...]}
    Precios, IVA y totales no se reciben: los calcula el controller con los datos de productos.
    """
    data = leer_json(("cliente_id", "metodo_pago", "detalles"), ("cliente_id", "detalles"))
    validar_numero(data, "cliente_id", minimo=1, entero=True)
    validar_opcion(data, "metodo_pago", METODOS_PAGO)
    if not isinstance(data["detalles"], list) or not data["detalles"]:
        abort(400, description="detalles debe ser una lista con al menos un producto")

    # Si un producto se repite en varias líneas se suman las cantidades
    cantidades = {}
    for linea in data["detalles"]:
        if not isinstance(linea, dict):
            abort(400, description="Cada detalle debe ser un objeto {producto_id, cantidad}")
        validar_numero(linea, "producto_id", minimo=1, entero=True)
        validar_numero(linea, "cantidad", minimo=1, entero=True)
        if linea.get("producto_id") is None or linea.get("cantidad") is None:
            abort(400, description="Cada detalle necesita producto_id y cantidad")
        cantidades[linea["producto_id"]] = cantidades.get(linea["producto_id"], 0) + linea["cantidad"]

    detalles = [DetalleFactura(producto_id, cantidad) for producto_id, cantidad in cantidades.items()]
    return Factura(data["cliente_id"], metodo_pago=data.get("metodo_pago") or "Efectivo", detalles=detalles)


@factura_bp.route('/factura', methods=['GET'])
@jwt_required()
def get_facturas():
    facturas = factura_control.get_facturas()
    return jsonify({"facturas": [factura.to_dict(con_detalles=False) for factura in facturas]})


@factura_bp.route('/factura', methods=['POST'])
@jwt_required()
def add_factura():
    try:
        factura_id = factura_control.add_factura(leer_factura())
    except factura_control.FacturaError as e:
        return jsonify({"message": e.message}), e.status
    return jsonify({"message": "OK", "factura": factura_control.get_factura(factura_id).to_dict()}), 201


@factura_bp.route('/factura/<int:id>', methods=['GET'])
@jwt_required()
def get_factura(id):
    factura = factura_control.get_factura(id)
    if factura is None:
        return jsonify({"message": "Factura no encontrada"}), 404
    return jsonify({"factura": factura.to_dict()})


@factura_bp.route('/factura/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_factura(id):
    if factura_control.get_factura(id) is None:
        return jsonify({"message": "Factura no encontrada"}), 404
    factura_control.delete_factura(id)
    return jsonify({"message": "OK"})
