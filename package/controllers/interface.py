import tkinter as tk
from package.models.telas import Tela1,Tela2
from package.controllers.treino_db import TreinoDB

class Interface:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Heavy")
        self.db = TreinoDB()
        
        app_width = 640
        app_height = 360
        screen_width = self.janela.winfo_screenwidth()
        screen_height = self.janela.winfo_screenheight()
    
        x = int((screen_width/2) - (app_width/2))
        y = int((screen_height/2) - (app_height/2))
        
        self.janela.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.frames = {
            'tela1': Tela1(self.janela, self),
            'tela2': Tela2(self.janela, self)
        }
        self.tela_atual = 'tela1'
        tela1 = self.frames['tela1']
        
        tela1.build()
        tela1.pack(fill="both", expand=True)
    
    def trocar_tela(self, tela_destino, tela_atual=None):
        try:
            if tela_atual:
                self.frames[tela_atual].pack_forget()
            self.frames[tela_destino].build() 
            self.frames[tela_destino].pack(fill="both", expand=True)
            self.tela_atual = tela_destino
        except Exception as e:
            print(f"ERRO ao trocar tela: {e}")
    
    def start(self):
        self.janela.mainloop()
