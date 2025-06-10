# from jwt_utils import verify_jwt
# from config import SERVERS
# from services import rest_service, graphql_service, soap_service, grpc_service, rabbitmq_service
# from notificador import notificar_todos


# async def route_message(data):
#     tipo = data.get("type")
#     endpoint = data.get("endpoint")
#     payload = data.get("payload", {})
#     token = data.get("token", "")

#     if token and not verify_jwt(token):
#         return {"error": "Token JWT inválido"}

#     if tipo == "rest":
#         return rest_service.call_rest(SERVERS["rest"], endpoint, payload)

#     elif tipo == "graphql":
#         return graphql_service.call_graphql(SERVERS["graphql"], payload)

#     elif tipo == "soap":
#         return soap_service.call_soap(SERVERS["soap"], payload)

#     elif tipo == "mq":
#         return rabbitmq_service.publish(SERVERS["mq"], payload)

#     elif tipo == "grpc":
#         return grpc_service.call_grpc(SERVERS["grpc"], payload)

#     return {"error": "Tipo de mensagem não suportado"}


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

    if tipo == "rest":
        resposta = rest_service.call_rest(SERVERS["rest"], endpoint, payload)

        # 🚨 Detecta se foi criação de novo usuário
        if endpoint == "/usuarios" and resposta.get("status") == "criado":
            await notificar_todos(resposta["dados"])

        return resposta

    elif tipo == "graphql":
        return graphql_service.call_graphql(SERVERS["graphql"], payload)

    elif tipo == "soap":
        return soap_service.call_soap(SERVERS["soap"], payload)

    elif tipo == "mq":
        return rabbitmq_service.publish(SERVERS["mq"], payload)

    elif tipo == "grpc":
        return grpc_service.call_grpc(SERVERS["grpc"], payload)

    return {"error": "Tipo de mensagem não suportado"}
