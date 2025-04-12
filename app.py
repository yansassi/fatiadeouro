import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")

# Inicializar estado do menu se não existir
if "sidebar_expandida" not in st.session_state:
    st.session_state.sidebar_expandida = True

# CSS atualizado para barra lateral com botão de toggle
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
    padding-top: 3.5rem;
    border-right: 1px solid #2c2f3a;
    z-index: 1000;
    transition: width 0.3s ease-in-out;
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
    padding: 4rem 2rem 2rem 2rem;
}
.toggle-container {
    position: fixed;
    top: 45%;
    left: 220px;
    z-index: 1001;
    transform: translateY(-50%);
}
.toggle-button {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 0.5rem 0.7rem;
    font-size: 1rem;
    font-weight: bold;
    border-radius: 0 6px 6px 0;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Botão para recolher a barra lateral
with st.container():
    toggle_html = f'''
    <div class="toggle-container">
        <form action="" method="get">
            <button name="toggle" value="1" class="toggle-button">{'⏴' if st.session_state.sidebar_expandida else '⏵'}</button>
        </form>
    </div>
    '''
    st.markdown(toggle_html, unsafe_allow_html=True)

# Alternar visibilidade da sidebar
query_params = st.query_params
if "toggle" in query_params:
    st.session_state.sidebar_expandida = not st.session_state.sidebar_expandida

# Mostrar sidebar apenas se estiver expandida
if st.session_state.sidebar_expandida:
    st.markdown("""
    <div class="sidebar-container">
        <h2>🍕 Fatia de Ouro</h2>
        <form action="" method="get">
            <button name="page" value="Clientes" class="sidebar-button">👤 Clientes</button>
            <button name="page" value="Produtos" class="sidebar-button">📦 Produtos</button>
            <button name="page" value="Pedidos" class="sidebar-button">🧾 Pedidos</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

# Página ativa
page = query_params.get("page", "Clientes")

# Conteúdo principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title(page)

if page == "Clientes":
    clientes.show_clientes()
elif page == "Produtos":
    produtos.show_produtos()
elif page == "Pedidos":
    pedidos.show_pedidos()

st.markdown('</div>', unsafe_allow_html=True)