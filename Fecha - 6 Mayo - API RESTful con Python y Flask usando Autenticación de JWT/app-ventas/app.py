from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from routes.cliente import cliente_bp
from routes.comercial import comercial_bp
from routes.pedido import pedido_bp
from routes.usuario import user_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'FraseSecretadelaapp'
jwt = JWTManager(app)

app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(comercial_bp, url_prefix='/api')
app.register_blueprint(pedido_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Tareas con MySQL"})

if __name__ == '__main__':
    with app.app_context():
        app.run(host="localhost", port="5000", debug=True)
