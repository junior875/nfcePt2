import os
import json
import requests
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Base URL da API
base_url = os.getenv('API_URL', 'http://localhost:5000/api')

# Configurações do certificado
CNPJ = "48.144.666-0001-40"  # CNPJ da empresa (ajustado)
CERTIFICADO_PATH = os.path.join("storage", "certificados", "barbearia.pfx")  # Caminho do certificado
SENHA_CERTIFICADO = "Mateus3286"  # Senha do certificado

def test_upload_certificado():
    """Testa o upload do certificado A1"""
    logger.info("\n=== Teste de Upload do Certificado A1 ===")
    
    # Verifica se o arquivo do certificado existe
    if not os.path.exists(CERTIFICADO_PATH):
        logger.error(f"Arquivo do certificado não encontrado: {CERTIFICADO_PATH}")
        return
    
    # Envia o certificado para a API
    with open(CERTIFICADO_PATH, 'rb') as file:
        files = {'file': (os.path.basename(CERTIFICADO_PATH), file)}
        data = {'senha': SENHA_CERTIFICADO}
        response = requests.put(f"{base_url}/certificado/{CNPJ}/certificado", files=files, data=data)
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        logger.info("Certificado enviado com sucesso!")
        logger.debug(f"Resposta da API: {json.dumps(data, indent=2)}")
    else:
        logger.error(f"Erro: {response.text}")

def test_consultar_certificado():
    """Testa a consulta do certificado A1"""
    logger.info("\n=== Teste de Consulta do Certificado A1 ===")
    
    # Consulta o certificado na API
    response = requests.get(f"{base_url}/certificado/{CNPJ}/certificado")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        logger.info("Detalhes do certificado:")
        logger.debug(f"Resposta da API: {json.dumps(data, indent=2)}")
        logger.info(f"Serial Number: {data.get('serial_number')}")
        logger.info(f"Validade: {data.get('not_valid_before')} até {data.get('not_valid_after')}")
    else:
        logger.error(f"Erro: {response.text}")

def test_excluir_certificado():
    """Testa a exclusão do certificado A1"""
    logger.info("\n=== Teste de Exclusão do Certificado A1 ===")
    
    # Exclui o certificado na API
    response = requests.delete(f"{base_url}/certificado/{CNPJ}/certificado")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 204:
        logger.info("Certificado excluído com sucesso!")
    else:
        logger.error(f"Erro: {response.text}")

def run_tests():
    """Executa todos os testes em sequência"""
    # Teste de upload do certificado
    test_upload_certificado()
    
    # Teste de consulta do certificado
    test_consultar_certificado()
    
    # Teste de exclusão do certificado
    test_excluir_certificado()

if __name__ == "__main__":
    run_tests()