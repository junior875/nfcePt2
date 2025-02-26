import os

class Config:
    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações da Nuvem Fiscal
    NUVEM_FISCAL_API_KEY = os.getenv('NUVEM_FISCAL_CLIENT_ID')
    STORAGE_PATH = os.getenv('STORAGE_PATH', 'storage')