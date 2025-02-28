# backend/app/services/empresa_service.py
import logging
from backend.app.models.empresa import Empresa, Endereco
from backend.app.services.nuvem_fiscal.client import NuvemFiscalClient
from database.factory import RepositoryFactory

# Configurar logger
logger = logging.getLogger(__name__)

class EmpresaService:
    """Serviço para gerenciar operações relacionadas a empresas"""
    
    def __init__(self):
        self.nuvem_fiscal = NuvemFiscalClient()
        # Usar a fábrica para obter o repositório adequado
        self.empresa_repository = RepositoryFactory.get_empresa_repository()
    
    def consultar_cnpj(self, cnpj):
        """Consulta informações de uma empresa pelo CNPJ na API da Nuvem Fiscal"""
        try:
            # Consulta na API da Nuvem Fiscal
            dados_cnpj = self.nuvem_fiscal.consultar_cnpj(cnpj)
            return dados_cnpj
        except Exception as e:
            logger.error(f"Erro ao consultar CNPJ {cnpj}: {str(e)}")
            raise
    
    def criar_empresa(self, dados_empresa):
        """
        Cria uma nova empresa no banco de dados local e na Nuvem Fiscal
        
        Args:
            dados_empresa (dict): Dicionário com os dados da empresa
            
        Returns:
            Empresa: Objeto da empresa criada
        """
        try:
            # Criar instância do modelo Empresa
            nova_empresa = Empresa.from_dict(dados_empresa)
            
            # Cadastrar na Nuvem Fiscal
            dados_nuvem_fiscal = nova_empresa.to_nuvem_fiscal_dict()
            resultado_api = self.nuvem_fiscal.cadastrar_empresa(dados_nuvem_fiscal)
            
            # Salvar no banco de dados local usando o repositório
            empresa_salva = self.empresa_repository.save(nova_empresa)
            
            logger.info(f"Empresa {nova_empresa.nome_razao_social} cadastrada com sucesso.")
            return empresa_salva
            
        except Exception as e:
            logger.error(f"Erro ao criar empresa: {str(e)}")
            raise
    
    def atualizar_empresa(self, empresa_id, dados_empresa):
        """
        Atualiza uma empresa existente no banco de dados local e na Nuvem Fiscal
        
        Args:
            empresa_id (int): ID da empresa a ser atualizada
            dados_empresa (dict): Dicionário com os dados atualizados
            
        Returns:
            Empresa: Objeto da empresa atualizada
        """
        try:
            # Buscar empresa no repositório
            empresa = self.empresa_repository.find_by_id(empresa_id)
            if not empresa:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada")
            
            # Atualizar campos da empresa
            empresa.nome_razao_social = dados_empresa.get('nome_razao_social', empresa.nome_razao_social)
            empresa.nome_fantasia = dados_empresa.get('nome_fantasia', empresa.nome_fantasia)
            empresa.email = dados_empresa.get('email', empresa.email)
            empresa.telefone = dados_empresa.get('telefone', empresa.telefone)
            empresa.inscricao_estadual = dados_empresa.get('inscricao_estadual', empresa.inscricao_estadual)
            empresa.inscricao_municipal = dados_empresa.get('inscricao_municipal', empresa.inscricao_municipal)
            
            # Atualizar endereço, se fornecido
            endereco_data = dados_empresa.get('endereco')
            if endereco_data:
                if empresa.endereco:
                    # Atualizar endereço existente
                    empresa.endereco.cep = endereco_data.get('cep', empresa.endereco.cep)
                    empresa.endereco.logradouro = endereco_data.get('logradouro', empresa.endereco.logradouro)
                    empresa.endereco.numero = endereco_data.get('numero', empresa.endereco.numero)
                    empresa.endereco.complemento = endereco_data.get('complemento', empresa.endereco.complemento)
                    empresa.endereco.bairro = endereco_data.get('bairro', empresa.endereco.bairro)
                    empresa.endereco.municipio = endereco_data.get('municipio', empresa.endereco.municipio)
                    empresa.endereco.uf = endereco_data.get('uf', empresa.endereco.uf)
                else:
                    # Criar novo endereço
                    empresa.endereco = Endereco.from_dict(endereco_data)
            
            # Atualizar na Nuvem Fiscal
            dados_nuvem_fiscal = empresa.to_nuvem_fiscal_dict()
            self.nuvem_fiscal.atualizar_empresa(empresa.cpf_cnpj, dados_nuvem_fiscal)
            
            # Salvar alterações no repositório
            empresa_atualizada = self.empresa_repository.save(empresa)
            
            logger.info(f"Empresa {empresa.nome_razao_social} atualizada com sucesso.")
            return empresa_atualizada
            
        except Exception as e:
            logger.error(f"Erro ao atualizar empresa: {str(e)}")
            raise
    
    def buscar_empresa_por_id(self, empresa_id):
        """
        Busca uma empresa pelo ID no banco de dados local
        
        Args:
            empresa_id (int): ID da empresa
            
        Returns:
            Empresa: Objeto da empresa encontrada ou None
        """
        try:
            return self.empresa_repository.find_by_id(empresa_id)
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por ID {empresa_id}: {str(e)}")
            raise
    
    def buscar_empresa_por_cnpj(self, cnpj):
        """
        Busca uma empresa pelo CNPJ no banco de dados local
        
        Args:
            cnpj (str): CNPJ da empresa
            
        Returns:
            Empresa: Objeto da empresa encontrada ou None
        """
        try:
            return self.empresa_repository.find_by_cnpj(cnpj)
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por CNPJ {cnpj}: {str(e)}")
            raise
    
    def listar_empresas(self, ativas=True):
        """
        Lista todas as empresas do banco de dados local
        
        Args:
            ativas (bool): Se True, lista apenas empresas ativas
            
        Returns:
            list: Lista de objetos Empresa
        """
        try:
            if ativas:
                return self.empresa_repository.find_active()
            else:
                return self.empresa_repository.find_all()
        except Exception as e:
            logger.error(f"Erro ao listar empresas: {str(e)}")
            raise
    
    def excluir_empresa(self, empresa_id):
        """
        Exclui uma empresa do banco de dados local e da Nuvem Fiscal
        
        Args:
            empresa_id (int): ID da empresa a ser excluída
            
        Returns:
            bool: True se a exclusão for bem-sucedida
        """
        try:
            # Buscar empresa no repositório
            empresa = self.empresa_repository.find_by_id(empresa_id)
            if not empresa:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada")
            
            # Excluir da Nuvem Fiscal
            self.nuvem_fiscal.excluir_empresa(empresa.cpf_cnpj)
            
            # Excluir do repositório local
            resultado = self.empresa_repository.delete(empresa_id)
            
            logger.info(f"Empresa {empresa.nome_razao_social} excluída com sucesso.")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao excluir empresa: {str(e)}")
            raise
    
    def desativar_empresa(self, empresa_id):
        """
        Desativa uma empresa no banco de dados local (não exclui)
        
        Args:
            empresa_id (int): ID da empresa a ser desativada
            
        Returns:
            Empresa: Objeto da empresa desativada
        """
        try:
            # Buscar empresa no repositório
            empresa = self.empresa_repository.find_by_id(empresa_id)
            if not empresa:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada")
            
            # Desativar
            empresa.ativo = False
            
            # Salvar no repositório
            empresa_desativada = self.empresa_repository.save(empresa)
            
            logger.info(f"Empresa {empresa.nome_razao_social} desativada com sucesso.")
            return empresa_desativada
            
        except Exception as e:
            logger.error(f"Erro ao desativar empresa: {str(e)}")
            raise