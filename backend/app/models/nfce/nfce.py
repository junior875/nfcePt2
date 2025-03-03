# backend/app/models/nfce/nfce.py
from backend.app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import Dict, Any, List

class NFCe(db.Model):
    """Modelo para Nota Fiscal de Consumidor Eletrônica (NFC-e)"""
    __tablename__ = 'nfces'
    
    id = db.Column(db.Integer, primary_key=True)
    nuvem_fiscal_id = db.Column(db.String(60), unique=True)  # ID da NFC-e na Nuvem Fiscal
    ambiente = db.Column(db.String(20), nullable=False, default="producao")  # producao ou homologacao
    created_at = db.Column(db.String(30), nullable=True)  # Data de criação na Nuvem Fiscal
    status = db.Column(db.String(20), nullable=False, default="processando")  # Status da NFC-e
    data_emissao = db.Column(db.String(30), nullable=True)  # Data de emissão
    serie = db.Column(db.Integer, nullable=True)  # Série da NFC-e
    numero = db.Column(db.Integer, nullable=True)  # Número da NFC-e
    valor_total = db.Column(db.Float, nullable=False)  # Valor total da NFC-e
    chave = db.Column(db.String(44), unique=True, nullable=True)  # Chave de acesso
    
    # Informações da autorização (quando autorizada)
    autorizacao_id = db.Column(db.String(60), nullable=True)  # ID do evento de autorização
    autorizacao_status = db.Column(db.String(20), nullable=True)  # Status da autorização
    autorizacao_data_evento = db.Column(db.String(30), nullable=True)  # Data do evento
    autorizacao_numero_protocolo = db.Column(db.String(20), nullable=True)  # Número do protocolo
    autorizacao_codigo_status = db.Column(db.Integer, nullable=True)  # Código do status
    autorizacao_motivo_status = db.Column(db.String(255), nullable=True)  # Motivo do status
    
    # Relacionamentos
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    empresa = relationship("Empresa", backref="nfces")
    
    # Campos de controle
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Payload e resposta completa (armazenados como JSON para auditoria)
    payload_enviado = db.Column(db.Text, nullable=True)  # JSON do payload enviado
    resposta_completa = db.Column(db.Text, nullable=True)  # JSON da resposta completa
    
    # Itens da nota
    itens = relationship("ItemNFCe", back_populates="nfce", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NFCe {self.nuvem_fiscal_id}: {self.status}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nuvem_fiscal_id': self.nuvem_fiscal_id,
            'ambiente': self.ambiente,
            'created_at': self.created_at,
            'status': self.status,
            'data_emissao': self.data_emissao,
            'serie': self.serie,
            'numero': self.numero,
            'valor_total': self.valor_total,
            'chave': self.chave,
            'autorizacao_id': self.autorizacao_id,
            'autorizacao_status': self.autorizacao_status,
            'autorizacao_data_evento': self.autorizacao_data_evento,
            'autorizacao_numero_protocolo': self.autorizacao_numero_protocolo,
            'autorizacao_codigo_status': self.autorizacao_codigo_status,
            'autorizacao_motivo_status': self.autorizacao_motivo_status,
            'empresa_id': self.empresa_id,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }


class ItemNFCe(db.Model):
    """Modelo para itens da NFC-e"""
    __tablename__ = 'itens_nfce'
    
    id = db.Column(db.Integer, primary_key=True)
    nfce_id = db.Column(db.Integer, db.ForeignKey('nfces.id'), nullable=False)
    codigo = db.Column(db.String(60), nullable=False)  # Código do produto
    descricao = db.Column(db.String(120), nullable=False)  # Descrição do produto
    ncm = db.Column(db.String(8), nullable=False)  # Classificação fiscal
    cfop = db.Column(db.String(4), nullable=False, default="5102")  # Código fiscal
    unidade = db.Column(db.String(6), nullable=False, default="UN")  # Unidade
    quantidade = db.Column(db.Float, nullable=False)  # Quantidade
    valor_unitario = db.Column(db.Float, nullable=False)  # Valor unitário
    valor_total = db.Column(db.Float, nullable=False)  # Valor total do item
    
    # Impostos
    icms_csosn = db.Column(db.String(3), default="102")  # CSOSN do ICMS para Simples Nacional
    pis_cst = db.Column(db.String(2), default="01")  # CST do PIS
    pis_valor = db.Column(db.Float, nullable=True)  # Valor do PIS
    cofins_cst = db.Column(db.String(2), default="01")  # CST do COFINS
    cofins_valor = db.Column(db.Float, nullable=True)  # Valor do COFINS
    
    # Relacionamentos
    nfce = relationship("NFCe", back_populates="itens")
    
    def __repr__(self):
        return f"<ItemNFCe {self.codigo}: {self.descricao} - {self.quantidade} x {self.valor_unitario}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nfce_id': self.nfce_id,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'ncm': self.ncm,
            'cfop': self.cfop,
            'unidade': self.unidade,
            'quantidade': self.quantidade,
            'valor_unitario': self.valor_unitario,
            'valor_total': self.valor_total,
            'icms_csosn': self.icms_csosn,
            'pis_cst': self.pis_cst,
            'pis_valor': self.pis_valor,
            'cofins_cst': self.cofins_cst,
            'cofins_valor': self.cofins_valor
        }