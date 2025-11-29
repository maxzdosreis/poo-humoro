import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import Database

class TimelineApp(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.db = Database()

        self.configuracoes()
        self.layout()
        self.carregar_timeline()

    def configuracoes(self):
        self.geometry("700x600")
        self.title("Timeline de Humor")
        self.resizable(False, False)

    def layout(self):
        self.lb_title = ctk.CTkLabel(
            self, text=f"Timeline de Humor - {self.username}",
            font=("Century Gothic Bold", 24)
        )
        self.lb_title.pack(pady=15)

        # Frame para lista
        self.frame_lista = ctk.CTkFrame(self, width=600, height=400)
        self.frame_lista.pack(pady=10)
        self.frame_lista.pack_propagate(False)

        # Área de rolagem
        self.scroll = ctk.CTkScrollableFrame(self.frame_lista, width=580, height=380)
        self.scroll.pack()

        # Seleção de humor para registrar
        self.humor_var = ctk.StringVar(value="")
        self.drop = ctk.CTkOptionMenu(
            self, width=300,
            values=["😀 Feliz", "🙂 Satisfeito", "😐 Neutro", "😔 Triste", "😭 Péssimo"],
            variable=self.humor_var
        )
        self.drop.pack(pady=10)

        self.btn_add = ctk.CTkButton(
            self,
            text="Registrar Humor",
            font=("Century Gothic Bold", 16),
            width=300,
            corner_radius=15,
            command=self.registrar_humor
        )
        self.btn_add.pack(pady=10)

    def carregar_timeline(self):
        registros = self.db.listar_humores(self.username)

        for widget in self.scroll.winfo_children():
            widget.destroy()

        if not registros:
            vazio = ctk.CTkLabel(self.scroll, text="Ainda não há registros.", font=("Century Gothic", 16))
            vazio.pack(pady=20)
            return

        for humor, data in registros:
            item = ctk.CTkFrame(self.scroll, width=500)
            item.pack(pady=10)

            lb_data = ctk.CTkLabel(item, text=data, font=("Century Gothic", 14))
            lb_data.pack(anchor="w", padx=5)

            lb_humor = ctk.CTkLabel(item, text=humor, font=("Century Gothic Bold", 18))
            lb_humor.pack(anchor="w", padx=5, pady=3)

    def registrar_humor(self):
        humor = self.humor_var.get()

        if humor == "":
            messagebox.showwarning("Aviso", "Selecione um humor!")
            return

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        sucesso, msg = self.db.salvar_humor(self.username, humor, data)

        if sucesso:
            messagebox.showinfo("Humor", "Humor registrado!")
            self.carregar_timeline()
        else:
            messagebox.showerror("Erro", msg)
