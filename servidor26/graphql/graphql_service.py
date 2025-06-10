from flask import Flask, request, jsonify, g
from flask_graphql import GraphQLView
import os, requests, sys
import graphene
from flask_cors import CORS

# Adiciona o caminho pai ao path para encontrar utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Endpoints remotos de autenticação e mensagens
AUTH_URL = os.getenv("AUTH_URL", "http://192.168.246.62:6000")
MESSAGING_URL = os.getenv("MESSAGING_URL", "http://192.168.246.62:8000/mensagem")

def enviar_evento_graphql(evento, dados, usuario=None):
    payload = {
        "evento": evento,
        "dados": dados,
        "usuario": usuario or {}
    }
    resp = requests.post(MESSAGING_URL, json=payload, timeout=5)
    resp.raise_for_status()

# Iniciar app Flask
app = Flask(__name__)
app.debug = True
CORS(app)

@app.before_request
def checar_jwt_remoto():
    if not request.path.startswith("/graphql"):
        return

    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"erro": "Token ausente"}), 403

    # chama o serviço de auth no .62
    resp = requests.get(f"{AUTH_URL}/verificar", headers={"Authorization": auth})
    if resp.status_code != 200:
        return jsonify({"erro": "Token inválido"}), 403

    payload = resp.json()
    if "erro" in payload:
        return jsonify({"erro": payload["erro"]}), 403

    g.user = payload

# Importa funções do MongoDB
from utils.mongodb_helper import listar_contatos, inserir_contato

# Tipo GraphQL
class Contato(graphene.ObjectType):
    id = graphene.String()
    nome = graphene.String()
    email = graphene.String()
    telefone = graphene.String()

# Query personalizada
class Query(graphene.ObjectType):
    contatos = graphene.List(Contato)
    buscar_contato_por_nome = graphene.Field(Contato, nome=graphene.String(required=True))

    def resolve_contatos(parent, info):
        dados = listar_contatos()
        return dados

    def resolve_buscar_contato_por_nome(parent, info, nome):
        contatos = listar_contatos()
        for contato in contatos:
            if contato["nome"].lower() == nome.lower():
                enviar_evento_graphql("contato_buscado", contato, g.user)
                return contato
        return None
    
# Mutations (exemplo de criação)
class CreateContato(graphene.Mutation):
    class Arguments:
        nome     = graphene.String(required=True)
        email    = graphene.String(required=True)
        telefone = graphene.String(required=True)

    contato = graphene.Field(lambda: Contato)

    def mutate(self, info, nome, email, telefone):
        novo = {"nome": nome, "email": email, "telefone": telefone}
        contato = novo.copy()
        contato["id"] = inserir_contato(novo)
        # dispara evento de criação
        enviar_evento_graphql("contato_criado", contato, g.user)
        return CreateContato(contato=contato)

class Mutation(graphene.ObjectType):
    criar_contato = CreateContato.Field()

# Criar schema
schema = graphene.Schema(query=Query)

# Registrar rota com GraphiQL ativado
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,  # interface web ativada
        get_context=lambda: {"user": g.get("user")}
    )
)

if __name__ == '__main__':
    print("🚀 Servidor GraphQL disponível em http://0.0.0.0:5000/graphql")
    app.run(host="0.0.0.0", port=5000)

