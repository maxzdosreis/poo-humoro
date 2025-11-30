import customtkinter as ctk
from tkinter import messagebox
from database import Database
from datetime import datetime

# classe que iria criar e manipular a tela de questionário
# utilizado CTkTopLevel, pois ele cria uma janela secundária (dessa maneira o programa não fecha quando fecham ela)
class Questionario(ctk.CTkToplevel):
    # método init para instanciar os métodos e variáveis
    def __init__(self, parent, username):
        super().__init__(parent)
        
        self.parent = parent
        self.username = username
        self.db = Database()

        # Variáveis de controle        
        self.modo_edicao = False
        self.questionario_id = None
        
        self.configuracoes_janela()
        self.verificar_questionario_existente()
        self.criar_questionario()
        
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
    # método que define as configurações da janela de questionário 
    def configuracoes_janela(self):
        self.geometry("950x750")
        self.title("Humoro - Questionário Diário")
        self.resizable(False, False)
        
        # Faz a janela aparecer na frente da tela de menu
        self.lift() # Traz a janela para frente
        self.focus_force() # Fora o foco nesse janela
        self.grab_set() # Torna a janela modal (fazendo com que o usuário não consiga interagir com a tela de menu enquanto a janela está aberta)
    
    def verificar_questionario_existente(self):
        """
        Verifica se o usuário já responde o questionário hoje.
        Se sim, carrega os dados para edição.
        """
        ja_respondeu, dados = self.db.verificar_questionario_hoje(self.username)
        
        if ja_respondeu:
            self.modo_edicao = True
            self.questionario_id = dados['id']
            self.dados_existentes = dados
            
            messagebox.showinfo(
                "Questionário já respondido",
                f"Você já respondeu o questionário hoje às {dados['hora']}.\n\n"
                "Você pode editar suas respostas se desejar."
            )
       
    # método que cria o questionário 
    def criar_questionario(self):
        # Título principal
        titulo_texto = "Editar Questionário" if self.modo_edicao else "Questionário Diário"
        self.lb_title = ctk.CTkLabel(
            self,
            text=titulo_texto,
            font=("Century Gothic Bold", 28)
        )
        self.lb_title.pack(pady=20)  
        
        # Subtítulo com nome do usuário
        if self.modo_edicao:
            subtitulo = f"Olá, {self.username}! Edite suas respostas de hoje:"
        else: 
            subtitulo = f"Olá, {self.username}! Como você está se sentindo hoje?"
        
        self.lb_subtitle = ctk.CTkLabel(
            self,
            text=subtitulo,
            font=("Century Gothic Bold", 14)
        )
        self.lb_subtitle.pack(pady=5)
        
        # Frame principal scrollable (cria um frame com barra de rolagem automática)
        self.frame_scroll = ctk.CTkScrollableFrame(self, width=900, height=500)
        self.frame_scroll.pack(pady=10, padx=10)
        
        for i in range(5):
            self.frame_scroll.grid_columnconfigure(i, weight=1, uniform="opcoes")
        
        '''
         - Variáveis para armazenar as respostas
         - StringVar() é uma variável especial do Tkinter que armazena valores dinâmicos
         - inicia com o valor vazio (sem nenhuma opção selecionada)
        '''
        if self.modo_edicao:
            self.var_humor = ctk.StringVar(value=self.dados_existentes['humor'])
            self.var_sono = ctk.StringVar(value=self.dados_existentes['sono'])
            self.var_social = ctk.StringVar(value=self.dados_existentes['social'])
            self.var_lazer = ctk.StringVar(value=self.dados_existentes['lazer'])
        else:
            self.var_humor = ctk.StringVar(value="")
            self.var_sono = ctk.StringVar(value="")
            self.var_social = ctk.StringVar(value="")
            self.var_lazer = ctk.StringVar(value="")
        
        # opções de resposta
        opcoes = ["Excelente", "Bom", "Mediano", "Ruim", "Péssimo"]
        
        # -- Humor --
        self.criar_pergunta(
            frame=self.frame_scroll,
            titulo="Como está o seu HUMOR hoje?",
            variavel=self.var_humor,
            opcoes=opcoes,
            row_start=0
        )
        
        # Linha separadora que é criada atráves do método criar_separador()
        self.criar_separador(self.frame_scroll, row=2)
        
        # -- Sono --
        self.criar_pergunta(
            frame=self.frame_scroll,
            titulo="Como foi a qualidade do seu SONO?",
            variavel=self.var_sono,
            opcoes=opcoes,
            row_start=3
        )
        
        # Linha separadora que é criada atráves do método criar_separador()
        self.criar_separador(self.frame_scroll, row=5)
        
        # -- Social --
        self.criar_pergunta(
            frame=self.frame_scroll,
            titulo="Como foram suas interações SOCIAIS?",
            variavel=self.var_social,
            opcoes=opcoes,
            row_start=6
        )
        
        # Linha separadora que é criada atráves do método criar_separador()
        self.criar_separador(self.frame_scroll, row=8)
        
        # -- Lazer --
        self.criar_pergunta(
            frame=self.frame_scroll,
            titulo="Como aproveitou seu tempo de LAZER?",
            variavel=self.var_lazer,
            opcoes=opcoes,
            row_start=9
        )
        
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=20)
        
        # Botão de salvar (texto muda dependendo do modo)
        texto_botao = "ATUALIZAR RESPOSTAS" if self.modo_edicao else "SALVAR RESPOSTAS"
        self.btn_salvar = ctk.CTkButton(
            self.frame_botoes,
            width=250,
            height=45,
            text=texto_botao,
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            fg_color="green",
            hover_color="#050",
            command=self.salvar_respostas
        )
        self.btn_salvar.grid(row=0, column=0, padx=10)
        
        # Botão de salvar
        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            width=250,
            height=45,
            text="VOLTAR AO MENU",
            font=("Century Gothic Bold", 14),
            corner_radius=15,
            fg_color="#444",
            hover_color="#333",
            command=self.fechar
        )
        self.btn_voltar.grid(row=0, column=1, padx=10)
        
    # Método reutilizável para criar as perguntas
    def criar_pergunta(self, frame, titulo, variavel, opcoes, row_start):
        """Cria uma pergunta com radio buttons"""
        # Título da pergunta
        lb_pergunta = ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Century Gothic Bold", 16)
        )
        lb_pergunta.grid(row=row_start, column=0, columnspan=5, pady=(20,15), padx=20)
        
        # Frame interno para centralizar os radio buttons
        frame_opcoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_opcoes.grid(row=row_start + 1, column=0, columnspan=5, pady=(0,10))
        
        # radio buttons para as opções
        for i, opcao in enumerate(opcoes):
            rb = ctk.CTkRadioButton(
                frame_opcoes,
                text=opcao,
                variable=variavel,
                value=opcao,
                font=("Century Gothic Bold", 14),
                corner_radius=10
            )
            rb.grid(row=0, column=i, padx=12, pady=5)
            
    # método que cria as linhas separadoras do questionário
    def criar_separador(self, frame, row):
        """Cria uma linha separadora visual"""
        separador = ctk.CTkFrame(frame, height=2, fg_color="gray")
        separador.grid(row=row, column=0, columnspan=5, sticky="ew", pady=15, padx=20)
         
    # método responsável por salvar as respostas dentro do banco de dados   
    def salvar_respostas(self):
        """Salva as respostas no banco de dados (novo ou atualização)"""
        # Validar se todas as perguntas forem respondidas
        if not all([
            self.var_humor.get(),
            self.var_sono.get(),
            self.var_social.get(),
            self.var_lazer.get() 
        ]):
            messagebox.showerror(
                "Erro",
                "Por favor, responda todas as perguntas antes de salvar!"
            )
            return
        
        # Obtém as datas e horas atuais (strftime formata a data/hora em string)
        data_atual = datetime.now().strftime("%Y-%m-%d")
        hora_atual = datetime.now().strftime("%H:%M:%S")
        
        if self.modo_edicao:
            # Atualiza o questionário existente
            sucesso, mensagem = self.db.atualizar_questionario(
                questionario_id = self.questionario_id,
                humor = self.var_humor.get(),
                sono = self.var_sono.get(),
                social = self.var_social.get(),
                lazer = self.var_lazer.get()
            )
            """
            em caso de sucesso, o sistema retorna uma messagebox, dizendo que foi um sucesso, e depois fecha
            """
            if sucesso:
                messagebox.showinfo(
                    "Sucesso!",
                    f"Questionário atualizado com sucesso!\n\nHora: {hora_atual}"
                )
                self.fechar()
                """
                em caso de falha, o sistema retorna uma messagebox, dizendo que ocorreu um erro
                """
            else:
                messagebox.showerror("Erro", mensagem)
        else:
            # Cria um novo questionário
            sucesso, mensagem = self.db.salvar_questionario(
                username=self.username,
                data=data_atual,
                hora=hora_atual,
                humor=self.var_humor.get(),
                sono=self.var_sono.get(),
                social=self.var_social.get(),
                lazer=self.var_lazer.get()
            )
            
            if sucesso:
                messagebox.showinfo(
                    "Sucesso!",
                    f"Respostas salvas com sucesso!\n\nData: {data_atual}\nHora: {hora_atual}"
                )
                # Atualiza para modo edição
                self.modo_edicao = True
                self.fechar()
            else:
                messagebox.showerror("Erro", mensagem)
            
    # método para limpar as respostas preenchidas no questionário
    def limpar_respostas(self):
        """Limpa todas as respostas selecionadas"""
        self.var_humor.set("")
        self.var_sono.set("")
        self.var_social.set("")
        self.var_lazer.set("")
        
    # método para fechar a janela do questionário
    def fechar(self):
        """Fecha a janela do questionário"""
        self.destroy()