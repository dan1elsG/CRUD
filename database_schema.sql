-- Criação das tabelas principais

-- Tabela de Universitários
CREATE TABLE IF NOT EXISTS Universitario (
    id SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Matricula INTEGER UNIQUE NOT NULL,
    Universidade VARCHAR(100) NOT NULL,
    Telefone VARCHAR(20) NOT NULL
);

-- Tabela de Transportes
CREATE TABLE IF NOT EXISTS Transporte (
    id SERIAL PRIMARY KEY,
    Placa VARCHAR(10) UNIQUE NOT NULL,
    Tipo_van_onibus VARCHAR(10) CHECK (Tipo_van_onibus IN ('Ônibus', 'Van')) NOT NULL,
    Modelo VARCHAR(50) NOT NULL,
    Numero_de_vagas INTEGER NOT NULL CHECK (Numero_de_vagas > 0)
);

-- Tabela de Viagens
CREATE TABLE IF NOT EXISTS Viagem (
    id SERIAL PRIMARY KEY,
    Data DATE NOT NULL CHECK (Data >= CURRENT_DATE)
);

-- Tabela de Reservas de Transporte
CREATE TABLE IF NOT EXISTS ReservaTransporte (
    id SERIAL PRIMARY KEY,
    ponto_de_embarque VARCHAR(100) NOT NULL,
    ponto_de_desembarque VARCHAR(100) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Pendente', 'Confirmado')) NOT NULL DEFAULT 'Pendente'
);

-- Tabelas de Relacionamentos

-- Relacionamento entre Universitário e Reserva
CREATE TABLE IF NOT EXISTS Universitario_Realiza_Reserva (
    fk_Universitario_ID INTEGER REFERENCES Universitario(id) ON DELETE CASCADE,
    fk_ReservaTransporte_ID INTEGER REFERENCES ReservaTransporte(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_Universitario_ID, fk_ReservaTransporte_ID)
);

-- Relacionamento entre Reserva e Viagem
CREATE TABLE IF NOT EXISTS ReservaTransporte_Para_Viagem (
    fk_ReservaTransporte_ID INTEGER REFERENCES ReservaTransporte(id) ON DELETE CASCADE,
    fk_Viagem_ID INTEGER REFERENCES Viagem(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_ReservaTransporte_ID, fk_Viagem_ID)
);

-- Relacionamento entre Transporte e Viagem
CREATE TABLE IF NOT EXISTS Transporte_Realiza_Viagem (
    fk_Transporte_ID INTEGER REFERENCES Transporte(id) ON DELETE CASCADE,
    fk_Viagem_ID INTEGER REFERENCES Viagem(id) ON DELETE CASCADE,
    PRIMARY KEY (fk_Transporte_ID, fk_Viagem_ID)
);

-- Índices para melhorar performance

-- Índices para chaves estrangeiras
CREATE INDEX IF NOT EXISTS idx_urr_universitario ON Universitario_Realiza_Reserva(fk_Universitario_ID);
CREATE INDEX IF NOT EXISTS idx_urr_reserva ON Universitario_Realiza_Reserva(fk_ReservaTransporte_ID);
CREATE INDEX IF NOT EXISTS idx_rtv_reserva ON ReservaTransporte_Para_Viagem(fk_ReservaTransporte_ID);
CREATE INDEX IF NOT EXISTS idx_rtv_viagem ON ReservaTransporte_Para_Viagem(fk_Viagem_ID);
CREATE INDEX IF NOT EXISTS idx_trv_transporte ON Transporte_Realiza_Viagem(fk_Transporte_ID);
CREATE INDEX IF NOT EXISTS idx_trv_viagem ON Transporte_Realiza_Viagem(fk_Viagem_ID);

-- Índices para buscas comuns
CREATE INDEX IF NOT EXISTS idx_universitario_nome ON Universitario(Nome);
CREATE INDEX IF NOT EXISTS idx_universitario_matricula ON Universitario(Matricula);
CREATE INDEX IF NOT EXISTS idx_transporte_placa ON Transporte(Placa);
CREATE INDEX IF NOT EXISTS idx_viagem_data ON Viagem(Data);
CREATE INDEX IF NOT EXISTS idx_reserva_status ON ReservaTransporte(status);

-- Comentários nas tabelas e colunas para documentação
COMMENT ON TABLE Universitario IS 'Tabela para armazenar informações dos universitários';
COMMENT ON TABLE Transporte IS 'Tabela para armazenar informações dos veículos de transporte';
COMMENT ON TABLE Viagem IS 'Tabela para armazenar as viagens programadas';
COMMENT ON TABLE ReservaTransporte IS 'Tabela para armazenar as reservas de transporte';
COMMENT ON TABLE Universitario_Realiza_Reserva IS 'Tabela de relacionamento entre universitários e suas reservas';
COMMENT ON TABLE ReservaTransporte_Para_Viagem IS 'Tabela de relacionamento entre reservas e viagens';
COMMENT ON TABLE Transporte_Realiza_Viagem IS 'Tabela de relacionamento entre transportes e viagens'; 