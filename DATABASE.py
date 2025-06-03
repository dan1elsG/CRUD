import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def get_db_config():
    """Retorna as configurações do banco de dados."""
    # Prioriza variáveis de ambiente do sistema
    if os.getenv('DATABASE_URL'):
        # Parse DATABASE_URL if provided (common in production)
        from urllib.parse import urlparse
        db_url = urlparse(os.getenv('DATABASE_URL'))
        return {
            'host': db_url.hostname,
            'database': db_url.path[1:],
            'user': db_url.username,
            'password': db_url.password,
            'port': str(db_url.port or 5432)
        }
    # Caso contrário, usa as variáveis individuais
    elif os.getenv('DB_HOST'):
        return {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'port': os.getenv('DB_PORT', '5432')
        }
    # Para desenvolvimento local
    else:
        return {
            'host': 'localhost',
            'database': 'rota',
            'user': 'postgres',
            'password': '0000',
            'port': '5432'
        }

@contextmanager
def conectar():
    """Gerenciador de contexto para conexão com o banco de dados."""
    conn = None
    try:
        # Tenta estabelecer a conexão
        conn = psycopg2.connect(**get_db_config())
        conn.autocommit = True
        yield conn
    except psycopg2.OperationalError as e:
        st.error(f"❌ Erro de conexão com o banco de dados: {e}")
        st.error("Verifique as configurações de conexão e se o banco de dados está acessível.")
        if os.getenv('DATABASE_URL'):
            st.info("Usando configuração de DATABASE_URL")
        elif os.getenv('DB_HOST'):
            st.info("Usando variáveis de ambiente individuais")
        else:
            st.info("Usando configuração local padrão")
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