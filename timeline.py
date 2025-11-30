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
        
        self.protocol("WM_DELETE_WINDOW", self.fechar)

    def configuracoes(self):
        self.geometry("900x700")
        self.title("Humoro - Timeline de Humor")
        self.resizable(False, False)
        
        # Faz a janela aparecer na frente da tela de menu
        self.lift() # Traz a janela para frente
        self.focus_force() # Fora o foco nesse janela
        self.grab_set() # Torna a janela modal (fazendo com que o usuário não consiga interagir com a tela de menu enquanto a janela está aberta)

    def layout(self):
        self.lb_title = ctk.CTkLabel(
            self, 
            text=f"Timeline de Humor",
            font=("Century Gothic Bold", 28)
        )
        self.lb_title.pack(pady=20)
        
        # Subtítulo com nome do usuário
        self.lb_subtitle = ctk.CTkLabel(
            self,
            text=f"Histórico de {self.username}",
            font=("Century Gothic", 16)
        )
        self.lb_subtitle.pack(pady=5)

        # Frame para lista com scroll
        self.frame_lista = ctk.CTkScrollableFrame(self, width=500, height=450)
        self.frame_lista.pack(pady=10, padx=25)

        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="VOLTAR AO MENU",
            font=("Century Gothic Bold", 14),
            width=300,
            height=45,
            corner_radius=15,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.fechar
        )
        self.btn_voltar.pack(pady=15)

    def carregar_timeline(self):
        """Carrega e exibe todos os questionários do usuário"""
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Busca questionários
        registros = self.db.listar_questionarios(self.username)

        if not registros:
            vazio = ctk.CTkLabel(
                self.frame_lista, 
                text="Você ainda não respondeu nenhum questionário.\n\nComece agora na Opção Questionário do menu!",
                font=("Century Gothic", 16),
                text_color="gray"
                )
            vazio.pack(pady=50)
            return
        
        # Exibe cada questionário
        for i, (data, hora, humor, sono, social, lazer) in enumerate(registros):
            self.criar_card_questionario(data, hora, humor, sono, social, lazer, i)     
                
    def criar_card_questionario(self, data, hora, humor, sono, social, lazer, index):
        """Criar um card visual para cada questionário"""
        # Frame do card
        card = ctk.CTkFrame(self.frame_lista, width=800, corner_radius=15)
        card.pack(pady=10, padx=10, fill="x")
        
        # Cor de fundo alternada
        if index % 2 == 0:
            card.configure(fg_color=("#E8E8E8", "#2B2B2B"))
            
        # Cabeçalho: Data e Hora
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill= "x", padx=15, pady=10)
        
        # Formata data (2025-11-29 -> 29/11/2025)
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        lb_data = ctk.CTkLabel(
            header_frame,
            text=f"Data: {data_formatada} Hora: {hora}",
            font=("Century Gothic Bold", 16),
            anchor="w"
        )
        lb_data.pack(side="left")
        
        # Separador
        separador = ctk.CTkFrame(card, height=2, fg_color="gray")
        separador.pack(fill="x", padx=15, pady=5)
        
        # Grid com as respostas
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=10)
        
        # Configura grid 2x2
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Emojis para cada categoria
        emojis = {
            "Excelente": "😄",
            "Bom": "🙂",
            "Mediano": "😐",
            "Ruim": "😟",
            "Péssimo": "😭"
        }
        
        # Humor 
        self.criar_item_resposta(
            grid_frame,
            "😊 Humor:",
            humor,
            emojis.get(humor, ""),
            0, 0
        )
        
        # Sono
        self.criar_item_resposta(
            grid_frame, 
            "😴 Sono:", 
            sono, 
            emojis.get(sono, ""),
            0, 1
        )
        
        # Social
        self.criar_item_resposta(
            grid_frame, 
            "👥 Social:", 
            social, 
            emojis.get(social, ""),
            1, 0
        )
        
        # Lazer
        self.criar_item_resposta(
            grid_frame, 
            "🎮 Lazer:", 
            lazer, 
            emojis.get(lazer, ""),
            1, 1
        )
        
    def criar_item_resposta(self, parent, label, valor, emoji, row, col):
        """Cria um item de resposta formatado"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.grid(row=row, column=col, padx=10, pady=8, sticky="w")
        
        # Label da categoria
        lb_categoria = ctk.CTkLabel(
            item_frame,
            text=label,
            font=("Century Gothic Bold", 14),
            anchor="w"
        )
        lb_categoria.pack(anchor="w")
        
        # Valor com emoji
        lb_valor = ctk.CTkLabel(
            item_frame,
            text=f"{emoji} {valor}",
            font=("Century Gothic", 14),
            anchor="w"
        )
        lb_valor.pack(anchor="w", padx=5)
        
    def fechar(self):
        """Fecha a timeline"""
        self.destroy()