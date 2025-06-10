from mongodb_helper import listar_contatos, inserir_contato, atualizar_contato, remover_contato

# Criar um contato de teste
contato_teste = {
    "id": "001",
    "nome": "Carlos Silva",
    "email": "carlos@example.com",
    "telefone": "913456789"
}

# 1. Inserir o contato
print("📥 Inserindo contato de teste...")
id_inserido = inserir_contato(contato_teste)
print(f"✅ Contato inserido com ID: {id_inserido}")

# 2. Listar todos os contatos
print("\n📃 Lista de contatos:")
for c in listar_contatos():
    print(c)

# 3. Atualizar o contato
print("\n✏️ Atualizando telefone...")
sucesso = atualizar_contato("001", {"telefone": "919999999"})
print("✅ Atualizado!" if sucesso else "⚠️ Contato não encontrado para atualizar.")

# 4. Listar novamente para confirmar
print("\n📃 Contatos após atualização:")
for c in listar_contatos():
    print(c)

# 5. Remover o contato
print("\n🗑️ Removendo contato...")
removido = remover_contato("001")
print("✅ Removido!" if removido else "⚠️ Contato não encontrado para remover.")

# 6. Listar novamente para verificar remoção
print("\n📃 Contatos após remoção:")
for c in listar_contatos():
    print(c)
