# backend/app/config/testing.py
from .development import DevelopmentConfig

class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    @staticmethod
    def init_app(app):
        pass
