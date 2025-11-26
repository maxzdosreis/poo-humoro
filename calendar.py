import customtkinter as ctk
import calendar

##
root = ctk.Tk()
root.geometry("400x300")
root.title("Calendário")
root.resizable(False,False)
root.configure(bg="#89cff0")

def Clear():
    ano_entrada.ctk.delete(0, ctk.END)
    mes_entrada.ctk.delete(0, ctk.END)
    cal.ctk.delete(0, ctk.END)

def Exit():
    root.destroy()

def Mostrar():
    m = mes.get()
    y = ano.get()

    if m <= 12:
        outupt = calendar.onth(y,m)
        cal.ctk.inserty("end", output)
    
    else:
        output = "O mês não existe"
        cal.ctk.insert("end", output)
#texto#
cal = ctk.text(width = 33 , height = 8, relif = ctk.RIDGE, borderwidth = 2)
cal.place(relx = 0.2, rely = 0.35)

#mês#

mes_label = ctk.Label(text = "mês", font= ("Ariel", 10, "bold"), bg="#89cff0", fg= "black")
mes_label.place(relx = 0.2, rely = 0.2)
mes = ctk.IntVar()
mes_entrada = ctk.Entry(textvariable = mes, justify = "center")
mes_entrada.place(relx = 0.3, rely = 0.2, relwidth = 0.1)

#ano#
ano_label = ctk.Label(text = "ano", font = ("Ariel", 10, "bold"), command = Mostrar)
ano_label.place(relx = 0.5, rely = 0.2)
ano = ctk.IntVar()
ano_entrada = ctk.Entry(textvariable = ano, justify = "center")
ano_entrada.place(relx = 0.6, rely = 0.2, relwidth = 0.15)

#botão#
#Mostar#

mostrarB = ctk.Button( text = "mostrar", font = ("Verdana", 10, "bold"), command = Mostrar)
mostrarB.place(relx = 0.3, rely = 0.85)
LimparB = ctk.Button(text = "Limpar", font = ("verdana", 10, "bold"), command = Clear)
LimparB.place(relx = 0.5, rely = 0.85)
ExitB = ctk.Button(text = "Sair", font = ("Verdana", 10, "bold"), command = Exit)
ExitB.place(relx = 0.7, rely = 0.85)

root.mainloop()