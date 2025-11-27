from tkinter import *
import calendar

##
root = Tk()
root.geometry("600x500")
root.title("Calendário")
root.resizable(False,False)
root.configure(bg="#CDC495")

def Clear():
    ano_entrada.delete(0, END)
    mes_entrada.delete(0, END)
    cal.delete(0, END)

def Exit():
    root.destroy()

def Mostrar():
    m = mes.get()
    y = ano.get()  

    if m <= 12 and m > 0:
        outupt = calendar.calendar(y,m)
        cal.insert(output = "end")
    
    else:
        output = "O mês não existe"
        cal.insert("end", output)
#texto#
cal = Text(width = 50 , height = 15, borderwidth = 2)
cal.place(relx = 0.16, rely = 0.30)

#mês#

mes_label = Label(text = "mês", font= ("Ariel", 10, "bold"), bg="#CDC495", fg= "black")
mes_label.place(relx = 0.2, rely = 0.2)
mes = IntVar()
mes_entrada = Entry(textvariable = mes, justify = "center")
mes_entrada.place(relx = 0.3, rely = 0.2, relwidth = 0.1)

#ano#
ano_label = Label(text = "ano", font = ("Ariel", 10, "bold"), bg="#CDC495", fg= "black")
ano_label.place(relx = 0.5, rely = 0.2)
ano = IntVar()
ano_entrada = Entry(textvariable = ano, justify = "center")
ano_entrada.place(relx = 0.6, rely = 0.2, relwidth = 0.15)

#botão#
#Mostar#

mostrarB = Button( text = "mostrar", font = ("Verdana", 10, "bold"), command = Mostrar)
mostrarB.place(relx = 0.2, rely = 0.85)
LimparB = Button(text = "Limpar", font = ("verdana", 10, "bold"), command = Clear)
LimparB.place(relx = 0.45, rely = 0.85)
ExitB = Button(text = "Sair", font = ("Verdana", 10, "bold"), command = Exit)
ExitB.place(relx = 0.7, rely = 0.85)

root.mainloop()