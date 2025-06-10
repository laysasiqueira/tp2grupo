import requests

def call_soap(url, payload):
    envelope = f"""<?xml version="1.0"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Body>
        {payload["body"]}
      </soapenv:Body>
    </soapenv:Envelope>"""
    headers = {"Content-Type": "text/xml"}
    res = requests.post(url, data=envelope, headers=headers)
    return {"soap_response": res.text}
