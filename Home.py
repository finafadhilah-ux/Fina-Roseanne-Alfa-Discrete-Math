import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Project Discrete Math",
    page_icon="🏠", # Tambahkan ikon, ini akan muncul di tab browser
    layout="wide"
)

# Halaman ini akan menjadi halaman awal Anda. 
# Anda dapat menghapus judul yang besar.
st.markdown("# Welcome to Our Project! 👋") # Ganti st.title dengan st.markdown
st.sidebar.success("Select a page above.") 

# Catatan: Karena namanya Home.py, menu di sidebar akan bertuliskan "Home".
# Ini lebih baik daripada "app".