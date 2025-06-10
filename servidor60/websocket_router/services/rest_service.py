from notificador import notificar_todos  # adicione isso

def call_rest(url, endpoint, payload):
    import requests

    full_url = url + endpoint
    response = requests.post(full_url, json=payload)

    try:
        data = response.json()
    except:
        data = {}

    # 👇 verifica se foi criação e notifica via WebSocket
    if response.status_code == 201:
        import asyncio
        asyncio.create_task(notificar_todos({
            "origem": "rest",
            "dados": data or payload
        }))

    return {
        "status": "criado" if response.status_code == 201 else "erro",

      
    }
