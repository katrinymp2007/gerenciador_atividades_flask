import os,tempfile
import pytest
from app import create_app
from app.models import init_db

@pytest.fixture()
def client():
    fd,path=tempfile.mkstemp(); os.close(fd)
    app=create_app(); app.config["TESTING"]=True; app.config["DATABASE_PATH"]=path; init_db(path)
    with app.test_client() as c: yield c
    os.unlink(path)

def test_inicio(client):
    r=client.get("/"); assert r.status_code==200; assert b"Minhas atividades" in r.data

def test_criar(client):
    r=client.post("/atividade/nova",data={"titulo":"Estudar Flask","descricao":"Teste","data_entrega":"2026-10-10","prioridade":"Alta"},follow_redirects=True)
    assert r.status_code==200; assert b"Estudar Flask" in r.data
