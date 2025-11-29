import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import json

serializable_events = []
events = []
events_list = []

class window(tk.Frame):
    def _innit_(self, root, name: str, sizeH: int, sizeW: int):
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
    def show_day_view(self):
        #"""Displays the current day."""#
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear previous widgets

        current_date = datetime.now().strftime("%A, %B %d, %Y")
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

        cal = Calendar(self.root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(pady=20)

        self.load_events()
        self.display_events_on_calendar(events)

        day_button = ttk.Button(self.root, text="Mostrar Dia Atual", command = lambda: self.show_day_view())
        day_button.pack(pady = 10)

        # Optional: Add a button to get selected date from calendar
        def get_selected_date():
            selected_date = cal.get_date()
            date_label.config(text=f"Data Selecionada: {selected_date}")

        select_button = ttk.Button(self.root, text = "Pegar Data Selecionada", command = get_selected_date)
        select_button.pack(pady = 5)
        date_label = ttk.Label(self.root, text = "Data Selecionada: None")
        date_label.pack(pady = 5)

    def New_event(self, events):
    
        moodNum = int(self.input)

        match moodNum:
            case 1:
                mood = "Muito Mal"
                moodCor = "red"
                moodLetra = "yellow"
        
            case 2:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"

            case 3:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
        
            case 4:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
        
            case 5:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
        
            case 6:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
        
            case 7:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"

            case 8:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
        
            case 9:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"
            
            case 10:
                mood = "Muito Bom"
                moodCor = "green"
                moodLetra = "white"
            
            case _:
                mood = "teste"
                moodCor = "teste"
                moodLetra = "teste"

        for event in events:
            event_date = event['date']
            event_title = event['title']
            event_tag = event['tag']
            event_bg = event['background']
            event_fg = event['foreground']#faz alguma coisa?#

        self.new_event = {
        'date': datetime.today(),
        'title': mood,
        'tag': "Humor",
        'background': moodCor,
        'foreground': moodLetra
        }

        event_date = self.new_event['date']
        event_title = self.new_event['title']
        event_tag = self.new_event['tag']
        event_bg = self.new_event['background']
        event_fg = self.new_event['foreground']

        events_list.append(self.new_event)

        Calendar.calevent_create(self, date = event_date, text = event_title, tags = (event_tag))
        Calendar.tag_config(self, event_tag, background = event_bg, foreground = event_fg)

        self.save_events(events, filename = "events.json")

    def save_events(self, events, filename="events.json"):
        # Convert datetime objects to string for JSON serialization
        for event in events:
            serializable_event = event.copy()
            serializable_event['date'] = event['date'].strftime('%Y-%m-%d')
            serializable_events.append(serializable_event)

        with open(filename, 'w') as f:
            json.dump(serializable_events, f, indent=4)

    def load_events(self, filename="events.json"):
        try:
            with open(filename, 'r') as f:
                serializable_events = json.load(f)
            
            for event_data in serializable_events:
                event_data['date'] = datetime.strptime(event_data['date'], '%Y-%m-%d').date()
                events.append(event_data)
            return events
        except FileNotFoundError:
            return []

    def display_events_on_calendar(self, events):
        for event in events:
            Calendar.calevent_create(event['date'], event['description'], event.get('tags', ''))

    def QuestionarioHumor(self):
        questionario = tk.Toplevel(self.root)
        questionario.title("Questionário de Humor")
        questionario.geometry(f"400x300")

        pergunta = ttk.Label(questionario, text = "De 1 á 10 qual seria seu humor hoje?")
        pergunta.pack(pady = 20)

        resposta = ttk.Entry(questionario, width = 10)
        resposta.pack(pady = 10)

        def get_input():
            self.input = resposta.get()
            self.New_event(events)
            questionario.destroy()
    
        resposta_button = ttk.Button(questionario, text = "Responder", command = lambda: get_input())
        resposta_button.pack(pady = 10)

def main():
    root = tk.Tk()

    calendarioW = Calendario()
    calendarioW._innit_(root, "calendarioW", 600, 500)
    calendarioW.create_window("Calendário")

    calendarioW.show_day_view()  # Start with the day view#

    root.mainloop()

if __name__ == "__main__":
    main()