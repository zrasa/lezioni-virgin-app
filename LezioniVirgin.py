import calendar
from datetime import date


# ============================================================
# 1. TIPI DI LEZIONE
# ============================================================

tipi_lezione = {
    "RefAtl": {
        "descrizione": "Pilates Reformer Athletic",
        "durata": 45
    },
    "RefAl": {
        "descrizione": "Pilates Reformer Align",
        "durata": 45
    },
    "PilAl": {
        "descrizione": "Mat Pilates Align",
        "durata": 45
    },
    "YogaStr": {
        "descrizione": "Yoga Strength",
        "durata": 60
    },
    "YogaAl": {
        "descrizione": "Yoga Align",
        "durata": 60
    },
    "YogaC": {
        "descrizione": "Yoga Calm",
        "durata": 60
    },
    "SB": {
        "descrizione": "Sound Bath",
        "durata": 60
    }
}


# ============================================================
# 2. CALENDARIO STANDARD SETTIMANALE
# ============================================================

# 0 = lunedì
# 1 = martedì
# 2 = mercoledì
# 3 = giovedì
# 4 = venerdì
# 5 = sabato
# 6 = domenica

calendario_standard = [
    {
        "giorno_settimana": 2,
        "ora": "14:00",
        "lezione": "RefAtl"
    },
    {
        "giorno_settimana": 2,
        "ora": "17:30",
        "lezione": "PilAl"
    },
    {
        "giorno_settimana": 2,
        "ora": "18:30",
        "lezione": "YogaStr"
    },
    {
        "giorno_settimana": 3,
        "ora": "13:00",
        "lezione": "YogaStr"
    }
]


# ============================================================
# 3. GENERA IL CALENDARIO DEL MESE
# ============================================================

def genera_calendario_mese():

    mese = int(input("Inserisci il mese (1-12): "))
    anno = int(input("Inserisci l'anno: "))

    lezioni_mese = []

    # Numero di giorni presenti nel mese scelto
    numero_giorni = calendar.monthrange(anno, mese)[1]

    for giorno in range(1, numero_giorni + 1):

        data_lezione = date(anno, mese, giorno)

        for lezione in calendario_standard:

            if data_lezione.weekday() == lezione["giorno_settimana"]:

                codice_lezione = lezione["lezione"]

                lezioni_mese.append({
                    "data": data_lezione,
                    "ora": lezione["ora"],
                    "codice": codice_lezione,
                    "descrizione": tipi_lezione[codice_lezione]["descrizione"],
                    "durata": tipi_lezione[codice_lezione]["durata"]
                })

    return lezioni_mese, mese, anno


# ============================================================
# 4. AGGIUNGI LEZIONI EXTRA
# ============================================================

def aggiungi_lezioni_extra(lezioni, mese, anno):

    risposta = input(
        "\nVuoi aggiungere una lezione extra? (si/no): "
    ).lower()

    while risposta == "si":

        print("\nLezioni disponibili:")

        for codice in tipi_lezione:
            print(
                codice,
                "-",
                tipi_lezione[codice]["descrizione"]
            )

        codice_lezione = input(
            "\nInserisci il codice della lezione: "
        )

        # Controllo che il codice inserito sia valido
        while codice_lezione not in tipi_lezione:

            print("\nCodice non valido.")
            print("\nLezioni disponibili:")

            for codice in tipi_lezione:
                print(
                    codice,
                    "-",
                    tipi_lezione[codice]["descrizione"]
                )

            codice_lezione = input(
                "\nInserisci nuovamente il codice della lezione: "
            )

        giorno = int(
            input("Inserisci il giorno del mese: ")
        )

        ora = input(
            "Inserisci l'orario di inizio (es. 18:45): "
        )

        data_lezione = date(
            anno,
            mese,
            giorno
        )

        lezioni.append({
            "data": data_lezione,
            "ora": ora,
            "codice": codice_lezione,
            "descrizione": tipi_lezione[codice_lezione]["descrizione"],
            "durata": tipi_lezione[codice_lezione]["durata"]
        })

        print("\nLezione aggiunta.")

        risposta = input(
            "\nVuoi aggiungere un'altra lezione extra? (si/no): "
        ).lower()

    # Ordina per data e ora
    lezioni.sort(
        key=lambda x: (x["data"], x["ora"])
    )

    return lezioni


# ============================================================
# 5. RIMUOVI LEZIONI NON FATTE
# ============================================================

