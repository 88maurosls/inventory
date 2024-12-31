
import streamlit as st
import pandas as pd
from io import BytesIO

# Stato dell'applicazione
if 'barcodes' not in st.session_state:
    st.session_state['barcodes'] = []

if 'selected_barcodes' not in st.session_state:
    st.session_state['selected_barcodes'] = []

# Funzione per esportare i dati in un file Excel
def export_to_excel(data, file_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.DataFrame(data, columns=['Barcode'])
    df.to_excel(writer, index=False, sheet_name='Barcodes')
    writer.save()
    output.seek(0)
    return output

# Titolo dell'app
st.title("Gestore Codici a Barre")

# Inserimento del codice a barre
barcode = st.text_input("Inserisci un barcode")
if st.button("Aggiungi Barcode"):
    if barcode:
        # Popup di conferma
        if st.session_state.get("confirm", False) or st.button("Conferma"):
            st.session_state['barcodes'].append(barcode)
            st.success(f"Barcode {barcode} aggiunto con successo!")
            st.session_state['confirm'] = False
        elif not st.session_state.get("confirm", False):
            st.warning(f"Confermare l'aggiunta del barcode {barcode}")
            st.session_state['confirm'] = True
    else:
        st.error("Per favore, inserisci un barcode valido.")

# Visualizzazione dei codici a barre inseriti
st.subheader("Anteprima Codici a Barre Inseriti")
if st.session_state['barcodes']:
    selected_barcodes = st.multiselect("Seleziona i barcode da eliminare:", st.session_state['barcodes'])

    # Pulsante per eliminare i barcode selezionati
    if st.button("Elimina Barcode Selezionati"):
        for barcode in selected_barcodes:
            st.session_state['barcodes'].remove(barcode)
        st.success("Barcode selezionati eliminati con successo!")
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
