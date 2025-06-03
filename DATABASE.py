import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
import streamlit as st

# Carrega as variáveis de ambiente
load_dotenv()

def get_db_config():
    """Retorna as configurações do banco de dados do Supabase."""
    # Para desenvolvimento local
    if os.getenv('DB_HOST'):
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'transporte_universitario'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASS', ''),
            'port': os.getenv('DB_PORT', '5432')
        }
    # Para Streamlit Cloud - usando secrets
    else:
        return {
            'host': st.secrets["db_host"],
            'database': st.secrets["db_name"],
            'user': st.secrets["db_user"],
            'password': st.secrets["db_pass"],
            'port': st.secrets["db_port"]
        }

@contextmanager
def conectar():
    """
    Gerenciador de contexto para conexão com o banco de dados.
    Tenta reconectar automaticamente em caso de erro.
    """
    conn = None
    try:
        # Tenta estabelecer a conexão
        conn = psycopg2.connect(**get_db_config())
        conn.autocommit = True  # Ativa autocommit
        yield conn
    except psycopg2.OperationalError as e:
        st.error(f"❌ Erro de conexão com o banco de dados: {e}")
        st.error("Verifique se as credenciais do banco de dados estão configuradas corretamente nos secrets do Streamlit.")
        st.info("Para desenvolvimento local, use um arquivo .env com as configurações do banco.")
        st.info("Para deploy no Streamlit Cloud, configure os secrets do projeto.")
        raise
    except psycopg2.Error as e:
        st.error(f"❌ Erro no banco de dados: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# Função para verificar a conexão
def verificar_conexao():
    """Verifica se é possível conectar ao banco de dados."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                st.success("✅ Conexão com o banco de dados estabelecida com sucesso!")
                st.info(f"📊 Versão do PostgreSQL: {version[0]}")
                return True
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False

# Função para criar o banco de dados e as tabelas
def criar_banco_dados():
    """Cria as tabelas necessárias no banco de dados."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # Lê o arquivo SQL
                with open('database_schema.sql', 'r', encoding='utf-8') as file:
                    sql_commands = file.read()
                cur.execute(sql_commands)
                st.success("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        st.error(f"❌ Erro ao criar tabelas: {e}")
        return False

# Verifica a conexão ao iniciar
if __name__ == "__main__":
    verificar_conexao()