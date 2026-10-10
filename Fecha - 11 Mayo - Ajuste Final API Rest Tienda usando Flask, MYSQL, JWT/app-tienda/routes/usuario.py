from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from model.usuario import Usuario
from routes.validacion import leer_json
import controller.usuario as usuario_control

user_bp = Blueprint('user_bp', __name__)

CAMPOS = ("nombre", "correo", "username", "password")


@user_bp.route('/usuario', methods=['POST'])
def add_usuario():
    usuario = Usuario(**leer_json(CAMPOS, CAMPOS))
    usuario_control.add_usuario(usuario)
    return jsonify({"message": "OK"}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = leer_json(("username", "password"), ("username", "password"))
    user = usuario_control.login(str(data["username"]), str(data["password"]))
    if user:
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token})
    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401


@user_bp.route('/usuario/perfil', methods=['GET'])
@jwt_required()
def perfil():
    # get_jwt_identity() devuelve el identity con el que se creó el token (el username)
    usuario = usuario_control.get_usuario(get_jwt_identity())
    if usuario is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify({"usuario": usuario.to_dict()})
