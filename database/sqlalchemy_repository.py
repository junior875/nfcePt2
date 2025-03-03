# database/sqlalchemy_repository.py
from typing import List, Dict, Any, Optional, Type, TypeVar
import logging
from database.repository import EmpresaRepository, NFCeRepository
from backend.app import db
from backend.app.models.empresa import Empresa, Endereco
from backend.app.models.nfce.nfce import NFCe, ItemNFCe

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

class SQLAlchemyNFCeRepository(NFCeRepository):
    """Implementação SQLAlchemy do repositório de NFCe"""
    
    def save(self, nfce: NFCe) -> NFCe:
        """
        Salva uma NFCe no banco de dados (cria ou atualiza)
        
        Args:
            nfce (NFCe): Objeto NFCe a ser salvo
            
        Returns:
            NFCe: Objeto com ID atualizado se for novo
        """
        try:
            # Adicionar à sessão
            db.session.add(nfce)
            # Commit para salvar
            db.session.commit()
            logger.info(f"NFCe salva com ID: {nfce.id}")
            return nfce
        except Exception as e:
            # Rollback em caso de erro
            db.session.rollback()
            logger.error(f"Erro ao salvar NFCe: {e}")
            raise
    
    def find_by_id(self, id: int) -> Optional[NFCe]:
        """
        Busca uma NFCe pelo ID
        
        Args:
            id (int): ID da NFCe
            
        Returns:
            Optional[NFCe]: NFCe encontrada ou None
        """
        try:
            return NFCe.query.get(id)
        except Exception as e:
            logger.error(f"Erro ao buscar NFCe por ID {id}: {e}")
            raise
    
    def find_by_chave(self, chave: str) -> Optional[NFCe]:
        """
        Busca uma NFCe pela chave de acesso
        
        Args:
            chave (str): Chave de acesso da NFCe
            
        Returns:
            Optional[NFCe]: NFCe encontrada ou None
        """
        try:
            return NFCe.query.filter_by(chave=chave).first()
        except Exception as e:
            logger.error(f"Erro ao buscar NFCe por chave {chave}: {e}")
            raise
    
    def find_by_nuvem_fiscal_id(self, nuvem_fiscal_id: str) -> Optional[NFCe]:
        """
        Busca uma NFCe pelo ID da Nuvem Fiscal
        
        Args:
            nuvem_fiscal_id (str): ID da Nuvem Fiscal
            
        Returns:
            Optional[NFCe]: NFCe encontrada ou None
        """
        try:
            return NFCe.query.filter_by(nuvem_fiscal_id=nuvem_fiscal_id).first()
        except Exception as e:
            logger.error(f"Erro ao buscar NFCe por nuvem_fiscal_id {nuvem_fiscal_id}: {e}")
            raise
    
    def find_by_empresa_id(self, empresa_id: int) -> List[NFCe]:
        """
        Busca NFCes pelo ID da empresa
        
        Args:
            empresa_id (int): ID da empresa
            
        Returns:
            List[NFCe]: Lista de NFCes
        """
        try:
            return NFCe.query.filter_by(empresa_id=empresa_id).all()
        except Exception as e:
            logger.error(f"Erro ao buscar NFCes por empresa_id {empresa_id}: {e}")
            raise
    
    def find_by_status(self, status: str) -> List[NFCe]:
        """
        Busca NFCes pelo status
        
        Args:
            status (str): Status da NFCe
            
        Returns:
            List[NFCe]: Lista de NFCes
        """
        try:
            return NFCe.query.filter_by(status=status).all()
        except Exception as e:
            logger.error(f"Erro ao buscar NFCes por status {status}: {e}")
            raise
    
    def find_all(self, filters: Dict[str, Any] = None) -> List[NFCe]:
        """
        Busca todas as NFCes que correspondem aos filtros
        
        Args:
            filters (Dict[str, Any], optional): Filtros opcionais
            
        Returns:
            List[NFCe]: Lista de NFCes
        """
        try:
            query = NFCe.query
            
            # Aplicar filtros se existirem
            if filters:
                if 'status' in filters:
                    query = query.filter_by(status=filters['status'])
                if 'empresa_id' in filters:
                    query = query.filter_by(empresa_id=filters['empresa_id'])
                if 'data_inicio' in filters and 'data_fim' in filters:
                    query = query.filter(
                        NFCe.data_cadastro >= filters['data_inicio'],
                        NFCe.data_cadastro <= filters['data_fim']
                    )
                    
            return query.all()
        except Exception as e:
            logger.error(f"Erro ao listar NFCes: {e}")
            raise
    
    def delete(self, id: int) -> bool:
        """
        Exclui uma NFCe pelo ID
        
        Args:
            id (int): ID da NFCe
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            nfce = self.find_by_id(id)
            if not nfce:
                return False
                
            db.session.delete(nfce)
            db.session.commit()
            logger.info(f"NFCe com ID {id} excluída com sucesso")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir NFCe: {e}")
            raise
    
    def exists(self, id: int) -> bool:
        """
        Verifica se uma NFCe existe pelo ID
        
        Args:
            id (int): ID da NFCe
            
        Returns:
            bool: True se existir
        """
        try:
            return db.session.query(NFCe.query.filter_by(id=id).exists()).scalar()
        except Exception as e:
            logger.error(f"Erro ao verificar existência da NFCe: {e}")
            raise