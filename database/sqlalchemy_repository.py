# database/sqlalchemy_repository.py
from typing import List, Dict, Any, Optional, Type, TypeVar
import logging
from database.repository import EmpresaRepository
from backend.app import db
from backend.app.models.empresa import Empresa, Endereco

logger = logging.getLogger(__name__)

T = TypeVar('T')

class SQLAlchemyEmpresaRepository(EmpresaRepository):
    """Implementação SQLAlchemy do repositório de empresas"""
    
    def save(self, empresa: Empresa) -> Empresa:
        """
        Salva uma empresa no banco de dados (cria ou atualiza)
        
        Args:
            empresa (Empresa): Objeto empresa a ser salvo
            
        Returns:
            Empresa: Objeto com ID atualizado se for novo
        """
        try:
            # Adicionar à sessão
            db.session.add(empresa)
            # Commit para salvar
            db.session.commit()
            logger.info(f"Empresa {empresa.nome_razao_social} salva com ID: {empresa.id}")
            return empresa
        except Exception as e:
            # Rollback em caso de erro
            db.session.rollback()
            logger.error(f"Erro ao salvar empresa: {e}")
            raise
    
    def find_by_id(self, id: int) -> Optional[Empresa]:
        """
        Busca uma empresa pelo ID
        
        Args:
            id (int): ID da empresa
            
        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        try:
            return Empresa.query.get(id)
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por ID {id}: {e}")
            raise
    
    def find_by_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """
        Busca uma empresa pelo CNPJ
        
        Args:
            cnpj (str): CNPJ da empresa
            
        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        try:
            # Limpar o CNPJ para busca (remover caracteres especiais)
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            return Empresa.query.filter_by(cpf_cnpj=cnpj_limpo).first()
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por CNPJ {cnpj}: {e}")
            raise
    
    def find_all(self, filters: Dict[str, Any] = None) -> List[Empresa]:
        """
        Busca todas as empresas que correspondem aos filtros
        
        Args:
            filters (Dict[str, Any], optional): Filtros opcionais
            
        Returns:
            List[Empresa]: Lista de empresas
        """
        try:
            query = Empresa.query
            
            # Aplicar filtros se existirem
            if filters:
                if 'ativo' in filters:
                    query = query.filter_by(ativo=filters['ativo'])
                    
            return query.all()
        except Exception as e:
            logger.error(f"Erro ao listar empresas: {e}")
            raise
    
    def find_active(self) -> List[Empresa]:
        """
        Busca todas as empresas ativas
        
        Returns:
            List[Empresa]: Lista de empresas ativas
        """
        return self.find_all(filters={'ativo': True})
    
    def delete(self, id: int) -> bool:
        """
        Exclui uma empresa pelo ID
        
        Args:
            id (int): ID da empresa
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            empresa = self.find_by_id(id)
            if not empresa:
                return False
                
            db.session.delete(empresa)
            db.session.commit()
            logger.info(f"Empresa com ID {id} excluída com sucesso")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir empresa: {e}")
            raise
    
    def exists(self, id: int) -> bool:
        """
        Verifica se uma empresa existe pelo ID
        
        Args:
            id (int): ID da empresa
            
        Returns:
            bool: True se existir
        """
        try:
            return db.session.query(Empresa.query.filter_by(id=id).exists()).scalar()
        except Exception as e:
            logger.error(f"Erro ao verificar existência da empresa: {e}")
            raise