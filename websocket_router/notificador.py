# notificador.py

connected_clients = set()

async def notificar_todos(payload):
    import json, asyncio
    if connected_clients:
        mensagem = json.dumps({"evento": "novo_usuario", "dados": payload})
        await asyncio.gather(*(cliente.send(mensagem) for cliente in connected_clients))
