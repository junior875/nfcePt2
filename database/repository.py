# database/repository.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    # Importações que só são utilizadas para tipagem, evita importações circulares
    from backend.app.models.empresa import Empresa

import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Interface base para repositórios de dados"""
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Salva uma entidade no repositório (cria se não existir, atualiza se existir)"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        """Busca uma entidade pelo ID"""
        pass
    
    @abstractmethod
    def find_all(self, filters: Dict[str, Any] = None) -> List[T]:
        """Busca todas as entidades que correspondem aos filtros"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Exclui uma entidade pelo ID"""
        pass
    
    @abstractmethod
    def exists(self, id: int) -> bool:
        """Verifica se uma entidade existe pelo ID"""
        pass

class EmpresaRepository(BaseRepository["Empresa"], ABC):
    """Interface específica para repositório de Empresas"""
    
    @abstractmethod
    def find_by_cnpj(self, cnpj: str) -> Optional["Empresa"]:
        """Busca uma empresa pelo CNPJ"""
        pass
    
    @abstractmethod
    def find_active(self) -> List["Empresa"]:
        """Busca todas as empresas ativas"""
        pass