import requests

def call_rest(base_url, endpoint, payload):
    res = requests.post(base_url + endpoint, json=payload)
    return res.json()
