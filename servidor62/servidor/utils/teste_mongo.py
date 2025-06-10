from pymongo import MongoClient

# Conectar ao MongoDB local
cliente = MongoClient("mongodb://localhost:27017")

# Aceder à base de dados e à coleção
db = cliente["agenda_contatos"]
colecao = db["contatos"]

# Inserir um contato de teste
contato_teste = {
    "nome": "Joana Silva",
    "email": "joana@example.com",
    "telefone": "912345678"
}

resultado = colecao.insert_one(contato_teste)
print("✅ Contato inserido com ID:", resultado.inserted_id)

# Listar contatos existentes
print("\n📋 Lista de contatos:")
for contato in colecao.find():
    print(contato)
