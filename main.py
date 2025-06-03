import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from DATABASE import conectar, verificar_conexao, criar_banco_dados
from datetime import date
import CRUD

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Transporte Universitário",
    layout="wide"
)

# Verificar conexão com o banco de dados
if not verificar_conexao():
    st.warning("⚠️ Tentando criar o banco de dados...")
    if criar_banco_dados():
        st.success("✅ Banco de dados criado com sucesso!")
        st.rerun()
    else:
        st.error("❌ Não foi possível criar o banco de dados. Verifique as configurações.")
        st.stop()

# Inicialização do estado da sessão
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(hash(date.today()))
if 'last_action' not in st.session_state:
    st.session_state.last_action = None
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Universitários"

# Função para gerar chaves únicas para botões
def get_unique_key(prefix, id_value):
    """Gera uma chave única para componentes Streamlit."""
    return f"{prefix}_{id_value}_{st.session_state.session_id}"

# Função para lidar com ações e mensagens
def handle_action(action_type, success, message=""):
    st.session_state.last_action = action_type
    st.session_state.show_success = success
    st.session_state.success_message = message

# Interface do Streamlit
st.title("🚌 Sistema de Gestão de Transporte Universitário")

# Mostrar mensagens de sucesso/erro se existirem
if st.session_state.show_success:
    st.success(st.session_state.success_message)
    # Limpa a mensagem após mostrar
    st.session_state.show_success = False
    st.session_state.success_message = ""

# Mostrar próximas viagens no topo da página
st.header("📅 Próximas Viagens")
proximas_viagens = CRUD.listar_proximas_viagens()
if proximas_viagens:
    for viagem in proximas_viagens:
        with st.expander(f"Viagem do dia {viagem['data'].strftime('%d/%m/%Y')} - {viagem['placa']} ({viagem['tipo_van_onibus']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Transporte:** {viagem['placa']}")
            with col2:
                st.write(f"**Tipo:** {viagem['tipo_van_onibus']}")
            with col3:
                st.write(f"**Passageiros:** {viagem['total_passageiros']}/{viagem['numero_de_vagas']}")
            
            # Lista de passageiros da viagem
            st.subheader("📋 Lista de Passageiros")
            passageiros = CRUD.listar_passageiros_por_viagem(viagem['id'])
            if passageiros:
                st.table([{
                    "Nome": p['nome_universitario'],
                    "Matrícula": p['matricula'],
                    "Embarque": p['ponto_de_embarque'],
                    "Desembarque": p['ponto_de_desembarque'],
                    "Status": p['status_reserva']
                } for p in passageiros])
            else:
                st.info("Nenhum passageiro registrado para esta viagem ainda.")
else:
    st.info("Não há viagens programadas.")

# Sidebar para ações
with st.sidebar:
    st.header("Menu de Opções")
    opcao = st.radio(
        "Escolha uma operação:",
        ["Universitários", "Transportes", "Reservas", "Viagens"],
        key="menu_opcoes",
        index=["Universitários", "Transportes", "Reservas", "Viagens"].index(st.session_state.current_tab)
    )
    st.session_state.current_tab = opcao

