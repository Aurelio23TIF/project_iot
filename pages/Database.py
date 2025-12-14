import streamlit as st
import pandas as pd
from connection import get_data
import time

st.set_page_config(page_title="Database Log", page_icon="📄", layout="wide")

st.title("📄 Log Data Lengkap")

# Sidebar khusus halaman ini
with st.sidebar:
    st.header("Pengaturan Tabel")
    limit = st.selectbox("Tampilkan Baris:", [100, 500, 1000, "Semua Data"], index=0)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False) # Default mati untuk analisis
    
    

# Load Data
raw_data = get_data(limit_val)
if raw_data:
    df = pd.DataFrame(raw_data)
    if '_id' in df.columns: df = df.drop(columns=['_id'])
    
    # Tombol Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV",
        csv,
        "data_iot.csv",
        "text/csv",
        key='download-csv'
    )
    
    st.dataframe(df, use_container_width=True, height=700)
else:
    st.info("Data tidak ditemukan.")