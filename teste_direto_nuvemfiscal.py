import os
import base64
import requests
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Dados da empresa
CNPJ = "48144666000140"  # Sem pontuação
CNPJ_FORMATADO = "48.144.666/0001-40"  # Com pontuação (para logs)
RAZAO_SOCIAL = "NUNES E BUSATO BARBEARIA LTDA"
EMAIL = "vivianfragoso@moveonsales.com.br"

# Dados do certificado
CERTIFICADO_PATH = os.path.abspath(os.path.join("storage", "certificados", "barbearia.pfx"))
SENHA_CERTIFICADO = "Mateus3286"

# Credenciais da Nuvem Fiscal
CLIENT_ID = os.getenv('NUVEM_FISCAL_CLIENT_ID')
CLIENT_SECRET = os.getenv('NUVEM_FISCAL_CLIENT_SECRET')

def obter_token():
    """Obtém um token de acesso OAuth2 da Nuvem Fiscal"""
    logger.info("Obtendo token de acesso...")
    
    token_url = "https://auth.nuvemfiscal.com.br/oauth/token"
    
    # Usar apenas os escopos disponíveis
    payload = {
        "grant_type": "client_credentials",
        "scope": "empresa cnpj"  # Apenas escopos que temos certeza que funcionam
    }
    
    # Log das credenciais (parciais para segurança)
    logger.info(f"Client ID: {CLIENT_ID[:5]}...")
    logger.info(f"Client Secret: {CLIENT_SECRET[:5]}...")
    
    response = requests.post(
        token_url,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data=payload
    )
    
    logger.info(f"Status da autenticação: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        logger.info(f"Token obtido com sucesso: {token[:15]}...")
        return token
    else:
        logger.error(f"Erro ao obter token: {response.status_code} - {response.text}")
        return None

def fazer_upload_certificado():
    """Faz upload direto do certificado para a Nuvem Fiscal"""
    logger.info(f"\n=== Upload de Certificado para {RAZAO_SOCIAL} (CNPJ: {CNPJ_FORMATADO}) ===")
    
    # Obter token
    token = obter_token()
    if not token:
        logger.error("Não foi possível obter token. Abortando.")
        return
    
    # Verificar se o arquivo existe
    if not os.path.exists(CERTIFICADO_PATH):
        logger.error(f"Arquivo não encontrado: {CERTIFICADO_PATH}")
        return
    
    # Mostrar informações do arquivo
    file_size = os.path.getsize(CERTIFICADO_PATH)
    logger.info(f"Arquivo encontrado: {CERTIFICADO_PATH}")
    logger.info(f"Tamanho: {file_size} bytes")
    
    # Ler arquivo e codificar em base64
    with open(CERTIFICADO_PATH, 'rb') as file:
        certificado_bytes = file.read()
    
    logger.info(f"Leitura do arquivo concluída: {len(certificado_bytes)} bytes")
    
    # Mostrar primeiros bytes do arquivo para debug
    primeiros_bytes = ' '.join(f'{b:02x}' for b in certificado_bytes[:16])
    logger.info(f"Primeiros bytes: {primeiros_bytes}")
    
    certificado_base64 = base64.b64encode(certificado_bytes).decode('utf-8')
    logger.info(f"Codificação Base64 concluída: {len(certificado_base64)} caracteres")
    
    # Montar payload conforme documentação
    payload = {
        "certificado": certificado_base64,
        "password": SENHA_CERTIFICADO
    }
    
    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # URL para upload - conforme documentação
    url = f"https://api.nuvemfiscal.com.br/empresas/{CNPJ}/certificado"
    
    logger.info(f"Enviando para URL: {url}")
    
    # Fazer requisição PUT
    response = requests.put(url, json=payload, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        logger.info("✅ Certificado enviado com sucesso!")
        logger.info(f"Resposta: {response.text}")
        return True
    else:
        logger.error(f"❌ Erro ao enviar certificado: {response.status_code} - {response.text}")
        return False

def consultar_certificado():
    """Consulta o certificado da empresa na Nuvem Fiscal"""
    logger.info(f"\n=== Consulta de Certificado para {RAZAO_SOCIAL} (CNPJ: {CNPJ_FORMATADO}) ===")
    
    # Obter token
    token = obter_token()
    if not token:
        logger.error("Não foi possível obter token. Abortando.")
        return
    
    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    # URL para consulta
    url = f"https://api.nuvemfiscal.com.br/empresas/{CNPJ}/certificado"
    
    logger.info(f"Consultando URL: {url}")
    
    # Fazer requisição GET
    response = requests.get(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        logger.info("✅ Certificado encontrado!")
        data = response.json()
        logger.info(f"Serial Number: {data.get('serial_number')}")
        logger.info(f"Emissor: {data.get('issuer_name')}")
        logger.info(f"Validade: {data.get('not_valid_before')} até {data.get('not_valid_after')}")
        return True
    else:
        logger.error(f"❌ Erro ao consultar certificado: {response.status_code} - {response.text}")
        return False

def excluir_certificado():
    """Exclui o certificado da empresa na Nuvem Fiscal"""
    logger.info(f"\n=== Exclusão de Certificado para {RAZAO_SOCIAL} (CNPJ: {CNPJ_FORMATADO}) ===")
    
    # Obter token
    token = obter_token()
    if not token:
        logger.error("Não foi possível obter token. Abortando.")
        return
    
    # Headers
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # URL para exclusão
    url = f"https://api.nuvemfiscal.com.br/empresas/{CNPJ}/certificado"
    
    logger.info(f"Excluindo URL: {url}")
    
    # Fazer requisição DELETE
    response = requests.delete(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 204:
        logger.info("✅ Certificado excluído com sucesso!")
        return True
    else:
        logger.error(f"❌ Erro ao excluir certificado: {response.status_code} - {response.text}")
        return False

def main():
    """Executa o fluxo completo de teste"""
    # Verificar ambiente
    logger.info("=== Verificando ambiente ===")
    logger.info(f"Diretório atual: {os.getcwd()}")
    
    # Verificar se o arquivo de certificado existe
    if os.path.exists(CERTIFICADO_PATH):
        logger.info(f"✅ Arquivo de certificado encontrado: {CERTIFICADO_PATH}")
    else:
        logger.error(f"❌ Arquivo de certificado NÃO encontrado: {CERTIFICADO_PATH}")
        pasta_pai = os.path.dirname(CERTIFICADO_PATH)
        if os.path.exists(pasta_pai):
            logger.info(f"   Pasta existe: {pasta_pai}")
            logger.info(f"   Arquivos na pasta: {os.listdir(pasta_pai)}")
        else:
            logger.info(f"   Pasta não existe: {pasta_pai}")
        return
    
    # 1. Tentar fazer upload do certificado
    logger.info("\n1. INICIANDO UPLOAD DO CERTIFICADO")
    upload_success = fazer_upload_certificado()
    
    # 2. Se o upload foi bem-sucedido, tentar consultar
    if upload_success:
        logger.info("\n2. INICIANDO CONSULTA DO CERTIFICADO")
        consulta_success = consultar_certificado()
    else:
        logger.warning("Pulando consulta devido à falha no upload")
        consulta_success = False
    
    # 3. Se upload ou consulta funcionou, tentar excluir
    if upload_success or consulta_success:
        logger.info("\n3. INICIANDO EXCLUSÃO DO CERTIFICADO")
        excluir_certificado()
    else:
        logger.warning("Pulando exclusão devido a falhas anteriores")

if __name__ == "__main__":
    main()