import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime
from database import Database

class CalendarioApp(ctk.CTkToplevel):
    
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.db = Database()
        
        self.configuracoes_janela()
        self.criar_interface()
        self.carregar_humores()
    
    def configuracoes_janela(self):
        self.geometry("800x700")
        self.title("Humoro - Calendário de Sono")
        self.resizable(False, False)
        
        # Faz a janela aparecer na frente da tela de menu
        self.lift() # Traz a janela para frente
        self.focus_force() # Fora o foco nesse janela
        self.grab_set() # Torna a janela modal (fazendo com que o usuário não consiga interagir com a tela de menu enquanto a janela está aberta)
        
    def criar_interface(self):
        # Título
        self.lb_titulo = ctk.CTkLabel(
            self,
            text="Calendário de Sono",
            font=("Century Gothic Bold", 28)
        )
        self.lb_titulo.pack(pady=20)
        
        # Frame para o calendário
        self.frame_calendario = ctk.CTkFrame(self, width=750, height=400)
        self.frame_calendario.pack(pady=10)
        self.frame_calendario.pack_propagate(False)
        
        # Calendário
        self.cal = Calendar(
            self.frame_calendario,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            background='#2b2b2b',
            foreground='white',
            bordercolor='#2b2b2b',
            headersbackground='#1f538d',
            headersforeground='white',
            selectbackground='#1f538d',
            selectforeground='white',
            normalbackground='#2b2b2b',
            normalforeground='white',
            weekendbackground='#2b2b2b',
            weekendforeground='white',
            othermonthforeground='gray',
            othermonthbackground='#2b2b2b',
            othermonthweforeground='gray',
            othermonthwebackground='#2b2b2b'
        )
        self.cal.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.frame_legenda = ctk.CTkFrame(self, width=750)
        self.frame_legenda.pack(pady=10, padx=20, fill='x')
        
        self.lb_legenda_titulo = ctk.CTkLabel(
            self.frame_legenda,
            text="Legenda de Qualidade do Sono:",
            font=("Century Gothic Bold", 16)
        )
        self.lb_legenda_titulo.pack(pady=10)
        
        # Frame com grid para a legenda
        self.frame_cores = ctk.CTkFrame(self.frame_legenda, fg_color="transparent")
        self.frame_cores.pack(pady=5)
        
        # Dicionário de qualidade do sono e suas cores (5 opções)
        self.sleep_colors = {
            "Excelente": "#008000",    # Verde
            "Bom": "#90EE90",          # Verde claro
            "Mediano": "#FFD700",      # Dourado/Amarelo
            "Ruim": "#FF8C00",         # Laranja
            "Péssimo": "#FF0000"       # Vermelho
        }
        
        # Criar legenda horizontal (5 opções)
        col = 0
        for sono, cor in self.sleep_colors.items():
            frame_item = ctk.CTkFrame(self.frame_cores, fg_color="transparent")
            frame_item.grid(row=0, column=col, padx=8, pady=5)
            
            # Quadradinho colorido
            quadrado = ctk.CTkLabel(
                frame_item,
                text="  ",
                fg_color=cor,
                width=20,
                height=20,
                corner_radius=3
            )
            quadrado.pack(side='left', padx=(0, 5))
            
            # Texto
            texto = ctk.CTkLabel(
                frame_item,
                text=sono,
                font=("Century Gothic", 12)
            )
            texto.pack(side='left')
            
            col += 1
            
        # Botão de atualizar
        self.btn_atualizar = ctk.CTkButton(
            self,
            text="Atualizar Calendário",
            font=("Century Gothic Bold", 14),
            width=200,
            command=self.carregar_humores
        )
        self.btn_atualizar.pack(pady=10)
        
        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="← Voltar ao Menu",
            font=("Century Gothic Bold", 14),
            width=200,
            command=self.destroy
        )
        self.btn_voltar.pack(pady=5)

    def carregar_humores(self):
        """Carrega os humores do banco de dados e marca no calendário"""
        # Limpar eventos anteriores
        for tag in self.cal.get_calevents():
            self.cal.calevent_remove(tag)
            
        # Buscar questionários do usuário
        questionarios = self.db.listar_questionarios(self.username)
        
        # Adicionar eventos no calendário
        for questionario in questionarios:
            data_str = questionario[0]  # Data no formato YYYY-MM-DD
            sono = questionario[3]      # Sono
            
            # Converter data de string para objeto datetime
            try:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
                
                # Pegar a cor do humor
                cor = self.sleep_colors.get(sono, "#808080")
                
                # Criar evento no calendário
                self.cal.calevent_create(
                    data_obj,
                    sono,
                    tags=sono
                )
                
                # Configurar a cor do evento
                self.cal.tag_config(
                    sono,
                    background=cor,
                    foreground='white'
                )
            except ValueError as e:
                print(f"Erro ao processar data {data_str}: {e}")
                continue