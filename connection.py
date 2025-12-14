import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def init_connection():
    try:
        # Mengambil data dari secrets.toml
        uri = st.secrets["mongo"]["uri"]
        return MongoClient(uri)
    except Exception as e:
        st.error(f"Gagal konek ke DB: {e}")
        return None

# Kita tambahkan parameter 'limit' (default 50)
def get_data(limit=1000):
    client = init_connection()
    if client:
        db_name = st.secrets["mongo"]["db"]
        col_name = st.secrets["mongo"]["collection"]
        db = client[db_name]
        collection = db[col_name]
        
        # Logika: Jika limit 0, ambil semua. Jika tidak, ambil sesuai limit.
        if limit == 0:
            items = list(collection.find().sort("_id", -1)) # AMBIL SEMUA
        else:
            items = list(collection.find().sort("_id", -1).limit(limit)) # AMBIL SEBAGIAN
        
        return items
    return []