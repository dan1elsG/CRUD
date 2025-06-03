from DATABASE import conectar
from typing import Dict, List, Optional, Union
import psycopg2.extras
from datetime import date

# Funções para Universitário
def inserir_universitario(nome: str, matricula: int, universidade: str, telefone: str) -> Optional[int]:
    """Insere um novo universitário no banco de dados e retorna o ID gerado."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Universitario (Nome, Matricula, Universidade, telefone)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (nome, matricula, universidade, telefone))
                id_gerado = cur.fetchone()[0]
                conn.commit()
                return id_gerado
    except Exception as e:
        print(f"Erro ao inserir universitário: {e}")
        return None

def listar_universitarios() -> List[Dict[str, Union[int, str]]]:
    """Retorna uma lista de todos os universitários."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM Universitario ORDER BY Nome")
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar universitários: {e}")
        return []

def buscar_universitario(id: int) -> Optional[Dict[str, Union[int, str]]]:
    """Busca um universitário pelo ID."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM universitario WHERE id = %s", (id,))
                return cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar universitário: {e}")
        return None

def atualizar_universitario(id: int, nome: str, matricula: str, universidade: str, telefone: str) -> bool:
    """Atualiza os dados de um universitário."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE universitario
                    SET nome = %s, matricula = %s, universidade = %s, telefone = %s
                    WHERE id = %s
                """, (nome, matricula, universidade, telefone, id))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao atualizar universitário: {e}")
        return False

def deletar_universitario(id: int) -> bool:
    """Deleta um universitário pelo ID."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM universitario WHERE id = %s", (id,))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao deletar universitário: {e}")
        return False

# Funções para Transporte
def inserir_transporte(placa: str, tipo: str, modelo: str, numero_vagas: int) -> Optional[int]:
    """Insere um novo transporte no banco de dados."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Transporte (placa, Tipo_van_onibus, modelo, Numero_de_vagas)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (placa, tipo, modelo, numero_vagas))
                id_gerado = cur.fetchone()[0]
                conn.commit()
                return id_gerado
    except Exception as e:
        print(f"Erro ao inserir transporte: {e}")
        return None

def listar_transportes() -> List[Dict[str, Union[int, str]]]:
    """Retorna uma lista de todos os transportes."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM Transporte ORDER BY placa")
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar transportes: {e}")
        return []

# Funções para Reserva
def inserir_reserva(ponto_embarque: str, ponto_desembarque: str, status: str = "Pendente") -> Optional[int]:
    """Insere uma nova reserva de transporte."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO ReservaTransporte (ponto_de_embarque, ponto_de_desembarque, status)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (ponto_embarque, ponto_desembarque, status))
                id_gerado = cur.fetchone()[0]
                conn.commit()
                return id_gerado
    except Exception as e:
        print(f"Erro ao inserir reserva: {e}")
        return None

def listar_reservas() -> List[Dict[str, Union[int, str]]]:
    """Retorna uma lista de todas as reservas."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT r.*, u.Nome as nome_universitario 
                    FROM ReservaTransporte r
                    LEFT JOIN Universitario_Realiza_Reserva urr ON r.id = urr.fk_ReservaTransporte_ID
                    LEFT JOIN Universitario u ON urr.fk_Universitario_ID = u.id
                    ORDER BY r.id
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar reservas: {e}")
        return []

# Funções para Viagem
def inserir_viagem(data: date) -> Optional[int]:
    """Insere uma nova viagem e associa reservas pendentes."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Viagem (Data)
                    VALUES (%s)
                    RETURNING id
                """, (data,))
                id_gerado = cur.fetchone()[0]
                conn.commit()
                return id_gerado
    except Exception as e:
        print(f"Erro ao inserir viagem: {e}")
        return None

