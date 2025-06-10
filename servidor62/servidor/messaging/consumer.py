import pika
import json
import asyncio
import websockets
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from servidor.sockets.websocket_server import notificar_clientes
pika.ConnectionParameters(host='192.168.246.26')  # exemplo

# Função para enviar mensagem ao WebSocket
async def enviar_ws(mensagem):
    uri = "ws://192.168.246.26:5005"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(mensagem))
    except Exception as e:
        print(f"[!] WebSocket indisponível: {e}")

# Função callback do RabbitMQ
def callback(ch, method, properties, body):
    mensagem = json.loads(body)

    print("\n\n=== MENSAGEM RECEBIDA ===")
    print("Evento:", mensagem["evento"])
    print("Dados:", mensagem["dados"])
    print("Usuário:", mensagem["usuario"])
        
    print(f"\n[x] Evento: {mensagem['evento']}")
    print("Dados:", mensagem['dados'])
    print("Usuário:", mensagem['usuario'])




# Configuração da ligação ao RabbitMQ
credenciais = pika.PlainCredentials('admin', 'admin')
parametros = pika.ConnectionParameters('192.168.246.62', credentials=credenciais)
conexao = pika.BlockingConnection(parametros)
canal = conexao.channel()
canal.queue_declare(queue='eventos_contato')

canal.basic_consume(queue='eventos_contato', on_message_callback=callback, auto_ack=True)

print('[*] A escutar mensagens...')
canal.start_consuming()
