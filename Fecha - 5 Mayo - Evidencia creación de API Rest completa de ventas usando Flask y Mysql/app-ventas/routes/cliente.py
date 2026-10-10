from flask import Blueprint, jsonify, request
from model.cliente import Cliente
import controller.cliente as cliente_control

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/cliente', methods=['GET'])
def get_clientes():
    clientes = cliente_control.get_clientes()
    return jsonify({"clientes": clientes})

@cliente_bp.route('/cliente', methods=['POST'])
def add_cliente():
    data = request.get_json()
    cliente=Cliente(**data)
    cliente_control.add_cliente(cliente)
    return jsonify({"message": "OK"})

@cliente_bp.route('/cliente/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    cliente=Cliente(**data)
    cliente_control.update_cliente(id, cliente)
    return jsonify({"message": "OK"})

@cliente_bp.route('/cliente/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente_control.delete_cliente(id)
    return jsonify({"message": "OK"})

@cliente_bp.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = cliente_control.get_cliente(id)
    return jsonify({"cliente": cliente.to_dict()})
