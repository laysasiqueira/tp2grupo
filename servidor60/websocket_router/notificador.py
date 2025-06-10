connected_clients = set()

async def notificar_todos(payload):
    import json, asyncio
    mensagem = json.dumps({
        "evento": "novo_usuario",
        "origem": payload.get("origem"),
        "dados": payload.get("dados")
    })
    print("🔔 Enviando para navegadores:", mensagem)
    await asyncio.gather(*(ws.send(mensagem) for ws in connected_clients))
