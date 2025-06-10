import jwt
from datetime import datetime, timedelta

# Chave secreta (idealmente viria de variável de ambiente ou ficheiro externo)
SEGREDO = "minha_chave_secreta"

def criar_token(dados_utilizador):
    payload = {
        "sub": dados_utilizador["username"],
        "role": dados_utilizador["role"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SEGREDO, algorithm="HS256")

def verificar_token(token):
    try:
        payload = jwt.decode(token, SEGREDO, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"erro": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"erro": "Token inválido"}
