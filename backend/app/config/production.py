import os
from pathlib import Path

class ProductionConfig:
    """Configuração para ambiente de produção"""
    
    # Configurações gerais
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Configurações do banco de dados
    basedir = Path(__file__).resolve().parents[3]
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{basedir}/database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de armazenamento
    STORAGE_PATH = os.path.join(basedir, 'storage')
    CERTIFICADOS_PATH = os.path.join(STORAGE_PATH, 'certificados')
    XML_PATH = os.path.join(STORAGE_PATH, 'xml')
    PDF_PATH = os.path.join(STORAGE_PATH, 'pdfs')
    
    # Diretórios para XMLs
    XML_ENVIADAS_PATH = os.path.join(XML_PATH, 'enviadas')
    XML_AUTORIZADAS_PATH = os.path.join(XML_PATH, 'autorizadas')
    XML_REJEITADAS_PATH = os.path.join(XML_PATH, 'rejeitadas')
    
    # Configurações de logging
    LOG_LEVEL = 'INFO'