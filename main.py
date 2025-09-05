from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from logic import calcola_punteggio_totale  # importa il modulo che abbiamo creato

Builder.load_file("skullking.kv")  # Assicurati di avere rinominato il file

PLAYER_COLORS = [
    (0.9, 0.1, 0.1, 1),   # rosso
    (0.1, 0.5, 0.9, 1),   # blu
    (0.1, 0.9, 0.3, 1),   # verde
    (0.9, 0.7, 0.1, 1),   # giallo
    (0.6, 0.2, 0.8, 1),   # viola
    (0.9, 0.5, 0.1, 1),   # arancione
    (0.3, 0.9, 0.9, 1),   # ciano
    (0.7, 0.7, 0.7, 1),   # grigio
]

# --- Schermata 1: Numero giocatori ---
class ScreenNumeroGiocatori(Screen):
    def validate_and_continue(self):
        num_text = self.ids.num_giocatori_input.text
        error_label = self.ids.error_label
        try:
            num = int(num_text)
            if 2 <= num <= 8:
                error_label.text = ""
                self.manager.app.num_giocatori = num
                self.manager.current = "nomi_giocatori"
            else:
                error_label.text = "Inserisci un numero tra 2 e 8!"
        except ValueError:
            error_label.text = "Numero non valido!"

# --- Schermata 2: Nomi giocatori ---
class ScreenNomiGiocatori(Screen):
    def on_pre_enter(self):
        """Genera dinamicamente TextInput in base al numero di giocatori"""
        self.ids.nomi_box.clear_widgets()
        self.name_inputs = []
        num_giocatori = self.manager.app.num_giocatori
        for i in range(num_giocatori):
            ti = TextInput(
                hint_text=f"Nome giocatore {i+1}",
                multiline=False,
                font_size=28,
                size_hint_y=None,
                height=50
            )
            self.ids.nomi_box.add_widget(ti)
            self.name_inputs.append(ti)
        self.ids.error_label.text = ""

    def validate_and_continue(self):
        names = [ti.text.strip() for ti in self.name_inputs]
        if "" in names:
            self.ids.error_label.text = "Tutti i giocatori devono avere un nome!"
            return
        self.manager.app.giocatori = names
        self.manager.current = "inserimento_mano"

class ScreenInserimentoMano(Screen):
    def on_pre_enter(self):
        self.ids.giocatori_box.clear_widgets()
        self.inputs = {}
        self.specials_vars = {}
        app = self.manager.app

        for i, nome in enumerate(app.giocatori):
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            frame = BoxLayout(
                orientation="vertical", 
                padding=5, spacing=5, 
                size_hint_y=None, height=180
            )
            frame.canvas.before.clear()
            with frame.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(*color)
                Rectangle(pos=frame.pos, size=frame.size)

            # Label con nome
            frame.add_widget(Label(
                text=nome, 
                font_size=24, 
                color=(1,1,1,1),  # testo bianco per contrasto
                size_hint_y=0.3
            ))

            # Puntata / Prese
            subframe = BoxLayout(size_hint_y=0.3, spacing=5)
            subframe.add_widget(Label(text="Puntata:", font_size=20, color=(1,1,1,1)))
            call_input = TextInput(input_filter="int", multiline=False, font_size=20)
            subframe.add_widget(call_input)
            subframe.add_widget(Label(text="Prese:", font_size=20, color=(1,1,1,1)))
            prese_input = TextInput(input_filter="int", multiline=False, font_size=20)
            subframe.add_widget(prese_input)
            tipo_spinner = Spinner(text="aperta", values=["aperta","chiusa"], size_hint=(0.3,1))
            subframe.add_widget(tipo_spinner)
            frame.add_widget(subframe)

            # Bonus speciali
            bonus_frame = BoxLayout(size_hint_y=0.3, spacing=5)
            specials = ["PiratavsSirena","SkullKingvsPirata","SirenavsSkullKing","Boutil","BoutilMaledetto","14","14Nero","AkabvsAbissale"]
            vars_ = {}
            for s in specials:
                cb = CheckBox()
                vars_[s] = cb
                bonus_frame.add_widget(Label(text=s, font_size=18, color=(1,1,1,1)))
                bonus_frame.add_widget(cb)
            frame.add_widget(bonus_frame)

            self.ids.giocatori_box.add_widget(frame)
            self.inputs[nome] = (call_input, prese_input, tipo_spinner)
            self.specials_vars[nome] = vars_

    def validate_and_continue(self):
        try:
            carte = int(self.ids.carte_input.text)
        except ValueError:
            self.ids.error_label.text = "Inserisci un numero valido di carte!"
            return

        self.round_data = {}
        for nome in self.manager.app.giocatori:
            call_input, prese_input, tipo_spinner = self.inputs[nome]
            try:
                puntata = int(call_input.text)
                prese = int(prese_input.text)
            except ValueError:
                self.ids.error_label.text = f"Inserisci numeri validi per {nome}"
                return
            tipo = tipo_spinner.text
            specials = [s for s, cb in self.specials_vars[nome].items() if cb.active]
            self.round_data[nome] = {"puntata": puntata, "prese": prese, "tipo": tipo, "specials": specials}

        # salva i dati del round nell'app per calcolo punteggio
        self.manager.app.round_data = self.round_data
        self.manager.app.carte = carte

        # passa alla schermata classifica parziale
        self.manager.current = "classifica_parziale"

