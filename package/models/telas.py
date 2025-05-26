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
    def __init__(self, parent, db, callback=None):
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
            command=self.confirmar_nome,
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

class SubJanelaEditarTreino(SubJanelaBase):
    def __init__(self, parent, db, callback1=None, callback2=None):
        self.db = db
        self.callback1 = callback1
        self.callback2 = callback2
        super().__init__(parent, "Editar Treino", "400x300")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Nome do Treino para Editar:").pack(pady=5)
        
        self.treino_entry = tk.Entry(self.janela)
        self.treino_entry.pack(pady=5)
        
        confirmar_btn = tk.Button(
            self.janela,
            text="Confirmar",
            command=self.confirmar_nome,
            width=15,
            font=("Arial", 12))
        confirmar_btn.pack(pady=5)
    
    def confirmar_nome(self):
        nome_treino = self.treino_entry.get().strip()
        if not nome_treino:
            self.show_warning("Por favor, insira um nome para o treino.")
            return
        
        if not self.db._get_treino(nome_treino):
            self.show_warning('Treino não encontrado, verifique se digitou o nome corretamente.')
            return
        
        def editar_nome_treino():
            if self.callback1:
                self.callback1(nome_treino)
            self.destroy()
            
        def editar_exercicio():
            if self.callback2:
                self.callback2(nome_treino)
            self.destroy()
        
        editar_nome_btn = tk.Button(
            self.janela,
            text="Editar Nome Treino",
            command=editar_nome_treino,
            width=15,
            font=("Arial", 12))
        editar_nome_btn.pack(pady=5)

        editar_exercicio_btn = tk.Button(
            self.janela,
            text="Editar Exercicio",
            command=editar_exercicio,
            width=15,
            font=("Arial", 12))
        editar_exercicio_btn.pack(pady=5)

class SubJanelaEditarNomeTreino(SubJanelaBase):
    def __init__(self, parent, db, nome_treino):
        self.db = db
        self.nome_treino = nome_treino
        super().__init__(parent, "Editar Nome do Treino", "500x400")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Nome novo do Treino:").pack(pady=5)
        
        self.novo_nome = tk.Entry(self.janela)
        self.novo_nome.pack(pady=5)

        editar_treino_btn = tk.Button(
            self.janela,  
            text="Editar Nome Treino",
            command=self.editar_nome_treino,
            width=15,
            font=("Arial", 12))
        editar_treino_btn.pack(pady=10)  
        
        tk.Label(self.janela, text="O nome será atualizado após confirmar.").pack(pady=5)

    def editar_nome_treino(self):
        novo_nome = self.novo_nome.get().strip()
        if not novo_nome:
            self.show_warning("Por favor, insira um novo nome para o treino.")
            return
            
        self.db._update_treino_name(self.nome_treino, novo_nome)
        self.nome_treino = novo_nome
        self.show_info("Nome do treino atualizado com sucesso!")
        self.destroy()

class SubJanelaEditarExercicio(SubJanelaBase):
    def __init__(self, parent, db, nome_treino):
        self.db = db
        self.nome_treino = nome_treino
        super().__init__(parent, "Editar Exercícios", "500x400")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Exercícios:").pack(pady=5)

        treino = self.db._get_treino(self.nome_treino)
        
        self.num_exercicio = len(treino.exercises) if treino and hasattr(treino, 'exercises') and treino.exercises is not None else 0
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
            text="Adicionar/Editar Exercício",
            command=self.check_exercicio_existe,
            width=20,
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
    
    def check_exercicio_existe(self):
        nome_exercicio = self.exercicio_entry.get().strip()
        treino = self.db._get_treino(self.nome_treino)
        
        exercise_exists = False
        
        if treino.exercises:
            for exercicio in treino.exercises:
                if nome_exercicio == exercicio.name:
                    exercise_exists = True
        
        if exercise_exists:
            self.edit_exercicio()
        else:
            self.add_exercicio()
    
    def add_exercicio(self):
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
        self.show_info("Exercício adicionado com sucesso!")
        self.resetar_texto()
        
        self.num_exercicio += 1
        self.exc_num_label.config(text=f"Num de Exercícios: {self.num_exercicio}")
    
    def edit_exercicio(self):
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
        
        exercicio = self.db._get_exercicio(nome, self.nome_treino)
        if not exercicio:
            self.show_warning("Exercício não encontrado.")
            return
            
        self.db._update_exercise(nome, self.nome_treino, peso, "weight")
        self.db._update_exercise(nome, self.nome_treino, repeticoes, "reps")
        self.show_info("Exercício editado com sucesso!")
        self.resetar_texto()
