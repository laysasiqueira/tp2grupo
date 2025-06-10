import grpc
from concurrent import futures
import json, time, sys, os, requests

# adiciona o utils ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.mongodb_helper import listar_contatos

# URL do serviço Auth
AUTH_URL = os.getenv("AUTH_URL", "http://192.168.246.62:6000")
MESSAGING_URL = os.getenv("MESSAGING_URL", "http://192.168.246.62:8000/mensagem")

def validar_token_remoto(token: str):
    """Verifica o JWT remoto chamando /verificar."""
    resp = requests.get(f"{AUTH_URL}/verificar", headers={"Authorization": f"Bearer {token}"}, timeout=5)
    if resp.status_code != 200:
        return None
    payload = resp.json()
    return payload if "erro" not in payload else None

def enviar_evento_grpc(evento: str, dados: dict, usuario: dict):
    payload = {"evento": evento, "dados": dados, "usuario": usuario}
    resp = requests.post(MESSAGING_URL, json=payload, timeout=5)
    resp.raise_for_status()

# Serviço gRPC
import agenda_pb2
import agenda_pb2_grpc

class AgendaService(agenda_pb2_grpc.AgendaServiceServicer):

    def StreamContatos(self, request, context):
        # Extrai o token JWT dos metadados
        token = None
        for key, value in context.invocation_metadata():
            if key == "authorization" and value.startswith("Bearer "):
                token = value.split(" ", 1)[1]
        payload = validar_token_remoto(token or "")
        if not payload:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token inválido ou ausente")

        # Stream de contatos
        for c in listar_contatos():
            contato_msg = {
                "id": c['id'],
                "nome": c['nome'],
                "email": c['email'],
                "telefone": c['telefone']
            }

            # Dispara evento de contato listado
            enviar_evento_grpc("contato_listado", contato_msg, payload)

            # Agora retorna via gRPC
            yield agenda_pb2.Contato(**contato_msg)
            time.sleep(0.1)  # ritmo lento para exemplificar

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agenda_pb2_grpc.add_AgendaServiceServicer_to_server(AgendaService(), server)
    server.add_insecure_port('[::]:50051')
    print("📡 Servidor gRPC a correr em http://0.0.0.0:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
