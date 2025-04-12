import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")

# Estilização geral para dashboard com barra lateral esquerda
st.markdown("""
<style>
body {
    background-color: #1e1e2f;
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
.sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 220px;
    height: 100%;
    background-color: #111827;
    padding-top: 2rem;
    border-right: 1px solid #2c2f3a;
    z-index: 1000;
}
.sidebar-container h2 {
    color: white;
    text-align: center;
    font-size: 20px;
    margin-bottom: 2rem;
}
.sidebar-button {
    display: block;
    background-color: transparent;
    color: white;
    border: none;
    text-align: left;
    padding: 0.8rem 1.5rem;
    width: 100%;
    font-size: 1rem;
    font-weight: 600;
    transition: background 0.2s;
}
.sidebar-button:hover {
    background-color: #374151;
    color: #60a5fa;
}
.main-container {
    margin-left: 240px;
    padding: 2rem;
}
</style>
<div class="sidebar-container">
    <h2>🍕 Fatia de Ouro</h2>
    <form action="" method="get">
        <button name="page" value="Clientes" class="sidebar-button">👤 Clientes</button>
        <button name="page" value="Produtos" class="sidebar-button">📦 Produtos</button>
        <button name="page" value="Pedidos" class="sidebar-button">🧾 Pedidos</button>
    </form>
</div>
""", unsafe_allow_html=True)

# Estado da navegação
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Clientes"])[0]

# Container principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title(f"{page}")

if page == "Clientes":
    clientes.show_clientes()
elif page == "Produtos":
    produtos.show_produtos()
elif page == "Pedidos":
    pedidos.show_pedidos()

st.markdown('</div>', unsafe_allow_html=True)