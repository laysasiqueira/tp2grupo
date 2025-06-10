import traceback
from flask import Flask, request, jsonify
from rabbitmq_helper import enviar_mensagem

app = Flask(__name__)

@app.post("/mensagem")
def publicar_mensagem():
    """
    Espera JSON:
    {
      "evento": "...",
      "dados": {...},
      "usuario": {...}
    }
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"erro":"JSON inválido"}), 400

    try:
        enviar_mensagem(
            evento=payload["evento"],
            dados=payload["dados"],
            usuario=payload.get("usuario")
        )
        return jsonify({"status":"ok"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
