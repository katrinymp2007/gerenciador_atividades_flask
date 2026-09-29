import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-desenvolvimento-gerenciador")
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "atividades.db")
