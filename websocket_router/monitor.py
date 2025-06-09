import asyncio
import aiohttp
import json
from datetime import datetime
from config import SERVERS

service_status = {}

async def check_services(callback, interval=5):
    global service_status
    while True:
        for name, url in SERVERS.items():
            status = "offline"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=3) as resp:
                        if resp.status < 500:
                            status = "online"
            except:
                status = "offline"

            if service_status.get(name) != status:
                service_status[name] = status
                await callback({
                    "event": "status_update",
                    "service": name,
                    "status": status,
                    "ip": url,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })

        await asyncio.sleep(interval)
