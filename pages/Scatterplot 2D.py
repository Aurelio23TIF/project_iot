import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

# Menambahkan path agar bisa import dari folder parent (connection.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import get_data

st.set_page_config(page_title="Scatter Plot 2D", page_icon="📍", layout="wide")

# --- SIDEBAR KHUSUS HALAMAN INI (Sesuai Request) ---
with st.sidebar:
    st.header("⚙️ Pengaturan Dashboard")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=1) # Default 100 biar ringan
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False) # Default mati untuk analisis

# --- KONTEN UTAMA ---
st.title("📍 Scatter Plot (Korelasi Sensor)")

# Pilihan Sumbu X dan Y (Ditaruh diluar loop agar tidak ter-reset saat refresh)
col_set1, col_set2 = st.columns(2)
sensor_cols = ['temperature', 'humidity', 'CO', 'NH3', 'NO2', 'CO2']
with col_set1:
    x_axis = st.selectbox("Pilih Sumbu X", sensor_cols, index=0)
with col_set2:
    y_axis = st.selectbox("Pilih Sumbu Y", sensor_cols, index=5)

# Container untuk visualisasi
placeholder = st.empty()

def render_chart():
    # Load Data
    raw_data = get_data(limit_val)
    if not raw_data: 
        st.warning("Data Kosong")
        return

    df = pd.DataFrame(raw_data)
    if '_id' in df.columns: df = df.drop(columns=['_id'])
    
    # Konversi ke numerik
    for c in sensor_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

    # Buat Chart
    fig = px.scatter(
        df, 
        x=x_axis, 
        y=y_axis, 
        color="kategori_cluster", # Sesuai screenshot data Anda
        title=f"Hubungan {x_axis} vs {y_axis}",
        template="plotly_dark",
        hover_data=sensor_cols
    )
    st.plotly_chart(fig, use_container_width=True)

# Logika Refresh
if auto_refresh:
    while True:
        with placeholder.container():
            render_chart()
        time.sleep(3)
else:
    with placeholder.container():
        render_chart()