def listar_viagens() -> List[Dict[str, Union[int, str, date]]]:
    """Retorna uma lista de todas as viagens com seus transportes."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT v.*, t.placa, t.Tipo_van_onibus
                    FROM Viagem v
                    LEFT JOIN Transporte_Realiza_Viagem trv ON v.id = trv.fk_Viagem_ID
                    LEFT JOIN Transporte t ON trv.fk_Transporte_ID = t.id
                    ORDER BY v.Data DESC
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar viagens: {e}")
        return []

# Funções para Relacionamentos
def criar_reserva_universitario(universitario_id: int, reserva_id: int) -> bool:
    """Associa um universitário a uma reserva."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Universitario_Realiza_Reserva (fk_Universitario_ID, fk_ReservaTransporte_ID)
                    VALUES (%s, %s)
                """, (universitario_id, reserva_id))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao criar relação universitário-reserva: {e}")
        return False

def associar_reserva_viagem(reserva_id: int, viagem_id: int) -> bool:
    """Associa uma reserva a uma viagem."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO ReservaTransporte_Para_Viagem (fk_ReservaTransporte_ID, fk_Viagem_ID)
                    VALUES (%s, %s)
                """, (reserva_id, viagem_id))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao associar reserva à viagem: {e}")
        return False

def associar_transporte_viagem(transporte_id: int, viagem_id: int) -> bool:
    """Associa um transporte a uma viagem."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Transporte_Realiza_Viagem (fk_Transporte_ID, fk_Viagem_ID)
                    VALUES (%s, %s)
                """, (transporte_id, viagem_id))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao associar transporte à viagem: {e}")
        return False

def listar_passageiros_por_viagem(viagem_id: int) -> List[Dict[str, Union[int, str]]]:
    """Retorna a lista de passageiros de uma viagem específica."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT DISTINCT 
                        u.id as universitario_id,
                        u.Nome as nome_universitario,
                        u.Matricula as matricula,
                        u.Universidade as universidade,
                        rt.ponto_de_embarque,
                        rt.ponto_de_desembarque,
                        rt.status as status_reserva,
                        t.placa as placa_transporte,
                        t.Tipo_van_onibus as tipo_transporte,
                        v.Data as data_viagem
                    FROM Universitario u
                    JOIN Universitario_Realiza_Reserva urr ON u.id = urr.fk_Universitario_ID
                    JOIN ReservaTransporte rt ON rt.id = urr.fk_ReservaTransporte_ID
                    JOIN ReservaTransporte_Para_Viagem rtv ON rt.id = rtv.fk_ReservaTransporte_ID
                    JOIN Viagem v ON v.id = rtv.fk_Viagem_ID
                    JOIN Transporte_Realiza_Viagem trv ON v.id = trv.fk_Viagem_ID
                    JOIN Transporte t ON t.id = trv.fk_Transporte_ID
                    WHERE v.id = %s
                    ORDER BY u.Nome
                """, (viagem_id,))
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar passageiros da viagem: {e}")
        return []

def listar_proximas_viagens() -> List[Dict[str, Union[int, str, date]]]:
    """Retorna a lista de viagens futuras com contagem de passageiros."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        v.id,
                        v.Data,
                        t.placa,
                        t.Tipo_van_onibus,
                        t.Numero_de_vagas,
                        COUNT(DISTINCT urr.fk_Universitario_ID) as total_passageiros
                    FROM Viagem v
                    JOIN Transporte_Realiza_Viagem trv ON v.id = trv.fk_Viagem_ID
                    JOIN Transporte t ON t.id = trv.fk_Transporte_ID
                    LEFT JOIN ReservaTransporte_Para_Viagem rtv ON v.id = rtv.fk_Viagem_ID
                    LEFT JOIN ReservaTransporte rt ON rt.id = rtv.fk_ReservaTransporte_ID
                    LEFT JOIN Universitario_Realiza_Reserva urr ON rt.id = urr.fk_ReservaTransporte_ID
                    WHERE v.Data >= CURRENT_DATE
                    GROUP BY v.id, v.Data, t.placa, t.Tipo_van_onibus, t.Numero_de_vagas
                    ORDER BY v.Data
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar próximas viagens: {e}")
        return []

def associar_reservas_pendentes_viagem(viagem_id: int) -> int:
    """Associa todas as reservas pendentes a uma viagem e retorna o número de reservas associadas."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # Primeiro, pega a capacidade do transporte para esta viagem
                cur.execute("""
                    SELECT t.Numero_de_vagas
                    FROM Viagem v
                    JOIN Transporte_Realiza_Viagem trv ON v.id = trv.fk_Viagem_ID
                    JOIN Transporte t ON t.id = trv.fk_Transporte_ID
                    WHERE v.id = %s
                """, (viagem_id,))
                
                resultado = cur.fetchone()
                if not resultado:
                    return 0
                
                capacidade = resultado[0]
                
                # Associa reservas pendentes até atingir a capacidade
                cur.execute("""
                    WITH ReservasPendentes AS (
                        SELECT rt.id
                        FROM ReservaTransporte rt
                        WHERE rt.status = 'Pendente'
                        AND NOT EXISTS (
                            SELECT 1 
                            FROM ReservaTransporte_Para_Viagem rtv 
                            WHERE rtv.fk_ReservaTransporte_ID = rt.id
                        )
                        LIMIT %s
                    )
                    INSERT INTO ReservaTransporte_Para_Viagem (fk_ReservaTransporte_ID, fk_Viagem_ID)
                    SELECT id, %s
                    FROM ReservasPendentes
                    RETURNING fk_ReservaTransporte_ID
                """, (capacidade, viagem_id))
                
                # Pega os IDs das reservas que foram associadas
                reservas_associadas = cur.fetchall()
                
                if reservas_associadas:
                    # Atualiza o status das reservas para 'Confirmado'
                    cur.execute("""
                        UPDATE ReservaTransporte
                        SET status = 'Confirmado'
                        WHERE id = ANY(%s)
                    """, ([r[0] for r in reservas_associadas],))
                
                conn.commit()
                return len(reservas_associadas)
                
    except Exception as e:
        print(f"Erro ao associar reservas pendentes à viagem: {e}")
        return 0

def excluir_viagem(viagem_id: int) -> bool:
    """Exclui uma viagem e suas associações."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # Primeiro, atualiza o status das reservas associadas para 'Pendente'
                cur.execute("""
                    UPDATE ReservaTransporte rt
                    SET status = 'Pendente'
                    FROM ReservaTransporte_Para_Viagem rtv
                    WHERE rtv.fk_ReservaTransporte_ID = rt.id
                    AND rtv.fk_Viagem_ID = %s
                """, (viagem_id,))
                
                # A exclusão das relações acontece automaticamente devido ao ON DELETE CASCADE
                cur.execute("DELETE FROM Viagem WHERE id = %s", (viagem_id,))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao excluir viagem: {e}")
        return False

