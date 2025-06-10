import json
import os
import xmltodict
import csv

# Exporta JSON → XML
def json_para_xml(caminho_json, caminho_xml):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados_json = json.load(f)

    dados_dict = {"contatos": {"contato": dados_json}}

    with open(caminho_xml, 'w', encoding='utf-8') as f:
        xml_str = xmltodict.unparse(dados_dict, pretty=True)
        f.write(xml_str)

# Exporta XML → JSON 
def xml_para_json(caminho_xml, caminho_json):
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        dados_dict = xmltodict.parse(f.read())

    novos_contatos = dados_dict["contatos"]["contato"]

    # Garante que seja lista
    if not isinstance(novos_contatos, list):
        novos_contatos = [novos_contatos]

    # Lê os contatos existentes
    contatos_existentes = []
    if os.path.exists(caminho_json):
        with open(caminho_json, 'r', encoding='utf-8') as f:
            try:
                contatos_existentes = json.load(f)
            except json.JSONDecodeError:
                contatos_existentes = []

    # Junta os dados
    todos_os_contatos = contatos_existentes + novos_contatos

    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(todos_os_contatos, f, indent=2, ensure_ascii=False)

# Importa JSON → JSON (com merge ao ficheiro JSON principal)
def importar_json(caminho_json_origem, caminho_json_destino):
    # Lê os novos contatos
    with open(caminho_json_origem, 'r', encoding='utf-8') as f:
        novos_contatos = json.load(f)

    if not isinstance(novos_contatos, list):
        novos_contatos = [novos_contatos]

    # Lê os contatos existentes
    contatos_existentes = []
    if os.path.exists(caminho_json_destino):
        with open(caminho_json_destino, 'r', encoding='utf-8') as f:
            try:
                contatos_existentes = json.load(f)
            except json.JSONDecodeError:
                contatos_existentes = []

    # Junta os dados
    todos_os_contatos = contatos_existentes + novos_contatos

    with open(caminho_json_destino, 'w', encoding='utf-8') as f:
        json.dump(todos_os_contatos, f, indent=2, ensure_ascii=False)

def json_para_csv(caminho_json, caminho_csv):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        contatos = json.load(f)

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nome', 'email', 'telefone'])
        writer.writeheader()
        for contato in contatos:
            writer.writerow(contato)