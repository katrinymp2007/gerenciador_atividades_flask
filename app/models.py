import sqlite3
from datetime import datetime

def get_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection

def init_db(database_path):
    connection = get_connection(database_path)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_entrega TEXT,
            prioridade TEXT NOT NULL DEFAULT 'Média',
            status TEXT NOT NULL DEFAULT 'Pendente',
            criado_em TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def listar_atividades(database_path, status=None, prioridade=None):
    connection = get_connection(database_path)
    query = "SELECT * FROM atividades WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if prioridade:
        query += " AND prioridade = ?"
        params.append(prioridade)

    query += """
        ORDER BY
            CASE WHEN status = 'Pendente' THEN 0 ELSE 1 END,
            CASE WHEN data_entrega IS NULL OR data_entrega = '' THEN 1 ELSE 0 END,
            data_entrega ASC,
            id DESC
    """

    atividades = connection.execute(query, params).fetchall()
    connection.close()
    return atividades

def buscar_atividade(database_path, atividade_id):
    connection = get_connection(database_path)
    atividade = connection.execute(
        "SELECT * FROM atividades WHERE id = ?", (atividade_id,)
    ).fetchone()
    connection.close()
    return atividade

def criar_atividade(database_path, titulo, descricao, data_entrega, prioridade):
    connection = get_connection(database_path)
    connection.execute("""
        INSERT INTO atividades
        (titulo, descricao, data_entrega, prioridade, status, criado_em)
        VALUES (?, ?, ?, ?, 'Pendente', ?)
    """, (titulo, descricao, data_entrega, prioridade, datetime.now().isoformat(timespec="seconds")))
    connection.commit()
    connection.close()

def atualizar_atividade(database_path, atividade_id, titulo, descricao, data_entrega, prioridade, status):
    connection = get_connection(database_path)
    connection.execute("""
        UPDATE atividades
        SET titulo = ?, descricao = ?, data_entrega = ?, prioridade = ?, status = ?
        WHERE id = ?
    """, (titulo, descricao, data_entrega, prioridade, status, atividade_id))
    connection.commit()
    connection.close()

def concluir_atividade(database_path, atividade_id):
    connection = get_connection(database_path)
    connection.execute(
        "UPDATE atividades SET status = 'Concluída' WHERE id = ?",
        (atividade_id,)
    )
    connection.commit()
    connection.close()

def excluir_atividade(database_path, atividade_id):
    connection = get_connection(database_path)
    connection.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
    connection.commit()
    connection.close()

def contar_atividades(database_path):
    connection = get_connection(database_path)
    total = connection.execute("SELECT COUNT(*) FROM atividades").fetchone()[0]
    pendentes = connection.execute(
        "SELECT COUNT(*) FROM atividades WHERE status = 'Pendente'"
    ).fetchone()[0]
    concluidas = connection.execute(
        "SELECT COUNT(*) FROM atividades WHERE status = 'Concluída'"
    ).fetchone()[0]
    connection.close()
    return {"total": total, "pendentes": pendentes, "concluidas": concluidas}
