from flask import Blueprint, jsonify, request
from model.comercial import Comercial
import controller.comercial as comercial_control

comercial_bp = Blueprint('comercial_bp', __name__)

@comercial_bp.route('/comercial', methods=['GET'])
def get_comerciales():
    comerciales = comercial_control.get_comerciales()
    return jsonify({"comerciales": comerciales})

@comercial_bp.route('/comercial', methods=['POST'])
def add_comercial():
    data = request.get_json()
    comercial=Comercial(**data)
    comercial_control.add_comercial(comercial)
    return jsonify({"message": "OK"})

@comercial_bp.route('/comercial/<int:id>', methods=['PUT'])
def update_comercial(id):
    data = request.get_json()
    comercial=Comercial(**data)
    comercial_control.update_comercial(id, comercial)
    return jsonify({"message": "OK"})

@comercial_bp.route('/comercial/<int:id>', methods=['DELETE'])
def delete_comercial(id):
    comercial_control.delete_comercial(id)
    return jsonify({"message": "OK"})

@comercial_bp.route('/comercial/<int:id>', methods=['GET'])
def get_comercial(id):
    comercial = comercial_control.get_comercial(id)
    return jsonify({"comercial": comercial.to_dict()})
