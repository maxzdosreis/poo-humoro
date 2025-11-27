from tkinter import *
import calendar

##
root = Tk()
root.geometry("400x300")
root.title("Calendário")
root.resizable(False,False)
root.configure(bg="#89cff0")

def Clear():
    ano_entrada.delete(0, END)
    mes_entrada.delete(0, END)
    cal.delete(0, END)

def Exit():
    root.destroy()

def Mostrar():
    m = mes.get()
    y = ano.get()

    if m <= 12:
        outupt = calendar(y,m)
        cal.inserty("end", output)
    
    else:
        output = "O mês não existe"
        cal.Insert("end", output)
#texto#


#mês#

mes_label = Label(text = "mês", font= ("Ariel", 10, "bold"), bg="#89cff0", fg= "black")
mes_label.place(relx = 0.2, rely = 0.2)
mes = IntVar()
mes_entrada = Entry(textvariable = mes, justify = "center")
mes_entrada.place(relx = 0.3, rely = 0.2, relwidth = 0.1)

#ano#
ano_label = Label(text = "ano", font = ("Ariel", 10, "bold"))
ano_label.place(relx = 0.5, rely = 0.2)
ano = IntVar()
ano_entrada = Entry(textvariable = ano, justify = "center")
ano_entrada.place(relx = 0.6, rely = 0.2, relwidth = 0.15)

#botão#
#Mostar#

mostrarB = Button( text = "mostrar", font = ("Verdana", 10, "bold"), command = Mostrar)
mostrarB.place(relx = 0.3, rely = 0.85)
LimparB = Button(text = "Limpar", font = ("verdana", 10, "bold"), command = Clear)
LimparB.place(relx = 0.5, rely = 0.85)
ExitB = Button(text = "Sair", font = ("Verdana", 10, "bold"), command = Exit)
ExitB.place(relx = 0.7, rely = 0.85)

root.mainloop()