import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
import streamlit as st

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
def get_db_config():
    """Retorna as configurações do banco de dados."""
    return {
        'host': st.secrets.get("DB_HOST") or os.getenv('DB_HOST', 'localhost'),
        'database': st.secrets.get("DB_NAME") or os.getenv('DB_NAME', 'transporte_universitario'),
        'user': st.secrets.get("DB_USER") or os.getenv('DB_USER', 'postgres'),
        'password': st.secrets.get("DB_PASS") or os.getenv('DB_PASS', ''),
        'port': st.secrets.get("DB_PORT") or os.getenv('DB_PORT', '5432')
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
        st.info("Tentando reconectar...")
        try:
            if conn:
                conn.close()
            conn = psycopg2.connect(**get_db_config())
            conn.autocommit = True
            yield conn
        except psycopg2.Error as e:
            st.error(f"❌ Falha na reconexão: {e}")
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
    """Cria o banco de dados e as tabelas necessárias."""
    config = get_db_config()
    try:
        # Primeiro tenta conectar ao banco postgres para criar o banco de dados
        conn = psycopg2.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            database='postgres'
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Verifica se o banco de dados existe
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{config['database']}'")
            if not cur.fetchone():
                # Cria o banco de dados se não existir
                cur.execute(f"CREATE DATABASE {config['database']}")
                st.success(f"✅ Banco de dados '{config['database']}' criado com sucesso!")
        
        conn.close()
        
        # Agora conecta ao banco criado para criar as tabelas
        with conectar() as conn:
            with conn.cursor() as cur:
                # Lê o arquivo SQL
                with open('database_schema.sql', 'r', encoding='utf-8') as file:
                    sql_commands = file.read()
                cur.execute(sql_commands)
                st.success("✅ Tabelas criadas com sucesso!")
        
        return True
    except Exception as e:
        st.error(f"❌ Erro ao criar banco de dados: {e}")
        return False

# Verifica a conexão ao iniciar
if __name__ == "__main__":
    verificar_conexao()