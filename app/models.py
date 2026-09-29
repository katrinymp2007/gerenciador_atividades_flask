import sqlite3
from datetime import datetime

def get_connection(path):
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row; return db

def init_db(path):
    db=get_connection(path)
    db.execute("""CREATE TABLE IF NOT EXISTS atividades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,titulo TEXT NOT NULL,descricao TEXT,
        data_entrega TEXT,prioridade TEXT NOT NULL DEFAULT 'Média',
        status TEXT NOT NULL DEFAULT 'Pendente',criado_em TEXT NOT NULL)""")
    db.commit(); db.close()

def listar_atividades(path,status=None,prioridade=None):
    db=get_connection(path); q="SELECT * FROM atividades WHERE 1=1"; p=[]
    if status: q+=" AND status=?"; p.append(status)
    if prioridade: q+=" AND prioridade=?"; p.append(prioridade)
    q+=" ORDER BY CASE WHEN status='Pendente' THEN 0 ELSE 1 END,data_entrega ASC,id DESC"
    rows=db.execute(q,p).fetchall(); db.close(); return rows

def buscar_atividade(path,i):
    db=get_connection(path); r=db.execute("SELECT * FROM atividades WHERE id=?",(i,)).fetchone(); db.close(); return r

def criar_atividade(path,t,d,dt,pr):
    db=get_connection(path); db.execute("INSERT INTO atividades(titulo,descricao,data_entrega,prioridade,status,criado_em) VALUES(?,?,?,?,?,?)",(t,d,dt,pr,"Pendente",datetime.now().isoformat(timespec="seconds"))); db.commit(); db.close()

def atualizar_atividade(path,i,t,d,dt,pr,s):
    db=get_connection(path); db.execute("UPDATE atividades SET titulo=?,descricao=?,data_entrega=?,prioridade=?,status=? WHERE id=?",(t,d,dt,pr,s,i)); db.commit(); db.close()

def concluir_atividade(path,i):
    db=get_connection(path); db.execute("UPDATE atividades SET status='Concluída' WHERE id=?",(i,)); db.commit(); db.close()

def excluir_atividade(path,i):
    db=get_connection(path); db.execute("DELETE FROM atividades WHERE id=?",(i,)); db.commit(); db.close()

def contar_atividades(path):
    db=get_connection(path)
    r={"total":db.execute("SELECT COUNT(*) FROM atividades").fetchone()[0],
       "pendentes":db.execute("SELECT COUNT(*) FROM atividades WHERE status='Pendente'").fetchone()[0],
       "concluidas":db.execute("SELECT COUNT(*) FROM atividades WHERE status='Concluída'").fetchone()[0]}
    db.close(); return r
