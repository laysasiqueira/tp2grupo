from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json, sys, os, requests
import base64  # Para decodificar os ficheiros recebidos
import tempfile  # Para uso de ficheiros temporários
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.mongodb_helper import listar_contatos as listar_contatos_mongo

AUTH_URL = os.getenv("AUTH_URL", "http://192.168.246.62:6000")

from bson.json_util import dumps  
from bson import ObjectId

def enviar_mensagem_http(evento, dados, usuario=None):
    url = "http://192.168.246.62:8000/mensagem"
    payload = {
        "evento": evento,
        "dados": dados,
        "usuario": usuario or {"id":None,"role":None}
    }
    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()

def validar_token_remoto(token: str):
    """Chama o /verificar do serviço Auth remoto e retorna payload ou None."""
    resp = requests.get(f"{AUTH_URL}/verificar", headers={"Authorization": f"Bearer {token}"}, timeout=5)
    if resp.status_code != 200:
        return None
    payload = resp.json()
    return payload if "erro" not in payload else None

def obter_payload_soap(ctx):
    auth_header = ctx.transport.req.environ.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    return validar_token_remoto(token)

def extrair_token_do_ctx(ctx):
    auth = ctx.transport.req_env.get('HTTP_AUTHORIZATION', '')
    if not auth.startswith("Bearer "):
        return {"erro": "Token ausente"}
    token = auth.split(" ", 1)[1]
    payload = validar_token_remoto(token)
    return payload or {"erro": "Token inválido"}

@rpc(_returns=Unicode)
def exportar_json(ctx):
    try:
        from utils.mongodb_helper import listar_contatos
        contatos = listar_contatos()
        return dumps(contatos, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Erro ao exportar JSON: {e}"

# NOVO: importar funções de conversão
from utils.conversor_funcoes import json_para_xml, importar_json, xml_para_json

# Caminhos dos ficheiros
base_dir = os.path.dirname(os.path.abspath(__file__))
dados_path = os.path.join(base_dir, '..', 'data', 'contatos.json')
xml_path = os.path.join(base_dir, '..', 'data', 'contatos.xml')

# Função utilitária para carregar contatos
def carregar_contatos():
    with open(dados_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Definição do serviço SOAP
class AgendaService(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def listar_contatos(ctx):
        contatos = listar_contatos_mongo()
        for contato in contatos:
            id_str = contato.get("id", "sem-id")
            yield f"{id_str} - {contato['nome']} - {contato['email']} - {contato['telefone']}"

    @rpc(_returns=Unicode)
    def exportar_json(ctx):
        try:
            from utils.mongodb_helper import listar_contatos
            contatos = listar_contatos()
            return dumps(contatos, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Erro ao exportar JSON: {e}"
            
    @rpc(_returns=Unicode)
    def exportar_xml(ctx):
        try:
            from utils.mongodb_helper import listar_contatos
            from utils.conversor_funcoes import json_para_xml

            # 1. Obter os contatos diretamente do MongoDB
            contatos = listar_contatos()

            # 2. Criar um ficheiro JSON temporário com os dados do MongoDB
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8') as tmp_json:
                json.dump(contatos, tmp_json, indent=2, ensure_ascii=False)
                tmp_json_path = tmp_json.name

            # 3. Gerar XML a partir do JSON temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='w', encoding='utf-8') as tmp_xml:
                tmp_xml_path = tmp_xml.name

            json_para_xml(tmp_json_path, tmp_xml_path)

            # 4. Ler o XML e devolver como string
            with open(tmp_xml_path, 'r', encoding='utf-8') as f:
                xml_str = f.read()

            # 5. Limpar os ficheiros temporários
            os.remove(tmp_json_path)
            os.remove(tmp_xml_path)

            return xml_str

        except Exception as e:
            return f"Erro ao exportar XML: {e}"


    # 🆕 Importar JSON codificado em Base64
    @rpc(Unicode, _returns=Unicode)
    def importar_json_base64(ctx, base64_str):
        payload = extrair_token_do_ctx(ctx)
        if not payload or "erro" in payload or payload.get("role") != "admin":
            return "Erro: Acesso restrito. Apenas administradores podem importar contatos."

        try:
            decoded = base64.b64decode(base64_str).decode('utf-8')
            contatos = json.loads(decoded)

            if isinstance(contatos, dict):
                contatos = [contatos]

            inseridos = 0
            for contato in contatos:
                from utils.mongodb_helper import inserir_contato
                inserir_contato(contato)
                if '_id' in contato and isinstance(contato['_id'], ObjectId):
                    contato['_id'] = str(contato['_id'])
                enviar_mensagem_http(
                    evento="contato_criado",
                    dados=contato,
                    usuario={"id": payload['sub'], "role": payload['role']}
                )
                inseridos += 1

            return f"✅ Importação JSON concluída! {inseridos} contatos inseridos."
        except Exception as e:
            return f"Erro ao importar JSON: {e}"


    # 🆕 Importar XML codificado em Base64
    @rpc(Unicode, _returns=Unicode)
    def importar_xml_base64(ctx, base64_str):
        payload = extrair_token_do_ctx(ctx)
        if not payload or "erro" in payload or payload.get("role") != "admin":
            return "Erro: Acesso restrito. Apenas administradores podem importar contatos."

        try:
            import xml.etree.ElementTree as ET
            from utils.mongodb_helper import inserir_contato

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='wb') as tmp:
                tmp.write(base64.b64decode(base64_str))
                tmp_path = tmp.name

            tree = ET.parse(tmp_path)
            root = tree.getroot()

            for elem in root.findall('contato'):
                contato = {
                    "id": elem.findtext("id"),
                    "nome": elem.findtext("nome"),
                    "email": elem.findtext("email"),
                    "telefone": elem.findtext("telefone")
                }
                inserir_contato(contato)
                if '_id' in contato and isinstance(contato['_id'], ObjectId):
                    contato['_id'] = str(contato['_id'])
                enviar_mensagem_http(
                    evento="contato_criado",
                    dados=contato,
                    usuario={"id": payload['sub'], "role": payload['role']}
                )

            os.remove(tmp_path)
            return "✅ Importação XML concluída com sucesso!"
        except Exception as e:
            return f"Erro ao importar XML: {e}"



# Executa o servidor SOAP
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    soap_app = Application(
        [AgendaService],
        tns='agenda.contatos',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )

    wsgi_app = WsgiApplication(soap_app)

    print("🚀 Servidor SOAP iniciado em http://127.0.0.1:8010")
    server = make_server('0.0.0.0', 8010, wsgi_app)
    server.serve_forever()