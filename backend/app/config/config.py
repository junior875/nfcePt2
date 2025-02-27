import os
import requests
import time

class Config:
    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações da Nuvem Fiscal
    NUVEM_FISCAL_CLIENT_ID = os.getenv('NUVEM_FISCAL_CLIENT_ID')
    NUVEM_FISCAL_CLIENT_SECRET = os.getenv('NUVEM_FISCAL_CLIENT_SECRET')
    STORAGE_PATH = os.getenv('STORAGE_PATH', 'storage')
    
    # Cache do token para não precisar requisitar a cada chamada
    _token_cache = None
    _token_expiry = 0
    
    @classmethod
    def get_access_token(cls):
        """Obtém um token OAuth2 da Nuvem Fiscal usando client credentials"""
        # Verificar se temos um token em cache válido
        current_time = time.time()
        if cls._token_cache and cls._token_expiry > current_time:
            return cls._token_cache
        
        # URL para obter token
        token_url = "https://auth.nuvemfiscal.com.br/oauth/token"
        
        # Dados para obter token
        data = {
            "grant_type": "client_credentials",
            "client_id": cls.NUVEM_FISCAL_CLIENT_ID,
            "client_secret": cls.NUVEM_FISCAL_CLIENT_SECRET
        }
        
        try:
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)  # Padrão de 1 hora
                
                # Armazenar token em cache
                cls._token_cache = access_token
                cls._token_expiry = current_time + expires_in - 60  # 60 segundos de margem
                
                return access_token
            else:
                print(f"Erro ao obter token: {response.text}")
                return None
        except Exception as e:
            print(f"Exceção ao obter token: {str(e)}")
            return None
        
    @classmethod
    def get_auth_headers(cls):
        """Retorna os headers de autenticação com o token OAuth2"""
        token = cls.get_access_token()
        if not token:
            return {}
            
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }