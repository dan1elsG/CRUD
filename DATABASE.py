import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="rota",
        user="postgres",
        password="0000",
        host="localhost",
        port="5432"
    )

try:
    conexao = conectar()
    print("Conexão com o banco de dados efetuada com sucesso!")
    conexao.close()
except Exception as erro:
    print("Erro ao conectar no banco de dados:")
    print(erro)