import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime
from database import Database


class Calendario(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.window_name = "calendarioW"
        self.sizeH = 600
        self.sizeW = 700
        self.parent = parent
        self.username = username
        self.database = Database()

        self.create_window()
        self.show_day_view()

    def centering(self):
        window_height = self.sizeH
        window_width = self.sizeW

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula a posição central
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        return center_x, center_y

    def create_window(self):
        self.window_title = "Calendário"
        self.sizeH = 600
        self.sizeW = 500

        self.title(f"{self.window_title}")
        center_x, center_y = self.centering()
        self.geometry(f"{self.sizeH}x{self.sizeW}+{center_x}+{center_y}")
        self.cal = None
        self.events = []

    def show_day_view(self):
        #"""Displays the current day."""#
        for widget in self.winfo_children():
            widget.pack_forget()  # Clear previous widgets

        current_date = datetime.now().strftime(f"%A, %d de %B de %Y")
        day_label = ctk.CTkLabel(self, text=f"Hoje é: {current_date}", font=("Arial", 16))
        day_label.pack(pady=20)

        month_button = ctk.CTkButton(self, width = 300, height = 45, corner_radius = 15, text = "Mostrar Mês Inteiro", font = ("Ariel", 15), fg_color = "#1f538d", hover_color = "#14375e", command = lambda: self.show_month_view())
        month_button.pack(pady = 15)

        menu_button = ctk.CTkButton(self, width = 300, height = 45, corner_radius = 15, text = "Menu", font = ("Ariel", 15), fg_color = "#1f538d", hover_color = "#14375e", command = lambda: self.fecharCal())
        menu_button.pack(pady = 15)

        moodL = "Não registrado"
        circle_color = "lightgray"

        self.get_humor()
        for event in self.events:
            if event['date'] == datetime.today().date():
                circle_color = event.get('background', '')
                moodL = event.get('title', '')
    

        mood_label = ctk.CTkLabel(self, text = f"O Humor de Hoje é: {moodL}")
        mood_label.pack(pady = 20)

        frame = ctk.CTkFrame(self, corner_radius = 15, fg_color = "transparent")
        frame.pack(fill = ctk.BOTH, expand = True, padx = 10, pady = 10)

        canva = tk.Canvas(frame, width = 300, height = 300, bg = "black", highlightthickness = 0)
        canva.pack(fill = tk.BOTH, expand = True, pady = 5)

        circle_center_x = 355
        circle_center_y = 110
        circle_radius = 100

        def create_circle(canva, x, y, r, **Kwargs):
            return canva.create_oval(x - r, y - r, x + r, y + r, **Kwargs)
        
        create_circle(canva, circle_center_x, circle_center_y, circle_radius, fill = circle_color, outline = "black", width = 2)


    def show_month_view(self):
        #"""Displays the full month calendar."""#
        for widget in self.winfo_children():
            widget.pack_forget()  # Clear previous widgets

        self.get_humor()

        self.cal = Calendar(self, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=30)

        self.display_events_on_calendar()

                # Optional: Add a button to get selected date from calendar
        def get_selected_date():
            selected_date = self.cal.get_date()
            date_label.configure(text=f"Data Selecionada: {selected_date}")

        day_button = ctk.CTkButton(self, width = 300, height = 35, corner_radius = 15, text="Mostrar Dia Atual", font = ("Ariel", 15), fg_color = "#1f538d", hover_color = "#14375e", command = lambda: self.show_day_view())
        day_button.pack(pady = 10)

        select_button = ctk.CTkButton(self, width = 300, height = 35, corner_radius = 15, text = "Pegar Data Selecionada", font = ("Ariel", 15), fg_color = "#1f538d", hover_color = "#14375e", command = get_selected_date)
        select_button.pack(pady = 10)



        date_label = ctk.CTkLabel(self, text = "Data Selecionada: None")
        date_label.pack(pady = 5)


    def New_event(self, mood_num: int, event_date):
    

        mood_config = {
            1: ("Péssimo", "red", "yellow"),
            2: ("Ruim", "darkorange", "white"),
            3: ("Mediano", "gray", "white"),
            4: ("Bom", "skyblue", "black"),
            5: ("Excelente", "green", "white")
        }

        mood, moodCor, moodLetra = mood_config.get(mood_num, ("Indefinido", "White", "Black"))

        new_event = {
        'date': event_date,
        'title': mood,
        'tag': mood,
        'background': moodCor,
        'foreground': moodLetra
        }
        isNew_event = False
        for i , event in enumerate(self.events):
            if event['date'] == event_date:
                self.events[i] = new_event
                isNew_event = True

            if not isNew_event:
                self.events.append(new_event)

    def display_events_on_calendar(self):
        if not self.cal:
            return
        
        for event in self.events:
            if self.cal:
                self.cal.calevent_create(event.get('date', ''), event.get('title', ''), event.get('tag', ''))
                self.cal.tag_config(event.get('tag', ''), background = event.get('background', ''), foreground = event.get('foreground', ''))
            else:
                print("algo deu errado")

    def get_humor(self):
        

        try:
            teste = self.database.listar_questionarios(self.username)
            dict_teste = dict(teste)

            mood_num = 0

            for event in enumerate(dict_teste):
                for humor in event:
                    
                    humor = dict_teste.get('Humor', '')

                    if humor == "Excelent":
                        mood_num = 5
                    elif humor == "Bom":
                        mood_num = 4
                    elif humor == "Mediano":
                        mood_num = 3
                    elif humor == "Ruim":
                        mood_num = 2
                    elif humor == "Péssimo":
                        mood_num = 1

            #for event in enumerate(dict_teste):
             #   if "Excelent" in event:
             #       mood_num = 5
             #   elif "Bom" in event:
             #       mood_num = 4
             #   elif "Mediano" in event:
             #       mood_num = 3
             #   elif "Ruim" in event:
             #       mood_num = 2
             #   elif "Péssimo" in event:
             #       mood_num = 1 

                for item in enumerate(dict_teste):
                    if item == "Data":
                        data_questi = item

                try:
                    data_questi = datetime.strptime(data_questi, "%Y-%m-%d").data
                except:
                    data_questi = datetime.today().date()
             
                if 1 <= mood_num <= 5:
                    self.New_event(mood_num, data_questi)
                

        except ValueError:
            print("erro no get_humor")

    def fecharCal(self):
        self.destroy()