import streamlit as st

st.title("Profil Tim")

# Data tim (Pastikan gambar ada di folder 'images')
team_data = [
    {"name": "Fina Nailatul Fadhilah", "program": "Actuarial Science", "image": "images/fina.jpg"},
    {"name": "Roseanne Nugraheni", "program": "Actuarial Science", "image": "images/anne.jpg"},
    {"name": "Rega Alfarizi", "program": "Actuarial Science", "image": "images/alfa.jpg"},
]

# --- BAGIAN KUNCI: Membuat TIGA Kolom (st.columns(3)) ---
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

# Loop untuk mengisi setiap kolom
for i, member in enumerate(team_data):
    if i < 3:
        with cols[i]:
            try:
                # Menampilkan Gambar
                st.image(member["image"], use_container_width=True)
                # Menampilkan Nama dan Program
                st.write(f"Name : **{member['name']}**")
                st.write(f"Program : {member['program']}")
            except FileNotFoundError:
                st.error(f"Gambar {member['image']} tidak ditemukan. Cek folder 'images'.")