import streamlit as st
import pandas as pd
from datetime import date, time
import calendar

from LezioniVirgin import tipi_lezione, calendario_standard


st.title("Gestione Lezioni")
st.write("Calendario e conteggio delle mie lezioni")


# ============================================================
# MESI
# ============================================================

mesi = {
    "Gennaio": 1,
    "Febbraio": 2,
    "Marzo": 3,
    "Aprile": 4,
    "Maggio": 5,
    "Giugno": 6,
    "Luglio": 7,
    "Agosto": 8,
    "Settembre": 9,
    "Ottobre": 10,
    "Novembre": 11,
    "Dicembre": 12
}


# ============================================================
# SESSION STATE
# ============================================================

if "lezioni_mese" not in st.session_state:
    st.session_state.lezioni_mese = []

if "mese" not in st.session_state:
    st.session_state.mese = None

if "anno" not in st.session_state:
    st.session_state.anno = None

if "mese_nome" not in st.session_state:
    st.session_state.mese_nome = None


# ============================================================
# SCELTA MESE E ANNO
# ============================================================

mese_nome = st.selectbox(
    "Seleziona il mese",
    list(mesi.keys())
)

mese = mesi[mese_nome]

anno = st.number_input(
    "Anno",
    min_value=2025,
    max_value=2035,
    value=2026,
    step=1
)


# ============================================================
# GENERA CALENDARIO STANDARD
# ============================================================

if st.button("Genera calendario"):

    lezioni_mese = []

    numero_giorni = calendar.monthrange(
        int(anno),
        mese
    )[1]

    for giorno in range(1, numero_giorni + 1):

        data_lezione = date(
            int(anno),
            mese,
            giorno
        )

        for lezione in calendario_standard:

            if data_lezione.weekday() == lezione["giorno_settimana"]:

                codice = lezione["lezione"]

                lezioni_mese.append({
                    "data": data_lezione,
                    "ora": lezione["ora"],
                    "codice": codice,
                    "descrizione": tipi_lezione[codice]["descrizione"],
                    "durata": tipi_lezione[codice]["durata"]
                })

    st.session_state.lezioni_mese = lezioni_mese
    st.session_state.mese = mese
    st.session_state.anno = int(anno)
    st.session_state.mese_nome = mese_nome


# ============================================================
# MOSTRA CALENDARIO
# ============================================================

