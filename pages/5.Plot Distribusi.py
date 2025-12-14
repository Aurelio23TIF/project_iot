import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import get_data

st.set_page_config(page_title="Distribusi Data", page_icon="📊", layout="wide")

# --- SIDEBAR KHUSUS HALAMAN INI ---
with st.sidebar:
    st.header("Isi Jumlah Data")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=0)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False)

# --- KONTEN UTAMA ---
st.title("📊 Plot Distribusi (Box Plot)")

# Pilihan Sensor
sensor_cols = ['temperature', 'humidity', 'CO', 'NH3', 'NO2', 'CO2']
target_sensor = st.selectbox("Pilih Sensor untuk Dianalisis:", sensor_cols, index=5)

placeholder = st.empty()

def render_chart():
    raw_data = get_data(limit_val)
    if not raw_data:
        st.warning("Data Kosong")
        return
        
    df = pd.DataFrame(raw_data)
    if '_id' in df.columns: df = df.drop(columns=['_id'])
    
    for c in sensor_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

    # Buat Chart Box Plot
    fig = px.box(
        df, 
        x="kategori_cluster", 
        y=target_sensor, 
        color="kategori_cluster",
        title=f"Distribusi Nilai {target_sensor} per Cluster",
        template="plotly_dark",
        points="all" # Menampilkan titik data asli
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