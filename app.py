import streamlit as st
import pandas as pd
from io import BytesIO

# Stato dell'applicazione
if 'barcodes' not in st.session_state:
    st.session_state['barcodes'] = []

# Funzione per esportare i dati in un file Excel
def export_to_excel(data, file_name):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.DataFrame(data, columns=['Barcode'])
    df.to_excel(writer, index=False, sheet_name='Barcodes')
    writer.save()
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

# Visualizzazione dei codici a barre inseriti
st.subheader("Anteprima Codici a Barre Inseriti")
if st.session_state['barcodes']:
    df = pd.DataFrame(st.session_state['barcodes'], columns=['Barcode'])
    selected_rows = st.multiselect("Seleziona i barcode da eliminare:", df.index, format_func=lambda x: df.iloc[x]['Barcode'])

    st.dataframe(df, use_container_width=True)

    # Pulsante per eliminare i barcode selezionati
    if st.button("Elimina Barcode Selezionati"):
        if selected_rows:
            remove_selected_barcodes(selected_rows)
            st.success("Barcode selezionati eliminati con successo!")
        else:
            st.warning("Nessun barcode selezionato per l'eliminazione.")
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
