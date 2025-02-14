# backend/app/models/nota_fiscal.py
class NotaFiscal(db.Model):
    __tablename__ = 'notas_fiscais'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    numero = db.Column(db.Integer)
    serie = db.Column(db.String(3), nullable=False, default='1')
    data_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor_produtos = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Campos do cliente (opcional para NFCe)
    cliente_nome = db.Column(db.String(60))
    cliente_cpf_cnpj = db.Column(db.String(14))
    
    # Status e controle
    status = db.Column(db.String(20), nullable=False)  # pendente, enviada, autorizada, rejeitada, cancelada
    chave_acesso = db.Column(db.String(44))
    protocolo_autorizacao = db.Column(db.String(15))
    protocolo_cancelamento = db.Column(db.String(15))
    
    # Arquivos
    xml_autorizado = db.Column(db.Text)
    xml_cancelamento = db.Column(db.Text)
    motivo_cancelamento = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemNotaFiscal', backref='nota_fiscal', lazy=True)
    pagamentos = db.relationship('PagamentoNotaFiscal', backref='nota_fiscal', lazy=True)

class ItemNotaFiscal(db.Model):
    __tablename__ = 'itens_nota_fiscal'
    
    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('notas_fiscais.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    
    # Tributação calculada
    icms_base_calculo = db.Column(db.Numeric(10, 2))
    icms_valor = db.Column(db.Numeric(10, 2))
    pis_valor = db.Column(db.Numeric(10, 2))
    cofins_valor = db.Column(db.Numeric(10, 2))

class PagamentoNotaFiscal(db.Model):
    __tablename__ = 'pagamentos_nota_fiscal'
    
    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('notas_fiscais.id'), nullable=False)
    forma_pagamento = db.Column(db.String(2), nullable=False)  # 01=Dinheiro, 02=Cartão Crédito, 03=Cartão Débito...
    valor = db.Column(db.Numeric(10, 2), nullable=False)