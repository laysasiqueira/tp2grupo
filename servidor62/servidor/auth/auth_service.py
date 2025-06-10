from flask import Flask, request, jsonify
from utils_jwt import criar_token, verificar_token

app = Flask(__name__)

# Simulação de utilizadores (ideal: vir de base de dados MongoDB no futuro)
utilizadores = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"}
}

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')

    utilizador = utilizadores.get(username)
    if utilizador and utilizador["password"] == password:
        token = criar_token(utilizador)
        return jsonify({"token": token})

    return jsonify({"erro": "Credenciais inválidas"}), 401

@app.route('/verificar', methods=['GET'])
def verificar():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"erro": "Token não fornecido"}), 403

    token = token.replace("Bearer ", "")
    resultado = verificar_token(token)
    return jsonify(resultado)

if __name__ == '__main__':
    print("🔐 Serviço de Autenticação disponível em http://localhost:6000")
    app.run(host='0.0.0.0', port=6000)

