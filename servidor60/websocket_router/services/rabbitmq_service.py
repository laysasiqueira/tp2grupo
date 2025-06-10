import pika
import json

def publish(amqp_url, payload):
    params = pika.URLParameters(amqp_url)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue='websocket_queue')
    ch.basic_publish(exchange='', routing_key='websocket_queue', body=json.dumps(payload))
    conn.close()
    return {"status": "Mensagem enviada ao RabbitMQ"}
