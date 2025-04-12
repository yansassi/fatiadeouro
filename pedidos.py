import streamlit as st
from utils.db import get_supabase
from utils.helpers import export_csv

def show_pedidos():
    st.title("🧾 Pedidos")
    supabase = get_supabase()

    # Simulação de popup com estado
    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = False

    if st.button("🟢 ABRIR PEDIDO"):
        st.session_state.mostrar_formulario = True

    if st.session_state.mostrar_formulario:
        with st.container():
            st.markdown("""
            <style>
            .modal-background {
                background-color: rgba(0, 0, 0, 0.8);
                padding: 2rem;
                border-radius: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            with st.expander("📋 Novo Pedido (clique para fechar)", expanded=True):
                with st.form("form_pedido"):
                    cliente = st.text_input("Cliente")
                    produtos = st.text_input("Produtos (separados por vírgula)")
                    total = st.number_input("Total (valor em Gs)", min_value=0.0, step=1000.0, format="%.2f")
                    status = st.selectbox("Status", ["Aguardando", "Em Preparo", "Finalizado"])
                    data = st.date_input("Data do pedido")
                    submitted = st.form_submit_button("Registrar Pedido")

                    if submitted:
                        if cliente and produtos:
                            try:
                                supabase.table("pedidos").insert({
                                    "cliente": cliente,
                                    "produtos": produtos,
                                    "total": total,
                                    "status": status,
                                    "data": str(data)
                                }).execute()
                                st.success("Pedido registrado com sucesso!")
                                st.session_state.mostrar_formulario = False
                            except Exception as e:
                                st.error(f"Erro ao registrar pedido: {e}")
                        else:
                            st.warning("Preencha todos os campos obrigatórios.")

    # Carregar pedidos
    try:
        pedidos = supabase.table("pedidos").select("*").order("id", desc=True).execute().data
        if pedidos:
            st.markdown("---")
            st.subheader("📤 Exportar todos os pedidos")
            export_csv(pedidos, "todos_pedidos.csv")

            st.markdown("---")
            st.subheader("🕓 Pedidos Não Confirmados")
            nao_confirmados = [p for p in pedidos if p["status"] == "Aguardando"]
            st.dataframe(nao_confirmados, use_container_width=True)

            st.subheader("⚙️ Pedidos em Andamento")
            andamento = [p for p in pedidos if p["status"] == "Em Preparo"]
            st.dataframe(andamento, use_container_width=True)

            st.subheader("✅ Pedidos Finalizados")
            finalizados = [p for p in pedidos if p["status"] == "Finalizado"]
            st.dataframe(finalizados, use_container_width=True)
        else:
            st.info("Nenhum pedido cadastrado.")
    except Exception as e:
        st.error(f"Erro ao buscar pedidos: {e}")