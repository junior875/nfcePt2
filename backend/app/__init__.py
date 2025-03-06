import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from logging.handlers import RotatingFileHandler

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Cria e configura a aplicação Flask
    """
    app = Flask(__name__)
    
    # Configurar a aplicação
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Carregar configurações com base no ambiente
    if config_name == 'production':
        app.config.from_object('backend.app.config.production')
    elif config_name == 'testing':
        app.config.from_object('backend.app.config.testing')
    else:
        app.config.from_object('backend.app.config.development')
    
    # Definir URL do banco de dados se não estiver configurada
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        # Caminho absoluto para o banco de dados
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        db_path = os.path.join(basedir, 'database', 'app.db')
        
        # Verificar e imprimir informações para debug
        print(f"Caminho do banco de dados: {db_path}")
        print(f"O arquivo existe? {os.path.exists(db_path)}")
        print(f"O diretório database existe? {os.path.exists(os.path.dirname(db_path))}")
        
        # Usar o caminho absoluto completo
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://www.izibar.com.br",
                "https://izibar.com.br",
                "http://localhost:3000"
            ]
        }
    })
    
    # Configurar logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Iniciando aplicação NFCe')
    
    # Registrar blueprints
    from backend.app.routes import register_blueprints
    register_blueprints(app)
    
    # Criar tabelas do banco de dados (se ainda não existirem)
    with app.app_context():
        db.create_all()
    
    return app