def rimuovi_lezioni_non_fatte(lezioni, mese, anno):

    risposta = input(
        "\nCi sono lezioni del mese che non hai fatto? (si/no): "
    ).lower()

    while risposta == "si":

        giorno = int(
            input("\nInserisci il giorno del mese: ")
        )

        data_scelta = date(
            anno,
            mese,
            giorno
        )

        # Trova tutte le lezioni presenti in quel giorno
        lezioni_giorno = [
            lezione
            for lezione in lezioni
            if lezione["data"] == data_scelta
        ]

        if len(lezioni_giorno) == 0:

            print(
                "\nNon risultano lezioni in questa data."
            )

        else:

            print(
                f"\nLezioni del {giorno:02d}/{mese:02d}/{anno}:"
            )

            for lezione in lezioni_giorno:

                print(
                    lezione["codice"],
                    "-",
                    lezione["ora"],
                    "-",
                    lezione["descrizione"]
                )

            codici_input = input(
                "\nInserisci il codice o i codici delle lezioni non fatte "
                "separati da virgola: "
            )

            codici_da_rimuovere = [
                codice.strip()
                for codice in codici_input.split(",")
            ]

            for codice in codici_da_rimuovere:

                trovato = False

                for lezione in lezioni_giorno:

                    if lezione["codice"] == codice:

                        lezioni.remove(lezione)

                        print(
                            codice,
                            "- lezione rimossa"
                        )

                        trovato = True

                if not trovato:

                    print(
                        codice,
                        "- codice non trovato per questa data"
                    )

        risposta = input(
            "\nCi sono altre lezioni non fatte? (si/no): "
        ).lower()

    return lezioni


# ============================================================
# 6. STAMPA LEZIONI E RIEPILOGO
# ============================================================

def stampa_lezioni(lezioni):

    print()

    print(
        f"{'DATA':<12} "
        f"{'ORA':<8} "
        f"{'CODICE':<10} "
        f"{'DESCRIZIONE':<30} "
        f"{'DURATA':<10}"
    )

    print("-" * 75)

    for lezione in lezioni:

        data = lezione["data"].strftime("%d/%m/%Y")
        ora = lezione["ora"]
        codice = lezione["codice"]
        descrizione = lezione["descrizione"]
        durata = lezione["durata"]

        print(
            f"{data:<12} "
            f"{ora:<8} "
            f"{codice:<10} "
            f"{descrizione:<30} "
            f"{durata} min"
        )

    # Conteggio delle lezioni
    count_45 = 0
    count_60 = 0

    for lezione in lezioni:

        if lezione["durata"] == 45:
            count_45 += 1

        elif lezione["durata"] == 60:
            count_60 += 1

    # Riepilogo finale
    print("\n" + "-" * 75)

    print("RIEPILOGO")

    print(
        f"Lezioni da 45 minuti: {count_45}"
    )

    print(
        f"Lezioni da 60 minuti: {count_60}"
    )


import calendar
import csv
from datetime import date

def salva_csv(lezioni, mese, anno):

    risposta = input(
        "\nVuoi scaricare il file CSV? (si/no): "
    ).lower()

    if risposta == "si":

        nome_file = f"Lezioni_{mese:02d}_{anno}.csv"

        with open(
            nome_file,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            # Intestazioni
            writer.writerow([
                "Data",
                "Ora",
                "Codice",
                "Descrizione",
                "Durata"
            ])

            # Lezioni
            for lezione in lezioni:

                writer.writerow([
                    lezione["data"].strftime("%d/%m/%Y"),
                    lezione["ora"],
                    lezione["codice"],
                    lezione["descrizione"],
                    lezione["durata"]
                ])

        print(
            f"\nFile {nome_file} creato con successo!"
        )

    else:

        print("\nFile CSV non creato.")

    
# ============================================================
# 7. FUNZIONE PRINCIPALE
# ============================================================

def gestione_lezioni_mese():

    lezioni_mese, mese, anno = genera_calendario_mese()

    lezioni_mese = aggiungi_lezioni_extra(
        lezioni_mese,
        mese,
        anno
    )

    lezioni_mese = rimuovi_lezioni_non_fatte(
        lezioni_mese,
        mese,
        anno
    )

    stampa_lezioni(
        lezioni_mese
    )

    salva_csv(
        lezioni_mese,
        mese,
        anno
    )

    return lezioni_mese

# ============================================================
# 8. AVVIO DEL PROGRAMMA
# ============================================================

if __name__ == "__main__":
    gestione_lezioni_mese()