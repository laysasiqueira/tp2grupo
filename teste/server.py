import asyncio
import json
import websockets

from handlers import rest_handler, graphql_handler, soap_handler, grpc_handler, rabbit_handler

async def handle_message(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            tipo = data.get("type")
            payload = data.get("payload", {})
            response = {}

            if tipo == "rest":
                response = rest_handler.rest_handler(payload)
            elif tipo == "graphql":
                response = graphql_handler.graphql_handler(payload)
            elif tipo == "soap":
                response = soap_handler.soap_handler(payload)
            elif tipo == "grpc":
                response = grpc_handler.grpc_handler(payload)
            elif tipo == "rabbit":
                response = rabbit_handler.rabbit_handler(payload)
            else:
                response = {"error": "Tipo desconhecido"}

            await websocket.send(json.dumps({"type": tipo, "response": response}))

        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))

async def main():
    print("Servidor WebSocket ouvindo na porta 8765...")
    async with websockets.serve(handle_message, "0.0.0.0", 8765):
        await asyncio.Future()  # roda para sempre

if __name__ == "__main__":
    asyncio.run(main())
