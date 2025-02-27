import os
import base64
import logging
from backend.app.services.nuvem_fiscal.client import NuvemFiscalClient

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CertificadoService:
    """Serviço para gerenciar certificados digitais"""
    
    def __init__(self, cpf_cnpj):
        """
        Inicializa o serviço de certificado para uma empresa específica
        
        Args:
            cpf_cnpj (str): CPF/CNPJ da empresa
        """
        self.cpf_cnpj = cpf_cnpj
        # Usar o mesmo cliente da Nuvem Fiscal que funciona para empresas
        self.nuvem_fiscal = NuvemFiscalClient()
    
    def get_certificado(self):
        """
        Consulta informações do certificado na API da Nuvem Fiscal
        
        Returns:
            dict: Informações do certificado ou None se não encontrado
        """
        try:
            # Remover caracteres especiais do CNPJ
            cpf_cnpj_limpo = ''.join(filter(str.isdigit, self.cpf_cnpj))
            
            # URL para consulta do certificado
            url = f"empresas/{cpf_cnpj_limpo}/certificado"
            
            # Fazer consulta usando o cliente da Nuvem Fiscal
            response = self.nuvem_fiscal.get(url)
            return response
            
        except Exception as e:
            logger.error(f"Erro ao consultar certificado: {str(e)}")
            return None
    
    def upload_certificado(self, certificado_file, senha):
        """
        Realiza o upload de um certificado digital para a Nuvem Fiscal
        
        Args:
            certificado_file: Arquivo do certificado (FileStorage ou caminho)
            senha (str): Senha do certificado
        
        Returns:
            dict: Informações do certificado ou None em caso de erro
        """
        try:
            # Remover caracteres especiais do CNPJ
            cpf_cnpj_limpo = ''.join(filter(str.isdigit, self.cpf_cnpj))
            
            # Ler o conteúdo do arquivo
            if hasattr(certificado_file, 'read'):
                # É um objeto FileStorage
                certificado_bytes = certificado_file.read()
            else:
                # É um caminho de arquivo
                with open(certificado_file, 'rb') as file:
                    certificado_bytes = file.read()
            
            # Codificar em base64
            certificado_base64 = base64.b64encode(certificado_bytes).decode('utf-8')
            
            # Construir payload
            payload = {
                "certificado": certificado_base64,
                "password": senha  # Nome correto conforme documentação
            }
            
            # URL para upload do certificado
            url = f"empresas/{cpf_cnpj_limpo}/certificado"
            
            # Fazer requisição usando o cliente da Nuvem Fiscal
            response = self.nuvem_fiscal.put(url, payload)
            return response
            
        except Exception as e:
            logger.error(f"Erro ao fazer upload do certificado: {str(e)}")
            return None
    
    def delete_certificado(self):
        """
        Exclui o certificado digital da Nuvem Fiscal
        
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        try:
            # Remover caracteres especiais do CNPJ
            cpf_cnpj_limpo = ''.join(filter(str.isdigit, self.cpf_cnpj))
            
            # URL para exclusão do certificado
            url = f"empresas/{cpf_cnpj_limpo}/certificado"
            
            # Fazer requisição usando o cliente da Nuvem Fiscal
            response = self.nuvem_fiscal.delete(url)
            
            # Verificar se a exclusão foi bem-sucedida
            return response is not None
            
        except Exception as e:
            logger.error(f"Erro ao excluir certificado: {str(e)}")
            return False