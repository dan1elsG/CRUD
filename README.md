# Sistema de Transporte Universitário

Sistema de gerenciamento de transporte universitário desenvolvido com Python, Streamlit e PostgreSQL.

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas:
- `Universitario`: Cadastro de estudantes
- `ReservaTransporte`: Gestão de reservas
- `Transporte`: Registro de veículos
- `Viagem`: Controle de viagens
- Tabelas de relacionamento para associações

## 🚀 Configuração

### Pré-requisitos
- PostgreSQL 12 ou superior
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie e ative um ambiente virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
# Conecte ao PostgreSQL
psql -U postgres

# Execute o script de criação do banco
\i create_tables.sql
```

## 📊 Funcionalidades

1. Gestão de Universitários
   - Cadastro e atualização de estudantes
   - Controle de matrículas

2. Sistema de Reservas
   - Criação de reservas de transporte
   - Definição de pontos de embarque/desembarque
   - Status de reserva (Pendente/Confirmado)

3. Controle de Transportes
   - Cadastro de veículos
   - Gestão de capacidade
   - Tipos de transporte (van/ônibus)

4. Gestão de Viagens
   - Agendamento de viagens
   - Associação com transportes
   - Controle de passageiros

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 