import calendar
from tkinter import Canvas
import customtkinter as ctk
from database import Database
from datetime import datetime
import locale

'''
    Classe: Mapa
    Objetos:
        - CTkFrame
        - CTkButton
        - CTkLabel
        - Canvas
'''
class Mapa(ctk.CTkToplevel):
    # Cores que representam cada emoção no mapa emocional.
    CORES = {
        "Excelente": "#006400",
        "Bom": "#90EE90",
        "Mediano": "#FFD700",
        "Ruim": "#FF8C00",
        "Péssimo": "#8B0000"
    }

    # Array de meses com os nomes em português.
    MESES_PT = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    def __init__(self, parent, username):
        super().__init__(parent)

        # username: nome de usuário para exibição na tela 
        self.username = username

        # db: banco de dados para checagem de dias respondidos
        self.db = Database()

        # ano: ano atual para limitar o calendário
        self.ano = 2025

        # começa no mês atual do sistema, mas forçando 2025
        self.mes = datetime.now().month

        # configuracoes: configurações específicas utilizadas na tela na instância da tela
        self.configuracoes()

        # top_bar: barra de navegação horizontal na parte de cima da tela
        self.top_bar()

        # canvas_area: parte central da tela onde o mapa é desenhado
        self.canvas_area()

        # desenhar_mapa: função para desenhar o mapa emocional no centro da tela
        self.desenhar_mapa()

        # botao_voltar: botão para retornar à tela inicial
        self.botao_voltar()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    '''
        Configurações para criar a tela.
    '''
    def configuracoes(self):
        self.geometry("900x700")
        self.title("Mapa do Humor")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set()

    '''
        Criação da barra de navegação horizontal superior.
    '''
    def top_bar(self):
        # Frame topo, sem cor fixa, herdando tema default
        top = ctk.CTkFrame(self, height=70)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        # Grid 3 colunas: botão | mês | botão
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=6)
        top.grid_columnconfigure(2, weight=1)

        # Botão mês anterior
        bt_prev = ctk.CTkButton(top, text="◀", width=60, height=40, font=("Arial", 18, "bold"),
                               command=self.mes_anterior)
        bt_prev.grid(row=0, column=0, padx=10, pady=15, sticky="e")

        # Label mês centralizado
        self.lb_mes = ctk.CTkLabel(top, text=self.MESES_PT[self.mes-1], font=("Century Gothic Bold", 26))
        self.lb_mes.grid(row=0, column=1, pady=10)

        # Botão próximo mês
        bt_next = ctk.CTkButton(top, text="▶", width=60, height=40, font=("Arial", 18, "bold"),
                               command=self.proximo_mes)
        bt_next.grid(row=0, column=2, padx=10, pady=15, sticky="w")

    def canvas_area(self):
        # Frame container padrão (sem cor definida)
        self.frame_mapa = ctk.CTkFrame(self)
        self.frame_mapa.pack(expand=True, fill="both", padx=20, pady=20)

        # Canvas herdando cor padrão do parent, adaptável ao dark mode
        cor_fundo = self.cget("bg")
        self.canvas = Canvas(self.frame_mapa, width=650, height=450, bg=cor_fundo, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

    def buscar_humor_do_dia(self, dia):
        self.db.conecta_db()
        data = f"{self.ano}-{self.mes:02d}-{dia:02d}"
        self.db.cursor.execute(
            "SELECT Humor FROM Questionarios WHERE Username = ? AND Data = ?",
            (self.username, data)
        )
        r = self.db.cursor.fetchone()
        self.db.desconecta_db()
        return r[0] if r else None

    '''
        Desenhando mapa no centro da tela (canvas).
    '''
    def desenhar_mapa(self):
        self.canvas.delete("all")

        _, total_dias = calendar.monthrange(self.ano, self.mes)
        cols = 10
        size = 32  # bolinhas menores, conforme você pediu
        gap = 14

        # cálculo de centralização do grid dentro do canvas
        largura_grid = cols * (size + gap) - gap
        altura_grid = ((total_dias-1)//cols + 1) * (size + gap) - gap

        inicio_x = (650 - largura_grid) / 2
        inicio_y = (450 - altura_grid) / 2

        for i, dia in enumerate(range(1, total_dias + 1)):
            col = i % cols
            row = i // cols

            x = inicio_x + col * (size + gap)
            y = inicio_y + row * (size + gap)

            humor = self.buscar_humor_do_dia(dia)
            cor = self.CORES.get(humor, "#cccccc")

            bola = self.canvas.create_oval(x, y, x+size, y+size, fill=cor, outline="#444")
            self.canvas.create_text(x+size/2, y+size/2, text=str(dia), font=("Arial", 10, "bold"))

            # adiciona área clicável
            self.canvas.tag_bind(bola, "<Button-1>", lambda e, d=dia: self.abrir_questionario_dia(d))

    '''
        Navegação para o próximo mês do calendário.
    '''
    def proximo_mes(self):
        if self.mes < 12:
            self.mes += 1
            self.lb_mes.configure(text=self.MESES_PT[self.mes-1])
            self.desenhar_mapa()

    '''
        Navegação para o mês anterior do calendário.
    '''
    def mes_anterior(self):
        if self.mes > 1:
            self.mes -= 1
            self.lb_mes.configure(text=self.MESES_PT[self.mes-1])
            self.desenhar_mapa()

    '''
        Criação do botão para retornar ao menu inicial.
    '''
    def botao_voltar(self):
        self.btn_voltar = ctk.CTkButton(
            self,
            width=250,
            height=45,
            text="VOLTAR AO MENU",
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            command=self.voltar_menu
        )
        self.btn_voltar.pack(side="bottom", pady=20)

    '''
        Fechar a janela atual quando retornar ao menu principal.
    '''
    def voltar_menu(self):
        self.destroy()