class ScreenClassificaParziale(Screen):
    def on_pre_enter(self):
        self.ids.classifica_box.clear_widgets()
        app = self.manager.app

        # inizializza i punteggi cumulativi se non esistono
        if not hasattr(app, "scores"):
            app.scores = {nome: 0 for nome in app.giocatori}

        carte = app.carte
        round_data = app.round_data
        self.round_details = {}

        # calcolo punteggi
        for nome, dati in round_data.items():
            puntata = dati["puntata"]
            prese = dati["prese"]
            tipo = dati["tipo"]
            specials = dati["specials"]

            totale = calcola_punteggio_totale(puntata, prese, tipo, carte, specials)
            app.scores[nome] += totale
            self.round_details[nome] = (puntata, prese, tipo, specials, totale, app.scores[nome])

            # widget per mostrare i dati
            txt = f"{nome}: +{totale} punti (totale: {app.scores[nome]})\n"
            txt += f"  Puntata: {puntata}, Prese: {prese}, Tipo: {tipo}, Bonus: {', '.join(specials) if specials else 'Nessuno'}"
            self.ids.classifica_box.add_widget(Label(text=txt, font_size=20, size_hint_y=None, height=60))

    def prossima_mano(self):
        self.manager.current = "inserimento_mano"

    def fine_partita(self):
        self.manager.current = "classifica_finale"

class ScreenClassificaFinale(Screen):
    def on_pre_enter(self):
        self.ids.final_box.clear_widgets()
        app = self.manager.app

        # ordina i giocatori per punteggio decrescente
        classifica = sorted(app.scores.items(), key=lambda x: x[1], reverse=True)

        for i, (nome, punti) in enumerate(classifica, start=1):
            txt = f"{i}. {nome}: {punti} punti"
            # evidenzia il vincitore
            if i == 1:
                color = (1, 0.84, 0, 1)  # oro per il vincitore
            else:
                # colore preso dalla lista PLAYER_COLORS in base all'ordine di inserimento
                color = PLAYER_COLORS[app.giocatori.index(nome) % len(PLAYER_COLORS)]

            lbl = Label(
                text=txt,
                font_size=28,
                color=color,
                size_hint_y=None,
                height=50
            )
            self.ids.final_box.add_widget(lbl)

    def nuova_partita(self):
        self.manager.app.scores = {}
        self.manager.app.giocatori = []
        self.manager.app.num_giocatori = 0
        self.manager.current = "numero_giocatori"

    def esci(self):
        App.get_running_app().stop()

# --- App principale ---
class SkullKingApp(App):
    def build(self):
        self.num_giocatori = 0
        self.giocatori = []
        sm = ScreenManager()
        sm.app = self
        sm.add_widget(ScreenNumeroGiocatori(name="numero_giocatori"))
        sm.add_widget(ScreenNomiGiocatori(name="nomi_giocatori"))
        sm.add_widget(ScreenInserimentoMano(name="inserimento_mano"))
        sm.add_widget(ScreenClassificaParziale(name="classifica_parziale"))
        sm.add_widget(ScreenClassificaFinale(name="classifica_finale"))
        return sm

if __name__ == "__main__":
    SkullKingApp().run()

