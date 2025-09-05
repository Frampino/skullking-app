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

if "punteggi" not in st.session_state:
    st.session_state.punteggi = {}

if "round_cards" not in st.session_state:
    st.session_state.round_cards = 1

if "show_round" not in st.session_state:
    st.session_state.show_round = False

if "reset_round_inputs" not in st.session_state:
    st.session_state.reset_round_inputs = False

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

# Bottone per iniziare il round
if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True

# -------------------------------
# Schermata 3: Dettagli round
# -------------------------------
if st.session_state.show_round:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

    # Numero di carte nel round
    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?",
        min_value=1, step=1,
        value=st.session_state.round_cards
    )

    # Dati temporanei per il round
    round_data = {}

    for nome in st.session_state.nomi:
        st.markdown(f"### {nome}")
        col1, col2, col3 = st.columns(3)

        # Puntata
        puntata = st.number_input(
            f"{nome} - Puntata",
            min_value=0, step=1,
            key=f"{nome}_puntata",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_puntata", 0)
        )

        # Prese
        prese = st.number_input(
            f"{nome} - Prese",
            min_value=0, step=1,
            key=f"{nome}_prese",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_prese", 0)
        )

        # Tipo
        tipo = st.selectbox(
            f"{nome} - Tipo",
            ["aperta", "chiusa"],
            key=f"{nome}_tipo",
            index=0 if st.session_state.reset_round_inputs else ["aperta", "chiusa"].index(st.session_state.get(f"{nome}_tipo", "aperta"))
        )

        # Bonus / Malus
        specials = st.multiselect(
            f"{nome} - Bonus / Malus",
            ["PiratavsSirena", "SkullKingvsPirata", "SirenavsSkullKing",
             "Boutil","14","14Nero","AkabvsAbissale","BoutilMaledetto"],
            key=f"{nome}_specials",
            default=[] if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_specials", [])
        )

        round_data[nome] = (puntata, prese, tipo, specials)

    # Reset flag dei widget appena impostati
    st.session_state.reset_round_inputs = False

    # -------------------------------
    # Bottone Prossimo Round
    # -------------------------------
    if st.button("➡️ Prossimo Round"):
        st.subheader("🏆 Classifica Round")
        for nome, (puntata, prese, tipo, specials) in round_data.items():
            punteggio = calcola_punteggio_totale(
                puntata, prese, tipo, st.session_state.round_cards, specials
            )

            # Aggiorna punteggi cumulativi
            st.session_state.punteggi[nome] = st.session_state.punteggi.get(nome, 0) + punteggio
            st.write(f"{nome}: +{punteggio} punti (Totale: {st.session_state.punteggi[nome]})")

        # Mostra classifica cumulativa
        st.subheader("📊 Classifica Cumulativa")
        sorted_total = sorted(st.session_state.punteggi.items(), key=lambda x: x[1], reverse=True)
        for i, (nome, punti) in enumerate(sorted_total, start=1):
            st.write(f"{i}. {nome}: {punti} punti")

        # Aggiorna numero round e resetta input dei widget
        st.session_state.round_num += 1
        st.session_state.reset_round_inputs = True














