
import pandas as pd
import streamlit as st

def export_csv(data, filename="export.csv"):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📁 Exportar CSV",
        data=csv,
        file_name=filename,
        mime='text/csv'
    )
