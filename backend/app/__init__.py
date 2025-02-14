from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from backend.app.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuração
    app.config.from_object(config[config_name])
    
    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    return app