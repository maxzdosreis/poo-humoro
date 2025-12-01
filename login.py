import customtkinter as ctk
from PIL import Image
import sqlite3 #não é acessado?#
from tkinter import messagebox
from database import Database

class BackEnd(): 
    def __init__(self):
        self.db = Database()
        self.db.cria_tabelas()
    
    def cadastrar_usuario(self):
        username = self.username_cadastro_entry.get()
        email = self.email_cadastro_entry.get()
        password = self.password_cadastro_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if (username == "" or email == "" or password == "" or confirm_password == ""):
            messagebox.showerror(title="Sistema de login", message="ERRO!!!\nPor favor preencha todos os campos!")
            return
        if (len(username) < 4):
            messagebox.showwarning(title="Sistema de Login", message="O nome de usuário deve ser de pelo menos 4 caracteres.")
            return
        if (len(password) < 4):
            messagebox.showwarning(title="Sistema de Login", message="A senha deve ser de pelo menos 4 caracteres.")
            return
        if (password != confirm_password):
            messagebox.showerror(title="Sistema de login", message="ERRO!!!\nAs senhas colocadas não são iguais, coloque senhas iguais.")
            return    
        
        sucesso, mensagem = self.db.cadastrar_usuario(username, email, password, confirm_password)
        
        if sucesso:
            messagebox.showinfo(title="Sistema de login", message=f"Parabéns {username}\nOs seus dados foram cadastrados com sucesso!")
            self.limpa_entry_login()
            self.tela_login()
        else:                   
            messagebox.showerror(title="Sistema de login", message=f"Erro!\n{mensagem}")
        
    def login_verify(self):
        username = self.username_login_entry.get()
        password = self.password_login_entry.get()
        
        if (username == "" or password == ""):
            messagebox.showerror(title="Sistema de Login", message="Por favor preencha todos os campos!")
            return
        
        sucesso, mensagem = self.db.verificar_login(username, password)
        if sucesso:
            self.limpa_entry_login()
            self.abrir_menu(username)
        else:
            messagebox.showerror(title="Sistema de Login", message=f"ERRO!!!\n{mensagem}\nPor favor verifique seus dados ou cadastre-se!")

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        BackEnd.__init__(self)
        self.configuracoes_janela_inicial()
        self.tela_login()
        
    def configuracoes_janela_inicial(self):
        self.geometry("750x450") # define o tamanho da janela
        self.title("Sistema de Login") # define o título da janela
        self.resizable(False, False) # não deixa o usuário maximizar ou trocar o tamanho da janela definada anteriormente

    def tela_login(self):
        # Limpa widgets anteriores se existirem
        if hasattr(self, 'frame_cadastro'):
            self.frame_cadastro.place_forget()
        if hasattr(self, 'frame_login'):
            self.frame_login.place_forget()
        
        self.img = ctk.CTkImage(
            light_image=Image.open("humoro-img.png"),
            dark_image=Image.open("humoro-img.png"),
            size=(300,300)
        ) # adiciona uma imagem na tela de login
        self.lb_img = ctk.CTkLabel(self, text="", image=self.img)
        self.lb_img.grid(row=1, column=0, padx=20, pady=20)
        
        # definindo um título na página
        self.lb_title_tela = ctk.CTkLabel(self, text="Faça o seu login ou cadastre-se\n na nossa plataforma para acessar\n os nossos serviços!", font=("Century Gothic Bold", 14))
        self.lb_title_tela.grid(row=0, column=0, pady=15, padx=10)
        
        # Criar a frame do formulário de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=375, y=35)
        
        # colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu login", font=("Century Gothic Bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário...", font=("Century Gothic Bold", 16), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)
        
        self.password_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha de usuário...", font=("Century Gothic Bold", 16), corner_radius=15, show="*")
        self.password_login_entry.grid(row=2, column=0, pady=10, padx=10)
        
        self.ver_password_login = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha",font=("Century Gothic Bold", 12), corner_radius=20, command=self.mostra_password_login)
        self.ver_password_login.grid(row=3, column=0, pady=10, padx=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer Login".upper(), font=("Century Gothic Bold", 14), corner_radius=15, command=self.login_verify)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)
        
        self.span = ctk.CTkLabel(self.frame_login, text="Se não tens conta, clique no botão abaixo\n para poder se cadastrar no nosso sistema!", font=("Century Gothic", 10))
        self.span.grid(row=5, column=0, pady=10, padx=10)
        
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic Bold", 14), corner_radius=15, command=self.tela_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=10, padx=10)
        
    def tela_cadastro(self):
        # remover tela de login
        self.frame_login.place_forget()
        
        # criando frame - formulário cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=375, y=35)
        
        # Criando o título da
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu cadastro", font=("Century Gothic Bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        # Cria os nossos widgets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário...", font=("Century Gothic Bold", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)
        
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email de usuário...", font=("Century Gothic Bold", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)
        
        self.password_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Sua senha de usuário...", font=("Century Gothic Bold", 16), corner_radius=15, show="*")
        self.password_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)
        
        self.confirm_password_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirma senha de usuário...", font=("Century Gothic Bold", 16), corner_radius=15, show="*")
        self.confirm_password_entry.grid(row=4, column=0, pady=5, padx=10)
        
        self.ver_password_cadastro = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha",font=("Century Gothic Bold", 12), corner_radius=20, command=self.mostra_password_cadastro)
        self.ver_password_cadastro.grid(row=5, column=0, pady=10)
        
        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic Bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)
        
        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar a Tela de Login".upper(), font=("Century Gothic Bold", 14), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_login)
        self.btn_login_back.grid(row=7, column=0, pady=10, padx=10)
        
    def mostra_password_login(self):
        if (self.ver_password_login.get()):
            self.password_login_entry.configure(show="")
        else:
            self.password_login_entry.configure(show="*")
            
    def mostra_password_cadastro(self):
        if (self.ver_password_cadastro.get()):
            self.password_cadastro_entry.configure(show="")
            self.confirm_password_entry.configure(show="")
        else:
            self.password_cadastro_entry.configure(show="*")
            self.confirm_password_entry.configure(show="*")        
        
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, ctk.END)
        self.email_cadastro_entry.delete(0, ctk.END)
        self.password_cadastro_entry.delete(0, ctk.END)
        self.confirm_password_entry.delete(0, ctk.END) 
        
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, ctk.END)
        self.password_login_entry.delete(0, ctk.END)
        
    def abrir_menu(self, username):
        self.withdraw()
        import menu
        menu_window = menu.MenuApp(self, username)
        
if __name__=="__main__":
    app = App()
    app.mainloop()