import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import grpc

# Adiciona o caminho raiz do projeto ao sys.path para encontrar os módulos gRPC
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações corrigidas
import agenda_pb2 as agenda_pb2
import agenda_pb2_grpc

def carregar_contatos():
    try:
        canal = grpc.insecure_channel('localhost:50051')
        stub = agenda_pb2_grpc.AgendaServiceStub(canal)
        request = agenda_pb2.StreamContatoRequest()
        resposta_stream = stub.StreamContatos(request)

        lista_contatos.delete(*lista_contatos.get_children())
        for contato in resposta_stream:
            lista_contatos.insert('', 'end', values=(contato.id, contato.nome, contato.email, contato.telefone))
    except grpc.RpcError as e:
        messagebox.showerror("Erro", f"Erro ao conectar com o servidor gRPC:\n{e}")

# Interface
janela = tk.Tk()
janela.title("Contatos - gRPC (Streaming)")
janela.geometry("600x400")
janela.configure(bg="#1c1c1c")

tk.Label(janela, text="Lista de Contatos (gRPC Streaming)", font=("Segoe UI", 16), bg="#1c1c1c", fg="#00ffcc").pack(pady=10)

tk.Button(janela, text="🔄 Carregar Contatos", font=("Segoe UI", 12), bg="#00cc99", fg="white", command=carregar_contatos).pack(pady=10)

colunas = ("ID", "Nome", "Email", "Telefone")
lista_contatos = ttk.Treeview(janela, columns=colunas, show="headings")
for col in colunas:
    lista_contatos.heading(col, text=col)
    lista_contatos.column(col, width=130)
lista_contatos.pack(expand=True, fill="both", padx=20, pady=10)

janela.mainloop()
