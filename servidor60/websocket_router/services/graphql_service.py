import requests

def call_graphql(url, payload):
    res = requests.post(url, json={"query": payload["query"]})
    return res.json()
