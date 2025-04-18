import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_pedidos():
    st.title("🧾 Pedidos")
    supabase = get_supabase()

    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = False
    if "itens_selecionados" not in st.session_state:
        st.session_state.itens_selecionados = []

    if st.button("🟢 ABRIR PEDIDO"):
        st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario
        if not st.session_state.mostrar_formulario:
            st.session_state.itens_selecionados = []

    if st.session_state.mostrar_formulario:
        with st.form("form_novo_pedido"):
            st.subheader("📋 Novo Pedido")
            cliente = st.text_input("Cliente")

            try:
                lista_produtos = supabase.table("produtos").select("*").execute().data
            except Exception as e:
                st.error(f"Erro ao buscar produtos: {e}")
                return

            nomes = [f"{p['nome']} - R${p['preco']:.2f}" for p in lista_produtos]
            nome_para_produto = {f"{p['nome']} - R${p['preco']:.2f}": p for p in lista_produtos}

            col1, col2 = st.columns([3, 1])
            with col1:
                produto_selecionado = st.selectbox("Selecionar Produto", nomes)
            with col2:
                st.markdown("<div style='margin-top: 2rem'></div>", unsafe_allow_html=True)
                if st.form_submit_button("Adicionar"):
                    if produto_selecionado and produto_selecionado not in st.session_state.itens_selecionados:
                        st.session_state.itens_selecionados.append(produto_selecionado)

            total = 0
            if st.session_state.itens_selecionados:
                st.markdown("### 🧾 Produtos Selecionados")
                for item in st.session_state.itens_selecionados:
                    produto = nome_para_produto[item]
                    st.markdown(f"- {produto['nome']} – <span style='color:limegreen;'>R${produto['preco']:.2f}</span>", unsafe_allow_html=True)
                    total += produto["preco"]
                st.markdown(f"### 💰 <strong>Total: <span style='background-color:#16a34a; color:white; padding:4px 8px; border-radius:6px;'>R${total:.2f}</span></strong>", unsafe_allow_html=True)
            else:
                st.info("Nenhum produto adicionado ainda.")

            status = st.selectbox("Status", ["Aguardando", "Em Preparo", "Finalizado"])
            data = st.date_input("Data do Pedido")
            registrar = st.form_submit_button("Registrar Pedido")

            if registrar:
                if cliente and st.session_state.itens_selecionados:
                    try:
                        nomes_formatados = ", ".join([nome_para_produto[x]["nome"] for x in st.session_state.itens_selecionados])
                        supabase.table("pedidos").insert({
                            "cliente": cliente,
                            "produtos": nomes_formatados,
                            "total": total,
                            "status": status,
                            "data": str(data)
                        }).execute()
                        st.success("Pedido registrado com sucesso!")
                        st.session_state.mostrar_formulario = False
                        st.session_state.itens_selecionados = []
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
                    st.markdown(f"**Data:** {pedido.get('data', '')}")
                    st.markdown(f"**Status:** {pedido.get('status', '')}")
                    st.markdown("**Produtos:**")
                    produtos_lista = [x.strip() for x in pedido.get("produtos", "").split(",")]
                    for produto in produtos_lista:
                        st.markdown(f"<li style='color:limegreen;'>• {produto}</li>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top: 0.5rem;'><strong>💰 Total:</strong> <span style='background-color:#16a34a; color:white; padding:4px 8px; border-radius:6px;'>R${pedido.get('total', 0):.2f}</span></div>", unsafe_allow_html=True)
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