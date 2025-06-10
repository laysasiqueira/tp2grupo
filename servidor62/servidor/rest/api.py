from flask import Flask, jsonify, request
from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from servidor.auth.utils_jwt import verificar_token
from utils.mongodb_helper import listar_contatos, inserir_contato, atualizar_contato, remover_contato
from servidor.messaging.rabbitmq_helper import enviar_mensagem

client = MongoClient(os.getenv("MONGO_URL"))

def obter_payload_do_token():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth.replace("Bearer ", "")
    return verificar_token(token)



app = Flask(__name__)


@app.route('/contatos', methods=['GET'])
def listar_contatos_endpoint():
    payload = obter_payload_do_token()
    if not payload or "erro" in payload:
        return jsonify({"erro": "Token inválido"}), 403

    contatos = listar_contatos()
    return jsonify(contatos)


@app.route('/contatos', methods=['POST'])
def adicionar_contato():
    payload = obter_payload_do_token()
    if not payload or "erro" in payload:
        return jsonify({"erro": "Token inválido"}), 403

    if payload["role"] != "admin":
        return jsonify({"erro": "Acesso não autorizado"}), 403

    novo = request.get_json()
    inserted_id = inserir_contato(novo)
    novo['_id'] = str(inserted_id)

    enviar_mensagem(
        evento="contato_criado",
        dados=novo,
        usuario={"id": payload['sub'], "role": payload['role']}
    )

    return jsonify(novo), 201

@app.route('/contatos/<id>', methods=['DELETE'])
def deletar_contato(id):
    payload = obter_payload_do_token()
    if not payload or "erro" in payload:
        return jsonify({"erro": "Token inválido"}), 403

    if payload["role"] != "admin":
        return jsonify({"erro": "Acesso não autorizado"}), 403

    sucesso = remover_contato(id)
    if sucesso:
        enviar_mensagem(
            evento="contato_removido",
            dados={"id": id},
            usuario={"id": payload['sub'], "role": payload['role']}
        )
        return '', 204
    else:
        return jsonify({"erro": "Contato não encontrado!"}), 404
        

if __name__ == '__main__':
    print("🚀 Servidor Flask inicializado na porta 5050!")
    app.run(host='0.0.0.0', port=5050, debug=True)
