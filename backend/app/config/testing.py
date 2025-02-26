import os
import tempfile

class TestingConfig:
    """Configuração para ambiente de testes"""
    
    # Configurações gerais
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'testing_secret_key'
    
    # Usar banco de dados temporário para testes
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de armazenamento
    temp_dir = tempfile.mkdtemp()
    STORAGE_PATH = temp_dir
    CERTIFICADOS_PATH = os.path.join(temp_dir, 'certificados')
    XML_PATH = os.path.join(temp_dir, 'xml')
    PDF_PATH = os.path.join(temp_dir, 'pdfs')
    
    # Diretórios para XMLs
    XML_ENVIADAS_PATH = os.path.join(XML_PATH, 'enviadas')
    XML_AUTORIZADAS_PATH = os.path.join(XML_PATH, 'autorizadas')
    XML_REJEITADAS_PATH = os.path.join(XML_PATH, 'rejeitadas')
    
    # Criar diretórios temporários
    for path in [CERTIFICADOS_PATH, XML_ENVIADAS_PATH, XML_AUTORIZADAS_PATH, XML_REJEITADAS_PATH, PDF_PATH]:
        os.makedirs(path, exist_ok=True)
    
    # Configurações de logging
    LOG_LEVEL = 'DEBUG'
    
    @classmethod
    def cleanup(cls):
        """Limpa recursos temporários após os testes"""
        import os
        import shutil
        os.close(cls.db_fd)
        os.unlink(cls.db_path)
        shutil.rmtree(cls.temp_dir)