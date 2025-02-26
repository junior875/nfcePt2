from flask import Flask
from .auth import auth_bp
from .empresa import empresa_bp
from .produto import produto_bp
from .nfce import nfce_bp
from .certificado import certificado_bp

def register_blueprints(app: Flask):
    """
    Registra todos os blueprints da aplicação com um prefixo de URL.

    Args:
        app (Flask): Aplicação Flask
    """
    # Registrar blueprints com prefixo de URL
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(empresa_bp, url_prefix='/api/empresa')
    app.register_blueprint(produto_bp, url_prefix='/api/produto')
    app.register_blueprint(nfce_bp, url_prefix='/api/nfce')
    app.register_blueprint(certificado_bp, url_prefix='/api/certificado')