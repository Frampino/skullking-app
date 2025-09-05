import streamlit as st
import pandas as pd

# -------------------------------
# INIZIALIZZAZIONE VARIABILI
# -------------------------------
if "players" not in st.session_state:
    st.session_state.players = ["Giocatore 1", "Giocatore 2"]
if "scores" not in st.session_state:
    st.session_state.scores = {nome: [] for nome in st.session_state.players}
if "round_num" not in st.session_state:
    st.session_state.round_num = 1
if "fine_partita" not in st.session_state:
    st.session_state.fine_partita = False
if "last_results" not in st.session_state:
    st.session_state.last_results = None

# -------------------------------
# HEADER
# -------------------------------
st.title("🏴‍☠️ Segnapunti Skull King")

# -------------------------------
# GESTIONE FINE PARTITA
# -------------------------------
if st.session_state.fine_partita:
    st.subheader("🏆 Fine partita!")
    punteggi_finali = {g: sum(st.session_state.scores[g]) for g in st.session_state.players}
    classifica_finale = pd.DataFrame.from_dict(
        punteggi_finali, orient="index", columns=["Punteggio Finale"]
    ).sort_values(by="Punteggio Finale", ascending=False)
    st.table(classifica_finale)

    # Bottone nuova partita: resetta tutto
    if st.button("🔄 Nuova partita"):
        st.session_state.scores = {nome: [] for nome in st.session_state.players}
        st.session_state.round_num = 1
        st.session_state.fine_partita = False
        st.session_state.last_results = None
        st.rerun()

    st.stop()  # blocca il resto della pagina se la partita è finita

# -------------------------------
# SEZIONE ROUND
# -------------------------------
st.subheader(f"3️⃣ Round {st.session_state.round_num} - Inserisci dettagli")

round_data = {}
for nome in st.session_state.players:
    col1, col2 = st.columns(2)
    with col1:
        puntata = st.number_input(
            f"Puntata {nome}", min_value=0, key=f"{nome}_puntata_{st.session_state.round_num}"
        )
        prese = st.number_input(
            f"Prese {nome}", min_value=0, key=f"{nome}_prese_{st.session_state.round_num}"
        )
    with col2:
        tipo = st.selectbox(
            f"Tipo mano {nome}", ["Normale", "Speciale"], key=f"{nome}_tipo_{st.session_state.round_num}"
        )
        specials = st.text_input(
            f"Bonus/Malus {nome}", key=f"{nome}_specials_{st.session_state.round_num}"
        )
    round_data[nome] = (puntata, prese, tipo, specials)

# -------------------------------
# BOTTONE PROSSIMO ROUND
# -------------------------------
if st.button("➡️ Prossimo round"):
    # Calcolo punteggi round
    risultati_round = {}
    for nome, (puntata, prese, tipo, specials) in round_data.items():
        punteggio = 0
        if puntata == prese:
            punteggio = 20 + puntata * 10
        else:
            punteggio = -10 * abs(puntata - prese)
        st.session_state.scores[nome].append(punteggio)
        risultati_round[nome] = punteggio

    # Salvo gli ultimi risultati
    st.session_state.last_results = risultati_round

    # Avanza al prossimo round
    st.session_state.round_num += 1

    # Reset input del nuovo round
    for nome in st.session_state.players:
        for key in [
            f"{nome}_puntata_{st.session_state.round_num}",
            f"{nome}_prese_{st.session_state.round_num}",
            f"{nome}_tipo_{st.session_state.round_num}",
            f"{nome}_specials_{st.session_state.round_num}",
        ]:
            if key in st.session_state:
                del st.session_state[key]

    st.rerun()

# -------------------------------
# RISULTATI ULTIMO ROUND (in fondo)
# -------------------------------
if st.session_state.last_results:
    st.subheader(f"📊 Risultati round {st.session_state.round_num - 1}")
    st.table(
        pd.DataFrame.from_dict(st.session_state.last_results, orient="index", columns=["Punteggio"])
    )

# -------------------------------
# CLASSIFICA CUMULATIVA
# -------------------------------
st.subheader("📈 Classifica cumulativa")
punteggi_totali = {g: sum(st.session_state.scores[g]) for g in st.session_state.players}
classifica = pd.DataFrame.from_dict(punteggi_totali, orient="index", columns=["Totale"]).sort_values(by="Totale", ascending=False)
st.table(classifica)

# -------------------------------
# BOTTONE FINE PARTITA
# -------------------------------
if st.button("🏁 Fine partita"):
    st.session_state.fine_partita = True
    st.rerun()


















