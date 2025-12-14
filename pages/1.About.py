import streamlit as st

st.set_page_config(page_title="Analisis Clustering Kualitas Udara dan Evaluasi Risiko Kesehatan Berbasis Standar WHO pada Data Sensor IoT", page_icon="")

st.title("💡 Tentang Proyek: Big Data Pipeline untuk Kualitas Udara")
st.markdown("---")

# ==============================================================================
# RINGKASAN LATAR BELAKANG
# ==============================================================================
st.header("Latar Belakang")

st.markdown("""
Perkembangan teknologi **Internet of Things (IoT)** menghasilkan volume dan kecepatan data sensor yang sangat tinggi, memenuhi karakteristik **Big Data** (Volume dan Velocity).
""")
st.info("""
Proyek ini mengatasi tantangan pengelolaan data sensor kualitas udara indoor (Suhu, Kelembapan, dan Gas: NH₃, NO₂, CO, CO₂) yang bersifat real-time dan multivariat.
""")
st.markdown("""
Diperlukan **Big Data Pipeline** yang terintegrasi untuk mengubah data mentah yang berskala besar menjadi informasi yang bermakna. Pipeline ini digunakan sebagai fondasi untuk **analisis clustering** dan **evaluasi risiko kesehatan** berdasarkan standar **World Health Organization (WHO)**.
""")

st.markdown("---")

# ==============================================================================
# TUJUAN
# ==============================================================================
st.header("Tujuan Proyek")

st.subheader("Merancang & Mengimplementasikan Big Data Pipeline")
st.markdown("""
Tujuan utama proyek ini adalah merancang dan mengimplementasikan arsitektur Big Data Pipeline yang komprehensif, mencakup tahapan:
""")
st.markdown("""
* **Data Ingestion** (Akuisisi Data Sensor IoT).
* **Data Preprocessing** (ETL).
* **Data Storage** (Penyimpanan).
* **Data Visualization** (Visualisasi Data).
""")
st.markdown("""
Selain itu, proyek ini bertujuan untuk:
""")
st.markdown("""
* Melakukan analisis deskriptif dan visualisasi untuk mengidentifikasi pola dan anomali data.
* Menerapkan teknik **K-Means Clustering** untuk mengelompokkan kondisi kualitas udara.
* Melakukan **evaluasi risiko** dengan membandingkan hasil clustering terhadap **ambang batas kualitas udara WHO**.
""")

st.markdown("---")

# ==============================================================================
# MANFAAT
# ==============================================================================


