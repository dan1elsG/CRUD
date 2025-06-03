# Sistema de Gestão de Transporte Universitário 🚌

Um sistema completo para gerenciamento de transporte universitário, desenvolvido com Python, Streamlit e PostgreSQL.

## 🌟 Funcionalidades

- Gestão de Universitários
  - Cadastro de estudantes
  - Visualização de lista de alunos
  - Exclusão de registros

- Gestão de Transportes
  - Cadastro de veículos (ônibus/van)
  - Controle de capacidade
  - Gerenciamento de frota

- Sistema de Reservas
  - Reservas de transporte
  - Status de confirmação automática
  - Pontos de embarque/desembarque

- Gestão de Viagens
  - Programação de viagens
  - Associação automática de reservas
  - Visualização de passageiros por viagem

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Streamlit
- PostgreSQL
- psycopg2-binary
- python-dotenv

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL instalado e rodando
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/transporte-universitario.git
cd transporte-universitario
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure o banco de dados PostgreSQL:
- Crie um banco de dados chamado 'rota'
- Execute o script SQL em `database_schema.sql`

## ⚙️ Configuração

O sistema está configurado para conectar ao PostgreSQL com as seguintes configurações padrão:
```python
{
    'host': 'localhost',
    'database': 'rota',
    'user': 'postgres',
    'password': '0000',
    'port': '5432'
}
```

Para alterar estas configurações, modifique o arquivo `DATABASE.py`.

## 🚀 Executando o Sistema

1. Ative o ambiente virtual (se ainda não estiver ativo)

2. Execute o aplicativo:
```bash
streamlit run main.py
```

3. Acesse o sistema no navegador (geralmente em http://localhost:8501)

## 📚 Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas:

- `Universitario`: Armazena informações dos estudantes
- `ReservaTransporte`: Gerencia as reservas de transporte
- `Transporte`: Cadastro de veículos
- `Viagem`: Programação de viagens
- Tabelas de relacionamento para gestão de reservas e viagens

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

* **Seu Nome** - *Trabalho Inicial* - [SeuUsuario](https://github.com/SeuUsuario)

## 📧 Contato

Seu Nome - [@seutwitter](https://twitter.com/seutwitter) - email@exemplo.com

Link do projeto: [https://github.com/seu-usuario/transporte-universitario](https://github.com/seu-usuario/transporte-universitario) 