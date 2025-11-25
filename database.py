import sqlite3

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
        
        # Tabela de usuários
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
               Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Username TEXT NOT NULL,
               Email TEXT NOT NULL,
               Senha TEXT NOT NULL,
               Confirma_senha TEXT NOT NULL
           );                 
        """)
        
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
        
    def cadastrar_usuario(self, username, email, senha, confirma_senha):
        self.conecta_db()
        try:
            self.cursor.execute("""
                INSERT INTO Usuarios (Username, Email, Senha, Confirma_senha)
                VALUES (?,?,?,?)                
                """, (username, email, senha, confirma_senha))
            
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
        self.conecta_db()
        try:
            self.cursor.execute("""
                SELECT * FROM Usuarios
                WHERE Username = ? AND Senha = ?               
            """, (username, senha))
            
            resultado = self.cursor.fetchone()
            self.desconecta_db()
            
            if resultado:
                return True, "Login realizado com sucesso!"
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