import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import json

serializable_events = []
events_list = []

class window(tk.Frame):
    def _init_(self, root, name: str, sizeH: int, sizeW: int):
        self.root = root
        self.window_name = name
        self.sizeH = sizeH
        self.sizeW = sizeW
    
    def centering(self):
        window_height = self.sizeH
        window_width = self.sizeW

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcula a posição central
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        return center_x, center_y

    def create_window(self, titulo: str):
        self.titulo = titulo

        self.root.title(f"{self.titulo}")
        center_x, center_y = self.centering()
        self.root.geometry(f"{self.sizeH}x{self.sizeW}+{center_x}+{center_y}")

class Calendario(window):
    def _init_(self, root, name: str, sizeH: int, sizeW: int):
        super()._init_( root, name, sizeH, sizeW)
        self.cal = None
        self.events = []

    def show_day_view(self):
        #"""Displays the current day."""#
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear previous widgets

        current_date = datetime.now().strftime("%A, %d de %B de %Y")
        day_label = ttk.Label(self.root, text=f"Hoje é: {current_date}", font=("Arial", 16))
        day_label.pack(pady=20)

        month_button = ttk.Button(self.root, text = "Mostrar Mês Inteiro", command = lambda: self.show_month_view())
        month_button.pack(pady = 10)

        mood_button = ttk.Button(self.root, text = "Defina Seu Humor Hoje", command = lambda: self.QuestionarioHumor())
        mood_button.pack(pady = 10)

    def show_month_view(self):
        #"""Displays the full month calendar."""#
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear previous widgets

        self.cal = Calendar(self.root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=20)

        self.load_events()
        self.display_events_on_calendar()

        day_button = ttk.Button(self.root, text="Mostrar Dia Atual", command = lambda: self.show_day_view())
        day_button.pack(pady = 10)

        # Optional: Add a button to get selected date from calendar
        def get_selected_date():
            selected_date = self.cal.get_date()
            date_label.config(text=f"Data Selecionada: {selected_date}")

        select_button = ttk.Button(self.root, text = "Pegar Data Selecionada", command = get_selected_date)
        select_button.pack(pady = 5)
        date_label = ttk.Label(self.root, text = "Data Selecionada: None")
        date_label.pack(pady = 5)

    def New_event(self):
    
        moodNum = int(self.mood_input)

        mood_config = {
            1: ("Muito Mal", "red", "yellow"),
            2: ("Mal", "orange", "black"),
            3: ("Desconfortável", "darkorange", "white"),
            4: ("Abaixo da Média", "gold", "black"),
            5: ("Neutro", "gray", "white"),
            6: ("Acima da Média", "lightblue", "black"),
            7: ("Bem", "skyblue", "black"),
            8: ("Muito Bem", "lightgreen", "black"),
            9: ("Ótimo", "limegreen", "white"),
            10: ("Excelente", "green", "white")
        }

        mood, moodCor, moodLetra = mood_config.get(moodNum, ("Indefinido", "White", "Black"))

        new_event = {
        'date': datetime.today().date(),
        'title': mood,
        'tag': "Humor",
        'background': moodCor,
        'foreground': moodLetra
        }

        self.events.append(new_event)

        if self.cal:
            self.cal.calevent_create(date = new_event['date'], title = new_event['title'], tag = new_event['tag'])
            self.cal.tag_config(new_event['tag'], background = new_event['background'], foreground = new_event['foreground'])

        self.save_events()

    def save_events(self, filename = "events.json"):
        # Convert datetime objects to string for JSON serialization
        for event in self.events:
            serializable_event = event.copy()
            serializable_event['date'] = event['date'].strftime('%Y-%m-%d')
            serializable_events.append(serializable_event)

        with open(filename, 'w') as f:
            json.dump(serializable_events, f, indent=4)

    def load_events(self, filename="events.json"):
        try:
            with open(filename, 'r') as f:
                serializable_events = json.load(f)

            self.events = []            
            for event_data in serializable_events:
                event_data['date'] = datetime.strptime(event_data['date'], '%Y-%m-%d').date()
                self.events.append(event_data)
            return self.events
        except FileNotFoundError:
            self.events = []

    def display_events_on_calendar(self):
        if not self.cal:
            return
        
        for event in self.events:
            self.cal.calevent_create(event['date'], event['description'], event.get('tags', ''))
            self.cal.tag_config(event['tag'], background = ['background'], foreground = ['foreground'])

    def QuestionarioHumor(self):
        questionario = tk.Toplevel(self.root)
        questionario.title("Questionário de Humor")
        questionario.geometry(f"400x300")

        pergunta = ttk.Label(questionario, text = "De 1 á 10 qual seria seu humor hoje?")
        pergunta.pack(pady = 20)

        resposta = ttk.Entry(questionario, width = 10)
        resposta.pack(pady = 10)

        def get_input():
            mood_input = resposta.get()

            try:
               mood_num = int(mood_input)
               if 1 <= mood_num <= 10:
                    self.New_event(mood_input)
                    questionario.destroy()

            except ValueError:
                error_label = ttk.Label(questionario, text = "Por favor, insira um número válido", foreground = "red")
                error_label.pack(pady = 5)
            
            resposta.bind('<Return>', lambda e: get_input())

    
        resposta_button = ttk.Button(questionario, text = "Responder", command = lambda: get_input)
        resposta_button.pack(pady = 10)

def main():
    root = tk.Tk()

    calendarioW = Calendario()
    calendarioW._init_(root, "calendarioW", 600, 500)
    calendarioW.create_window("Calendário")

    calendarioW.show_day_view()  # Start with the day view#

    root.mainloop()

if __name__ == "__main__":
    main()