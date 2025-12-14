import streamlit as st
import pandas as pd
import plotly.express as px
import time
from connection import get_data

st.set_page_config(page_title="Dashboard Grafik", page_icon="📈", layout="wide")

# --- FUNGSI LOAD DATA ---
def load_data(limit):
    raw_data = get_data(limit)
    if not raw_data: return pd.DataFrame()
    df = pd.DataFrame(raw_data)
    if '_id' in df.columns: df = df.drop(columns=['_id'])
    df = df.iloc[::-1].reset_index(drop=True)
    df['Urutan'] = df.index
    return df

# --- SIDEBAR KHUSUS HALAMAN INI ---
with st.sidebar:
    st.header("Isi Jumlah Data")
    limit = st.selectbox("Jumlah Data:", [50, 100, 500, "Semua Data"], index=0)
    limit_val = 0 if limit == "Semua Data" else limit
    auto_refresh = st.toggle("🔴 Live Auto-Refresh", value=True)

# --- TAMPILAN UTAMA ---
st.title("📈 Dashboard Real-Time")
placeholder = st.empty()

# Logic Auto Refresh
if auto_refresh:
    while True:
        df = load_data(limit_val)
        with placeholder.container():
            if not df.empty:
                latest = df.iloc[-1]
                # KPI
                k1, k2, k3= st.columns(3)
                k1.metric("Suhu", f"{latest.get('temperature')} °C")
                k2.metric("Lembap", f"{latest.get('humidity')} %")
                status = latest.get('kategori_who', '-')
                warna = "🟢" if "Baik" in status else "🔴"
                k3.metric("Status", f"{warna} {status}")
                
                # Grafik
                c1, c2, c3 = st.columns(3)
                # Key unik pakai time.time() biar gak error
                unik = time.time()
                with c1:
                    st.plotly_chart(px.line(df, x='Urutan', y=['temperature','humidity']), use_container_width=True, key=f"g1_{unik}")
                with c2:
                    st.plotly_chart(px.area(df, x='Urutan', y=['CO','NH3']), use_container_width=True, key=f"g2_{unik}")
                with c3:
                    st.plotly_chart(px.area(df, x='Urutan', y=['CO2','NO2']), use_container_width=True, key=f"g3_{unik}")
            else:
                st.warning("Data Kosong")
        time.sleep(3)
else:
    # Tampilan Statis (Jika auto refresh mati)
    df = load_data(limit_val)
    if not df.empty:
        latest = df.iloc[-1]
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Suhu", f"{latest.get('temperature')} °C")
        k2.metric("Lembap", f"{latest.get('humidity')} %")
        k3.metric("Status", latest.get('kategori', '-'))
        
        c1, c2, c3 = st.columns(2)
        with c1: st.plotly_chart(px.line(df, x='Urutan', y=['temperature','humidity']), use_container_width=True)
        with c2: st.plotly_chart(px.area(df, x='Urutan', y=['CO','NH3']), use_container_width=True)
        with c3: st.plotly_chart(px.area(df, x='Urutan', y=['CO2','NO2']), use_container_width=True)