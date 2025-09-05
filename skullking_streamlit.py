# skullking_streamlit.py
import streamlit as st
from logic import calcola_punteggio_totale

st.set_page_config(page_title="Skull King", layout="wide")
st.title("🏴‍☠️ Skull King")

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
    st.session_state.punteggi = {}   # punteggi cumulativi

if "round_cards" not in st.session_state:
    st.session_state.round_cards = 1

if "show_round" not in st.session_state:
    st.session_state.show_round = False

if "reset_round_inputs" not in st.session_state:
    st.session_state.reset_round_inputs = False

if "round_last_results" not in st.session_state:
    st.session_state.round_last_results = []

if "fine_partita" not in st.session_state:
    st.session_state.fine_partita = False

# -------------------------------
# Schermata finale (mostra solo classifica e nuova partita)
# -------------------------------
if st.session_state.fine_partita:
    st.title("🏴‍☠️ Skull King")
    st.markdown("## 🏆 Classifica Finale")

    classifica_finale = sorted(
        st.session_state.punteggi.items(),
        key=lambda x: x[1],
        reverse=True
    )
    for i, (nome, punti) in enumerate(classifica_finale, 1):
        corona = " 👑" if i == 1 else ""
        st.write(f"{i}. **{nome}** — {punti} punti{corona}")

    st.markdown("---")
    if st.button("🔄 Nuova Partita"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 🔴 Importantissimo: blocca qui il codice,
    # così non mostra più schermate sotto
    st.stop()

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

if all(st.session_state.nomi):
    if st.button("Inizia Round"):
        st.session_state.show_round = True
        st.session_state.round_last_results = []  # pulizia

# -------------------------------
# Schermata 3: Inserimento dettagli round
# -------------------------------
if st.session_state.show_round and not st.session_state.fine_partita:
    st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

    st.session_state.round_cards = st.number_input(
        "Quante carte in questo round?",
        min_value=1, step=1,
        value=st.session_state.round_cards
    )

    round_data = {}
    for nome in st.session_state.nomi:
        st.markdown(f"### {nome}")
        col1, col2, col3 = st.columns([1,1,1])

        puntata = st.number_input(
            f"{nome} - Puntata",
            min_value=0, step=1,
            key=f"{nome}_puntata",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_puntata", 0)
        )
        prese = st.number_input(
            f"{nome} - Prese",
            min_value=0, step=1,
            key=f"{nome}_prese",
            value=0 if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_prese", 0)
        )
        tipo_index = 0 if st.session_state.reset_round_inputs else ["aperta", "chiusa"].index(
            st.session_state.get(f"{nome}_tipo", "aperta")
        )
        tipo = st.selectbox(
            f"{nome} - Tipo",
            ["aperta", "chiusa"],
            key=f"{nome}_tipo",
            index=tipo_index
        )
        specials = st.multiselect(
            f"{nome} - Bonus / Malus",
            ["PiratavsSirena", "SkullKingvsPirata", "SirenavsSkullKing",
             "Boutil", "14", "14Nero", "AkabvsAbissale", "BoutilMaledetto"],
            key=f"{nome}_specials",
            default=[] if st.session_state.reset_round_inputs else st.session_state.get(f"{nome}_specials", [])
        )

        round_data[nome] = (puntata, prese, tipo, specials)

    st.session_state.reset_round_inputs = False

    # -------------------------------
    # Bottone "Calcola Punteggi Round"
    # -------------------------------
    if st.button("Calcola Punteggi Round"):
        risultati = []
        for nome, (puntata, prese, tipo, specials) in round_data.items():
            punteggio = calcola_punteggio_totale(
                puntata, prese, tipo, st.session_state.round_cards, specials
            )
            st.session_state.punteggi[nome] = st.session_state.punteggi.get(nome, 0) + punteggio
            risultati.append(f"{nome}: +{punteggio} punti (Totale: {st.session_state.punteggi[nome]})")

        # salvo i risultati in session_state per mostrarli sopra
        st.session_state.round_last_results = risultati
        st.session_state.round_num += 1
        st.session_state.reset_round_inputs = True
        st.rerun()

    # Pulsante fine partita
    if st.button("🏁 Fine Partita"):
        st.session_state.fine_partita = True
    # -------------------------------
# Risultati ultimo round (in basso, sopra la classifica cumulativa)
# -------------------------------
    if st.session_state.round_last_results:
        st.markdown("---")
        last_round_number = st.session_state.round_num - 1
        st.subheader(f"📣 Risultati round {last_round_number}")
        for line in st.session_state.round_last_results:
            st.write(line)

# -------------------------------
# Classifica cumulativa (solo se partita NON finita)
# -------------------------------
elif st.session_state.punteggi:
    st.markdown("---")
    st.subheader("📊 Classifica Cumulativa (aggiornata)")
    sorted_total = sorted(st.session_state.punteggi.items(), key=lambda x: x[1], reverse=True)
    for i, (nome, punti) in enumerate(sorted_total, start=1):
        st.write(f"{i}. {nome}: {punti} punti")

























