import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'port': os.getenv('DB_PORT', '5432')
}

@contextmanager
def conectar():
    """
    Gerenciador de contexto para conexão com o banco de dados.
    Garante que a conexão será fechada após o uso.
    """
    conn = None
    try:
        # Estabelece a conexão
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

try:
    with conectar() as conexao:
        print("Conexão com o banco de dados efetuada com sucesso!")
except Exception as erro:
    print("Erro ao conectar no banco de dados:")
    print(erro)