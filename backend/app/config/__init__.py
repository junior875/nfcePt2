# Exportar configurações
from backend.app.config.development import DevelopmentConfig
from backend.app.config.production import ProductionConfig
from backend.app.config.testing import TestingConfig

__all__ = ['DevelopmentConfig', 'ProductionConfig', 'TestingConfig']