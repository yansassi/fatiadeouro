import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_clientes():
    st.title("📇 Clientes")
    supabase = get_supabase()

    with st.form("form_cliente"):
        nome = st.text_input("Nome do Cliente")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Adicionar Cliente")

        if submitted:
            if nome:
                try:
                    supabase.table("clientes").insert({"nome": nome, "telefone": telefone, "email": email}).execute()
                    st.success("Cliente adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar cliente: {e}")
            else:
                st.warning("O campo nome é obrigatório.")

    try:
        clientes_data = supabase.table("clientes").select("*").execute().data
        if clientes_data:
            st.subheader("Lista de Clientes")
            export_csv(clientes_data, "clientes.csv")
            st.table(clientes_data)
        else:
            st.info("Nenhum cliente cadastrado.")
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {e}")