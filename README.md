# Sistema de Gestão de Transporte Universitário 🚌

Um sistema web desenvolvido com Python e Streamlit para gerenciar o transporte universitário, incluindo cadastro de estudantes, reservas de viagens e gestão de veículos.

## Funcionalidades 🎯

- Gestão de Universitários
  - Cadastro de estudantes
  - Listagem e exclusão de registros
  - Informações completas (nome, matrícula, universidade, telefone)

- Gestão de Transportes
  - Cadastro de veículos (ônibus/van)
  - Controle de capacidade
  - Informações do veículo (placa, modelo, número de vagas)

- Sistema de Reservas
  - Criação de reservas de transporte
  - Associação automática com viagens disponíveis
  - Status de reserva (Pendente/Confirmado)
  - Pontos de embarque e desembarque

- Gestão de Viagens
  - Agendamento de viagens
  - Associação automática de reservas pendentes
  - Lista de passageiros por viagem
  - Controle de capacidade do veículo

## Tecnologias Utilizadas 💻

- Python
- Streamlit
- PostgreSQL
- psycopg2

## Requisitos 📋

- Python 3.8+
- PostgreSQL
- Bibliotecas Python (ver requirements.txt)

## Instalação 🚀

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd sistema-transporte-universitario
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto
- Adicione as configurações do banco de dados:
```
DB_HOST=seu_host
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_PORT=5432
```

5. Execute o aplicativo:
```bash
streamlit run main.py
```

## Estrutura do Projeto 📁

```
sistema-transporte-universitario/
├── main.py              # Aplicativo principal Streamlit
├── CRUD.py             # Operações do banco de dados
├── DATABASE.py         # Configuração de conexão
├── requirements.txt    # Dependências do projeto
├── .env               # Variáveis de ambiente (não versionado)
└── README.md          # Documentação
```

## Contribuição 🤝

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença 📄

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 