if st.session_state.lezioni_mese:

    st.success(
        f"Calendario di "
        f"{st.session_state.mese_nome} "
        f"{st.session_state.anno} generato!"
    )

    st.subheader("Lezioni del mese")

    df = pd.DataFrame(
        st.session_state.lezioni_mese
    )

    df_visualizza = df.copy()

    df_visualizza["data"] = df_visualizza["data"].apply(
        lambda x: x.strftime("%d/%m/%Y")
    )

    df_visualizza.columns = [
        "Data",
        "Ora",
        "Codice",
        "Descrizione",
        "Durata"
    ]

    st.dataframe(
        df_visualizza,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # AGGIUNGI LEZIONE EXTRA
    # ========================================================

    st.subheader("Aggiungi lezione extra")

    codice_extra = st.selectbox(
        "Tipo di lezione",
        list(tipi_lezione.keys()),
        format_func=lambda codice:
            f"{codice} - "
            f"{tipi_lezione[codice]['descrizione']}"
    )

    numero_giorni = calendar.monthrange(
        st.session_state.anno,
        st.session_state.mese
    )[1]

    giorno_extra = st.number_input(
        "Giorno del mese",
        min_value=1,
        max_value=numero_giorni,
        value=1,
        step=1
    )

    ora_extra = st.time_input(
        "Orario di inizio",
        value=time(18, 0)
    )

    if st.button("Aggiungi lezione extra"):

        nuova_lezione = {
            "data": date(
                st.session_state.anno,
                st.session_state.mese,
                int(giorno_extra)
            ),
            "ora": ora_extra.strftime("%H:%M"),
            "codice": codice_extra,
            "descrizione":
                tipi_lezione[codice_extra]["descrizione"],
            "durata":
                tipi_lezione[codice_extra]["durata"]
        }

        st.session_state.lezioni_mese.append(
            nuova_lezione
        )

        st.session_state.lezioni_mese.sort(
            key=lambda x: (
                x["data"],
                x["ora"]
            )
        )

        st.success("Lezione extra aggiunta.")


        

        st.rerun()

            # ========================================================
    # LEZIONI NON FATTE
    # ========================================================

    st.subheader("Lezioni non fatte")

    giorno_rimozione = st.number_input(
        "Giorno delle lezioni non fatte",
        min_value=1,
        max_value=numero_giorni,
        value=1,
        step=1,
        key="giorno_rimozione"
    )

    data_rimozione = date(
        st.session_state.anno,
        st.session_state.mese,
        int(giorno_rimozione)
    )

    lezioni_giorno = [
        lezione
        for lezione in st.session_state.lezioni_mese
        if lezione["data"] == data_rimozione
    ]

    if len(lezioni_giorno) == 0:

        st.info(
            "Non risultano lezioni in questo giorno."
        )

    else:

        st.write(
            f"Lezioni del "
            f"{giorno_rimozione:02d}/"
            f"{st.session_state.mese:02d}/"
            f"{st.session_state.anno}"
        )

        opzioni_rimozione = []

        for i, lezione in enumerate(lezioni_giorno):

            etichetta = (
                f"{lezione['ora']} - "
                f"{lezione['codice']} - "
                f"{lezione['descrizione']}"
            )

            opzioni_rimozione.append(
                (i, etichetta)
            )

        lezioni_da_rimuovere = st.multiselect(
            "Seleziona le lezioni non fatte",
            options=opzioni_rimozione,
            format_func=lambda x: x[1]
        )

        if st.button(
            "Rimuovi lezioni selezionate"
        ):

            for indice, etichetta in lezioni_da_rimuovere:

                lezione_da_rimuovere = lezioni_giorno[indice]

                st.session_state.lezioni_mese.remove(
                    lezione_da_rimuovere
                )

            st.success(
                "Lezioni rimosse."
            )

            st.rerun()

    # ========================================================
    # RIEPILOGO
    # ========================================================

    st.subheader("Riepilogo")

    count_45 = sum(
        1
        for lezione in st.session_state.lezioni_mese
        if lezione["durata"] == 45
    )

    count_60 = sum(
        1
        for lezione in st.session_state.lezioni_mese
        if lezione["durata"] == 60
    )

    totale_lezioni = len(
        st.session_state.lezioni_mese
    )

    minuti_totali = sum(
        lezione["durata"]
        for lezione in st.session_state.lezioni_mese
    )

    ore = minuti_totali // 60
    minuti = minuti_totali % 60

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Lezioni 45 min",
            count_45
        )

    with col2:
        st.metric(
            "Lezioni 60 min",
            count_60
        )

    with col3:
        st.metric(
            "Totale lezioni",
            totale_lezioni
        )

    st.write(
        f"**Totale ore lavorate: {ore} h {minuti} min**"
    )

    # ========================================================
    # DOWNLOAD CSV
    # ========================================================

    st.subheader("Scarica report")

    df_csv = pd.DataFrame(
        st.session_state.lezioni_mese
    ).copy()

    df_csv["data"] = df_csv["data"].apply(
        lambda x: x.strftime("%d/%m/%Y")
    )

    df_csv.columns = [
        "Data",
        "Ora",
        "Codice",
        "Descrizione",
        "Durata"
    ]

    csv = df_csv.to_csv(
        index=False
    ).encode("utf-8-sig")

    nome_file = (
        f"Lezioni_Report_"
        f"{st.session_state.mese_nome}_"
        f"{st.session_state.anno}.csv"
    )

    st.download_button(
        label="Scarica CSV",
        data=csv,
        file_name=nome_file,
        mime="text/csv"
    )
