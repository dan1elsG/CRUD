from DATABASE import conectar

def setup_database():
    # SQL para criar todas as tabelas
    sql = """
    DROP TABLE IF EXISTS Transporte_Realiza_Viagem;
    DROP TABLE IF EXISTS ReservaTransporte_Para_Viagem;
    DROP TABLE IF EXISTS Universitario_Realiza_Reserva;
    DROP TABLE IF EXISTS Viagem;
    DROP TABLE IF EXISTS Transporte;
    DROP TABLE IF EXISTS ReservaTransporte;
    DROP TABLE IF EXISTS Universitario;

    CREATE TABLE Universitario (
        id SERIAL PRIMARY KEY,
        Nome VARCHAR(255) NOT NULL,
        Matricula INT UNIQUE NOT NULL,
        Universidade VARCHAR(255),
        telefone VARCHAR(20)
    );

    CREATE TABLE ReservaTransporte (
        id SERIAL PRIMARY KEY,
        ponto_de_embarque VARCHAR(255) NOT NULL,
        ponto_de_desembarque VARCHAR(255) NOT NULL,
        status VARCHAR(50)
    );

    CREATE TABLE Transporte (
        id SERIAL PRIMARY KEY,
        placa VARCHAR(20) UNIQUE NOT NULL,
        Tipo_van_onibus VARCHAR(50),
        modelo VARCHAR(100),
        Numero_de_vagas INT
    );

    CREATE TABLE Viagem (
        id SERIAL PRIMARY KEY,
        Data DATE NOT NULL
    );

    CREATE TABLE Universitario_Realiza_Reserva (
        fk_Universitario_ID INT NOT NULL,
        fk_ReservaTransporte_ID INT NOT NULL,
        PRIMARY KEY (fk_Universitario_ID, fk_ReservaTransporte_ID),
        FOREIGN KEY (fk_Universitario_ID) REFERENCES Universitario (ID) ON DELETE CASCADE,
        FOREIGN KEY (fk_ReservaTransporte_ID) REFERENCES ReservaTransporte (ID) ON DELETE CASCADE
    );

    CREATE TABLE ReservaTransporte_Para_Viagem (
        fk_ReservaTransporte_ID INT NOT NULL,
        fk_Viagem_ID INT NOT NULL,
        PRIMARY KEY (fk_ReservaTransporte_ID, fk_Viagem_ID),
        FOREIGN KEY (fk_ReservaTransporte_ID) REFERENCES ReservaTransporte (ID) ON DELETE CASCADE,
        FOREIGN KEY (fk_Viagem_ID) REFERENCES Viagem (ID) ON DELETE CASCADE
    );

    CREATE TABLE Transporte_Realiza_Viagem (
        fk_Transporte_ID INT NOT NULL,
        fk_Viagem_ID INT NOT NULL,
        PRIMARY KEY (fk_Transporte_ID, fk_Viagem_ID),
        FOREIGN KEY (fk_Transporte_ID) REFERENCES Transporte (ID) ON DELETE CASCADE,
        FOREIGN KEY (fk_Viagem_ID) REFERENCES Viagem (ID) ON DELETE CASCADE
    );
    """
    
    try:
        # Conecta ao banco e executa o SQL
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
        print("Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False

if __name__ == "__main__":
    setup_database() 