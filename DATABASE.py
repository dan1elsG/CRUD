import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import streamlit as st

def get_db_config():
    """Retorna as configurações do banco de dados."""
    return {
        'host': 'localhost',
        'database': 'rota',
        'user': 'postgres',
        'password': '0000',
        'port': '5432'
    }

@contextmanager
def conectar():
    """
    Gerenciador de contexto para conexão com o banco de dados.
    """
    conn = None
    try:
        conn = psycopg2.connect(**get_db_config())
        conn.autocommit = True
        yield conn
    except psycopg2.OperationalError as e:
        st.error(f"❌ Erro de conexão com o banco de dados: {e}")
        st.error("Verifique se o banco de dados está rodando e se as credenciais estão corretas.")
        raise
    except psycopg2.Error as e:
        st.error(f"❌ Erro no banco de dados: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

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