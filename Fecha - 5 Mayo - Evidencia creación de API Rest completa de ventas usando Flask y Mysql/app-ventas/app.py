from flask import Flask, request, jsonify
from routes.cliente import cliente_bp
from routes.comercial import comercial_bp
from routes.pedido import pedido_bp

app = Flask(__name__)
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(comercial_bp, url_prefix='/api')
app.register_blueprint(pedido_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Tareas con MySQL"})

if __name__ == '__main__':
    with app.app_context():
        app.run(host="localhost", port="5000", debug=True)
