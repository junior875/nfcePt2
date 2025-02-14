from datetime import datetime
from app import db
from sqlalchemy.orm import validates
import re

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    # Campos de controle
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    # Campos NFCe
    codigo = db.Column(db.String(60), nullable=False, unique=True)  # cProd
    ean = db.Column(db.String(14))  # cEAN
    descricao = db.Column(db.String(120), nullable=False)  # xProd
    ncm = db.Column(db.String(8), nullable=False)  # NCM
    cfop = db.Column(db.String(4), nullable=False)  # CFOP
    unidade_comercial = db.Column(db.String(6), nullable=False)  # uCom
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)  # vUnCom
    
    # Campos adicionais de controle fiscal
    ean_tributavel = db.Column(db.String(14))  # cEANTrib
    unidade_tributavel = db.Column(db.String(6))  # uTrib
    valor_unitario_tributavel = db.Column(db.Numeric(10, 2))  # vUnTrib
    
    # Validações
    @validates('codigo')
    def validate_codigo(self, key, codigo):
        if not codigo:
            raise ValueError('Código do produto é obrigatório')
        if len(codigo) > 60:
            raise ValueError('Código do produto deve ter no máximo 60 caracteres')
        return codigo

    @validates('ean', 'ean_tributavel')
    def validate_ean(self, key, ean):
        if ean:
            if not ean.isdigit():
                raise ValueError('EAN deve conter apenas números')
            if len(ean) not in [8, 12, 13, 14]:
                raise ValueError('EAN deve ter 8, 12, 13 ou 14 dígitos')
        return ean

    @validates('ncm')
    def validate_ncm(self, key, ncm):
        if not ncm:
            raise ValueError('NCM é obrigatório')
        if not ncm.isdigit() or len(ncm) != 8:
            raise ValueError('NCM deve ter 8 dígitos numéricos')
        return ncm

    @validates('cfop')
    def validate_cfop(self, key, cfop):
        if not cfop:
            raise ValueError('CFOP é obrigatório')
        if not cfop.isdigit() or len(cfop) != 4:
            raise ValueError('CFOP deve ter 4 dígitos numéricos')
        return cfop

    @validates('unidade_comercial', 'unidade_tributavel')
    def validate_unidade(self, key, unidade):
        if key == 'unidade_comercial' and not unidade:
            raise ValueError('Unidade comercial é obrigatória')
        if unidade and len(unidade) > 6:
            raise ValueError('Unidade deve ter no máximo 6 caracteres')
        return unidade

    @validates('valor_unitario', 'valor_unitario_tributavel')
    def validate_valor(self, key, valor):
        if key == 'valor_unitario' and not valor:
            raise ValueError('Valor unitário é obrigatório')
        if valor and valor < 0:
            raise ValueError('Valor não pode ser negativo')
        return valor

    def to_dict(self):
        """Converte o modelo para dicionário (útil para API)"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'ean': self.ean,
            'descricao': self.descricao,
            'ncm': self.ncm,
            'cfop': self.cfop,
            'unidade_comercial': self.unidade_comercial,
            'valor_unitario': float(self.valor_unitario),
            'ean_tributavel': self.ean_tributavel,
            'unidade_tributavel': self.unidade_tributavel,
            'valor_unitario_tributavel': float(self.valor_unitario_tributavel) if self.valor_unitario_tributavel else None,
            'active': self.active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Produto {self.codigo}: {self.descricao}>'