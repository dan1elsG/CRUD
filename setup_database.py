import os
import psycopg2
from dotenv import load_dotenv

def setup_database():
    """Configura o banco de dados usando as variáveis de ambiente."""
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configurações do banco de dados
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'port': os.getenv('DB_PORT', '5432')
    }

    try:
        # Tenta conectar ao banco de dados
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        print("✅ Conexão estabelecida com sucesso!")

        # Lê o arquivo SQL
        with open('database_schema.sql', 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        # Executa os comandos SQL
        with conn.cursor() as cur:
            cur.execute(sql_commands)
        print("✅ Estrutura do banco de dados criada com sucesso!")

        # Fecha a conexão
        conn.close()
        print("✅ Configuração do banco de dados concluída!")
        return True

    except psycopg2.Error as e:
        print(f"❌ Erro ao configurar o banco de dados: {e}")
        return False
    except FileNotFoundError:
        print("❌ Arquivo database_schema.sql não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Iniciando configuração do banco de dados...")
    setup_database() 