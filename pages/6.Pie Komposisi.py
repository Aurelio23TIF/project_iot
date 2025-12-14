import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import get_data

st.set_page_config(page_title="Komposisi Cluster", page_icon="🍰", layout="wide")

# --- SIDEBAR KHUSUS HALAMAN INI ---
with st.sidebar:
    st.header("Isi Jumlah Data")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=0)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False)

# --- KONTEN UTAMA ---
st.title("🍰 Komposisi Data Cluster")

placeholder = st.empty()

def render_chart():
    raw_data = get_data(limit_val)
    if not raw_data:
        st.warning("Data Kosong")
        return

    df = pd.DataFrame(raw_data)
    
    # Hitung jumlah data per kategori cluster
    if 'kategori_cluster' in df.columns:
        df_count = df['kategori_cluster'].value_counts().reset_index()
        df_count.columns = ['kategori_cluster', 'jumlah']

        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("### Detail Angka")
            st.dataframe(df_count, hide_index=True, use_container_width=True)

        with c2:
            fig = px.pie(
                df_count, 
                values='jumlah', 
                names='kategori_cluster', 
                title='Persentase Cluster',
                hole=0.4, # Donut chart
                template="plotly_dark"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Kolom 'kategori_cluster' tidak ditemukan di data.")

# Logika Refresh
if auto_refresh:
    while True:
        with placeholder.container():
            render_chart()
        time.sleep(3)
else:
    with placeholder.container():
        render_chart()