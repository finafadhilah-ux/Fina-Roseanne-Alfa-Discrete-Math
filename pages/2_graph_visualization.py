import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ===== CUSTOM PAGE CONFIG =====
st.set_page_config(page_title="Graph Visualization", layout="wide")

# ===== CUSTOM CSS FOR MODERN UI =====
st.markdown("""
    <style>
        .block-container {
            padding-top: 3rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        h1 {
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: #2c2f38;
        }
        label {
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            color: #2c2f38 !important;
        }
        .stNumberInput input {
            font-size: 1.3rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.title("Graph Visualization")

# ===== INPUT AREA =====
nodes = st.number_input("Enter the number of nodes:", min_value=1, value=5)
edges = st.number_input("Enter the number of edges:", min_value=0, value=4)

generate = st.button("Generate Graph")

# ===== GRAPH VISUALIZATION =====
if generate:
    if edges > nodes * (nodes - 1) / 2:
        st.warning("Too many edges for a simple graph!")
    else:
        G = nx.gnm_random_graph(nodes, edges)

        st.markdown(f"<h3 style='text-align: center;'>Graph with {nodes} Nodes and {edges} Edges</h3>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 5))
        nx.draw(G, with_labels=True, node_color="#8BD3E6", node_size=1300, font_size=14, font_weight="bold")
        st.pyplot(fig)
