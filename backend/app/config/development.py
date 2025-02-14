# backend/app/config/development.py
import os

class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'
    JWT_SECRET_KEY = 'jwt-secret-key-dev'
    
    # Configurações da Nuvem Fiscal
    NUVEM_FISCAL_API_KEY = os.getenv('NUVEM_FISCAL_API_KEY')
    NUVEM_FISCAL_BASE_URL = 'https://api.nuvemfiscal.com.br/v2'
    
    # Configurações de armazenamento
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../storage')
    CERTIFICADOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'certificados')
    XML_FOLDER = os.path.join(UPLOAD_FOLDER, 'xml')
    
    @staticmethod
    def init_app(app):
        pass