class SubJanelaListarTreinos(SubJanelaBase):
    def __init__(self, parent, db):
        self.db = db
        self.treinos = self.db._get_treinos()
        self.index = 0
        super().__init__(parent, "Listar Treinos", "600x500")
        
        if not self.treinos:
            self.show_warning("Nenhum treino encontrado!")
            self.destroy()

    def setup_ui(self):
        main_frame = tk.Frame(self.janela)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.titulo_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"))
        self.titulo_label.pack(pady=(0, 10))
        
        self.exercicios_frame = tk.Frame(main_frame, relief="solid", borderwidth=1)
        self.exercicios_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        botoes_frame = tk.Frame(main_frame)
        botoes_frame.pack(fill="x", pady=(10, 0))
        
        anterior_btn = tk.Button(
            botoes_frame,
            text="◀ Anterior",
            command=self.treino_anterior,
            width=12,
            font=("Arial", 10))
        anterior_btn.pack(side="left", padx=(0, 5))
        
        self.posicao_label = tk.Label(botoes_frame, text="", font=("Arial", 10))
        self.posicao_label.pack(side="left", expand=True)
        
        proximo_btn = tk.Button(
            botoes_frame,
            text="Próximo ▶",
            command=self.proximo_treino,
            width=12,
            font=("Arial", 10))
        proximo_btn.pack(side="right", padx=(5, 0))
        
        fechar_btn = tk.Button(
            main_frame,
            text="Fechar",
            command=self.destroy,
            width=15,
            font=("Arial", 12))
        fechar_btn.pack(pady=(10, 0))
        
        self.mostrar_treino_atual()
    
    def mostrar_treino_atual(self):
        if not self.treinos:
            return
            
        treino_atual = self.treinos[self.index]
        
        self.titulo_label.config(text=f"Treino: {treino_atual.name}")
        
        self.posicao_label.config(text=f"{self.index + 1} de {len(self.treinos)}")
        
        for widget in self.exercicios_frame.winfo_children():
            widget.destroy()
        
        if hasattr(treino_atual, 'exercises') and treino_atual.exercises:
            header_frame = tk.Frame(self.exercicios_frame)
            header_frame.pack(fill="x", padx=5, pady=5)
            
            tk.Label(header_frame, text="Exercícios:", font=("Arial", 12, "bold")).pack(anchor="w")
            
            for i, exercicio in enumerate(treino_atual.exercises, 1):
                exercicio_frame = tk.Frame(self.exercicios_frame, relief="groove", borderwidth=1)
                exercicio_frame.pack(fill="x", padx=5, pady=2)
                
                info_text = f"{i}. {exercicio.name} - {exercicio.weight}kg - {exercicio.reps}x"
                exercicio_label = tk.Label(exercicio_frame, text=info_text, font=("Arial", 11), anchor="w")
                exercicio_label.pack(fill="x", padx=5, pady=3)
        else:
            sem_exercicios_label = tk.Label(
            self.exercicios_frame,
            text="Nenhum exercício encontrado neste treino.",
            font=("Arial", 12),
            fg="gray"
        )
            sem_exercicios_label.pack(expand=True)
    
    def proximo_treino(self):
        if not self.treinos:
            return
            
        self.index = (self.index + 1) % len(self.treinos) 
        self.mostrar_treino_atual()
    
    def treino_anterior(self):
        if not self.treinos:
            return
            
        self.index = (self.index - 1) % len(self.treinos)  
        self.mostrar_treino_atual()
