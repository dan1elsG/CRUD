-- Criar o banco de dados se não existir
CREATE DATABASE IF NOT EXISTS rota;

-- Conectar ao banco de dados
\c rota;

-- Criar as tabelas
CREATE TABLE IF NOT EXISTS Universitario (
    id SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Matricula INTEGER UNIQUE NOT NULL,
    Universidade VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS ReservaTransporte (
    id SERIAL PRIMARY KEY,
    ponto_de_embarque VARCHAR(100) NOT NULL,
    ponto_de_desembarque VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente' CHECK (status IN ('Pendente', 'Confirmado'))
);

CREATE TABLE IF NOT EXISTS Transporte (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    Tipo_van_onibus VARCHAR(10) CHECK (Tipo_van_onibus IN ('Ônibus', 'Van')) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    Numero_de_vagas INTEGER NOT NULL CHECK (Numero_de_vagas > 0)
);

CREATE TABLE IF NOT EXISTS Viagem (
    id SERIAL PRIMARY KEY,
    Data DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Universitario_Realiza_Reserva (
    fk_Universitario_ID INTEGER REFERENCES Universitario(id) ON DELETE CASCADE,
    fk_ReservaTransporte_ID INTEGER REFERENCES ReservaTransporte(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_Universitario_ID, fk_ReservaTransporte_ID)
);

CREATE TABLE IF NOT EXISTS ReservaTransporte_Para_Viagem (
    fk_ReservaTransporte_ID INTEGER REFERENCES ReservaTransporte(id) ON DELETE CASCADE,
    fk_Viagem_ID INTEGER REFERENCES Viagem(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_ReservaTransporte_ID, fk_Viagem_ID)
);

CREATE TABLE IF NOT EXISTS Transporte_Realiza_Viagem (
    fk_Transporte_ID INTEGER REFERENCES Transporte(id) ON DELETE CASCADE,
    fk_Viagem_ID INTEGER REFERENCES Viagem(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_Transporte_ID, fk_Viagem_ID)
);

-- Comentários das tabelas
COMMENT ON TABLE Universitario IS 'Tabela para armazenar informações dos estudantes universitários';
COMMENT ON TABLE ReservaTransporte IS 'Tabela para gerenciar as reservas de transporte';
COMMENT ON TABLE Transporte IS 'Tabela para cadastro de veículos (ônibus e vans)';
COMMENT ON TABLE Viagem IS 'Tabela para programação de viagens';
COMMENT ON TABLE Universitario_Realiza_Reserva IS 'Tabela de relacionamento entre universitários e suas reservas';
COMMENT ON TABLE ReservaTransporte_Para_Viagem IS 'Tabela de relacionamento entre reservas e viagens';
COMMENT ON TABLE Transporte_Realiza_Viagem IS 'Tabela de relacionamento entre transportes e viagens'; 