connected_clients = set()

async def notify_clients(message):
    import json
    import asyncio
    if connected_clients:
        data = json.dumps(message)
        await asyncio.gather(*(client.send(data) for client in connected_clients))
