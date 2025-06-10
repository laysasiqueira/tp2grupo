from pymongo import MongoClient
import uuid

# Conectar ao MongoDB local (ajusta se estiver noutro host/porta)
client = MongoClient("mongodb://192.168.246.62:27017/")

# Base de dados e coleção
db = client["agenda_contatos"]
colecao = db["contatos"]

def listar_contatos():
    """Retorna todos os contatos da base de dados, sem o campo _id."""
    return list(colecao.find({}, {"_id": 0}))

def inserir_contato(contato):
    """Insere um novo contato (dict) na base de dados com um campo 'id' gerado."""
    contato['id'] = str(uuid.uuid4())  # Gera um ID único como string
    resultado = colecao.insert_one(contato)
    return str(resultado.inserted_id)

def atualizar_contato(id_contato, novos_dados):
    """Atualiza os dados de um contato com base no campo 'id'."""
    resultado = colecao.update_one({"id": id_contato}, {"$set": novos_dados})
    return resultado.modified_count > 0

def remover_contato(id_contato):
    """Remove um contato com base no campo 'id'."""
    resultado = colecao.delete_one({"id": id_contato})
    return resultado.deleted_count > 0
