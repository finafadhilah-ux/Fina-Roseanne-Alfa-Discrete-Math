import streamlit as st
import pandas as pd
import pydeck as pdk

# --- KONFIGURASI DATA KOTA & KONEKSI PULAU SUMATRA ---

# 1. Data Lokasi Kota (List Lengkap)
CITY_LOCATIONS = {
    # Aceh (4 Kota)
    "Banda Aceh": [5.5536, 95.3211], "Lhokseumawe": [5.1500, 97.1500], "Meulaboh": [4.1500, 96.8667], "Langsa": [4.4667, 97.9333],
    # Sumatera Utara (5 Kota)
    "Medan": [3.5952, 98.6722], "Sibolga": [1.7450, 98.7831], "Pematangsiantar": [2.9500, 99.0500], "Kisaran": [2.9800, 99.6400], "Tebing Tinggi": [3.3300, 99.1600],
    # Riau (3 Kota)
    "Pekanbaru": [0.5071, 101.4478], "Dumai": [1.6700, 101.4400], "Rengat": [-0.3700, 102.6300],
    # Sumatera Barat (4 Kota)
    "Padang": [-0.9493, 100.3543], "Bukittinggi": [-0.3083, 100.3667], "Solok": [-0.7833, 100.6500], "Payakumbuh": [0.2333, 100.6333],
    # Jambi (3 Kota)
    "Kota Jambi": [-1.6101, 103.6100], "Muara Bungo": [-1.6101, 102.1388], "Sarolangun": [-2.9833, 103.3667],
    # Sumatera Selatan (5 Kota)
    "Palembang": [-2.9761, 104.7754], "Pagar Alam": [-4.1167, 103.2500], "Prabumulih": [-3.4500, 104.2333], "Lahat": [-3.8000, 103.5333], "Lubuklinggau": [-3.2970, 102.8680],
    # Lampung (3 Kota)
    "Bandar Lampung": [-5.4297, 105.2623], "Metro": [-5.1167, 105.3000], "Kalianda": [-5.7500, 105.6167],
    # Bengkulu (4 Kota)
    "Bengkulu City": [-3.7928, 102.2608], "Curup": [-3.4667, 102.5333], "Manna": [-4.1000, 102.9333], "Bintuhan": [-4.6333, 103.4500],
    # Kepulauan Riau (3 Kota)
    "Batam": [1.1460, 104.0177], "Tanjung Pinang": [0.9167, 104.4500], "Karimun": [1.0000, 103.4333],
    # Bangka Belitung (3 Kota)
    "Pangkal Pinang": [-2.1399, 106.1077], "Tanjung Pandan": [-2.7333, 107.5500], "Sungai Liat": [-1.9000, 106.1000]
}

# 2. Data Koneksi (Garis) per Provinsi
PROVINCE_CONNECTIONS = {
    # --- PERUBAHAN DI SINI ---
    # Koneksi Seluruh Sumatra (HANYA MENGHUBUNGKAN IBU KOTA/KOTA UTAMA)
    "Sumatra (All)": [
        ["Medan", "Banda Aceh"], 
        ["Medan", "Pekanbaru"], 
        ["Pekanbaru", "Padang"], 
        ["Pekanbaru", "Kota Jambi"], 
        ["Kota Jambi", "Palembang"], 
        ["Palembang", "Bandar Lampung"],
        ["Padang", "Bengkulu City"]
    ],
    # --- Data Provinsi Lain TETAP dengan Jaringan Kota Bervariasi ---
    "Aceh": [["Banda Aceh", "Lhokseumawe"], ["Lhokseumawe", "Meulaboh"], ["Meulaboh", "Banda Aceh"], ["Lhokseumawe", "Langsa"]],
    "North Sumatra": [["Medan", "Sibolga"], ["Medan", "Pematangsiantar"], ["Medan", "Kisaran"], ["Pematangsiantar", "Tebing Tinggi"], ["Kisaran", "Tebing Tinggi"]],
    "Riau": [["Pekanbaru", "Dumai"], ["Dumai", "Rengat"], ["Rengat", "Pekanbaru"]],
    "West Sumatra": [["Padang", "Bukittinggi"], ["Bukittinggi", "Solok"], ["Solok", "Padang"], ["Bukittinggi", "Payakumbuh"]],
    "Jambi": [["Kota Jambi", "Muara Bungo"], ["Muara Bungo", "Sarolangun"], ["Sarolangun", "Kota Jambi"]],
    "South Sumatra": [["Palembang", "Pagar Alam"], ["Palembang", "Prabumulih"], ["Prabumulih", "Lahat"], ["Lahat", "Lubuklinggau"], ["Pagar Alam", "Lubuklinggau"]],
    "Lampung": [["Bandar Lampung", "Metro"], ["Metro", "Kalianda"], ["Kalianda", "Bandar Lampung"]],
    "Bengkulu": [["Bengkulu City", "Curup"], ["Curup", "Manna"], ["Manna", "Bintuhan"], ["Bengkulu City", "Manna"]],
    "Riau Islands": [["Batam", "Tanjung Pinang"], ["Tanjung Pinang", "Karimun"], ["Karimun", "Batam"]],
    "Bangka Belitung": [["Pangkal Pinang", "Tanjung Pandan"], ["Tanjung Pandan", "Sungai Liat"], ["Sungai Liat", "Pangkal Pinang"]]
}

