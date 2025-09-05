# skullking_streamlit.py
import streamlit as st
from logic import calcola_punteggio_totale  # usa il tuo modulo di punteggio

st.set_page_config(page_title="Skull King - Rascall", layout="wide")
st.title("🎴 Skull King - Variante Rascall")

# --- Schermata 1: Numero giocatori ---
num_giocatori = st.number_input("Quanti giocatori?", min_value=2, max_value=8, step=1)

# --- Schermata 2: Nomi giocatori ---
nomi = []
for i in range(num_giocatori):
    nome = st.text_input(f"Nome giocatore {i+1}")
    nomi.append(nome.strip())

# Controllo che tutti i nomi siano inseriti
if all(nomi) and st.button("Inizia Round"):
    st.success("Tutti i nomi inseriti! Inserisci i dettagli del round qui sotto:")

    round_num = st.number_input("Quante carte in questo round?", min_value=1, step=1)

    punteggi_round = {}
    for nome in nomi:
        st.subheader(f"{nome}")
        col1, col2, col3 = st.columns(3)

        with col1:
            puntata = st.number_input(f"{nome} - Puntata", min_value=0, step=1)
        with col2:
            prese = st.number_input(f"{nome} - Prese", min_value=0, step=1)
        with col3:
            tipo = st.selectbox(f"{nome} - Tipo", ["aperta", "chiusa"])

        specials = st.multiselect(
            f"{nome} - Bonus / Malus",
            ["PiratavsSirena", "SkullKingvsPirata", "SirenavsSkullKing",
             "Boutil","14","14Nero","AkabvsAbissale","BoutilMaledetto"]
        )

        punteggio = calcola_punteggio_totale(puntata, prese, tipo, round_num, specials)
        punteggi_round[nome] = punteggio
        st.write(f"Punteggio round: **{punteggio}**")

    if st.button("Mostra Classifica Round"):
        st.subheader("🏆 Classifica Round")
        sorted_round = sorted(punteggi_round.items(), key=lambda x: x[1], reverse=True)
        for i, (nome, punti) in enumerate(sorted_round, start=1):
            st.write(f"{i}. {nome}: {punti} punti")

