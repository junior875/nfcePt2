# backend/app/config/production.py
from .development import DevelopmentConfig

class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    # Sobrescrever configurações específicas de produção
    
    @staticmethod
    def init_app(app):
        pass