import os
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
        with open(certificado_file, 'rb') as file:
            files = {'file': file}
            data = {'senha': senha}
            response = requests.put(self.base_url, headers=self.headers, files=files, data=data)
            if response.status_code == 200:
                # Salvar uma cópia do certificado
                certificado_path = os.path.join(Config.STORAGE_PATH, 'certificados', f'{self.cpf_cnpj}.pfx')
                with open(certificado_path, 'wb') as local_file:
                    local_file.write(file.read())
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