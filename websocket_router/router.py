from jwt_utils import verify_jwt
from config import SERVERS
from services import rest_service, graphql_service, soap_service, grpc_service, rabbitmq_service
from notificador import notificar_todos


async def route_message(data):
    tipo = data.get("type")
    endpoint = data.get("endpoint")
    payload = data.get("payload", {})
    token = data.get("token", "")

    if token and not verify_jwt(token):
        return {"error": "Token JWT inválido"}

    # Executa chamada conforme o tipo
    if tipo == "rest":
        resposta = rest_service.call_rest(SERVERS["rest"], endpoint, payload)

    elif tipo == "graphql":
        resposta = graphql_service.call_graphql(SERVERS["graphql"], payload)

    elif tipo == "soap":
        resposta = soap_service.call_soap(SERVERS["soap"], payload)

    elif tipo == "mq":
        resposta = rabbitmq_service.publish(SERVERS["mq"], payload)

    elif tipo == "grpc":
        resposta = grpc_service.call_grpc(SERVERS["grpc"], payload)

    else:
        return {"error": "Tipo de mensagem não suportado"}

    # 🔔 Se for um retorno com status de criação, notifica todos
    if isinstance(resposta, dict) and resposta.get("status") == "criado":
        await notificar_todos({
            "origem": tipo,
            "dados": resposta.get("dados", payload)
        })

    return resposta
