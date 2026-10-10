from flask import Flask, request, jsonify
from routes.cliente import cliente_bp

app = Flask(__name__)
app.register_blueprint(cliente_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Tareas con MySQL"})

if __name__ == '__main__':
    with app.app_context():
        app.run(host="localhost", port="5000", debug=True)
