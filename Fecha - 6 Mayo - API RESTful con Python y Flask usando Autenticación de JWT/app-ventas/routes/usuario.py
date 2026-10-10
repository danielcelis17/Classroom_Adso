from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from model.usuario import Usuario
import controller.usuario as usuario_control

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/usuario', methods=['POST'])
def add_usuario():
    data = request.get_json()
    usuario=Usuario(**data)
    usuario_control.add_usuario(usuario)
    return jsonify({"message": "OK"})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = usuario_control.login(data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
