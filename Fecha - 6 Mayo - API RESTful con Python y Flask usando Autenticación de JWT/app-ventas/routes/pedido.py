from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from model.pedido import Pedido
import controller.pedido as pedido_control

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route('/pedido', methods=['GET'])
@jwt_required()
def get_pedidos():
    pedidos = pedido_control.get_pedidos()
    return jsonify({"pedidos": pedidos})

@pedido_bp.route('/pedido', methods=['POST'])
@jwt_required()
def add_pedido():
    data = request.get_json()
    pedido=Pedido(**data)
    pedido_control.add_pedido(pedido)
    return jsonify({"message": "OK"})

@pedido_bp.route('/pedido/<int:id>', methods=['PUT'])
@jwt_required()
def update_pedido(id):
    data = request.get_json()
    pedido=Pedido(**data)
    pedido_control.update_pedido(id, pedido)
    return jsonify({"message": "OK"})

@pedido_bp.route('/pedido/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pedido(id):
    pedido_control.delete_pedido(id)
    return jsonify({"message": "OK"})

@pedido_bp.route('/pedido/<int:id>', methods=['GET'])
@jwt_required()
def get_pedido(id):
    pedido = pedido_control.get_pedido(id)
    return jsonify({"pedido": pedido.to_dict()})
