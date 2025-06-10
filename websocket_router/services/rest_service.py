import aiohttp
from notificador import notificar_todos

async def call_rest(base_url, endpoint, payload):
    url = base_url + endpoint
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as res:
            data = await res.json()

            # Supondo que a adição de utilizador é reconhecida por um campo no payload
            nome = payload.get("nome", "desconhecido")
            if "add" in endpoint or "create" in endpoint or "register" in endpoint:
                await notify_clients({
                    "event": "user_added",
                    "service": "rest",
                    "message": f'REST: utilizador adicionado: "{nome}"'
                })
            elif "delete" in endpoint or "remove" in endpoint:
                await notify_clients({
                    "event": "user_removed",
                    "service": "rest",
                    "message": f'REST: utilizador removido: "{nome}"'
                })

            return data
