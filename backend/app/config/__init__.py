from .config import Config
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

# Exporta as configurações
__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']