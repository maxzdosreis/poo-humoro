import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

class MenuApp(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        
        self.configuracoes_janela()
        self.criar_menu()
        
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        
    def configuracoes_janela(self):
        self.geometry("900x650")
        self.title("Humoro - Menu Principal")
        self.resizable(False, False)
        
    def criar_menu(self):
        try:
            self.img = ctk.CTkImage(
                light_image=Image.open("humoro-img.png"),
                dark_image=Image.open("humoro-img.png"),
                size=(200,200)
            )
            self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
            self.lb_img.pack(pady=20)
        except:
            # Se não encontrar a imagem, o programa irá continuar sem ela (evitando assim que quebre algo)
            pass
        
        self.lb_welcome = ctk.CTkLabel(
            self,
            text=f"Bem-vindo(a), {self.username}!",
            font=("Century Gothic Bold", 24)
        )
        self.lb_welcome.pack(pady=10)
        
        # Frame para os botões
        self.frame_menu = ctk.CTkFrame(self, width=750,height=400)
        self.frame_menu.pack(pady=20)
        self.frame_menu.pack_propagate(False)
        
        # Título do Menu
        self.lb_title = ctk.CTkLabel(
            self.frame_menu,
            text="Escolha uma opção",
            font=("Century Gothic Bold", 20)
        )
        self.lb_title.pack(pady=20)
        
        # Frame de botões (2 colunas)
        self.frame_botoes = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.frame_botoes.pack(pady=10)
        
        # Questionário
        self.btn_tela1 = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Questionário".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.abrir_tela1
        )
        self.btn_tela1.grid(row=0, column=0, padx=15, pady=10)
        
        # Timeline
        self.btn_tela2 = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Timeline do Humor".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.abrir_tela2
        )
        self.btn_tela2.grid(row=1, column=0, padx=15, pady=10)
        
        self.btn_tela3 = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Opção 3".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.abrir_tela3
        )
        self.btn_tela3.grid(row=2, column=0, padx=15, pady=10)
        
        # Coluna 2
        self.btn_tela4 = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Mapa Emocional".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.abrir_tela4
        )
        self.btn_tela4.grid(row=0, column=1, padx=15, pady=10)
        
        self.btn_tela5 = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Opção 5".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.abrir_tela5
        )
        self.btn_tela5.grid(row=1, column=1, padx=15, pady=10)
        
        self.btn_sair = ctk.CTkButton(
            self.frame_botoes,
            width=300,
            height=50,
            text="Sair e Voltar ao Login".upper(),
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.voltar_login
        )
        self.btn_sair.grid(row=2, column=1, padx=15, pady=10)
        
    def abrir_tela1(self):
        import questionario
        questionario.Questionario(self, self.username)
    
    def abrir_tela2(self):
        import timeline
        timeline.TimelineApp(self, self.username)
    
    def abrir_tela3(self):
        messagebox.showinfo("Menu", "Tela 3 ainda não implementada!")
    
    def abrir_tela4(self):
        import mapa
        mapa.Mapa(self, self.username)
    
    def abrir_tela5(self):
        messagebox.showinfo("Menu", "Tela 5 ainda não implementada!")
    
    def voltar_login(self):
        # Fecha o menu
        self.destroy()
        # Mostra a tela de login novamente
        self.parent.deiconify()
    
    def fechar_aplicacao(self):
        try:
            self.parent.destroy()
        except:
            pass
