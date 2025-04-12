import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_pedidos():
    st.title("🧾 Pedidos")
    supabase = get_supabase()

    with st.form("form_pedido"):
        cliente_id = st.text_input("ID do Cliente")
        produto_id = st.text_input("ID do Produto")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        submitted = st.form_submit_button("Registrar Pedido")

        if submitted:
            if cliente_id and produto_id:
                try:
                    supabase.table("pedidos").insert({
                        "cliente_id": cliente_id,
                        "produto_id": produto_id,
                        "quantidade": quantidade
                    }).execute()
                    st.success("Pedido registrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao registrar pedido: {e}")
            else:
                st.warning("Campos obrigatórios: ID do Cliente e Produto.")

    try:
        pedidos_data = supabase.table("pedidos").select("*").execute().data
        if pedidos_data:
            st.subheader("Histórico de Pedidos")
            export_csv(pedidos_data, "pedidos.csv")
            st.table(pedidos_data)
        else:
            st.info("Nenhum pedido registrado.")
    except Exception as e:
        st.error(f"Erro ao buscar pedidos: {e}")