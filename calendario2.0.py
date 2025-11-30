import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import json


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

        current_date = datetime.now().strftime(f"%A, %d de %B de %Y")
        day_label = ttk.Label(self.root, text=f"Hoje é: {current_date}", font=("Arial", 16))
        day_label.pack(pady=20)

        with open("events.json", "r") as f:
            teste = []
            teste = json.load(f)

        month_button = ttk.Button(self.root, text = "Mostrar Mês Inteiro", command = lambda: self.show_month_view())
        month_button.pack(pady = 10)

        mood_button = ttk.Button(self.root, text = "Defina Seu Humor Hoje", command = lambda: self.QuestionarioHumor())
        mood_button.pack(pady = 10)

        self.load_events()

        frame = ttk.Frame(self.root, padding = 10)
        frame.pack(fill = tk.BOTH, expand = True)

        canva = tk.Canvas(frame, bg = "white", highlightthickness = 0)
        canva.pack(fill = tk.BOTH, expand = True)

        circle_center_x = 285
        circle_center_y = 150
        circle_radius = 100
        for event in self.events:
            if event.get('date') == datetime.today().date():
                circle_color = event.get('background', '')

        def create_circle(canva, x, y, r, **Kwargs):
            return canva.create_oval(x - r, y - r, x + r, y + r, **Kwargs)
        
        create_circle(canva, circle_center_x, circle_center_y, circle_radius, fill = circle_color, outline = "")


    def show_month_view(self):
        #"""Displays the full month calendar."""#
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear previous widgets
        
        self.load_events()

        self.cal = Calendar(self.root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=20)

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
        'tag': mood,
        'background': moodCor,
        'foreground': moodLetra
        }
        
        verify = datetime.today().date()
    
        if verify not in self.events:
            self.events.append(new_event)
        else:
            self.events["date": verify] = new_event
    
        self.save_events(filename= "events.json")

    def save_events(self, filename = "events.json"):
        # Convert datetime objects to string for JSON serialization
        try:
            with open(filename, "r") as f:
                self.serializable_events = json.load(f)
        except FileNotFoundError:
                self.serializable_events = []

        for event in self.events:
            serializable_event = event.copy()
            try:
                serializable_event['date'] = event['date'].strftime('%Y-%m-%d')
            except AttributeError:
                serializable_event['date'] = event['date']
            if serializable_event not in self.serializable_events:
                self.serializable_events.append(serializable_event)

        try:
            with open(filename, 'w') as f:
                json.dump(self.serializable_events, f, indent=4)

        except json.JSONDecodeError:
            self.serializable_events = []

    def load_events(self, filename="events.json"):
        try:
            with open(filename, 'r') as f:
                self.serializable_events = json.load(f)
          
            for event_data in self.serializable_events:
                event_data['date'] = datetime.strptime(event_data['date'], '%Y-%m-%d').date()
                self.events.append(event_data)
            return self.events
        except FileNotFoundError:
            self.events = []

    def display_events_on_calendar(self):
        if not self.cal:
            return
        
        for event in self.events:
            if self.cal:
                self.cal.calevent_create(event.get('date', ''), event.get('description', ''), event.get('tag', ''))
                self.cal.tag_config(event.get('tag', ''), background = event.get('background', ''), foreground = event.get('foreground', ''))
            else:
                print("algo deu errado")

    def QuestionarioHumor(self):
        questionario = tk.Toplevel(self.root)
        questionario.title("Questionário de Humor")
        questionario.geometry(f"400x300")

        pergunta = ttk.Label(questionario, text = "De 1 á 10 qual seria seu humor hoje?")
        pergunta.pack(pady = 20)

        resposta = ttk.Entry(questionario, width = 10)
        resposta.pack(pady = 10)

        resposta_button = ttk.Button(questionario, text = "Responder", command = lambda: get_input())
        resposta_button.pack(pady = 10)

        resposta.bind('<Return>', lambda e: get_input())


        def get_input():
            self.mood_input = resposta.get()

            try:
               print("teste")
               mood_num = int(self.mood_input)
               if 1 <= mood_num <= 10:
                    self.New_event()
                    questionario.destroy()

            except ValueError:
                error_label = ttk.Label(questionario, text = "Por favor, insira um número válido", foreground = "red")
                error_label.pack(pady = 5)


def main():
    root = tk.Tk()

    calendarioW = Calendario()
    calendarioW._init_(root, "calendarioW", 600, 500)
    calendarioW.create_window("Calendário")

    calendarioW.show_day_view()  # Start with the day view#

    root.mainloop()

if __name__ == "__main__":
    main()