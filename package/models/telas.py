import tkinter as tk
from tkinter import CENTER, messagebox

from package.models.treino import Treino
from package.models.exercicio import Exercicio

class SubJanelaBase:
    def __init__(self, parent, title="Subjanela", geometry="400x300"):
        self.parent = parent
        self.janela = tk.Toplevel(parent)
        self.janela.title(title)
        self.janela.geometry(geometry)
        self.setup_ui()
    
    def setup_ui(self):
        pass
    
    def destroy(self):
        self.janela.destroy()
    
    def show_warning(self, message):
        messagebox.showwarning("Aviso", message)
    
    def show_info(self, message):
        messagebox.showinfo("Sucesso", message)

class SubJanelaCriarTreino(SubJanelaBase):
    def __init__(self, parent, db, callback:function =None):
        self.db = db
        self.callback = callback
        super().__init__(parent, "Criar Novo Treino", "400x300")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Nome do Treino:").pack(pady=5)
        
        self.treino_entry = tk.Entry(self.janela)
        self.treino_entry.pack(pady=5)
        
        confirmar_btn = tk.Button(
            self.janela,
            text="Confirmar",
            command=lambda: self.confirmar_nome,
            width=15,
            font=("Arial", 12))
        confirmar_btn.pack(pady=5)
    
    def confirmar_nome(self):
        nome_treino = self.treino_entry.get().strip()
        if not nome_treino:
            self.show_warning("Por favor, insira um nome para o treino.")
            return
        
        treino = Treino(nome_treino)
        self.db._add_treino(treino)
        self.show_info("Nome salvo com sucesso!")
        self.destroy()
        
        # Open the exercise addition window
        if self.callback:
            self.callback(nome_treino)

class SubJanelaAdicionarExercicios(SubJanelaBase):
    def __init__(self, parent, db, nome_treino):
        self.db = db
        self.nome_treino = nome_treino
        self.num_exercicio = 0
        super().__init__(parent, "Adicionar Exercícios", "400x400")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Exercícios:").pack(pady=5)
        
        self.exc_num_label = tk.Label(self.janela, text=f"Num de Exercícios: {self.num_exercicio}")
        self.exc_num_label.pack(pady=5)
        
        # Exercise name
        self.exercicio_entry = tk.Entry(self.janela, width=30)
        self.exercicio_entry.insert(0, "Ex: Supino")
        self.exercicio_entry.pack(pady=5)
        self.exercicio_entry.bind("<FocusIn>", lambda e: self.limpar_texto(self.exercicio_entry))
        
        # Weight
        self.peso_entry = tk.Entry(self.janela, width=30)
        self.peso_entry.insert(0, "Ex: 10kg")
        self.peso_entry.pack(pady=5)
        self.peso_entry.bind("<FocusIn>", lambda e: self.limpar_texto(self.peso_entry))
        
        # Repetitions
        self.repeticoes_entry = tk.Entry(self.janela, width=30)
        self.repeticoes_entry.insert(0, "Ex: 10x")
        self.repeticoes_entry.pack(pady=5)
        self.repeticoes_entry.bind("<FocusIn>", lambda e: self.limpar_texto(self.repeticoes_entry))
        
        # Buttons
        exercicio_btn = tk.Button(
            self.janela,
            text="Adicionar Exercício",
            command=self.add_exercicio,
            width=15,
            font=("Arial", 12))
        exercicio_btn.pack(pady=5)
        
        end_btn = tk.Button(
            self.janela,
            text="Sair",
            command=self.destroy,
            width=15,
            font=("Arial", 12))
        end_btn.pack(pady=5)
    
    def limpar_texto(self, entry):
        entry.delete(0, tk.END)
    
    def resetar_texto(self):
        entries = [self.exercicio_entry, self.peso_entry, self.repeticoes_entry]
        placeholders = ["Ex: Supino", "Ex: 10kg", "Ex: 10x"]
        
        for entry, placeholder in zip(entries, placeholders):
            self.limpar_texto(entry)
            entry.insert(0, placeholder)
    
    def add_exercicio(self):
        # Extract numeric values from entries
        peso_text = self.peso_entry.get().replace('kg', '').strip()
        repeticoes_text = self.repeticoes_entry.get().replace('x', '').strip()
        
        if not peso_text.isdigit() or not repeticoes_text.isdigit():
            self.show_warning("Por favor, insira valores numéricos para peso e repetições.")
            return
        
        nome = self.exercicio_entry.get().strip()
        peso = int(peso_text)
        repeticoes = int(repeticoes_text)
        
        if not nome or nome.startswith("Ex:") or peso <= 0 or repeticoes <= 0:
            self.show_warning("Por favor, preencha todos os campos corretamente.")
            return
        
        exercicio = Exercicio(nome, peso, repeticoes)
        self.db._add_exercicio(self.nome_treino, exercicio)
        self.show_info("Exercício salvo com sucesso!")
        self.resetar_texto()
        
        self.num_exercicio += 1
        self.exc_num_label.config(text=f"Num de Exercícios: {self.num_exercicio}")

