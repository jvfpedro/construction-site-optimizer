import customtkinter as ctk
from tkinter import filedialog
import cad
import os


class Janela(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.titulo = "Criação de Canteiro"

        self.label_titulo = ctk.CTkLabel(self, text=self.titulo, font=("Arial", 20))
        self.label_titulo.pack(pady=10)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_nome = ctk.CTkLabel(self.frame, text="Nome da Obra:")
        self.label_nome.grid(row=0, column=0, pady=10, padx=10)
        self.entry_nome = ctk.CTkEntry(self.frame)
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10)

        self.label_largura = ctk.CTkLabel(self.frame, text="Largura do Canteiro (m):")
        self.label_largura.grid(row=1, column=0, pady=10, padx=10)
        self.entry_largura = ctk.CTkEntry(self.frame)
        self.entry_largura.grid(row=1, column=1, pady=10, padx=10)

        self.label_altura = ctk.CTkLabel(self.frame, text="Altura do Canteiro (m):")
        self.label_altura.grid(row=2, column=0, pady=10, padx=10)
        self.entry_altura = ctk.CTkEntry(self.frame)
        self.entry_altura.grid(row=2, column=1, pady=10, padx=10)

        self.label_pessoas = ctk.CTkLabel(self.frame, text="Número de Pessoas:")
        self.label_pessoas.grid(row=3, column=0, pady=10, padx=10)
        self.entry_pessoas = ctk.CTkEntry(self.frame)
        self.entry_pessoas.grid(row=3, column=1, pady=10, padx=10)
        
        self.label_diretorio = ctk.CTkLabel(self, text="")
        self.label_diretorio.pack(pady=10)

        self.botao_blocos = ctk.CTkButton(self, text="Selecionar Blocos", command=self.blocos)
        self.botao_blocos.pack(pady=10)

        self.botao_diretorio = ctk.CTkButton(self, text="Selecionar Diretório", command=self.selecionar_diretorio)
        self.botao_diretorio.pack(pady=10)

        self.botao_executar = ctk.CTkButton(self, text="Executar", command=self.executar_projeto)
        self.botao_executar.pack(pady=10)

        self.diretorio_selecionado = ""

        # Variáveis de estado para os CheckBox
        self.estado_deposito = ctk.IntVar(value=1)
        self.estado_elevador = ctk.IntVar(value=1)
        self.estado_banheiro = ctk.IntVar(value=1)
        self.estado_refeitorio = ctk.IntVar(value=1)
        self.estado_almoxarifado = ctk.IntVar(value=1)
        self.estado_bebedouro = ctk.IntVar(value=1)
        self.estado_vestiario = ctk.IntVar(value=1)

        self.blocos_selecionados = []

    def selecionar_diretorio(self):
        self.diretorio_selecionado = filedialog.askdirectory()
        self.label_diretorio.configure(text=self.diretorio_selecionado)

    def blocos(self):
        janela_blocos = ctk.CTkToplevel(self)
        janela_blocos.title("Selecionar Blocos")
        janela_blocos.geometry("300x350")

        label_info = ctk.CTkLabel(janela_blocos, text="Selecione os blocos desejados:")
        label_info.pack(pady=10)

        self.check_deposito = ctk.CTkCheckBox(janela_blocos, text="Depósito", variable=self.estado_deposito)
        self.check_deposito.pack(pady=5)
        self.check_elevador = ctk.CTkCheckBox(janela_blocos, text="Elevador", variable=self.estado_elevador)
        self.check_elevador.pack(pady=5)
        self.check_banheiro = ctk.CTkCheckBox(janela_blocos, text="Banheiro", variable=self.estado_banheiro)
        self.check_banheiro.pack(pady=5)
        self.check_refeitorio = ctk.CTkCheckBox(janela_blocos, text="Refeitório", variable=self.estado_refeitorio)
        self.check_refeitorio.pack(pady=5)
        self.check_almoxarifado = ctk.CTkCheckBox(janela_blocos, text="Almoxarifado", variable=self.estado_almoxarifado)
        self.check_almoxarifado.pack(pady=5, padx=10)
        self.check_bebedouro = ctk.CTkCheckBox(janela_blocos, text="Bebedouro", variable=self.estado_bebedouro)
        self.check_bebedouro.pack(pady=5)
        self.check_vestiario = ctk.CTkCheckBox(janela_blocos, text="Vestiário", variable=self.estado_vestiario)
        self.check_vestiario.pack(pady=5)

        botao_confirmar = ctk.CTkButton(janela_blocos, text="Confirmar", command=self.confirmar_blocos)
        botao_confirmar.pack(pady=10)

    def confirmar_blocos(self):
        if self.estado_deposito.get() == 1:
            self.blocos_selecionados.append("Deposito")
        if self.estado_elevador.get() == 1:
            self.blocos_selecionados.append("Elevador")
        if self.estado_banheiro.get() == 1:
            self.blocos_selecionados.append("Banheiro")
        if self.estado_refeitorio.get() == 1:
            self.blocos_selecionados.append("Refeitorio")
        if self.estado_almoxarifado.get() == 1:
            self.blocos_selecionados.append("Almoxarifado")
        if self.estado_bebedouro.get() == 1:
            self.blocos_selecionados.append("Bebedouro")
        if self.estado_vestiario.get() == 1:
            self.blocos_selecionados.append("Vestiario")


    def executar_projeto(self):
        nome_obra = self.entry_nome.get()
        largura = float(self.entry_largura.get())
        altura = float(self.entry_altura.get())
        pessoas = int(self.entry_pessoas.get())

        projeto = cad.ProjetoCanteiro(self.diretorio_selecionado, nome_obra, (largura, altura), pessoas, self.blocos_selecionados)
        projeto.executar(self.diretorio_selecionado)


if __name__ == "__main__":
    app = Janela()
    app.mainloop()
