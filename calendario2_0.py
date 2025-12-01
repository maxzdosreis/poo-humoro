import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime
from database import Database


class window(ctk.CTkToplevel):
    def _init_(self, parent, username):
        super()._init_(parent)
        self.window_name = "calendarioW"
        self.sizeH = 600
        self.sizeW = 500
        self.parent = parent
        self.username = username
        self.database = Database()
    
    def centering(self):
        window_height = self.sizeH
        window_width = self.sizeW

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcula a posição central
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        return center_x, center_y

    def create_window(self, titulo: str):
        self.titulo = titulo

        window.title(f"{self.titulo}")
        center_x, center_y = self.centering()
        window.geometry(f"{self.sizeH}x{self.sizeW}+{center_x}+{center_y}")

class Calendario(window):
    def _init_(self, parent):
        super()._init_(parent)
        self.cal = None
        self.events = []

        self.create_window("Calendário")
        self.show_day_view()

    def show_day_view(self):
        #"""Displays the current day."""#
        for widget in Calendario.winfo_children():
            widget.destroy()  # Clear previous widgets

        current_date = datetime.now().strftime(f"%A, %d de %B de %Y")
        day_label = ttk.Label(Calendario, text=f"Hoje é: {current_date}", font=("Arial", 16))
        day_label.pack(pady=20)

        month_button = ttk.Button(Calendario, text = "Mostrar Mês Inteiro", command = lambda: self.show_month_view())
        month_button.pack(pady = 10)

        menu_button = ttk.Button(Calendario, text = "Menu", command = lambda: self.fecharCal())
        menu_button.pack(pady = 10)

        self.get_humor()
        for event in self.events:
            if event.get('date') == datetime.today().date():
                circle_color = event.get('background', '')
                moodL = event.get('title', '')
    

        mood_label = ttk.Label(Calendario, text = f"O Humor de Hoje é: {moodL}")
        mood_label.pack(pady = 10)

        frame = ttk.Frame(Calendario, padding = 10)
        frame.pack(fill = tk.BOTH, expand = True)

        canva = tk.Canvas(frame, bg = "white", highlightthickness = 0)
        canva.pack(fill = tk.BOTH, expand = True)

        circle_center_x = 285
        circle_center_y = 150
        circle_radius = 100

        def create_circle(canva, x, y, r, **Kwargs):
            return canva.create_oval(x - r, y - r, x + r, y + r, **Kwargs)
        
        create_circle(canva, circle_center_x, circle_center_y, circle_radius, fill = circle_color, outline = "")


    def show_month_view(self):
        #"""Displays the full month calendar."""#
        for widget in Calendario.winfo_children():
            widget.destroy()  # Clear previous widgets

        self.get_humor()

        self.cal = Calendar(Calendario, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=20)

        self.display_events_on_calendar()

        day_button = ttk.Button(Calendario, text="Mostrar Dia Atual", command = lambda: self.show_day_view())
        day_button.pack(pady = 10)

        # Optional: Add a button to get selected date from calendar
        def get_selected_date():
            selected_date = self.cal.get_date()
            date_label.config(text=f"Data Selecionada: {selected_date}")

        select_button = ttk.Button(Calendario, text = "Pegar Data Selecionada", command = get_selected_date)
        select_button.pack(pady = 5)
        date_label = ttk.Label(Calendario, text = "Data Selecionada: None")
        date_label.pack(pady = 5)

    def New_event(self):
    
        moodNum = int(self.mood_input)

        mood_config = {
            1: ("Péssimo", "red", "yellow"),
            2: ("Ruim", "darkorange", "white"),
            3: ("Mediano", "gray", "white"),
            4: ("Bom", "skyblue", "black"),
            5: ("Excelente", "green", "white")
        }

        mood, moodCor, moodLetra = mood_config.get(moodNum, ("Indefinido", "White", "Black"))

        new_event = {
        'date': datetime.today().date(),
        'title': mood,
        'tag': mood,
        'background': moodCor,
        'foreground': moodLetra
        }
        
        verify = datetime.today().date()
    
        if verify not in self.events:
            self.events.append(new_event)
        else:
            self.events['date': verify] = new_event

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
            teste = []
            teste = self.database.listar_questionarios()

            for event in teste:
                event = teste.copy()

                if event['humor'] == "Excelente":
                    mood_num = 5
                elif event['humor'] == "Bom":
                    mood_num = 4
                elif event['humor'] == "Mediano":
                    mood_num = 3
                elif event['humor'] == "Ruim":
                    mood_num = 2
                elif event['humor'] == "Péssimo":
                    mood_num = 1

             
                if 1 <= mood_num <= 5:
                    self.New_event()
                

        except ValueError:
            print("erro no get_humor")

    def fecharCal(self):
        self.destroy()