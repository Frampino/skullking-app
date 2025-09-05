"""
Logica del gioco Skull King - Variante Rascall
Gestione punteggi e bonus (senza GUI).
"""

def calcola_punteggio(puntata, prese, tipo_puntata, round_num):
    """
    Calcola il punteggio base secondo la variante Rascall.

    :param puntata: int - numero di prese dichiarate
    :param prese: int - prese effettivamente fatte
    :param tipo_puntata: str - "aperta" o "chiusa"
    :param round_num: int - numero del round (quante carte in mano)
    :return: int - punteggio base
    """
    if tipo_puntata == "aperta":
        if prese == puntata:
            return 10 * round_num
        elif abs(prese - puntata) == 1:
            return 5 * round_num
        else:
            return 0
    elif tipo_puntata == "chiusa":
        if prese == puntata:
            return 15 * round_num
        else:
            return 0
    return 0


def calcola_bonus(speciali, puntata, prese):
    """
    Calcola i bonus/malus legati alle carte speciali.

    :param speciali: lista di str - carte speciali usate (es. ["PiratavsSirena"])
    :param puntata: int - prese dichiarate
    :param prese: int - prese fatte
    :return: int - punteggio bonus/malus
    """
    bonus = 0

    # Bonus/malus
    if prese == puntata:
        if "PiratavsSirena" in speciali:
            bonus += 20
        if "SkullKingvsPirata" in speciali:
            bonus += 30
        if "SirenavsSkullKing" in speciali:
            bonus += 40
        if "Boutil" in speciali:
            bonus += 20
        if "14" in speciali:
            bonus += 10
        if "14Nero" in speciali:
            bonus += 20
        if "AkabvsAbissale" in speciali:
            bonus += 30

    # Malus "BoutilMaledetto"
    if "BoutilMaledetto" in speciali:
        bonus -= 20

    return bonus


def calcola_punteggio_totale(puntata, prese, tipo_puntata, round_num, speciali):
    """
    Calcola punteggio base + bonus.

    :return: int - punteggio totale del round
    """
    base = calcola_punteggio(puntata, prese, tipo_puntata, round_num)
    extra = calcola_bonus(speciali, puntata, prese)
    return base + extra


# -------------------
# Test veloce in console
# -------------------
if __name__ == "__main__":
    # Esempio: round 5, puntata 2 chiusa, prese 2, usati pirati + tesori
    punti = calcola_punteggio_totale(
        puntata=2,
        prese=2,
        tipo_puntata="chiusa",
        round_num=5,
        speciali=["PiratavsSirena"]
    )
    print("Punteggio round:", punti)
