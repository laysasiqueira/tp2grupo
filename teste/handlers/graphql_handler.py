import requests

def graphql_handler(payload):
    url = "http://192.168.0.26:4000/graphql"
    query = payload.get("query")
    variables = payload.get("variables", {})

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
