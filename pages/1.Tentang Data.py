"""
DOKUMENTASI STRUKTUR DATA IOT & LOGIKA CLEANING
File Referensi: DataFix_IOT_BigData.datasensor.csv
"""

import pandas as pd
import numpy as np

# ==============================================================================
# 1. CONTOH DATA MENTAH (RAW DATA)
# ==============================================================================
# Ini adalah representasi satu baris data seperti yang keluar dari database/CSV.
# Penjelasan ada di komentar (#).

raw_data_sample = {
    # --- METADATA (Identitas) ---
    "_id": "693d02ae67adc5b89e184193",  # Tipe: String (ObjectId). ID Unik dari MongoDB. 
                                        # ACTION: Biasanya di-drop di dashboard karena tidak visual.
    
    "device": "ESP8266-Sensors",        # Tipe: String. Nama perangkat pengirim.
                                        # ACTION: Berguna untuk filter jika punya banyak alat.

    "timestamp": "2025-12-13|06:07:35", # Tipe: String. Waktu pengambilan data.
                                        # MASALAH: Menggunakan simbol '|' (pipa) sebagai pemisah.
                                        # ACTION: Wajib di-replace '|' jadi ' ' agar bisa jadi DateTime.

    # --- SENSOR LINGKUNGAN (Numerik) ---
    # Tipe: Float (Angka Desimal). Siap divisualisasikan.
    "temperature": 29.68,  # Suhu (Celcius)
    "humidity": 64.76,     # Kelembaban (%)
    "NH3": 1.68,           # Gas Amonia (PPM)
    "CO": 2.78,            # Gas Karbon Monoksida (PPM)
    "NO2": 0.21,           # Gas Nitrogen Dioksida (PPM)
    "CO2": 588.76,         # Gas Karbon Dioksida (PPM)

    # --- HASIL AI / CLUSTERING ---
    # Tipe: Float & String. Bisa kosong (NaN) jika AI belum memproses baris ini.
    "cluster": 2.0,                         # ID Kelompok (0, 1, 2). Digunakan untuk warna Scatter Plot.
    "kategori": "Kualitas Udara Sedang",    # Label Manusia. Digunakan untuk teks status/alert.
}

# ==============================================================================
# 2. LOGIKA PEMROSESAN (DATA PROCESSING)
# ==============================================================================
# Fungsi ini menerjemahkan "cerita" data di atas menjadi kode Python pandas.

def process_iot_data(data_list):
    # 1. Load Data ke DataFrame
    df = pd.DataFrame(data_list)
    
    # 2. CLEANING WAKTU (Bagian paling krusial dari data ini)
    # Penjelasan: Mengubah "2025-12-13|06:07:35" menjadi object datetime Python
    if 'timestamp' in df.columns:
        # Step A: Buang karakter '|' yang aneh
        df['timestamp'] = df['timestamp'].astype(str).str.replace('|', ' ')
        
        # Step B: Ubah jadi format waktu standar agar bisa di-plot di Sumbu X
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 3. HANDLING DATA KOSONG (Clustering)
    # Penjelasan: Tidak semua data punya label cluster (NaN).
    # Kita isi default agar kode tidak error saat plotting.
    if 'kategori' in df.columns:
        df['kategori'] = df['kategori'].fillna("Belum Teridentifikasi")
        
    if 'cluster' in df.columns:
        df['cluster'] = df['cluster'].fillna(-1) # -1 menandakan 'Noise' atau 'Unknown'

    return df

# ==============================================================================
# 3. PENERAPAN DI VISUALISASI (CONTOH)
# ==============================================================================
# Bagaimana data di atas dipetakan ke Grafik Streamlit/Plotly?

"""
TENTANG DATA:

# --- METADATA (Identitas) ---
    "_id": "693d02ae67adc5b89e184193",  # Tipe: String (ObjectId). ID Unik dari MongoDB. 
                                        # ACTION: Biasanya di-drop di dashboard karena tidak visual.
    
    "device": "ESP8266-Sensors",        # Tipe: String. Nama perangkat pengirim.
                                        # ACTION: Berguna untuk filter jika punya banyak alat.

    "timestamp": "2025-12-13|06:07:35", # Tipe: String. Waktu pengambilan data.
                                        # MASALAH: Menggunakan simbol '|' (pipa) sebagai pemisah.
                                        # ACTION: Wajib di-replace '|' jadi ' ' agar bisa jadi DateTime.

# --- SENSOR LINGKUNGAN (Numerik) ---
    # Tipe: Float (Angka Desimal). Siap divisualisasikan.
    "temperature": 29.68,  # Suhu (Celcius)
    "humidity": 64.76,     # Kelembaban (%)
    "NH3": 1.68,           # Gas Amonia (PPM)
    "CO": 2.78,            # Gas Karbon Monoksida (PPM)
    "NO2": 0.21,           # Gas Nitrogen Dioksida (PPM)
    "CO2": 588.76,         # Gas Karbon Dioksida (PPM)

"""