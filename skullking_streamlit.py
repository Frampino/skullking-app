# skullking_streamlit.py
import streamlit as st
from logic import calcola_punteggio_totale

st.set_page_config(page_title="Skull King - Rascall", layout="wide")
st.title("🎴 Skull King - Variante Rascall")

# -------------------------------
# Inizializzazioni di session_state
# -------------------------------
# IMPORTANTISSIMO: inizializziamo TUTTE le chiavi che useremo,
# così evitiamo AttributeError / KeyError nei rerun.
if "round_num" not in st.session_state:
    st.session_state.round_num = 1

if "num_giocatori" not in st.session_state:
    st.session_state.num_giocatori = 2

if "nomi" not in st.session_state:
    st.session_state.nomi = []

if "punteggi" not in st.session_state:
    st.session_state.punteggi = {}   # punteggi cumulativi

if "round_cards" not in st.session_state:
    st.session_state.round_cards = 1

if "show_round" not in st.session_state:
    st.session_state.show_round = False

if "reset_round_inputs" not in st.session_state:
    st.session_state.reset_round_inputs = False

# Questa memoria contiene i risultati testuali dell'ultimo round calcolato.
# Viene salvata prima del rerun e mostrata nella run successiva.
if "round_last_results" not in st.session_state:
    st.session_state.round_last_results = []

# -------------------------------
# Schermata 0: (opzionale) Mostra risultati ultimo round se presenti
# -------------------------------
if st.session_state.round_last_results:
    last_round_number = st.session_state.round_num - 1
    st.subheader(f"📣 Risultati round {last_round_number}")
    for line in st.session_state.round_last_results:
        st.write(line)
    st.markdown("---")

# -------------------------------
# Schermata 1: Numero giocatori
# -------------------------------
st.session_state.num_giocatori = st.number_input(
    "Quanti giocatori?",
    min_value=2, max_value=8, step=1,
    value=st.session_state.num_giocatori
)

# -------------------------------
# Schermata 2: Nomi giocatori
# -------------------------------
st.session_state.nomi = []
for i in range(st.session_state.num_giocatori):
    nome = st.text_input(f"Nome giocatore {i+1}", key=f"nome_{i}")
    st.session_state.nomi.append(nome.strip())

# Bottone per iniziare il round (mostra la sezione inserimento dettagli)
if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True
        # Puliamo eventuali risultati vecchi solo quando ri-partiamo (opzionale)
        st.session_state.round_last_results = []

# -------------------------------
# Schermata 3: Inserimento dettagli del round
# -------------------------------
if st.session_state.show_round:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

    # Numero di carte nel round
    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?",
        min_value=1, step=1,
        value=st.session_state.round_cards
    )

    # Costruiamo i widget di input per ogni giocatore.
    # Se st.session_state.reset_round_inputs è True usiamo i valori "puliti" come default.
    # Altrimenti recuperiamo eventuali valori esistenti nello session_state.
    round_data = {}
    for nome in st.session_state.nomi:
        st.markdown(f"### {nome}")
        col1, col2, col3 = st.columns([1,1,1])

        # number_input - puntata
        puntata = st.number_input(
            f"{nome} - Puntata",
            min_value=0, step=1,
            key=f"{nome}_puntata",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_puntata", 0)
        )

        # number_input - prese
        prese = st.number_input(
            f"{nome} - Prese",
            min_value=0, step=1,
            key=f"{nome}_prese",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_prese", 0)
        )

        # selectbox - tipo
        tipo_index = 0 if st.session_state.reset_round_inputs else ["aperta", "chiusa"].index(
            st.session_state.get(f"{nome}_tipo", "aperta")
        )
        tipo = st.selectbox(
            f"{nome} - Tipo",
            ["aperta", "chiusa"],
            key=f"{nome}_tipo",
            index=tipo_index
        )

        # multiselect - specials
        specials = st.multiselect(
            f"{nome} - Bonus / Malus",
            ["PiratavsSirena", "SkullKingvsPirata", "SirenavsSkullKing",
             "Boutil", "14", "14Nero", "AkabvsAbissale", "BoutilMaledetto"],
            key=f"{nome}_specials",
            default=[] if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_specials", [])
        )

        round_data[nome] = (puntata, prese, tipo, specials)

    # Una volta creati i widget, azzeriamo il flag (così il prossimo rerun userà i valori reali,
    # e il flag tornerà a False finché non verrà impostato di nuovo al click del bottone).
    st.session_state.reset_round_inputs = False

    # -------------------------------
    # Bottone "Prossimo Round"
    # -------------------------------
    if st.button("➡️ Prossimo Round"):
        # Calcoliamo i punteggi e salviamo i risultati testuali in una lista.
        resultado_lines = []
        for nome in st.session_state.nomi:
            # Leggiamo i valori dai widget (session_state li contiene grazie alle key)
            puntata = st.session_state.get(f"{nome}_puntata", 0)
            prese = st.session_state.get(f"{nome}_prese", 0)
            tipo = st.session_state.get(f"{nome}_tipo", "aperta")
            specials = st.session_state.get(f"{nome}_specials", [])

            punteggio = calcola_punteggio_totale(
                puntata, prese, tipo, st.session_state.round_cards, specials
            )

            # aggiorniamo i cumulativi
            st.session_state.punteggi[nome] = st.session_state.punteggi.get(nome, 0) + punteggio

            # salviamo la riga di testo per mostrarla dopo il rerun
            resultado_lines.append(f"{nome}: +{punteggio} punti (Totale: {st.session_state.punteggi[nome]})")

        # Salviamo i risultati dell'ultimo round nello session_state
        st.session_state.round_last_results = resultado_lines

        # Incrementiamo il numero del round
        st.session_state.round_num += 1

        # Impostiamo il flag per resettare i widget al prossimo run
        st.session_state.reset_round_inputs = True

        # Manteniamo la vista della schermata round
        st.session_state.show_round = True

        # Forziamo un rerun IMMEDIATO: la run successiva leggerà reset_round_inputs=True
        # e quindi i widget verranno inizializzati ai valori puliti.
        st.rerun()

# -------------------------------
# In basso: mostra sempre la classifica cumulativa (opzionale)
# -------------------------------
if st.session_state.punteggi:
    st.markdown("---")
    st.subheader("📊 Classifica Cumulativa (aggiornata)")
    sorted_total = sorted(st.session_state.punteggi.items(), key=lambda x: x[1], reverse=True)
    for i, (nome, punti) in enumerate(sorted_total, start=1):
        st.write(f"{i}. {nome}: {punti} punti")
















