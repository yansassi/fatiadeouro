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

    st.subheader("📤 Exportar todos os pedidos")
    export_csv(pedidos, "todos_pedidos.csv")
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

        colunas = st.columns(3)  # 3 cards por linha

        for i, pedido in enumerate(filtrados):
            with colunas[i % 3]:
                st.markdown(
                    f'''
<div style="border:1px solid #444; border-radius:10px; padding:1rem; margin-bottom:1rem; background-color:#1f2937;">
<strong>Cliente:</strong> {pedido.get("cliente", "")}<br>
<strong>Total:</strong> {pedido.get("total", "")}<br>
<strong>Status:</strong> {pedido.get("status", "")}<br>
<strong>Data:</strong> {pedido.get("data", "")}<br>
<strong>Produtos:</strong> {pedido.get("produtos", "")}
</div>
                    ''',
                    unsafe_allow_html=True
                )
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