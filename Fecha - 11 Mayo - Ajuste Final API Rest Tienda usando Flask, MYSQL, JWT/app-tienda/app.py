import os
from datetime import timedelta

import pymysql
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from routes.cliente import cliente_bp
from routes.producto import producto_bp
from routes.factura import factura_bp
from routes.usuario import user_bp

app = Flask(__name__)
app.json.ensure_ascii = False

# Frase secreta para firmar los tokens (la de la guía, salvo que venga en el .env)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'FraseSecretadelaapp')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


# Errores de token con la misma forma {"message": ...} que el resto de la API
@jwt.unauthorized_loader
def token_faltante(motivo):
    return jsonify({"message": "Falta el token de acceso (Authorization: Bearer <token>)"}), 401


@jwt.invalid_token_loader
def token_invalido(motivo):
    return jsonify({"message": "Token inválido", "detalle": motivo}), 401


@jwt.expired_token_loader
def token_expirado(jwt_header, jwt_payload):
    return jsonify({"message": "El token expiró, vuelva a hacer login"}), 401


app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(producto_bp, url_prefix='/api')
app.register_blueprint(factura_bp, url_prefix='/api')


@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de la Tienda con MySQL y JWT"})


@app.errorhandler(HTTPException)
def http_error(e):
    # Errores 400/404/405... en JSON en vez de la página HTML de Flask
    return jsonify({"message": e.description}), e.code


@app.errorhandler(pymysql.err.IntegrityError)
def integrity_error(e):
    # Documento/email/username repetido, o borrar un cliente/producto que ya está en una factura
    return jsonify({"message": "La operación viola una restricción de la base de datos", "detalle": e.args[1]}), 409


@app.errorhandler(pymysql.err.DataError)
def data_error(e):
    # Texto más largo que la columna (ej. numero_documento de más de 15 caracteres)
    return jsonify({"message": "Dato inválido", "detalle": e.args[1]}), 400


if __name__ == '__main__':
    with app.app_context():
        # En Docker se escucha en 0.0.0.0; en local queda localhost como en la guía.
        app.run(host=os.getenv("FLASK_RUN_HOST", "localhost"), port=5000, debug=True)
