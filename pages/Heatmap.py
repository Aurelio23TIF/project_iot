import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import get_data

st.set_page_config(page_title="Matrix Korelasi", page_icon="🔥", layout="wide")

with st.sidebar:
    st.header("⚙️ Pengaturan Dashboard")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=1)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False)

st.title("🔥 Heatmap Korelasi Sensor")


placeholder = st.empty()

def render_chart():
    raw_data = get_data(limit_val)
    if not raw_data:
        st.warning("Data Kosong")
        return

    df = pd.DataFrame(raw_data)
    sensor_cols = ['temperature', 'humidity', 'CO', 'NH3', 'NO2', 'CO2']
    
    # Bersihkan data
    valid_cols = []
    for c in sensor_cols:
        if c in df.columns: 
            df[c] = pd.to_numeric(df[c], errors='coerce')
            valid_cols.append(c)
    
    if len(valid_cols) > 1:
        # Hitung Matriks Korelasi
        corr_matrix = df[valid_cols].corr()

        fig = px.imshow(
            corr_matrix,
            text_auto=".2f", # Tampilkan angka 2 desimal
            aspect="auto",
            color_continuous_scale="RdBu_r", # Merah ke Biru
            title="Matriks Korelasi Antar Sensor",
            template="plotly_dark",
            origin='lower'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data sensor tidak cukup untuk korelasi.")

if auto_refresh:
    while True:
        with placeholder.container():
            render_chart()
        time.sleep(3)
else:
    with placeholder.container():
        render_chart()