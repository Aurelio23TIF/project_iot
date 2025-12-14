import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection import get_data

st.set_page_config(page_title="Profil Cluster", page_icon="〰️", layout="wide")

with st.sidebar:
    st.header("⚙️ Pengaturan Dashboard")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=1)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=False)

st.title("〰️ Profil Karakteristik Cluster (Parallel Coordinates)")
st.write("Grafik ini menunjukkan pola nilai sensor. Ikuti garis warna untuk melihat karakteristik setiap cluster.")

placeholder = st.empty()

def render_chart():
    raw_data = get_data(limit_val)
    if not raw_data:
        st.warning("Data Kosong")
        return

    df = pd.DataFrame(raw_data)
    if '_id' in df.columns: df = df.drop(columns=['_id'])
    
    sensor_cols = ['temperature', 'humidity', 'CO', 'NH3', 'NO2', 'CO2']
    for c in sensor_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

    if 'kategori_cluster' in df.columns:
        # Parallel Coordinates butuh warna dalam bentuk ANGKA, bukan String.
        # Kita buat mapping manual agar warnanya konsisten.
        list_cluster = df['kategori_cluster'].unique()
        # Contoh map: {'Cluster 0': 0, 'Cluster 1': 1}
        cat_map = {val: i for i, val in enumerate(list_cluster)}
        
        df['Cluster_ID'] = df['kategori_cluster'].map(cat_map)
        
        # Gabung Label untuk Hover (biar user tau ID 0 itu Cluster apa)
        df['Label_Hover'] = df['kategori_cluster'].astype(str) 
        if 'kategori_who' in df.columns:
             df['Label_Hover'] += " (" + df['kategori_who'].astype(str) + ")"

        fig = px.parallel_coordinates(
            df, 
            dimensions=sensor_cols, # Menampilkan semua sensor
            color="Cluster_ID",
            title="Pola Sensor per Cluster",
            template="plotly_dark",
            color_continuous_scale=px.colors.diverging.Tealrose, # Skala warna
        )
        
        # Hilangkan color bar angka karena agak membingungkan user awam,
        # kita ganti dengan keterangan teks di bawah chart
        fig.update_layout(coloraxis_showscale=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Buat Legenda Manual agar user tahu ID warna
        st.markdown("### 🏷️ Keterangan Warna (Cluster ID)")
        cols = st.columns(len(cat_map))
        for idx, (nama_cluster, id_cluster) in enumerate(cat_map.items()):
            with cols[idx]:
                st.metric(label=f"ID Warna: {id_cluster}", value=nama_cluster)

    else:
        st.error("Data kategori_cluster tidak ditemukan.")

if auto_refresh:
    while True:
        with placeholder.container():
            render_chart()
        time.sleep(3)
else:
    with placeholder.container():
        render_chart()