def excluir_reserva(reserva_id: int) -> bool:
    """Exclui uma reserva e suas associações."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # A exclusão das relações acontece automaticamente devido ao ON DELETE CASCADE
                cur.execute("DELETE FROM ReservaTransporte WHERE id = %s", (reserva_id,))
                conn.commit()
                return True
    except Exception as e:
        print(f"Erro ao excluir reserva: {e}")
        return False

def obter_reserva(reserva_id: int) -> Optional[Dict[str, Union[int, str]]]:
    """Retorna os detalhes de uma reserva específica."""
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT rt.*, u.Nome as nome_universitario, u.Matricula as matricula
                    FROM ReservaTransporte rt
                    LEFT JOIN Universitario_Realiza_Reserva urr ON rt.id = urr.fk_ReservaTransporte_ID
                    LEFT JOIN Universitario u ON urr.fk_Universitario_ID = u.id
                    WHERE rt.id = %s
                """, (reserva_id,))
                return cur.fetchone()
    except Exception as e:
        print(f"Erro ao obter reserva: {e}")
        return None

def buscar_viagem_disponivel() -> Optional[int]:
    """Busca uma viagem disponível com vagas."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT v.id, t.Numero_de_vagas, COUNT(DISTINCT urr.fk_Universitario_ID) as total_passageiros
                    FROM Viagem v
                    JOIN Transporte_Realiza_Viagem trv ON v.id = trv.fk_Viagem_ID
                    JOIN Transporte t ON t.id = trv.fk_Transporte_ID
                    LEFT JOIN ReservaTransporte_Para_Viagem rtv ON v.id = rtv.fk_Viagem_ID
                    LEFT JOIN ReservaTransporte rt ON rt.id = rtv.fk_ReservaTransporte_ID
                    LEFT JOIN Universitario_Realiza_Reserva urr ON rt.id = urr.fk_ReservaTransporte_ID
                    WHERE v.Data >= CURRENT_DATE
                    GROUP BY v.id, t.Numero_de_vagas
                    HAVING COUNT(DISTINCT urr.fk_Universitario_ID) < t.Numero_de_vagas
                    ORDER BY v.Data
                    LIMIT 1
                """)
                resultado = cur.fetchone()
                return resultado[0] if resultado else None
    except Exception as e:
        print(f"Erro ao buscar viagem disponível: {e}")
        return None

def criar_reserva_completa(universitario_id: int, ponto_embarque: str, ponto_desembarque: str) -> Dict[str, Union[bool, str, int]]:
    """Cria uma reserva e tenta associá-la a uma viagem disponível."""
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # 1. Criar a reserva
                cur.execute("""
                    INSERT INTO ReservaTransporte (ponto_de_embarque, ponto_de_desembarque, status)
                    VALUES (%s, %s, 'Pendente')
                    RETURNING id
                """, (ponto_embarque, ponto_desembarque))
                reserva_id = cur.fetchone()[0]

                # 2. Associar universitário à reserva
                cur.execute("""
                    INSERT INTO Universitario_Realiza_Reserva (fk_Universitario_ID, fk_ReservaTransporte_ID)
                    VALUES (%s, %s)
                """, (universitario_id, reserva_id))

                # 3. Buscar viagem disponível
                viagem_id = buscar_viagem_disponivel()
                status_final = "Pendente"
                mensagem = "Reserva criada e aguardando viagem disponível"

                if viagem_id:
                    # 4. Associar à viagem se disponível
                    cur.execute("""
                        INSERT INTO ReservaTransporte_Para_Viagem (fk_ReservaTransporte_ID, fk_Viagem_ID)
                        VALUES (%s, %s)
                    """, (reserva_id, viagem_id))
                    
                    # 5. Atualizar status para confirmado
                    cur.execute("""
                        UPDATE ReservaTransporte
                        SET status = 'Confirmado'
                        WHERE id = %s
                    """, (reserva_id,))
                    status_final = "Confirmado"
                    mensagem = "Reserva criada e associada a uma viagem automaticamente"

                conn.commit()
                return {
                    "sucesso": True,
                    "mensagem": mensagem,
                    "reserva_id": reserva_id,
                    "viagem_id": viagem_id,
                    "status": status_final
                }

    except Exception as e:
        print(f"Erro ao criar reserva completa: {e}")
        return {
            "sucesso": False,
            "mensagem": f"Erro ao criar reserva: {str(e)}",
            "reserva_id": None,
            "viagem_id": None,
            "status": "Erro"
        }
