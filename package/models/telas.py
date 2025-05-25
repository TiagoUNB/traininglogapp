import tkinter as tk
from tkinter import CENTER, messagebox

from package.models.treino import Treino
from package.models.exercicio import Exercicio

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
        texto.place(relx=0.5,rely=50/380,anchor=CENTER)
        
        self.entrybox = tk.Entry(self, width=50)
        self.entrybox.place(relx=0.5,rely=100/380,anchor=CENTER)
        
        entrar_button = tk.Button(
            self, text="Entrar",
            command=self.confirmar_nome,
            font=("Arial", 16))
        entrar_button.place(relx=0.5,rely=200/380,anchor=CENTER)
        
        assinatura = tk.Label(self, text="Desenvolvido por Tiago Geovane", font=("Arial", 10))
        assinatura.place(relx=0.5,rely=330/380,anchor=CENTER)
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

        #subjanela 1

        sub_janela = tk.Toplevel(self)
        sub_janela.title("Criar Novo Treino")
        
        sub_janela.geometry("400x300")

        self.num_exercicio = 0
        
        tk.Label(sub_janela, text="Nome do Treino:").pack(pady=5)
        
        treino_entry = tk.Entry(sub_janela)
        treino_entry.pack(pady=5)

        self.nome_treino = treino_entry.get()

        def confirmar_nome():
            nome_treino = treino_entry.get()
            if not nome_treino:
                messagebox.showwarning("Aviso", "Por favor, insira um nome para o treino.")
                return
            treino = Treino(nome_treino)
            self.db._add_treino(treino) #objeto
            self.nome_treino = nome_treino
            messagebox.showinfo("Sucesso", "Nome salvo com sucesso!")
            sub_janela.destroy()
            subjanela2()
        
        confirmar_btn = tk.Button(
            sub_janela,
            text="Confirmar",
            command=lambda: confirmar_nome(),
            width=15,
            font=("Arial", 12))
        confirmar_btn.pack(pady=5)

        def subjanela2():
            sub_janela2 = tk.Toplevel(self)
            sub_janela2.title("Criar Novo Treino")
            
            sub_janela2.geometry("400x300")
            
            tk.Label(sub_janela2, text="Exercicios:").pack(pady=5)
            tk.Label(sub_janela2, text=f"Num de Exercicios: {self.num_exercicio}").pack(pady=5)


            exercicio_entry = tk.Entry(sub_janela2, width=30)
            exercicio_entry.insert(0, "Ex: Supino")
            exercicio_entry.pack(pady=5)
            exercicio_entry.bind("<FocusIn>", lambda e: limpar_texto(exercicio_entry))
            
            # Peso
            peso_entry = tk.Entry(sub_janela2, width=30)
            peso_entry.insert(0, "Ex: 10kg")
            peso_entry.pack(pady=5)
            peso_entry.bind("<FocusIn>", lambda e: limpar_texto(peso_entry))
            
            # Repetições
            repeticoes_entry = tk.Entry(sub_janela2, width=30)
            repeticoes_entry.insert(0, "Ex: 10x")
            repeticoes_entry.pack(pady=5)
            repeticoes_entry.bind("<FocusIn>", lambda e: limpar_texto(repeticoes_entry))

            def limpar_texto(entry):
                entry.delete(0, tk.END)

            def add_exercicio(nome_treino):
                if not peso_entry.get().isdigit() or not repeticoes_entry.get().isdigit() :
                    messagebox.showwarning("Aviso", "Por favor, insira valores numéricos para peso e repetições.")
                    return
                
                nome = exercicio_entry.get()
                peso = int(peso_entry.get())
                repeticoes = int(repeticoes_entry.get())
                
                if not nome != "" and peso != 0 and repeticoes != 0:
                    messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
                    return
                exercicio = Exercicio(nome, peso, repeticoes)
                self.db._add_exercicio(nome_treino, exercicio)
                messagebox.showinfo("Sucesso", "Exercicio salvo com sucesso!")
                sub_janela2.destroy()
                return
                

            exercicio_btn = tk.Button(
                sub_janela2,
                text="Adicionar Exercicio",
                command=lambda: add_exercicio(self.nome_treino),
                width=15,
                font=("Arial", 12))
            exercicio_btn.pack(pady=5)
    def editar_treino(self):
        # Implementação futura para editar treino
        messagebox.showinfo("Informação", "Funcionalidade de editar treino será implementada em breve!")
        
    def ver_treino(self):
        # Implementação futura para visualizar treino
        messagebox.showinfo("Informação", "Funcionalidade de visualizar treinos será implementada em breve!")
        
    def ver_estatisticas(self):
        # Implementação futura para visualizar estatísticas
        messagebox.showinfo("Informação", "Funcionalidade de estatísticas será implementada em breve!")
