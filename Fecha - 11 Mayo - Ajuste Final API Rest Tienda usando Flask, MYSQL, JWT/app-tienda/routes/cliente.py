from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from model.cliente import Cliente
from routes.validacion import leer_json, validar_opcion
import controller.cliente as cliente_control

cliente_bp = Blueprint('cliente_bp', __name__)

CAMPOS = ("tipo_documento", "numero_documento", "nombre", "apellido",
          "telefono", "email", "direccion", "ciudad")
OBLIGATORIOS = ("numero_documento", "nombre", "apellido")
TIPOS_DOCUMENTO = ("CC", "NIT", "CE", "PP")


def leer_cliente():
    data = leer_json(CAMPOS, OBLIGATORIOS)
    validar_opcion(data, "tipo_documento", TIPOS_DOCUMENTO)
    # Si no vienen, se dejan los DEFAULT de la tabla
    data = {campo: valor for campo, valor in data.items()
            if not (campo in ("tipo_documento", "ciudad") and valor is None)}
    return Cliente(**data)


@cliente_bp.route('/cliente', methods=['GET'])
@jwt_required()
def get_clientes():
    clientes = cliente_control.get_clientes()
    return jsonify({"clientes": [cliente.to_dict() for cliente in clientes]})


@cliente_bp.route('/cliente', methods=['POST'])
@jwt_required()
def add_cliente():
    cliente_id = cliente_control.add_cliente(leer_cliente())
    return jsonify({"message": "OK", "cliente_id": cliente_id}), 201


@cliente_bp.route('/cliente/<int:id>', methods=['PUT'])
@jwt_required()
def update_cliente(id):
    if cliente_control.get_cliente(id) is None:
        return jsonify({"message": "Cliente no encontrado"}), 404
    cliente_control.update_cliente(id, leer_cliente())
    return jsonify({"message": "OK"})


@cliente_bp.route('/cliente/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(id):
    if cliente_control.get_cliente(id) is None:
        return jsonify({"message": "Cliente no encontrado"}), 404
    cliente_control.delete_cliente(id)
    return jsonify({"message": "OK"})


@cliente_bp.route('/cliente/<int:id>', methods=['GET'])
@jwt_required()
def get_cliente(id):
    cliente = cliente_control.get_cliente(id)
    if cliente is None:
        return jsonify({"message": "Cliente no encontrado"}), 404
    return jsonify({"cliente": cliente.to_dict()})
