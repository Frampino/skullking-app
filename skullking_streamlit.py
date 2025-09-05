import streamlit as st
from logic import calcola_punteggio_totale

st.set_page_config(page_title="Skull King - Rascall", layout="wide")
st.title("🎴 Skull King - Variante Rascall")

# -------------------------------
# Inizializzazioni di session_state
# -------------------------------
if "round_num" not in st.session_state:
    st.session_state.round_num = 1

if "num_giocatori" not in st.session_state:
    st.session_state.num_giocatori = 2

if "nomi" not in st.session_state:
    st.session_state.nomi = []

if "punteggi_round" not in st.session_state:
    st.session_state.punteggi_round = {}

if "punteggi" not in st.session_state:
    st.session_state.punteggi = {}

if "round_cards" not in st.session_state:
    st.session_state.round_cards = 1

if "show_round" not in st.session_state:
    st.session_state.show_round = False

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

# Controllo che tutti i nomi siano inseriti
if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True

# -------------------------------
# Schermata 3: Dettagli round
# -------------------------------

if "show_round" in st.session_state and st.session_state.show_round:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

# Numero di carte in questo round
    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?", min_value=1, step=1,
        value=st.session_state.round_cards if "round_cards" in st.session_state else 1
    )

# Dati temporanei del round
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

import streamlit as st
from logic import calcola_punteggio_totale

st.set_page_config(page_title="Skull King - Rascall", layout="wide")
st.title("🎴 Skull King - Variante Rascall")

# -------------------------------
# Inizializzazioni di session_state
# -------------------------------
if "round_num" not in st.session_state:
    st.session_state.round_num = 1

if "num_giocatori" not in st.session_state:
    st.session_state.num_giocatori = 2

if "nomi" not in st.session_state:
    st.session_state.nomi = []

if "punteggi_round" not in st.session_state:
    st.session_state.punteggi_round = {}

if "punteggi" not in st.session_state:
    st.session_state.punteggi = {}

if "round_cards" not in st.session_state:
    st.session_state.round_cards = 1

if "show_round" not in st.session_state:
    st.session_state.show_round = False

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

# Controllo che tutti i nomi siano inseriti
if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True

# -------------------------------
# Schermata 3: Dettagli round
# -------------------------------

if "show_round" in st.session_state and st.session_state.show_round:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

        # Numero di carte in questo round
    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?", min_value=1, step=1,
        value=st.session_state.round_cards if "round_cards" in st.session_state else 1
    )

     # Dati temporanei del round
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

        # Bottone per calcolare punteggi del round
    if st.button("Calcola Punteggi Round"):
        st.subheader("🏆 Classifica Round")
        for nome, (puntata, prese, tipo, specials) in round_data.items():
            punteggio = calcola_punteggio_totale(puntata, prese, tipo,
                                                  st.session_state.round_cards, specials)
             # Aggiorna i punteggi cumulativi
            if nome not in st.session_state.punteggi:
                st.session_state.punteggi[nome] = 0
            st.session_state.punteggi[nome] += punteggio
            st.write(f"{nome}: +{punteggio} punti (Totale: {st.session_state.punteggi[nome]})")

# Mostra classifica cumulativa
        st.subheader("📊 Classifica Cumulativa")
        sorted_total = sorted(st.session_state.punteggi.items(), key=lambda x: x[1], reverse=True)
        for i, (nome, punti) in enumerate(sorted_total, start=1):
            st.write(f"{i}. {nome}: {punti} punti")

        # Aggiorna numero round e resetta round_data
        st.session_state.round_num += 1
        st.session_state.show_round = False  # torna alla schermata di inserimento dettagli round






