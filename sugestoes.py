import customtkinter as ctk
from database import Database
from datetime import datetime, timedelta
import random

class SugestoesApp(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.db = Database()
        
        self.configuracoes_janela()
        self.analisar_dados()
        self.criar_interface()
        
    def configuracoes_janela(self):
        self.geometry("900x700")
        self.title("Humoro - Sugestões de Bem-Estar")
        self.resizable(False, False)
        
        # Faz a janela aparecer na frente
        self.lift()
        self.focus_force()
        self.grab_set()
        
    def analisar_dados(self):
        """Analisa os últimos 7 dias de questionários do usuário"""
        questionarios = self.db.listar_questionarios(self.username)
        
        # Pegar últimos 7 dias
        data_limite = datetime.now() - timedelta(days=7)
        
        self.lazer_scores = []
        self.social_scores = []
        
        for q in questionarios:
            data_str = q[0]
            try:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d")
                
                if data_obj >= data_limite:
                    lazer = q[5]  # Índice 5 = Lazer
                    social = q[4]  # Índice 4 = Social
                    
                    # Converter para scores numéricos
                    self.lazer_scores.append(self.converter_para_score(lazer))
                    self.social_scores.append(self.converter_para_score(social))
            except:
                continue
        
        # Calcular médias
        self.media_lazer = sum(self.lazer_scores) / len(self.lazer_scores) if self.lazer_scores else 3
        self.media_social = sum(self.social_scores) / len(self.social_scores) if self.social_scores else 3
        
    def converter_para_score(self, opcao):
        """Converte opção em score numérico (1-5)"""
        conversao = {
            "Péssimo": 1,
            "Ruim": 2,
            "Mediano": 3,
            "Bom": 4,
            "Excelente": 5
        }
        return conversao.get(opcao, 3)
    
    def criar_interface(self):
        # Título
        self.lb_titulo = ctk.CTkLabel(
            self,
            text="Sugestões de Bem-Estar",
            font=("Century Gothic Bold", 32)
        )
        self.lb_titulo.pack(pady=20)
        
        # Subtítulo
        self.lb_subtitulo = ctk.CTkLabel(
            self,
            text="Baseado nos seus últimos 7 dias",
            font=("Century Gothic", 14),
            text_color="gray"
        )
        self.lb_subtitulo.pack(pady=(0, 20))
        
        # Frame principal com scroll
        self.frame_scroll = ctk.CTkScrollableFrame(self, width=850, height=450)
        self.frame_scroll.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Análise de Lazer
        self.criar_secao_lazer()
        
        # Espaçador
        ctk.CTkLabel(self.frame_scroll, text="", height=20).pack()
        
        # Análise Social
        self.criar_secao_social()
        
        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="← Voltar ao Menu",
            font=("Century Gothic Bold", 14),
            width=300,
            height=45,
            command=self.destroy
        )
        self.btn_voltar.pack(pady=15)
        
    def criar_secao_lazer(self):
        """Cria seção de análise e sugestões de lazer"""
        # Frame da seção
        frame_lazer = ctk.CTkFrame(self.frame_scroll, corner_radius=15)
        frame_lazer.pack(pady=10, padx=10, fill="x")
        
        # Título da seção
        lb_titulo_lazer = ctk.CTkLabel(
            frame_lazer,
            text="🎮 Lazer e Entretenimento",
            font=("Century Gothic Bold", 24),
            anchor="w"
        )
        lb_titulo_lazer.pack(pady=15, padx=20, anchor="w")
        
        # Status atual
        status_lazer = self.obter_status(self.media_lazer)
        cor_lazer = self.obter_cor(self.media_lazer)
        
        frame_status = ctk.CTkFrame(frame_lazer, fg_color=cor_lazer, corner_radius=10)
        frame_status.pack(pady=10, padx=20, fill="x")
        
        lb_status = ctk.CTkLabel(
            frame_status,
            text=f"Status atual: {status_lazer}",
            font=("Century Gothic Bold", 16),
            text_color="white"
        )
        lb_status.pack(pady=10)
        
        # Sugestões
        lb_sugestoes_titulo = ctk.CTkLabel(
            frame_lazer,
            text="📋 Sugestões para melhorar:",
            font=("Century Gothic Bold", 18),
            anchor="w"
        )
        lb_sugestoes_titulo.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Lista de sugestões baseada no score
        sugestoes_lazer = self.obter_sugestoes_lazer(self.media_lazer)
        
        for sugestao in sugestoes_lazer:
            self.criar_card_sugestao(frame_lazer, sugestao)
    
    def criar_secao_social(self):
        """Cria seção de análise e sugestões sociais"""
        # Frame da seção
        frame_social = ctk.CTkFrame(self.frame_scroll, corner_radius=15)
        frame_social.pack(pady=10, padx=10, fill="x")
        
        # Título da seção
        lb_titulo_social = ctk.CTkLabel(
            frame_social,
            text="👥 Vida Social",
            font=("Century Gothic Bold", 24),
            anchor="w"
        )
        lb_titulo_social.pack(pady=15, padx=20, anchor="w")
        
        # Status atual
        status_social = self.obter_status(self.media_social)
        cor_social = self.obter_cor(self.media_social)
        
        frame_status = ctk.CTkFrame(frame_social, fg_color=cor_social, corner_radius=10)
        frame_status.pack(pady=10, padx=20, fill="x")
        
        lb_status = ctk.CTkLabel(
            frame_status,
            text=f"Status atual: {status_social}",
            font=("Century Gothic Bold", 16),
            text_color="white"
        )
        lb_status.pack(pady=10)
        
        # Sugestões
        lb_sugestoes_titulo = ctk.CTkLabel(
            frame_social,
            text="📋 Sugestões para melhorar:",
            font=("Century Gothic Bold", 18),
            anchor="w"
        )
        lb_sugestoes_titulo.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Lista de sugestões
        sugestoes_social = self.obter_sugestoes_social(self.media_social)
        
        for sugestao in sugestoes_social:
            self.criar_card_sugestao(frame_social, sugestao)
    
    def criar_card_sugestao(self, parent, sugestao):
        """Cria um card visual para cada sugestão"""
        frame_card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#2b2b2b")
        frame_card.pack(pady=8, padx=20, fill="x")
        
        # Ícone e título
        frame_header = ctk.CTkFrame(frame_card, fg_color="transparent")
        frame_header.pack(fill="x", padx=15, pady=(10, 5))
        
        lb_icone = ctk.CTkLabel(
            frame_header,
            text=sugestao["icone"],
            font=("Arial", 24)
        )
        lb_icone.pack(side="left", padx=(0, 10))
        
        lb_titulo = ctk.CTkLabel(
            frame_header,
            text=sugestao["titulo"],
            font=("Century Gothic Bold", 16),
            anchor="w"
        )
        lb_titulo.pack(side="left", fill="x", expand=True)
        
        # Descrição
        lb_desc = ctk.CTkLabel(
            frame_card,
            text=sugestao["descricao"],
            font=("Century Gothic", 13),
            anchor="w",
            wraplength=750,
            justify="left"
        )
        lb_desc.pack(padx=15, pady=(0, 10), anchor="w")
    
    def obter_status(self, media):
        """Retorna o status baseado na média"""
        if media >= 4.5:
            return "Excelente! Continue assim!"
        elif media >= 3.5:
            return "Bom, mas pode melhorar"
        elif media >= 2.5:
            return "Mediano, precisa de atenção"
        elif media >= 1.5:
            return "Ruim, precisa melhorar urgente"
        else:
            return "Péssimo, atenção necessária!"
    
    def obter_cor(self, media):
        """Retorna a cor baseada na média"""
        if media >= 4.5:
            return "#008000"  # Verde
        elif media >= 3.5:
            return "#90EE90"  # Verde claro
        elif media >= 2.5:
            return "#FFD700"  # Amarelo
        elif media >= 1.5:
            return "#FF8C00"  # Laranja
        else:
            return "#FF0000"  # Vermelho
    
    def obter_sugestoes_lazer(self, media):
        """Retorna sugestões de lazer baseadas na média"""
        todas_sugestoes = [
            {
                "icone": "🎮",
                "titulo": "Jogos e Entretenimento Digital",
                "descricao": "Reserve 30 minutos por dia para jogar seus jogos favoritos ou explorar novos hobbies digitais. Isso ajuda a relaxar e se divertir."
            },
            {
                "icone": "📚",
                "titulo": "Leitura Recreativa",
                "descricao": "Dedique 20-30 minutos para ler um livro, revista ou artigos sobre assuntos que você gosta. A leitura é ótima para relaxar a mente."
            },
            {
                "icone": "🎬",
                "titulo": "Cinema e Séries",
                "descricao": "Assista a filmes ou séries que você estava querendo ver. Criar uma lista de favoritos ajuda a ter opções prontas para momentos livres."
            },
            {
                "icone": "🎨",
                "titulo": "Hobbies Criativos",
                "descricao": "Explore atividades criativas como desenho, pintura, artesanato, música ou fotografia. Expressão artística ajuda no bem-estar mental."
            },
            {
                "icone": "🏃",
                "titulo": "Atividades Físicas Divertidas",
                "descricao": "Pratique esportes, dança, caminhadas ou qualquer atividade física prazerosa. Exercício libera endorfina e melhora o humor."
            },
            {
                "icone": "🌳",
                "titulo": "Contato com a Natureza",
                "descricao": "Passe tempo ao ar livre em parques, praias ou trilhas. O contato com a natureza reduz estresse e melhora o bem-estar."
            },
            {
                "icone": "🎵",
                "titulo": "Música e Podcasts",
                "descricao": "Ouça suas músicas favoritas ou descubra novos artistas e podcasts. A música tem poder terapêutico e relaxante."
            },
            {
                "icone": "🍳",
                "titulo": "Culinária Recreativa",
                "descricao": "Experimente novas receitas ou prepare seus pratos favoritos. Cozinhar pode ser terapêutico e divertido."
            }
        ]
        
        # Quanto menor a média, mais sugestões
        if media < 2.5:
            num_sugestoes = 6
        elif media < 3.5:
            num_sugestoes = 4
        else:
            num_sugestoes = 3
        
        return random.sample(todas_sugestoes, min(num_sugestoes, len(todas_sugestoes)))
    
    def obter_sugestoes_social(self, media):
        """Retorna sugestões sociais baseadas na média"""
        todas_sugestoes = [
            {
                "icone": "☕",
                "titulo": "Encontros Casuais",
                "descricao": "Marque um café ou lanche com amigos próximos. Conversas descontraídas fortalecem laços e melhoram o humor."
            },
            {
                "icone": "👨‍👩‍👧‍👦",
                "titulo": "Tempo em Família",
                "descricao": "Dedique momentos de qualidade com familiares. Jogos de tabuleiro, refeições juntos ou simples conversas fazem diferença."
            },
            {
                "icone": "🎉",
                "titulo": "Eventos Sociais",
                "descricao": "Participe de festas, eventos culturais ou reuniões. Sair da rotina e socializar traz energia positiva."
            },
            {
                "icone": "🏋️",
                "titulo": "Atividades em Grupo",
                "descricao": "Participe de aulas coletivas, grupos de esporte ou clubes de interesse. Compartilhar hobbies cria conexões."
            },
            {
                "icone": "💬",
                "titulo": "Conversas Significativas",
                "descricao": "Tenha conversas profundas com pessoas queridas. Compartilhar sentimentos e experiências fortalece relacionamentos."
            },
            {
                "icone": "🤝",
                "titulo": "Voluntariado",
                "descricao": "Envolva-se em causas sociais ou trabalho voluntário. Ajudar outros traz satisfação e amplia sua rede social."
            },
            {
                "icone": "📱",
                "titulo": "Reconectar-se",
                "descricao": "Entre em contato com amigos que você não fala há tempo. Uma mensagem simples pode reacender amizades importantes."
            },
            {
                "icone": "🎓",
                "titulo": "Grupos de Estudo ou Aprendizado",
                "descricao": "Participe de workshops, cursos ou grupos de estudo. Aprender em grupo cria vínculos e expande horizontes."
            },
            {
                "icone": "🎮",
                "titulo": "Gaming Social",
                "descricao": "Jogue online com amigos ou participe de comunidades de jogos. É uma forma moderna e divertida de socializar."
            },
            {
                "icone": "🍽️",
                "titulo": "Refeições Compartilhadas",
                "descricao": "Organize jantares, almoços ou potlucks com amigos. Comer junto é uma forma ancestral de fortalecer laços."
            }
        ]
        
        # Quanto menor a média, mais sugestões
        if media < 2.5:
            num_sugestoes = 6
        elif media < 3.5:
            num_sugestoes = 4
        else:
            num_sugestoes = 3
        
        return random.sample(todas_sugestoes, min(num_sugestoes, len(todas_sugestoes)))