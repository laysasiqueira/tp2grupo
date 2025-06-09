import requests

def rest_handler(payload):
    method = payload.get("method", "get").lower()
    endpoint = payload.get("endpoint")
    data = payload.get("data", {})
    url = f"http://192.168.0.62:3001/{endpoint}"

    try:
        response = requests.request(method, url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