# 3. Pengaturan Peta (View State & Kota yang termasuk)
MAIN_PROVINCIAL_NODES = [
    "Banda Aceh", "Medan", "Pekanbaru", "Padang", "Kota Jambi", 
    "Palembang", "Bandar Lampung", "Bengkulu City",
    "Batam", "Pangkal Pinang" # Tambahkan perwakilan pulau kecil
]

PROVINCE_INFO = {
    # --- PERUBAHAN DI SINI: Hanya simpul utama yang dihitung ---
    "Sumatra (All)": {
        "cities": MAIN_PROVINCIAL_NODES,
        "view_state": pdk.ViewState(latitude=0.0, longitude=101.0, zoom=4.5)
    },
    # --- Data Provinsi Lain TETAP ---
    "Aceh": {"cities": ["Banda Aceh", "Lhokseumawe", "Meulaboh", "Langsa"], "view_state": pdk.ViewState(latitude=4.8, longitude=96.5, zoom=6.5)},
    "North Sumatra": {"cities": ["Medan", "Sibolga", "Pematangsiantar", "Kisaran", "Tebing Tinggi"], "view_state": pdk.ViewState(latitude=3.0, longitude=99.0, zoom=6.5)},
    "Riau": {"cities": ["Pekanbaru", "Dumai", "Rengat"], "view_state": pdk.ViewState(latitude=0.4, longitude=102.0, zoom=6.5)},
    "West Sumatra": {"cities": ["Padang", "Bukittinggi", "Solok", "Payakumbuh"], "view_state": pdk.ViewState(latitude=-0.5, longitude=100.5, zoom=6.5)},
    "Jambi": {"cities": ["Kota Jambi", "Muara Bungo", "Sarolangun"], "view_state": pdk.ViewState(latitude=-2.0, longitude=102.5, zoom=6.5)},
    "South Sumatra": {"cities": ["Palembang", "Pagar Alam", "Prabumulih", "Lahat", "Lubuklinggau"], "view_state": pdk.ViewState(latitude=-3.0, longitude=104.0, zoom=6.5)},
    "Lampung": {"cities": ["Bandar Lampung", "Metro", "Kalianda"], "view_state": pdk.ViewState(latitude=-5.3, longitude=105.4, zoom=7.0)},
    "Bengkulu": {"cities": ["Bengkulu City", "Curup", "Manna", "Bintuhan"], "view_state": pdk.ViewState(latitude=-3.8, longitude=102.5, zoom=7.0)},
    "Riau Islands": {"cities": ["Batam", "Tanjung Pinang", "Karimun"], "view_state": pdk.ViewState(latitude=1.0, longitude=103.8, zoom=7.0)},
    "Bangka Belitung": {"cities": ["Pangkal Pinang", "Tanjung Pandan", "Sungai Liat"], "view_state": pdk.ViewState(latitude=-2.3, longitude=106.8, zoom=7.0)}
}

# --- FUNGSI UTAMA STREAMLIT (Tidak ada perubahan) ---

st.title("Visualisasi Jaringan Kota")
st.subheader("Pilih Provinsi")

selected_province = st.selectbox(
    "Provinsi",
    options=list(PROVINCE_INFO.keys()),
    label_visibility="collapsed"
)

province_data = PROVINCE_INFO[selected_province]
initial_view_state = province_data["view_state"]
cities_in_province = province_data["cities"]
connections_in_province = PROVINCE_CONNECTIONS.get(selected_province, []) 

st.write(f"Menampilkan koneksi kota untuk Provinsi **{selected_province}**")

# --- 1. Persiapan Data Titik Kota ---
city_df_list = []
for city in cities_in_province:
    if city in CITY_LOCATIONS: 
        loc = CITY_LOCATIONS[city]
        city_df_list.append({"name": city, "lat": loc[0], "lon": loc[1]})
city_df = pd.DataFrame(city_df_list)

# --- 2. Persiapan Data Garis Koneksi ---
line_df_list = []
if connections_in_province: 
    for conn in connections_in_province:
        city_a, city_b = conn
        if city_a in CITY_LOCATIONS and city_b in CITY_LOCATIONS:
            loc_a = CITY_LOCATIONS[city_a]
            loc_b = CITY_LOCATIONS[city_b]
            line_df_list.append({
                "start_lon": loc_a[1], "start_lat": loc_a[0],
                "end_lon": loc_b[1], "end_lat": loc_b[0],
                "name": f"{city_a} - {city_b}"
            })
line_df = pd.DataFrame(line_df_list)

# --- Layer Pydeck ---
city_layer = pdk.Layer(
    "ScatterplotLayer",
    data=city_df,
    get_position=["lon", "lat"],
    get_color=[255, 0, 0, 200], 
    get_radius=15000, 
    pickable=True,
    tooltip={"text": "{name}"}
)

connection_layer = pdk.Layer(
    "LineLayer",
    data=line_df,
    get_source_position=["start_lon", "start_lat"],
    get_target_position=["end_lon", "end_lat"],
    get_color=[255, 0, 0, 200],
    get_width=5,
    pickable=True,
    tooltip={"text": "{name}"}
)

# Tentukan layer mana yang akan di-render
layers_to_render = [city_layer]
if not line_df.empty:
    layers_to_render.append(connection_layer)


# --- Menampilkan Peta ---
st.pydeck_chart(pdk.Deck(
    map_style=pdk.map_styles.ROAD,
    initial_view_state=initial_view_state,
    layers=layers_to_render,
    height=550 
))