class TelaBase(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
    
    def limpar_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

class Tela1(TelaBase):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.build()
    
    def build(self):
        self.limpar_widgets()
        texto = tk.Label(self, text="Bem-vindo ao sistema treinos!", font=("Arial", 16, "bold"))
        texto.place(relx=0.5, rely=50/380, anchor=CENTER)
        
        self.entrybox = tk.Entry(self, width=50)
        self.entrybox.place(relx=0.5, rely=100/380, anchor=CENTER)
        
        entrar_button = tk.Button(
            self, text="Entrar",
            command=self.confirmar_nome,
            font=("Arial", 16))
        entrar_button.place(relx=0.5, rely=200/380, anchor=CENTER)
        
        assinatura = tk.Label(self, text="Desenvolvido por Tiago Geovane", font=("Arial", 10))
        assinatura.place(relx=0.5, rely=330/380, anchor=CENTER)
    
    def confirmar_nome(self):
        name = self.entrybox.get().strip()
        if not name:
            messagebox.showwarning("Aviso", "Por favor, digite um nome.")
            return
        self.controller.trocar_tela('tela2', 'tela1')

class Tela2(TelaBase):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.build()
        self.db = controller.db
    
    def build(self):
        self.limpar_widgets()
        
        titulo = tk.Label(self, text="Menu Principal", font=("Arial", 16, "bold"))
        titulo.place(relx=0.5, rely=50/380, anchor=CENTER)

        criar_treino_btn = tk.Button(
            self, text="Criar Treino",
            command=self.criar_treino,
            width=15,
            font=("Arial", 12))
        criar_treino_btn.place(relx=0.5, rely=120/380, anchor=CENTER)
        
        editar_treino_btn = tk.Button(
            self, text="Editar Treino",
            command=self.editar_treino,
            width=15,
            font=("Arial", 12))
        editar_treino_btn.place(relx=0.5, rely=170/380, anchor=CENTER)
        
        ver_treino_btn = tk.Button(
            self, text="Ver Treinos",
            command=self.ver_treino,
            width=15,
            font=("Arial", 12))
        ver_treino_btn.place(relx=0.5, rely=220/380, anchor=CENTER)
        
        estatisticas_btn = tk.Button(
            self, text="Estatísticas",
            command=self.ver_estatisticas,
            width=15,
            font=("Arial", 12))
        estatisticas_btn.place(relx=0.5, rely=270/380, anchor=CENTER)
        
        voltar_button = tk.Button(
            self, text="Voltar",
            command=lambda: self.controller.trocar_tela('tela1', 'tela2'),
            width=8,
            font=("Arial", 10))
        voltar_button.place(relx=0.5, rely=330/380, anchor=CENTER)

    def criar_treino(self):
        def abrir_janela_exercicios(nome_treino):
            SubJanelaAdicionarExercicios(self, self.db, nome_treino)
        
        SubJanelaCriarTreino(self, self.db, callback=abrir_janela_exercicios)

    def editar_treino(self):
        # Implementação futura para editar treino
        messagebox.showinfo("Informação", "Funcionalidade de editar treino será implementada em breve!")
        
    def ver_treino(self):
        # Implementação futura para visualizar treino
        messagebox.showinfo("Informação", "Funcionalidade de visualizar treinos será implementada em breve!")
        
    def ver_estatisticas(self):
        # Implementação futura para visualizar estatísticas
        messagebox.showinfo("Informação", "Funcionalidade de estatísticas será implementada em breve!")