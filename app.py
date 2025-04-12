import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")
st.sidebar.title("📋 Menu")
pagina = st.sidebar.selectbox("Navegue", ["Clientes", "Produtos", "Pedidos"])

if pagina == "Clientes":
    clientes.show_clientes()
elif pagina == "Produtos":
    produtos.show_produtos()
elif pagina == "Pedidos":
    pedidos.show_pedidos()