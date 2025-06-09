from zeep import Client

def soap_handler(payload):
    wsdl = "http://192.168.0.26:8080/service?wsdl"
    method = payload.get("method")
    args = payload.get("args", {})

    try:
        client = Client(wsdl=wsdl)
        result = getattr(client.service, method)(**args)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
