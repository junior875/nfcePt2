import os
import requests
from typing import Optional, Dict
from flask import current_app

class NuvemFiscalClient:
    def __init__(self):
        self.base_url = os.getenv('NUVEM_FISCAL_BASE_URL', 'https://api.nuvemfiscal.com.br/v2')
        self.auth_url = "https://auth.nuvemfiscal.com.br/oauth/token"
        self.client_id = os.getenv('NUVEM_FISCAL_CLIENT_ID')
        self.client_secret = os.getenv('NUVEM_FISCAL_CLIENT_SECRET')
        self.access_token = None

    def authenticate(self) -> None:
        """Realiza a autenticação OAuth e obtém o token de acesso"""
        try:
            payload = {
                'grant_type': 'client_credentials',
                'scope': 'cnpj'
            }
            
            response = requests.post(
                self.auth_url,
                auth=(self.client_id, self.client_secret),
                data=payload
            )
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            current_app.logger.info("Autenticação NuvemFiscal realizada com sucesso")
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erro na autenticação NuvemFiscal: {str(e)}")
            raise Exception("Falha na autenticação com a NuvemFiscal")

    def get_headers(self) -> Dict:
        """Retorna os headers com o token de autenticação"""
        if not self.access_token:
            self.authenticate()
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def consultar_cnpj(self, cnpj: str) -> Optional[Dict]:
        """
        Consulta informações de uma empresa pelo CNPJ
        
        Args:
            cnpj (str): CNPJ da empresa (com ou sem formatação)
            
        Returns:
            Dict: Dados da empresa ou None em caso de erro
        """
        try:
            # Remove caracteres especiais do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            
            if len(cnpj_limpo) != 14:
                raise ValueError("CNPJ inválido")

            url = f"{self.base_url}/cnpj/{cnpj_limpo}"
            
            response = requests.get(url, headers=self.get_headers())
            
            # Se der erro 401, tenta reautenticar uma vez
            if response.status_code == 401:
                self.authenticate()
                response = requests.get(url, headers=self.get_headers())
            
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erro ao consultar CNPJ {cnpj}: {str(e)}")
            return None
        except ValueError as e:
            current_app.logger.error(f"CNPJ inválido {cnpj}: {str(e)}")
            return None

    def formatar_endereco(self, dados_empresa: Dict) -> Dict:
        """
        Formata os dados de endereço retornados pela API
        
        Args:
            dados_empresa (Dict): Dados brutos retornados pela API
            
        Returns:
            Dict: Dados formatados do endereço
        """
        endereco = dados_empresa.get('endereco', {})
        return {
            'cep': endereco.get('cep', ''),
            'logradouro': endereco.get('logradouro', ''),
            'numero': endereco.get('numero', ''),
            'complemento': endereco.get('complemento', ''),
            'bairro': endereco.get('bairro', ''),
            'cidade': endereco.get('municipio', {}).get('nome', ''),
            'uf': endereco.get('uf', '')
        }

    def formatar_dados_empresa(self, dados: Dict) -> Dict:
        """
        Formata os dados da empresa retornados pela API
        
        Args:
            dados (Dict): Dados brutos retornados pela API
            
        Returns:
            Dict: Dados formatados da empresa
        """
        return {
            'cnpj': dados.get('cnpj', ''),
            'razao_social': dados.get('razao_social', ''),
            'nome_fantasia': dados.get('nome_fantasia', ''),
            'email': dados.get('email', ''),
            'telefone': dados.get('telefone', {}).get('numero', ''),
            'endereco': self.formatar_endereco(dados)
        }