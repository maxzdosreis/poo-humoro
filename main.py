# Importa classe App definida no arquivo login.py
from login import App

def main():
    # Instancia a aplicação gráfica
    app = App()
    # Inicia o loop principal do tkinter
    app.mainloop()

# Ponto de entrada padrão em aplicações Python
# a função main() será chamada e o programa será iniciado.
if __name__=="__main__":
    main()