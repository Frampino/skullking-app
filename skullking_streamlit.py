# skullking_streamlit.py
import streamlit as st
from logic import calcola_punteggio_totale

st.set_page_config(page_title="Skull King - Rascall", layout="wide")
st.title("🎴 Skull King - Variante Rascall")

# --- Inizializza session state ---
if "num_giocatori" not in st.session_state:
    st.session_state.num_giocatori = 0
if "nomi" not in st.session_state:
    st.session_state.nomi = []
if "punteggi" not in st.session_state:
    st.session_state.punteggi = {}  # punteggi cumulativi
if "round_num" not in st.session_state:
    st.session_state.round_num = 1

# --- Schermata 1: Numero giocatori ---
st.subheader("1️⃣ Seleziona numero giocatori")
st.session_state.num_giocatori = st.number_input(
    "Quanti giocatori?", 
    min_value=2, max_value=8, step=1, 
    value=st.session_state.num_giocatori
)

# --- Schermata 2: Nomi giocatori ---
st.subheader("2️⃣ Inserisci nomi giocatori")
nomi = []
for i in range(st.session_state.num_giocatori):
    nome = st.text_input(f"Nome giocatore {i+1}", 
                         value=st.session_state.nomi[i] if i < len(st.session_state.nomi) else "")
    nomi.append(nome.strip())
st.session_state.nomi = nomi

# Controllo che tutti i nomi siano inseriti
if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True

# --- Schermata 3: Dettagli round ---
if "show_round" in st.session_state and st.session_state.show_round:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?", min_value=1, step=1,
        value=st.session_state.round_cards if "round_cards" in st.session_state else 1
    )

    round_data = {}
    for nome in st.session_state.nomi:
        st.markdown(f"### {nome}")
        col1, col2, col3 = st.columns(3)

        with col1:
            puntata = st.number_input(f"{nome} - Puntata", min_value=0, step=1,
                                      key=f"{nome}_puntata")
        with col2:
            prese = st.number_input(f"{nome} - Prese", min_value=0, step=1,
                                    key=f"{nome}_prese")
        with col3:
            tipo = st.selectbox(f"{nome} - Tipo", ["aperta", "chiusa"],
                                key=f"{nome}_tipo")

        specials = st.multiselect(
            f"{nome} - Bonus / Malus",
            ["PiratavsSirena", "SkullKingvsPirata", "SirenavsSkullKing",
             "Boutil","14","14Nero","AkabvsAbissale","BoutilMaledetto"],
            key=f"{nome}_specials"
        )

        round_data[nome] = (puntata, prese, tipo, specials)

    if st.button("Calcola Punteggi Round"):
        st.subheader("🏆 Classifica Round")
        for nome, (puntata, prese, tipo, specials) in round_data.items():
            punteggio = calcola_punteggio_totale(puntata, prese, tipo,
                                                  st.session_state.round_cards, specials)
            if nome not in st.session_state.punteggi:
                st.session_state.punteggi[nome] = 0
            st.session_state.punteggi[nome] += punteggio
            st.write(f"{nome}: +{punteggio} punti (Totale: {st.session_state.punteggi[nome]})")

        st.session_state.round_num += 1  # passa al round successivo



