connected_clients = set()

async def notificar_todos(payload):
    import asyncio, json
    print("🔔 Notificando navegadores via WebSocket:", payload)  # ADICIONE ISSO

    if connected_clients:
        mensagem = json.dumps({
            "evento": "novo_usuario",
            "origem": payload.get("origem"),
            "dados": payload.get("dados")
        })
        await asyncio.gather(*(cliente.send(mensagem) for cliente in connected_clients))
