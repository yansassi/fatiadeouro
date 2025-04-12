import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_pedidos():
    st.title("🧾 Pedidos")
    supabase = get_supabase()

    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = False

    if st.button("🟢 ABRIR PEDIDO"):
        st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario

    if st.session_state.mostrar_formulario:
        with st.form("form_novo_pedido"):
            st.subheader("📋 Novo Pedido")
            cliente = st.text_input("Cliente")

            try:
                lista_produtos = supabase.table("produtos").select("*").execute().data
            except Exception as e:
                st.error(f"Erro ao buscar produtos: {e}")
                return

            nomes = [f"{p['nome']} - {p['preco']}" for p in lista_produtos]
            nome_para_produto = {f"{p['nome']} - {p['preco']}": p for p in lista_produtos}

            selecionados = st.multiselect("Selecionar Produtos", nomes)

            total = 0
            if selecionados:
                st.markdown("### 🧾 Produtos Selecionados")
                for item in selecionados:
                    produto = nome_para_produto[item]
                    st.write(f"- {produto['nome']} – {produto['preco']} Gs")
                    total += produto["preco"]
                st.markdown(f"### 💰 Total: `{total}` Gs")
            else:
                st.info("Nenhum produto selecionado.")

            status = st.selectbox("Status", ["Aguardando", "Em Preparo", "Finalizado"])
            data = st.date_input("Data do Pedido")
            enviar = st.form_submit_button("Registrar Pedido")

            if enviar:
                if cliente and selecionados:
                    try:
                        nomes_formatados = ", ".join([nome_para_produto[x]["nome"] for x in selecionados])
                        supabase.table("pedidos").insert({
                            "cliente": cliente,
                            "produtos": nomes_formatados,
                            "total": total,
                            "status": status,
                            "data": str(data)
                        }).execute()
                        st.success("Pedido registrado com sucesso!")
                        st.session_state.mostrar_formulario = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao registrar pedido: {e}")
                else:
                    st.warning("Preencha todos os campos obrigatórios.")

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