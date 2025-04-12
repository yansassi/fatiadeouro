import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")

st.markdown("""
<style>
.top-menu {
    display: flex;
    justify-content: left;
    gap: 2rem;
    padding: 1rem 0;
    border-bottom: 1px solid #333;
}
.top-menu a {
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1rem;
    color: white;
}
</style>
""", unsafe_allow_html=True)

pagina = st.selectbox("Menu", ["Clientes", "Produtos", "Pedidos"], label_visibility="collapsed")

st.markdown('<div class="top-menu">📋 Fatia de Ouro - Sistema</div>', unsafe_allow_html=True)

if pagina == "Clientes":
    clientes.show_clientes()
elif pagina == "Produtos":
    produtos.show_produtos()
elif pagina == "Pedidos":
    pedidos.show_pedidos()