from datetime import datetime
from backend.app import db

class Endereco(db.Model):
    """Modelo para armazenar os dados de endereço das empresas"""
    __tablename__ = 'enderecos'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255), nullable=False)
    codigo_municipio = db.Column(db.String(20))  # Adicione esta linha
    municipio = db.Column(db.String(255), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    
    # Relacionamento com Empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id', ondelete='CASCADE'))
    
    def __init__(self, cep, logradouro, numero, bairro, municipio, uf, complemento=None):
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
    
    def to_dict(self):
        """Converte o modelo para um dicionário"""
        return {
            'id': self.id,
            'cep': self.cep,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'municipio': self.municipio,
            'uf': self.uf
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Endereco a partir de um dicionário"""
        return Endereco(
            cep=data.get('cep'),
            logradouro=data.get('logradouro'),
            numero=data.get('numero'),
            complemento=data.get('complemento'),
            bairro=data.get('bairro'),
            municipio=data.get('municipio'),
            uf=data.get('uf')
        )


class Empresa(db.Model):
    """Modelo para armazenar os dados das empresas"""
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(18), unique=True, index=True)
    inscricao_estadual = db.Column(db.String(30), nullable=True)
    inscricao_municipal = db.Column(db.String(30), nullable=True)
    nome_razao_social = db.Column(db.String(255))
    nome_fantasia = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com Endereço
    endereco = db.relationship('Endereco', backref='empresa', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, cpf_cnpj, nome_razao_social, email, endereco=None, 
                 inscricao_estadual=None, inscricao_municipal=None, nome_fantasia=None, telefone=None):
        self.cpf_cnpj = cpf_cnpj
        self.nome_razao_social = nome_razao_social
        self.email = email
        self.inscricao_estadual = inscricao_estadual
        self.inscricao_municipal = inscricao_municipal
        self.nome_fantasia = nome_fantasia
        self.telefone = telefone
        # Se endereço for fornecido como dicionário, converter para objeto Endereco
        if endereco and isinstance(endereco, dict):
            self.endereco = Endereco.from_dict(endereco)
        else:
            self.endereco = endereco
    
    def to_dict(self):
        """Converte o modelo para um dicionário"""
        return {
            'id': self.id,
            'cpf_cnpj': self.cpf_cnpj,
            'inscricao_estadual': self.inscricao_estadual,
            'inscricao_municipal': self.inscricao_municipal,
            'nome_razao_social': self.nome_razao_social,
            'nome_fantasia': self.nome_fantasia,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo,
            'endereco': self.endereco.to_dict() if self.endereco else None
        }

    def to_nuvem_fiscal_dict(self):
        """Converte o modelo para o formato esperado pela API da Nuvem Fiscal"""
        endereco_data = None
        if self.endereco:
            endereco_data = {
                "logradouro": self.endereco.logradouro,
                "numero": self.endereco.numero,
                "complemento": self.endereco.complemento,
                "bairro": self.endereco.bairro,
                "codigo_municipio": "2304400",  # Código IBGE de Fortaleza
                "cidade": "FORTALEZA",  # Nome da cidade
                "uf": self.endereco.uf,
                "codigo_pais": "1058",  # Código do Brasil
                "pais": "Brasil",
                "cep": self.endereco.cep
            }
        
        return {
            "cpf_cnpj": self.cpf_cnpj,
            "created_at": datetime.utcnow().isoformat() + "Z",  # Data atual no formato ISO
            "updated_at": datetime.utcnow().isoformat() + "Z",  # Data atual no formato ISO
            "inscricao_estadual": self.inscricao_estadual or "",
            "inscricao_municipal": self.inscricao_municipal or "",
            "nome_razao_social": self.nome_razao_social,
            "nome_fantasia": self.nome_fantasia,
            "fone": f"+55{self.telefone}",  # Formato internacional
            "email": self.email,
            "endereco": endereco_data
        }
        
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Empresa a partir de um dicionário"""
        endereco_data = data.get('endereco')
        endereco = Endereco.from_dict(endereco_data) if endereco_data else None
        
        return Empresa(
            cpf_cnpj=data.get('cpf_cnpj'),
            nome_razao_social=data.get('nome_razao_social'),
            email=data.get('email'),
            endereco=endereco,
            inscricao_estadual=data.get('inscricao_estadual'),
            inscricao_municipal=data.get('inscricao_municipal'),
            nome_fantasia=data.get('nome_fantasia'),
            telefone=data.get('telefone')
        )
        
    @staticmethod
    def from_cnpj_data(cnpj_data):
        """Cria uma instância de Empresa a partir dos dados retornados pela consulta de CNPJ"""
        # Extrair informações do endereço
        endereco_data = cnpj_data.get('endereco', {})
        endereco = Endereco(
            cep=endereco_data.get('cep'),
            logradouro=endereco_data.get('logradouro'),
            numero=endereco_data.get('numero'),
            complemento=endereco_data.get('complemento'),
            bairro=endereco_data.get('bairro'),
            municipio=endereco_data.get('municipio'),
            uf=endereco_data.get('uf')
        )
        
        # Extrair telefone, se disponível
        telefone = None
        if cnpj_data.get('telefone'):
            telefone = cnpj_data.get('telefone').get('numero')
        
        return Empresa(
            cpf_cnpj=cnpj_data.get('cnpj'),
            nome_razao_social=cnpj_data.get('razao_social'),
            email=cnpj_data.get('email', ''),
            endereco=endereco,
            nome_fantasia=cnpj_data.get('nome_fantasia'),
            telefone=telefone
        )