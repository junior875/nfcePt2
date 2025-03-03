# database/factory.py
import os
import logging
from database.repository import EmpresaRepository
from database.sqlalchemy_repository import SQLAlchemyEmpresaRepository
from database.repository import NFCeRepository
from database.sqlalchemy_repository import SQLAlchemyNFCeRepository


logger = logging.getLogger(__name__)

class RepositoryFactory:
    """
    Fábrica para criar instâncias de repositórios
    
    Esta classe facilita a troca de implementações no futuro,
    bastando modificar os métodos para retornar outras implementações
    baseado em configuração do ambiente.
    """
    
    @staticmethod
    def get_empresa_repository() -> EmpresaRepository:
        """
        Cria e retorna um repositório de empresas
        
        Returns:
            EmpresaRepository: Repositório de empresas
        """
        # Obter tipo de repositório da configuração ou variável de ambiente
        # Por padrão, usar o SQLAlchemy para compatibilidade com código existente
        repo_type = os.environ.get('DB_REPOSITORY_TYPE', 'sqlalchemy')
        
        if repo_type.lower() == 'sqlalchemy':
            return SQLAlchemyEmpresaRepository()
        else:
            # No futuro, adicionar outras implementações aqui
            # Por exemplo: PostgreSQL, MySQL, MongoDB, etc.
            logger.warning(f"Tipo de repositório '{repo_type}' não suportado. Usando SQLAlchemy.")
            return SQLAlchemyEmpresaRepository()
        
    @staticmethod
    def get_nfce_repository() -> NFCeRepository:
        """
        Cria e retorna um repositório de NFCe
        
        Returns:
            NFCeRepository: Repositório de NFCe
        """
        # Obter tipo de repositório da configuração ou variável de ambiente
        repo_type = os.environ.get('DB_REPOSITORY_TYPE', 'sqlalchemy')
        
        if repo_type.lower() == 'sqlalchemy':
            return SQLAlchemyNFCeRepository()
        else:
            # No futuro, adicionar outras implementações aqui
            logger.warning(f"Tipo de repositório '{repo_type}' não suportado. Usando SQLAlchemy.")
            return SQLAlchemyNFCeRepository()