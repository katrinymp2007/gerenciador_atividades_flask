from flask import Flask
from config import Config
from app.models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app.config["DATABASE_PATH"])
    from app.routes import main
    app.register_blueprint(main)
    return app
