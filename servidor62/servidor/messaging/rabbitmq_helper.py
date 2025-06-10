import pika, os, json
host = os.getenv("RABBITMQ_HOST", "localhost")
port = int(os.getenv("RABBITMQ_PORT", 5672))

def enviar_mensagem(evento, dados, usuario=None):
    user = os.getenv('RABBITMQ_USER', 'guest')
    pwd  = os.getenv('RABBITMQ_PASS', 'guest')

    credenciais = pika.PlainCredentials(user, pwd)
    parametros= pika.ConnectionParameters(host=host, credentials=credenciais)
    conexao  = pika.BlockingConnection(parametros)

    canal = conexao.channel()

    canal.queue_declare(queue='eventos_contato')

    mensagem = {
        "evento": evento,
        "dados": dados,
        "usuario": usuario or {"id": "desconhecido", "role": "guest"}
    }

    canal.basic_publish(
        exchange='',
        routing_key='eventos_contato',
        body=json.dumps(mensagem)
    )

    conexao.close()
