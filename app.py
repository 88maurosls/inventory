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

if 'last_file_name' not in st.session_state:
    st.session_state['last_file_name'] = "barcodes.xlsx"

# Funzione per esportare i dati in un file Excel
def export_to_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df = pd.DataFrame(data, columns=['Barcode'])
        df.to_excel(writer, index=False, sheet_name='Barcodes')
    output.seek(0)
    return output

# Funzione per rimuovere i barcode selezionati
def remove_selected_barcodes(selected_indices):
    for index in sorted(selected_indices, reverse=True):
        del st.session_state['barcodes'][index]

# Titolo dell'app
st.title("Gestore Codici a Barre")

# Inserimento del codice a barre
barcode = st.text_input("Inserisci un barcode")
if st.button("Aggiungi Barcode"):
    if barcode:
        st.session_state['barcodes'].append(barcode)
        st.success(f"Barcode {barcode} aggiunto con successo!")
    else:
        st.error("Per favore, inserisci un barcode valido.")

# Visualizzazione e gestione dei codici a barre inseriti
st.subheader("Gestione Codici a Barre Inseriti")
if st.session_state['barcodes']:
    df = pd.DataFrame(st.session_state['barcodes'], columns=['Barcode'])
    df.index += 1  # Aggiusta l'indice per partire da 1

    # Selezione di un solo barcode da eliminare con opzione vuota
    options = ["Seleziona un barcode"] + df['Barcode'].tolist()
    selected_barcode = st.selectbox("Seleziona il barcode da eliminare:", options)

    # Pulsante per avviare la conferma di eliminazione
    if st.button("Elimina Barcode Selezionato"):
        if selected_barcode != "Seleziona un barcode":
            st.session_state['confirm_delete'] = True
            st.session_state['barcode_to_delete'] = selected_barcode
        else:
            st.warning("Seleziona un barcode valido per l'eliminazione.")

    # Mostra il pulsante di conferma
    if st.session_state['confirm_delete']:
        barcode_to_delete = st.session_state['barcode_to_delete']
        st.warning(f"Sei sicuro di voler eliminare il barcode: {barcode_to_delete}?")
        if st.button("Conferma Eliminazione"):
            st.session_state['barcodes'].remove(barcode_to_delete)
            st.success("Barcode selezionato eliminato con successo!")
            st.session_state['confirm_delete'] = False
            st.session_state['barcode_to_delete'] = None
        elif st.button("Annulla Eliminazione"):
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

# Esportazione in Excel e Download
st.subheader("Esporta e Scarica Codici a Barre")
file_name = st.text_input("Nome del file Excel", value=st.session_state['last_file_name'])
if file_name:
    st.session_state['last_file_name'] = file_name

if st.session_state['barcodes']:
    excel_file = export_to_excel(st.session_state['barcodes'])
    st.download_button(label="Scarica il file Excel",
                       data=excel_file,
                       file_name=st.session_state['last_file_name'],
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.error("Nessun barcode da esportare.")
