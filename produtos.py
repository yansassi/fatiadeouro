import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_produtos():
    st.title("📦 Produtos")
    supabase = get_supabase()

    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.0, step=0.01, format="%.2f")
        estoque = st.number_input("Estoque", min_value=0, step=1)
        submitted = st.form_submit_button("Adicionar Produto")

        if submitted:
            if nome:
                try:
                    supabase.table("produtos").insert({
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }).execute()
                    st.success("Produto adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar produto: {e}")
            else:
                st.warning("O campo nome é obrigatório.")

    try:
        produtos_data = supabase.table("produtos").select("*").execute().data
        if produtos_data:
            st.subheader("Lista de Produtos")
            export_csv(produtos_data, "produtos.csv")
            st.table(produtos_data)
        else:
            st.info("Nenhum produto cadastrado.")
    except Exception as e:
        st.error(f"Erro ao buscar produtos: {e}")