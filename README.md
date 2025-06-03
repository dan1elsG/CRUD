# Sistema de Transporte Universitário

Este é um sistema de gerenciamento de transporte universitário que utiliza PostgreSQL como banco de dados.

## Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas:
- `Universitario`: Armazena informações dos estudantes
- `ReservaTransporte`: Gerencia as reservas de transporte
- `Transporte`: Cadastro de veículos
- `Viagem`: Registro de viagens
- Tabelas de relacionamento para gestão das associações

## Configuração do Ambiente

### Pré-requisitos
- PostgreSQL instalado e rodando
- Python 3.x
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Instale as dependências:
```bash
pip install psycopg2-binary python-dotenv
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes informações:
```
DB_HOST=localhost
DB_NAME=transporte_universitario
DB_USER=postgres
DB_PASS=sua_senha_aqui
DB_PORT=5432
```

4. Execute o script de configuração do banco de dados:
```bash
python setup_database.py
```

## Estrutura do Projeto

- `database_schema.sql`: Definição das tabelas do banco de dados
- `setup_database.py`: Script para criar o banco de dados e as tabelas
- `.env`: Arquivo de configuração (você precisa criar)

## Uso

Após a configuração, o banco de dados estará pronto para uso com as seguintes funcionalidades:

1. Gestão de Universitários
   - Cadastro de estudantes
   - Registro de informações de contato

2. Gestão de Transportes
   - Cadastro de veículos
   - Controle de capacidade

3. Sistema de Reservas
   - Criação de reservas
   - Associação com viagens
   - Controle de status

4. Gestão de Viagens
   - Agendamento de viagens
   - Associação com transportes
   - Controle de passageiros

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas alterações
4. Faça push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 