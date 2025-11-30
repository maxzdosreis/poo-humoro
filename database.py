import sqlite3
from datetime import datetime
import bcrypt

class Database:
    def __init__(self, db_name="humoro.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def conecta_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado!")
        return self.conn, self.cursor
    
    def desconecta_db(self):
        if self.conn:
            self.conn.close()
            print("Banco de dados desconectado!")
                   
    def cria_tabelas(self):
        self.conecta_db()

        # Tabela Usuarios
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_senha TEXT NOT NULL
            );
        """)
  
        # Tabela Humores
        #self.cursor.execute("""
            #CREATE TABLE IF NOT EXISTS Humores(
                #Id INTEGER PRIMARY KEY AUTOINCREMENT,
                #Username TEXT NOT NULL,
                #Humor TEXT NOT NULL,
                #Data TEXT NOT NULL
            #);
        #""")
    
        # Tabela de Questionários
        """
        Query que cria a tabela no banco de dados
        
        Colunas que serão criadas:
         - id: identificador do questionário (PRIMARY KEY e AUTOINCREMENT)
         - username: nome do usuário que está respondendo (FOREIGN KEY -> tabela Usuarios)
         - data: data no formato YYYY-MM-DD (ex: 2025-11-25)
         - hora: hora no formato HH:MM:SS (ex: 08:25:33)
         - humor, sono, social, lazer: respostas selecionadas 
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Questionarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Data TEXT NOT NULL,
                Hora TEXT NOT NULL,
                Humor TEXT NOT NULL,
                Sono TEXT NOT NULL,
                Social TEXT NOT NULL,
                Lazer TEXT NOT NULL,
                FOREIGN KEY (Username) REFERENCES Usuarios(Username)    
            );               
        """)
        
        self.conn.commit()
        print("Tabelas criadas com sucesso!")
        self.desconecta_db()
        
    def criptografar_senha(self, senha):
        """
        Criptografa uma senha usando bcrypt
        
        Parâmetros:
         - senha: senha em texto (string)
         
        Retorna:
         - senha_hash: senha criptografada (bytes)
        """
        # Gera um salt aleatório e criptografa a senha
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return senha_hash
    
    def verificar_senha(self, senha_digitada, senha_hash):
        """
        Verifica se a senha digitada corresponde ao hash armazenado
        
        Parâmetros:
         - senha_digitada: senha em texto plano (string)
         - senha_hash: hash armazenado no bano (bytes ou string)
         
        Retorna:
         - True se a senha está correta
         - False se a senha está incorreta
        """
        if isinstance(senha_hash, str):
            senha_hash = senha_hash.encode('utf-8')
            
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash)
        
    def cadastrar_usuario(self, username, email, senha, confirma_senha):
        """
        Cadastra um novo usuário com senha criptografada
        """
        self.conecta_db()
        try:
            # Criptografa as senhas antes de salvar
            senha_hash = self.criptografar_senha(senha)
            confirma_senha_hash = self.criptografar_senha(confirma_senha)
            
            self.cursor.execute("""
                INSERT INTO Usuarios (Username, Email, Senha, Confirma_senha)
                VALUES (?,?,?,?)                
                """, (username, email, senha_hash, confirma_senha_hash))
            
            self.conn.commit()
            self.desconecta_db()
            return True, "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError:
            self.desconecta_db()
            return False, "Usuário ou email já cadastrado!"
        except Exception as e:
            self.desconecta_db()
            return False, f"Erro ao cadastrar: {str(e)}"
        
    def verificar_login(self, username, senha):
        """
        Verifica login comparando senha criptografada
        """
        self.conecta_db()
        try:
            # Busca APENAS a senha do usuário
            self.cursor.execute("""
                SELECT Senha FROM Usuarios
                WHERE Username = ?               
            """, (username,))
            
            resultado = self.cursor.fetchone()
            self.desconecta_db()
            
            if resultado:
                senha_hash = resultado[0]
                
                # Verifica se a senha digitada corresponde ao hash
                if self.verificar_senha(senha, senha_hash):
                    return True, "Login realizado com sucesso!"
                else:
                    return False, "Usuário ou senha incorretos!"
            else:
                return False, "Usuário ou senha incorretos!"
        except Exception as e:
            self.desconecta_db()
            return False, f"Erro ao fazer login: {str(e)}"
        
    def salvar_questionario(self, username, data, hora, humor, sono, social, lazer):
        """
        Salva um questionário no banco de dados
        
        Parâmetros:
         - username: nome do usuário que está respondendo
         - data: data no formato YYYY-MM-DD (ex: 2025-11-25)
         - hora: hora no formato HH:MM:SS (ex: 08:25:33)
         - humor, sono, social, lazer: respostas selecionadas
        
        Retorna:
         - (True, mensagem) se salvou com sucesso
         - (False, mensagem) se ocorreu algum erro
        """
        self.conecta_db()
        try:
            # Query para salvar questionario no banco de dados
            self.cursor.execute("""
                INSERT INTO Questionarios (Username, Data, Hora, Humor, Sono, Social, Lazer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, data, hora, humor, sono, social, lazer))
            
            self.conn.commit()
            self.desconecta_db()
            return True, "Questionário salvo com sucesso!"
        except Exception as e:
            self.desconecta_db()
            return False, f"Erro ao salvar questionário: {str(e)}"
        
    # método que verifica se o questionário já foi respondido hoje
    def verificar_questionario_hoje(self, username):
        """
        Verifica se o usuário já respondeu o questionário hoje
        
        Retorna:
         - (True, dados_questionario) se já respondeu
         - (False, None) se ainda não respondeu
        """
        self.conecta_db()
        try:
            # verifica a data de hoje
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            
            # consulta no banco de dados se determinado usuário tem algum questionário criado na current_date
            self.cursor.execute("""
                SELECT Id, Humor, Sono, Social, Lazer, Hora
                FROM Questionarios
                WHERE Username = ? AND Data = ?                
            """, (username, data_hoje))
            
            resultado = self.cursor.fetchone()
            self.desconecta_db()
            
            if resultado:
                return True, {
                    'id': resultado[0],
                    'humor': resultado[1],
                    'sono': resultado[2],
                    'social': resultado[3],
                    'lazer': resultado[4],
                    'hora': resultado[5]
                }
            else:
                return False, None
        except Exception as e:
            self.desconecta_db()
            print(f"Erro ao verificar questionário: {str(e)}")
            return False, None
        
    def atualizar_questionario(self, questionario_id, humor, sono, social, lazer):
        """
        Atualiza um questionário existente
        
        Parâmetros:
         - questionario_id: ID do questionário a ser atualizado
         - humor, sono, social, lazer: novas respostas
         
        Retorna:
         - (True, mensagem) se atualizou com sucesso 
         - (False, None) se ocorreu erro
        """
        self.conecta_db()
        try:
            # Atualiza a a hora para registrar quando foi editado
            hora_atual = datetime.now().strftime("%H:%M:%S")
            
            # Atualiza o questionário no banco de dados
            self.cursor.execute("""
                UPDATE Questionarios
                SET Humor = ?, Sono = ?, Social = ?, Lazer = ?, Hora = ?
                WHERE Id = ?                
            """, (humor, sono, social, lazer, hora_atual, questionario_id))
            
            self.conn.commit()
            self.desconecta_db()
            
            return True, "Questionário atualizado com sucesso!"
        except Exception as e:
            self.desconecta_db()
            return False, f"Erro ao atualizar questionário: {str(e)}"
        
    def listar_questionarios(self,username):
        """
        Lista todos os questionários de um usuário ordenados por data
        
        Retorna:
         - Lista de tuplas (Data, Hora, Humor, Sono, Social, Lazer) 
        """
        self.conecta_db()
        try:
            self.cursor.execute("""
                SELECT Data, Hora, Humor, Sono, Social, Lazer
                FROM Questionarios
                WHERE Username = ?
                ORDER BY Data DESC, Hora DESC
            """, (username,))
            
            resultado = self.cursor.fetchall()
            self.desconecta_db()
            return resultado
        except Exception as e:
            self.desconecta_db()
            print(f"Erro ao listar questionários: {str(e)}")
            return []