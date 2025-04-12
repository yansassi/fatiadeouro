import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")

# CSS para o layout moderno
st.markdown("""
<style>
body {
    background-color: #1e1e2f;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.navbar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding: 1rem 0;
    background-color: #111827;
    border-bottom: 1px solid #333;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar button {
    background-color: transparent;
    color: white;
    border: none;
    font-weight: bold;
    font-size: 1.1rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
}
.navbar button:hover {
    background-color: #374151;
    color: #60a5fa;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Clientes"

col1, col2, col3 = st.columns([1,1,1])
with st.container():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    if col1.button("Clientes"):
        st.session_state.pagina = "Clientes"
    if col2.button("Produtos"):
        st.session_state.pagina = "Produtos"
    if col3.button("Pedidos"):
        st.session_state.pagina = "Pedidos"
    st.markdown('</div>', unsafe_allow_html=True)

# Exibe a página selecionada
if st.session_state.pagina == "Clientes":
    clientes.show_clientes()
elif st.session_state.pagina == "Produtos":
    produtos.show_produtos()
elif st.session_state.pagina == "Pedidos":
    pedidos.show_pedidos()