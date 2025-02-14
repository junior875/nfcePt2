# backend/app/models/empresa.py
from .. import db
from datetime import datetime

class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(120), nullable=False)
    nome_fantasia = db.Column(db.String(120))
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    inscricao_estadual = db.Column(db.String(20))
    endereco = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(60), nullable=False)
    cidade = db.Column(db.String(60), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    certificado_path = db.Column(db.String(255))
    certificado_senha = db.Column(db.String(255))
    ambiente = db.Column(db.String(1), default='2')  # 1=Produção, 2=Homologação
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)