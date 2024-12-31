import streamlit as st
import pandas as pd
from io import BytesIO

# Stato dell'applicazione
if 'barcodes' not in st.session_state:
    st.session_state['barcodes'] = []
if 'confirm_delete' not in st.session_state:
    st.session_state['confirm_delete'] = False
if 'barcode_to_delete' not in st.session_state:
    st.session_state['barcode_to_delete'] = None

# Funzione per esportare i dati in un file Excel
def export_to_excel(data, file_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.DataFrame(data, columns=['Barcode'])
    df.to_excel(writer, index=False, sheet_name='Barcodes')
    writer.save()
    output.seek(0)
    return output

# Funzione per rimuovere un barcode selezionato
def remove_selected_barcode(index):
    del st.session_state['barcodes'][index]

# Titolo dell'app
st.title("Gestione Codici a Barre")

# Inserimento del codice a barre
barcode = st.text_input("Inserisci un barcode")
if st.button("Aggiungi Barcode"):
    if barcode:
        st.session_state['barcodes'].append(barcode)
        st.success(f"Barcode {barcode} aggiunto con successo!")
    else:
        st.error("Per favore, inserisci un barcode valido.")

# Visualizzazione e gestione dei codici a barre inseriti
st.subheader("Codici a Barre Inseriti")
if st.session_state['barcodes']:
    df = pd.DataFrame(st.session_state['barcodes'], columns=['Barcode'])
    df.index += 1  # Aggiusta l'indice per partire da 1

    # Selezione di un solo barcode da eliminare
    selected_row = st.selectbox(
        "Seleziona il barcode da eliminare:",
        options=["Seleziona un barcode"] + list(df.index),
        format_func=lambda x: "Seleziona un barcode" if x == "Seleziona un barcode" else df.loc[x - 1, 'Barcode'] if isinstance(x, int) else None
    )

    # Mostra il pulsante di eliminazione solo se è selezionato un barcode valido
    if st.button("Elimina Barcode Selezionato"):
        if selected_row != "Seleziona un barcode":
            st.session_state['confirm_delete'] = True
            st.session_state['barcode_to_delete'] = selected_row - 1
        else:
            st.warning("Seleziona un barcode valido per l'eliminazione.")

    # Mostra il messaggio di conferma
    if st.session_state['confirm_delete']:
        barcode_to_confirm = st.session_state['barcodes'][st.session_state['barcode_to_delete']]
        st.warning(f"Sei sicuro di voler eliminare il barcode: {barcode_to_confirm}?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Conferma Eliminazione"):
                remove_selected_barcode(st.session_state['barcode_to_delete'])
                st.session_state['confirm_delete'] = False
                st.session_state['barcode_to_delete'] = None
                st.success("Barcode eliminato con successo!")
        with col2:
            if st.button("Annulla"):
                st.session_state['confirm_delete'] = False
                st.session_state['barcode_to_delete'] = None

    # Visualizza la tabella aggiornata
    if st.session_state['barcodes']:
        df = pd.DataFrame(st.session_state['barcodes'], columns=['Barcode'])
        df.index += 1  # Ripristina l'indice per partire da 1
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nessun barcode inserito.")
else:
    st.info("Nessun barcode inserito.")

# Esportazione in Excel
st.subheader("Esporta Codici a Barre")
file_name = st.text_input("Nome del file Excel", value="barcodes.xlsx")
if st.button("Esporta in Excel"):
    if st.session_state['barcodes']:
        excel_file = export_to_excel(st.session_state['barcodes'], file_name)
        st.download_button(label="Scarica il file Excel",
                           data=excel_file,
                           file_name=file_name,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("Nessun barcode da esportare.")
