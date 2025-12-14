import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Tren Gas Berdasarkan Tanggal (CSV)", layout="wide")

# --- 1. FUNGSI LOAD & CLEAN DATA DARI CSV ---
@st.cache_data
def load_and_clean_data():
    try:
        # Ganti nama file sesuai nama file Anda
        df = pd.read_csv('DataFix_IOT_BigData.datasensor.csv')
        
        # PEMBERSIHAN TIMESTAMP (Ganti '|' dengan ' ' agar bisa dibaca DateTime)
        df['timestamp'] = df['timestamp'].astype(str).str.replace('|', ' ')
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Pastikan kolom gas numerik dan isi NaN dengan 0 untuk keamanan
        gas_cols = ['CO2', 'CO', 'NH3', 'NO2']
        for col in gas_cols:
             if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        # Urutkan berdasarkan waktu
        return df.sort_values('timestamp')
        
    except FileNotFoundError:
        st.error("File CSV 'DataFix_IOT_BigData.datasensor.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
        return pd.DataFrame()
        
df = load_and_clean_data()

# --- 2. VISUALISASI UTAMA ---
st.title("📈 Analisis Waktu Gas")

if not df.empty:
    
    # Filter dan agregasi data per hari (jika ingin melihat tren harian)
    # df['tanggal'] = df['timestamp'].dt.date
    # df_daily = df.groupby('tanggal')[['CO2', 'CO', 'NH3', 'NO2']].mean().reset_index()
    # Pilihan: Tampilkan data detail per detik/menit (lebih akurat)
    
    gas_cols_list = ['CO2', 'CO', 'NH3', 'NO2']
    
    # Select Box untuk memilih gas
    target_gas = st.selectbox(
        "",
        gas_cols_list,
        index=0 # Default CO2
    )

    if target_gas in df.columns:
        # Membuat Grafik Garis (Time Series)
        fig_gas = px.line(
            df, 
            x='timestamp', 
            y=target_gas, 
            title=f"Tren Konsentrasi {target_gas} Berdasarkan Waktu",
            template="plotly_dark",
            markers=False # Garis tanpa titik-titik
        )
        
        # Label Sumbu Y
        fig_gas.update_yaxes(title=f"Konsentrasi {target_gas} (PPM)")
        
        st.plotly_chart(fig_gas, use_container_width=True)
        
    else:
        st.error(f"Kolom '{target_gas}' tidak ditemukan dalam data.")
        
else:
    st.warning("Gagal memuat data atau file CSV kosong.")