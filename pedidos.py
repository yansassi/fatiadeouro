import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_pedidos():
    st.title("🧾 Pedidos")
    supabase = get_supabase()

    st.button("🟢 ABRIR PEDIDO", type="primary")

    try:
        pedidos = supabase.table("pedidos").select("*").order("id", desc=True).execute().data
    except Exception as e:
        st.error(f"Erro ao buscar pedidos: {e}")
        return

    if not pedidos:
        st.info("Nenhum pedido cadastrado.")
        return

    st.markdown("---")

    categorias = {
        "Aguardando": "🕓 Pedidos Não Confirmados",
        "Em Preparo": "⚙️ Pedidos em Andamento",
        "Finalizado": "✅ Pedidos Finalizados"
    }

    for status, titulo in categorias.items():
        st.subheader(titulo)
        filtrados = [p for p in pedidos if p["status"] == status]

        if not filtrados:
            st.caption("Nenhum pedido nesta categoria.")
            continue

        colunas = st.columns(3)

        for i, pedido in enumerate(filtrados):
            with colunas[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**Cliente:** {pedido.get('cliente', '')}")
                    st.markdown(f"**Total:** {pedido.get('total', '')}")
                    st.markdown(f"**Status:** {pedido.get('status', '')}")
                    st.markdown(f"**Data:** {pedido.get('data', '')}")
                    st.markdown(f"**Produtos:** {pedido.get('produtos', '')}")
                    st.markdown("---")
                    novo_status = st.selectbox(
                        "Alterar Status",
                        ["Aguardando", "Em Preparo", "Finalizado"],
                        index=["Aguardando", "Em Preparo", "Finalizado"].index(pedido["status"]),
                        key=f"status_{pedido['id']}"
                    )
                    if novo_status != pedido["status"]:
                        try:
                            supabase.table("pedidos").update({"status": novo_status}).eq("id", pedido["id"]).execute()
                            st.success("Status atualizado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar status: {e}")

    st.markdown("---")
    st.subheader("📤 Exportar todos os pedidos")
    export_csv(pedidos, "todos_pedidos.csv")