import asyncio
import websockets
import json
from router import route_message
from notificador import connected_clients

# FUNÇÃO OBRIGATÓRIA
async def handler(websocket, path):
    print("Novo cliente:", websocket.remote_address)
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                response = await route_message(data)
            except Exception as e:
                response = {"error": str(e)}
            await websocket.send(json.dumps(response))
    finally:
        connected_clients.remove(websocket)

# FUNÇÃO PRINCIPAL
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor WebSocket rodando na porta 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
