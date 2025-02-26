import os
import base64
import requests
from ...config import Config

class CertificadoService:
    def __init__(self, cpf_cnpj):
        self.cpf_cnpj = cpf_cnpj
        self.base_url = f"https://api.nuvemfiscal.com.br/empresas/{cpf_cnpj}/certificado"
        self.headers = {
            "Authorization": f"Bearer {Config.NUVEM_FISCAL_API_KEY}",
            "Content-Type": "application/json"
        }

    def get_certificado(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def upload_certificado(self, certificado_file, senha):
        # Ler o conteúdo do arquivo e codificar em base64
        with open(certificado_file, 'rb') as file:
            certificado_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # Montar o payload no formato JSON
        payload = {
            "certificado": certificado_base64,
            "password": senha
        }
        
        # Enviar o certificado para a API
        response = requests.put(self.base_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            # Salvar uma cópia do certificado
            certificado_path = os.path.join(Config.STORAGE_PATH, 'certificados', f'{self.cpf_cnpj}.pfx')
            os.makedirs(os.path.dirname(certificado_path), exist_ok=True)  # Cria o diretório se não existir
            with open(certificado_path, 'wb') as local_file:
                local_file.write(base64.b64decode(certificado_base64))
            return response.json()
        return None

    def delete_certificado(self):
        response = requests.delete(self.base_url, headers=self.headers)
        if response.status_code == 204:
            # Remover o arquivo local se existir
            certificado_path = os.path.join(Config.STORAGE_PATH, 'certificados', f'{self.cpf_cnpj}.pfx')
            if os.path.exists(certificado_path):
                os.remove(certificado_path)
            return True
        return False