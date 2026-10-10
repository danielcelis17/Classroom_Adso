from flask import Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required
from model.producto import Producto
from routes.validacion import leer_json, validar_numero
import controller.producto as producto_control

producto_bp = Blueprint('producto_bp', __name__)

CAMPOS = ("nombre_producto", "descripcion", "precio_unitario", "stock", "iva_porcentaje")
OBLIGATORIOS = ("nombre_producto", "precio_unitario")


def leer_producto():
    data = leer_json(CAMPOS, OBLIGATORIOS)
    validar_numero(data, "precio_unitario")
    validar_numero(data, "stock", entero=True)
    validar_numero(data, "iva_porcentaje")
    if data.get("iva_porcentaje") is not None and data["iva_porcentaje"] >= 100:
        abort(400, description="iva_porcentaje debe ser menor a 100")
    # Si no vienen, se dejan los DEFAULT de la tabla
    data = {campo: valor for campo, valor in data.items()
            if not (campo in ("stock", "iva_porcentaje") and valor is None)}
    return Producto(**data)


@producto_bp.route('/producto', methods=['GET'])
@jwt_required()
def get_productos():
    productos = producto_control.get_productos()
    return jsonify({"productos": [producto.to_dict() for producto in productos]})


@producto_bp.route('/producto', methods=['POST'])
@jwt_required()
def add_producto():
    producto_id = producto_control.add_producto(leer_producto())
    return jsonify({"message": "OK", "producto_id": producto_id}), 201


@producto_bp.route('/producto/<int:id>', methods=['PUT'])
@jwt_required()
def update_producto(id):
    if producto_control.get_producto(id) is None:
        return jsonify({"message": "Producto no encontrado"}), 404
    producto_control.update_producto(id, leer_producto())
    return jsonify({"message": "OK"})


@producto_bp.route('/producto/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_producto(id):
    if producto_control.get_producto(id) is None:
        return jsonify({"message": "Producto no encontrado"}), 404
    producto_control.delete_producto(id)
    return jsonify({"message": "OK"})


@producto_bp.route('/producto/<int:id>', methods=['GET'])
@jwt_required()
def get_producto(id):
    producto = producto_control.get_producto(id)
    if producto is None:
        return jsonify({"message": "Producto no encontrado"}), 404
    return jsonify({"producto": producto.to_dict()})
