import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualisasi Timestamp", layout="wide")

# --- 1. LOAD & CLEAN DATA ---
@st.cache_data
def load_data():
    # Ganti nama file sesuai file Anda di VS Code
    df = pd.read_csv('DataFix_IOT_BigData.datasensor.csv')
    
    # PEMBERSIHAN TIMESTAMP (CRITICAL STEP)
    df['timestamp'] = df['timestamp'].astype(str).str.replace('|', ' ')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Ekstrak komponen waktu untuk analisis
    df['jam'] = df['timestamp'].dt.hour
    df['tanggal'] = df['timestamp'].dt.date
    df['hari_nama'] = df['timestamp'].dt.day_name()
    
    # Pastikan kolom numerik (diperlukan untuk selectbox dinamis)
    num_cols = ['temperature', 'humidity', 'NH3', 'CO', 'NO2', 'CO2']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.sort_values('timestamp')

df = load_data()

st.title("⏳ Analisis Waktu")
st.write(f"Total Data: **{len(df)}** baris | Rentang Waktu: **{df['timestamp'].min()}** s/d **{df['timestamp'].max()}**")

# --- 2. PILIHAN VISUALISASI ---
tab1, tab2 = st.tabs(["📈 Tren Sensor (Time Series)", "📊 Volume Data per Jam"])

# --- TAB 1: TIME SERIES (DENGAN DROPDOWN) ---
with tab1:
    st.subheader("Tren Sensor Seiring Waktu")
    st.write("")

    # --- PERUBAHAN UTAMA 1: Tambahkan semua sensor ke options ---
    sensor_options = ['temperature', 'humidity'] 
    
    # Memilih lebih dari satu variabel (multiselect)
    selected_vars = st.multiselect(
        "",
        options=sensor_options,
        default=['temperature', 'humidity'] # Default saat pertama kali dibuka
    )
    
    # Downsample data jika terlalu banyak (mengambil 1 data setiap 5 baris)
    df_chart = df.iloc[::5, :] 
    
    if selected_vars:
        
        fig = px.line(
            df_chart, 
            x='timestamp', 
            # Menggunakan variabel yang dipilih pengguna
            y=selected_vars, 
            title=f"Fluktuasi {', '.join(selected_vars)} (Time Series)",
            template="plotly_dark"
        )
        fig.update_layout(legend_title="Parameter") 
        st.plotly_chart(fig, use_container_width=True)
    # --- PERUBAHAN UTAMA 2: Blok 'else' dihilangkan ---


# --- TAB 2: HISTOGRAM (Kapan sensor paling aktif?) ---
with tab2:
    st.subheader("Jumlah Data Masuk per Jam")
    
    # Hitung jumlah data per jam
    df_per_jam = df.groupby('jam').size().reset_index(name='jumlah_data')
    
    fig = px.bar(
        df_per_jam,
        x='jam',
        y='jumlah_data',
        title="Distribusi Data Berdasarkan Jam (0-23)",
        template="plotly_dark",
        color='jumlah_data',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis=dict(tickmode='linear', dtick=1)) # Tampilkan semua angka jam
    st.plotly_chart(fig, use_container_width=True)