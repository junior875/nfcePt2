import os
import csv
import requests
from dotenv import load_dotenv
import logging
import json
import requests
import logging

# Configurar logger
logger = logging.getLogger(__name__)

class NuvemFiscalClient:
    """Cliente para comunicação com a API da Nuvem Fiscal"""
    
    def __init__(self):
        """Inicializa o cliente com as credenciais carregadas do .env ou arquivo CSV"""
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Tentar obter credenciais do ambiente
        self.client_id = os.getenv('NUVEM_FISCAL_CLIENT_ID')
        self.client_secret = os.getenv('NUVEM_FISCAL_CLIENT_SECRET')
        
        # Se não encontrar no ambiente, tentar carregar do arquivo CSV
        if not self.client_id or not self.client_secret:
            self._load_credentials_from_csv()
            
        # Definir URLs base
        self.auth_base_url = "https://auth.nuvemfiscal.com.br"
        self.api_base_url = "https://api.nuvemfiscal.com.br"
        
        # Inicializar token de acesso
        self.access_token = None
        
    def _load_credentials_from_csv(self):
        """Carrega credenciais do arquivo CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'NuvemFiscal_credentials.csv')
            
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                credentials = next(csv_reader)
                self.client_id = credentials.get('Client ID')
                self.client_secret = credentials.get('Client Secret')
                
            if not self.client_id or not self.client_secret:
                raise ValueError("Credenciais não encontradas no arquivo CSV")
                
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais do CSV: {str(e)}")
            raise ValueError(f"Não foi possível carregar as credenciais da Nuvem Fiscal: {str(e)}")
    
    def authenticate(self):
        """Realiza autenticação OAuth2 e obtém token de acesso"""
        try:
            auth_url = f"{self.auth_base_url}/oauth/token"
            
            payload = {
                'grant_type': 'client_credentials',
                'scope': 'empresa cnpj nfe'  # Escopos necessários para a API
            }
            
            response = requests.post(
                auth_url,
                auth=(self.client_id, self.client_secret),
                data=payload
            )
            
            response.raise_for_status()
            auth_data = response.json()
            self.access_token = auth_data['access_token']
            
            logger.info("Autenticação na Nuvem Fiscal realizada com sucesso")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na autenticação com a Nuvem Fiscal: {str(e)}")
            raise Exception(f"Falha na autenticação com a Nuvem Fiscal: {str(e)}")
    
    def get_headers(self):
        """Retorna os headers com o token de autenticação"""
        if not self.access_token:
            self.authenticate()
            
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    
    def consultar_cnpj(self, cnpj):
        """Consulta informações de uma empresa pelo CNPJ"""
        try:
            # Remove caracteres especiais do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            
            url = f"{self.api_base_url}/cnpj/{cnpj_limpo}"
            response = requests.get(url, headers=self.get_headers())
            
            # Verifica se o token expirou (401) e tenta novamente
            if response.status_code == 401:
                self.authenticate()
                response = requests.get(url, headers=self.get_headers())
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consultar CNPJ {cnpj}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta da API: {e.response.text}")
            raise Exception(f"Erro ao consultar CNPJ: {str(e)}")
    
    def cadastrar_empresa(self, dados_empresa):
        """Cadastra uma nova empresa na Nuvem Fiscal."""
        try:
            url = f"{self.api_base_url}/empresas"
            headers = self.get_headers()
            
            # Log do payload para depuração
            logger.debug(f"Payload enviado para Nuvem Fiscal: {json.dumps(dados_empresa, indent=2)}")
            
            # Enviar requisição POST
            response = requests.post(url, headers=headers, json=dados_empresa)
            
            # Verificar se o token expirou (401) e tentar novamente
            if response.status_code == 401:
                self.authenticate()
                response = requests.post(url, headers=headers, json=dados_empresa)
            
            # Levantar exceção para erros HTTP
            response.raise_for_status()
            
            # Log da resposta da API
            logger.debug(f"Resposta da Nuvem Fiscal: {response.text}")
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro ao cadastrar empresa: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao cadastrar empresa: {str(e)}")
            raise
    
    def atualizar_empresa(self, cpf_cnpj, dados_empresa):
        """Atualiza uma empresa existente na Nuvem Fiscal"""
        try:
            # Remove caracteres especiais do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cpf_cnpj))
            
            url = f"{self.api_base_url}/empresas/{cnpj_limpo}"
            response = requests.put(url, headers=self.get_headers(), json=dados_empresa)
            
            # Verifica se o token expirou (401) e tenta novamente
            if response.status_code == 401:
                self.authenticate()
                response = requests.put(url, headers=self.get_headers(), json=dados_empresa)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao atualizar empresa {cpf_cnpj}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta da API: {e.response.text}")
            raise Exception(f"Erro ao atualizar empresa: {str(e)}")
    
    def consultar_empresa(self, cpf_cnpj):
        """Consulta uma empresa cadastrada na Nuvem Fiscal"""
        try:
            # Remove caracteres especiais do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cpf_cnpj))
            
            url = f"{self.api_base_url}/empresas/{cnpj_limpo}"
            response = requests.get(url, headers=self.get_headers())
            
            # Verifica se o token expirou (401) e tenta novamente
            if response.status_code == 401:
                self.authenticate()
                response = requests.get(url, headers=self.get_headers())
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consultar empresa {cpf_cnpj}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta da API: {e.response.text}")
            raise Exception(f"Erro ao consultar empresa: {str(e)}")
    
    def excluir_empresa(self, cpf_cnpj):
        """Exclui uma empresa cadastrada na Nuvem Fiscal"""
        try:
            # Remove caracteres especiais do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cpf_cnpj))
            
            url = f"{self.api_base_url}/empresas/{cnpj_limpo}"
            response = requests.delete(url, headers=self.get_headers())
            
            # Verifica se o token expirou (401) e tenta novamente
            if response.status_code == 401:
                self.authenticate()
                response = requests.delete(url, headers=self.get_headers())
            
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao excluir empresa {cpf_cnpj}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta da API: {e.response.text}")
            raise Exception(f"Erro ao excluir empresa: {str(e)}")
        
    # Adicione estes métodos à classe NuvemFiscalClient

    # Adicione estes métodos à classe NuvemFiscalClient

    def get(self, endpoint):
        """
        Executa uma requisição GET na API da Nuvem Fiscal
        
        Args:
            endpoint (str): Caminho do endpoint relativo à URL base
            
        Returns:
            dict: Resposta da API em formato JSON ou None em caso de erro
        """
        try:
            url = f"{self.api_base_url}/{endpoint}"
            headers = self.get_headers()
            
            response = requests.get(url, headers=headers)
            
            # Verificar se o token expirou
            if response.status_code == 401:
                self.authenticate()
                headers = self.get_headers()
                response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
                
            return None
            
        except Exception as e:
            logger.error(f"Erro na requisição GET para {endpoint}: {str(e)}")
            return None

    def put(self, endpoint, data):
        """
        Executa uma requisição PUT na API da Nuvem Fiscal
        
        Args:
            endpoint (str): Caminho do endpoint relativo à URL base
            data (dict): Dados a serem enviados no corpo da requisição
            
        Returns:
            dict: Resposta da API em formato JSON ou None em caso de erro
        """
        try:
            url = f"{self.api_base_url}/{endpoint}"
            headers = self.get_headers()
            
            response = requests.put(url, json=data, headers=headers)
            
            # Verificar se o token expirou
            if response.status_code == 401:
                self.authenticate()
                headers = self.get_headers()
                response = requests.put(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.json()
                
            logger.error(f"Erro na requisição PUT: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Erro na requisição PUT para {endpoint}: {str(e)}")
            return None

    def delete(self, endpoint):
        """
        Executa uma requisição DELETE na API da Nuvem Fiscal
        
        Args:
            endpoint (str): Caminho do endpoint relativo à URL base
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            url = f"{self.api_base_url}/{endpoint}"
            headers = self.get_headers()
            
            response = requests.delete(url, headers=headers)
            
            # Verificar se o token expirou
            if response.status_code == 401:
                self.authenticate()
                headers = self.get_headers()
                response = requests.delete(url, headers=headers)
            
            return response.status_code in [200, 204]
            
        except Exception as e:
            logger.error(f"Erro na requisição DELETE para {endpoint}: {str(e)}")
            return False