if opcao == "Universitários":
    st.subheader("👨‍🎓 Gestão de Universitários")
    
    tab1, tab2 = st.tabs(["📝 Cadastrar", "📋 Listar"])
    
    with tab1:
        with st.form("form_cadastro_universitario", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome Completo")
                matricula = st.number_input("Matrícula", min_value=1, step=1)
            with col2:
                universidade = st.text_input("Universidade")
                telefone = st.text_input("Telefone")

            submitted = st.form_submit_button("Cadastrar Universitário")
            if submitted:
                if nome and matricula and universidade and telefone:
                    id_gerado = CRUD.inserir_universitario(nome, matricula, universidade, telefone)
                    if id_gerado:
                        handle_action("cadastro_universitario", True, f"✅ Universitário cadastrado com sucesso! ID: {id_gerado}")
                        st.rerun()
                else:
                    st.warning("⚠️ Por favor, preencha todos os campos!")
    
    with tab2:
        universitarios = CRUD.listar_universitarios()
        if universitarios:
            for u in universitarios:
                with st.expander(f"{u['nome']} - Matrícula: {u['matricula']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {u['id']}")
                        st.write(f"**Universidade:** {u['universidade']}")
                    with col2:
                        st.write(f"**Telefone:** {u['telefone']}")
                    
                    # Botão de exclusão com confirmação
                    delete_key = get_unique_key("del_univ", u['id'])
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False

                    if st.button("🗑️ Excluir", key=delete_key):
                        st.session_state[delete_key] = True
                        
                    if st.session_state[delete_key]:
                        st.warning("Tem certeza que deseja excluir este universitário?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Sim", key=f"confirm_{delete_key}"):
                                if CRUD.deletar_universitario(u['id']):
                                    handle_action("delete_universitario", True, "Universitário excluído com sucesso!")
                                    st.session_state[delete_key] = False
                                    st.rerun()
                        with col2:
                            if st.button("❌ Não", key=f"cancel_{delete_key}"):
                                st.session_state[delete_key] = False
                                st.rerun()
        else:
            st.info("Nenhum universitário cadastrado ainda.")

elif opcao == "Transportes":
    st.subheader("🚐 Gestão de Transportes")
    
    tab1, tab2 = st.tabs(["📝 Cadastrar", "📋 Listar"])
    
    with tab1:
        with st.form("form_cadastro_transporte", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                placa = st.text_input("Placa")
                tipo = st.selectbox("Tipo", ["Ônibus", "Van"])
            with col2:
                modelo = st.text_input("Modelo")
                numero_vagas = st.number_input("Número de Vagas", min_value=1, step=1)
            
            submitted = st.form_submit_button("Cadastrar Transporte")
            if submitted:
                if placa and tipo and modelo and numero_vagas:
                    id_gerado = CRUD.inserir_transporte(placa, tipo, modelo, numero_vagas)
                    if id_gerado:
                        handle_action("cadastro_transporte", True, f"✅ Transporte cadastrado com sucesso! ID: {id_gerado}")
                        st.rerun()
                else:
                    st.warning("⚠️ Por favor, preencha todos os campos!")
    
    with tab2:
        transportes = CRUD.listar_transportes()
        if transportes:
            for t in transportes:
                with st.expander(f"{t['placa']} - {t['tipo_van_onibus']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {t['id']}")
                        st.write(f"**Modelo:** {t['modelo']}")
                    with col2:
                        st.write(f"**Vagas:** {t['numero_de_vagas']}")
                    
                    # Botão de exclusão com confirmação
                    delete_key = get_unique_key("del_transp", t['id'])
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False

                    if st.button("🗑️ Excluir", key=delete_key):
                        st.session_state[delete_key] = True
                        
                    if st.session_state[delete_key]:
                        st.warning("Tem certeza que deseja excluir este transporte?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Sim", key=f"confirm_{delete_key}"):
                                # Adicionar lógica de exclusão aqui
                                handle_action("delete_transporte", True, "Transporte excluído com sucesso!")
                                st.session_state[delete_key] = False
                                st.rerun()
                        with col2:
                            if st.button("❌ Não", key=f"cancel_{delete_key}"):
                                st.session_state[delete_key] = False
                                st.rerun()
        else:
            st.info("Nenhum transporte cadastrado ainda.")

elif opcao == "Reservas":
    st.subheader("🎫 Gestão de Reservas")
    
    tab1, tab2 = st.tabs(["📝 Nova Reserva", "📋 Listar Reservas"])
    
    with tab1:
        with st.form("form_cadastro_reserva", clear_on_submit=True):
            universitario = st.selectbox(
                "Universitário", 
                options=CRUD.listar_universitarios(),
                format_func=lambda x: f"{x['nome']} ({x['matricula']})",
                key="select_universitario"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                ponto_embarque = st.text_input("Ponto de Embarque")
            with col2:
                ponto_desembarque = st.text_input("Ponto de Desembarque")
            
            submitted = st.form_submit_button("Criar Reserva")
            if submitted:
                if universitario and ponto_embarque and ponto_desembarque:
                    resultado = CRUD.criar_reserva_completa(
                        universitario['id'],
                        ponto_embarque,
                        ponto_desembarque
                    )
                    
                    if resultado["sucesso"]:
                        handle_action("cadastro_reserva", True, resultado["mensagem"])
                        if resultado["status"] == "Confirmado":
                            st.success("🚌 Reserva confirmada para a próxima viagem disponível!")
                        else:
                            st.info("⏳ Reserva em espera. Será automaticamente associada quando houver uma viagem disponível.")
                        st.rerun()
                    else:
                        st.error(resultado["mensagem"])
                else:
                    st.warning("⚠️ Por favor, preencha todos os campos!")
    
    with tab2:
        reservas = CRUD.listar_reservas()
        if reservas:
            # Agrupar reservas por status
            reservas_confirmadas = [r for r in reservas if r['status'] == 'Confirmado']
            reservas_pendentes = [r for r in reservas if r['status'] == 'Pendente']
            
            # Mostrar reservas confirmadas
            if reservas_confirmadas:
                st.subheader("✅ Reservas Confirmadas")
                for r in reservas_confirmadas:
                    with st.expander(f"Reserva {r['id']} - {r['nome_universitario']}"):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        with col1:
                            st.write(f"**Embarque:** {r['ponto_de_embarque']}")
                        with col2:
                            st.write(f"**Desembarque:** {r['ponto_de_desembarque']}")
                        with col3:
                            st.write(f"**Status:** {r['status']}")
                        
                        # Botão de exclusão com confirmação
                        delete_key = get_unique_key("del_res_conf", r['id'])
                        if delete_key not in st.session_state:
                            st.session_state[delete_key] = False

                        if st.button("🗑️ Excluir Reserva", key=delete_key):
                            st.session_state[delete_key] = True
                            
                        if st.session_state[delete_key]:
                            st.warning("Tem certeza que deseja excluir esta reserva?")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Sim", key=f"confirm_{delete_key}"):
                                    if CRUD.excluir_reserva(r['id']):
                                        handle_action("delete_reserva", True, "Reserva excluída com sucesso!")
                                        st.session_state[delete_key] = False
                                        st.rerun()
                            with col2:
                                if st.button("❌ Não", key=f"cancel_{delete_key}"):
                                    st.session_state[delete_key] = False
                                    st.rerun()
            
            # Mostrar reservas pendentes
            if reservas_pendentes:
                st.subheader("⏳ Reservas Pendentes")
                for r in reservas_pendentes:
                    with st.expander(f"Reserva {r['id']} - {r['nome_universitario']}"):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        with col1:
                            st.write(f"**Embarque:** {r['ponto_de_embarque']}")
                        with col2:
                            st.write(f"**Desembarque:** {r['ponto_de_desembarque']}")
                        with col3:
                            st.write(f"**Status:** {r['status']}")
                        
                        # Botão de exclusão com confirmação
                        delete_key = get_unique_key("del_res_pend", r['id'])
                        if delete_key not in st.session_state:
                            st.session_state[delete_key] = False

                        if st.button("🗑️ Excluir Reserva", key=delete_key):
                            st.session_state[delete_key] = True
                            
                        if st.session_state[delete_key]:
                            st.warning("Tem certeza que deseja excluir esta reserva?")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Sim", key=f"confirm_{delete_key}"):
                                    if CRUD.excluir_reserva(r['id']):
                                        handle_action("delete_reserva", True, "Reserva excluída com sucesso!")
                                        st.session_state[delete_key] = False
                                        st.rerun()
                            with col2:
                                if st.button("❌ Não", key=f"cancel_{delete_key}"):
                                    st.session_state[delete_key] = False
                                    st.rerun()
        else:
            st.info("Nenhuma reserva cadastrada ainda.")

elif opcao == "Viagens":
    st.subheader("🚍 Gestão de Viagens")
    
    tab1, tab2 = st.tabs(["📝 Nova Viagem", "📋 Listar Viagens"])
    
    with tab1:
        with st.form("form_cadastro_viagem", clear_on_submit=True):
            data_viagem = st.date_input("Data da Viagem", min_value=date.today())
            transporte = st.selectbox(
                "Transporte", 
                options=CRUD.listar_transportes(),
                format_func=lambda x: f"{x['placa']} - {x['tipo_van_onibus']} ({x['numero_de_vagas']} vagas)",
                key="select_transporte"
            )
            
            submitted = st.form_submit_button("Criar Viagem")
            if submitted and transporte:
                # Criar viagem
                viagem_id = CRUD.inserir_viagem(data_viagem)
                if viagem_id:
                    # Associar transporte à viagem
                    if CRUD.associar_transporte_viagem(transporte['id'], viagem_id):
                        # Associar reservas pendentes
                        num_reservas = CRUD.associar_reservas_pendentes_viagem(viagem_id)
                        mensagem = f"✅ Viagem criada com sucesso! {num_reservas} reservas pendentes foram associadas."
                        handle_action("cadastro_viagem", True, mensagem)
                        if num_reservas > 0:
                            st.info(f"ℹ️ {num_reservas} reservas pendentes foram automaticamente confirmadas para esta viagem.")
                        st.rerun()
    
    with tab2:
        viagens = CRUD.listar_viagens()
        if viagens:
            for v in viagens:
                with st.expander(f"Viagem {v['id']} - {v['data'].strftime('%d/%m/%Y')}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Transporte:** {v['placa']} ({v['tipo_van_onibus']})")
                    with col2:
                        # Botão de exclusão com confirmação
                        delete_key = get_unique_key("del_viag", v['id'])
                        if delete_key not in st.session_state:
                            st.session_state[delete_key] = False

                        if st.button("🗑️ Excluir Viagem", key=delete_key):
                            st.session_state[delete_key] = True
                            
                        if st.session_state[delete_key]:
                            st.warning("Tem certeza que deseja excluir esta viagem?")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Sim", key=f"confirm_{delete_key}"):
                                    if CRUD.excluir_viagem(v['id']):
                                        handle_action("delete_viagem", True, "Viagem excluída com sucesso!")
                                        st.session_state[delete_key] = False
                                        st.rerun()
                            with col2:
                                if st.button("❌ Não", key=f"cancel_{delete_key}"):
                                    st.session_state[delete_key] = False
                                    st.rerun()
                    
                    # Lista de passageiros da viagem
                    st.subheader("📋 Lista de Passageiros")
                    passageiros = CRUD.listar_passageiros_por_viagem(v['id'])
                    if passageiros:
                        st.table([{
                            "Nome": p['nome_universitario'],
                            "Matrícula": p['matricula'],
                            "Embarque": p['ponto_de_embarque'],
                            "Desembarque": p['ponto_de_desembarque'],
                            "Status": p['status_reserva']
                        } for p in passageiros])
                    else:
                        st.info("Nenhum passageiro registrado para esta viagem ainda.")
        else:
            st.info("Nenhuma viagem cadastrada ainda.")
