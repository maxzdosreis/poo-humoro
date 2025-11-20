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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
               Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Username TEXT NOT NULL,
               Email TEXT NOT NULL,
               Senha TEXT NOT NULL,
               Confirma_senha TEXT NOT NULL
           );                 
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
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