import pika
import json

def rabbit_handler(payload):
    queue = payload.get("queue", "default")
    message = payload.get("message", {})

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.62'))
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
        connection.close()

        return {"status": "Mensagem enviada com sucesso"}
    except Exception as e:
        return {"error": str(e)}