class SubJanelaRemoverTreino(SubJanelaBase):
    def __init__(self, parent, db):
        self.db = db
        super().__init__(parent, "Remover Treino", "400x300")
    
    def setup_ui(self):
        tk.Label(self.janela, text="Nome do Treino para Remover:").pack(pady=5)
        
        self.treino_entry = tk.Entry(self.janela, width=30)
        self.treino_entry.pack(pady=5)
        

        confirmar_btn = tk.Button(
            self.janela,
            text="Remover Treino",
            command=self.confirmar_remocao,
            width=15,
            font=("Arial", 12),
            bg="#ff4444",
            fg="white")
        confirmar_btn.pack(pady=10)
        
        listar_btn = tk.Button(
            self.janela,
            text="Ver Treinos Disponíveis",
            command=self.mostrar_treinos_disponiveis,
            width=20,
            font=("Arial", 10))
        listar_btn.pack(pady=5)
        
        self.lista_frame = tk.Frame(self.janela)
        self.lista_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cancelar_btn = tk.Button(
            self.janela,
            text="Cancelar",
            command=self.destroy,
            width=10,
            font=("Arial", 10))
        cancelar_btn.pack(pady=5)
    
    def mostrar_treinos_disponiveis(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        treinos = self.db._get_treinos()
        
        if not treinos:
            tk.Label(self.lista_frame, text="Nenhum treino encontrado.", 
                    font=("Arial", 10), fg="gray").pack()
            return
        
        tk.Label(self.lista_frame, text="Treinos disponíveis:", 
                font=("Arial", 10, "bold")).pack(anchor="w")
        
        canvas = tk.Canvas(self.lista_frame, height=100)
        scrollbar = tk.Scrollbar(self.lista_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, treino in enumerate(treinos, 1):
            treino_text = f"{i}. {treino.name}"
            treino_label = tk.Label(scrollable_frame, text=treino_text, 
                                  font=("Arial", 9), anchor="w")
            treino_label.pack(fill="x", padx=5, pady=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def confirmar_remocao(self):
        nome_treino = self.treino_entry.get().strip()
        
        if not nome_treino:
            self.show_warning("Por favor, insira o nome do treino.")
            return
        
        treino = self.db._get_treino(nome_treino)
        if not treino:
            self.show_warning("Treino não encontrado. Verifique se digitou o nome corretamente.")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover o treino '{nome_treino}'?\n\n"
            f"Esta ação não pode ser desfeita e todos os exercícios "
            f"deste treino também serão removidos.",
            icon="warning"
        )
        
        if resposta:
            try:
                self.db._remove_treino(nome_treino)
                self.show_info(f"Treino '{nome_treino}' removido com sucesso!")
                self.destroy()
            except Exception as e:
                self.show_warning(f"Erro ao remover treino: {str(e)}")

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
            command=self.ver_treinos,
            width=15,
            font=("Arial", 12))
        ver_treino_btn.place(relx=0.5, rely=220/380, anchor=CENTER)
        
        remover_btn = tk.Button(
            self, text="Remover Treino",
            command=self.remover_treino,
            width=15,
            font=("Arial", 12))
        remover_btn.place(relx=0.5, rely=270/380, anchor=CENTER)
        
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
        def abrir_janela_editar_nome(nome_treino):
            SubJanelaEditarNomeTreino(self, self.db, nome_treino)
            
        def abrir_janela_editar_exercicio(nome_treino):
            SubJanelaEditarExercicio(self, self.db, nome_treino)
        
        SubJanelaEditarTreino(self, self.db, callback1=abrir_janela_editar_nome, callback2=abrir_janela_editar_exercicio)
    def ver_treinos(self):
        SubJanelaListarTreinos(self,self.db)
    def remover_treino(self):
       SubJanelaRemoverTreino(self,self.db)