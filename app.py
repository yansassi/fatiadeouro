import streamlit as st
import clientes
import produtos
import pedidos

st.set_page_config(page_title="Fatia de Ouro", layout="wide")

# Sidebar com menu simples e direto
st.sidebar.title("📋 Menu")
pagina = st.sidebar.radio("Navegar para:", ["Clientes", "Produtos", "Pedidos"])

st.title("🍕 Fatia de Ouro - " + pagina)

if pagina == "Clientes":
    clientes.show_clientes()
elif pagina == "Produtos":
    produtos.show_produtos()
elif pagina == "Pedidos":
    pedidos.show_pedidos()