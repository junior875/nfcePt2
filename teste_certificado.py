import os
import logging
from dotenv import load_dotenv
import requests

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  

# Carregar variáveis de ambiente
load_dotenv()

# Base URL da API
base_url = os.getenv('API_URL', 'http://localhost:5000/api')

# Configurações do certificado
CNPJ_LIMPO = "48144666000140"  # CNPJ sem formatação
CERTIFICADO_PATH = os.path.abspath(os.path.join("storage", "certificados", "barbearia.pfx"))
SENHA_CERTIFICADO = "Mateus3286"  # Senha do certificado

def test_upload_certificado():
    """Faz o upload do certificado A1 para a API"""
    logger.info("\n=== Fazendo upload do certificado A1 ===")
    
    # Verifica se o arquivo existe
    if not os.path.exists(CERTIFICADO_PATH):
        logger.error(f"❌ Arquivo NÃO encontrado: {CERTIFICADO_PATH}")
        return False
    
    # Envia o certificado para a API
    with open(CERTIFICADO_PATH, 'rb') as file:
        files = {'file': (os.path.basename(CERTIFICADO_PATH), file)}
        data = {'senha': SENHA_CERTIFICADO}
        
        # Log detalhado
        logger.debug(f"URL: {base_url}/certificado/{CNPJ_LIMPO}/certificado")
        logger.debug(f"Arquivo: {os.path.basename(CERTIFICADO_PATH)}")
        logger.debug(f"Tamanho do arquivo: {os.path.getsize(CERTIFICADO_PATH)} bytes")
        
        response = requests.put(
            f"{base_url}/certificado/{CNPJ_LIMPO}/certificado", 
            files=files, 
            data=data
        )
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        logger.info("✅ Certificado enviado com sucesso!")
        return True
    else:
        logger.error(f"❌ Erro no upload: {response.text}")
        return False

if __name__ == "__main__":
    test_upload_certificado()