import os
import json
import requests
import sys
from dotenv import load_dotenv

# Adicionar diretório raiz ao path para importar corretamente
sys.path.append(os.path.abspath("."))

# Ajuste o caminho de importação conforme a estrutura do seu projeto
# Se sua Config está em backend/app/config.py:
from backend.app.config import Config

# Carregar variáveis de ambiente
load_dotenv()

def test_oauth2_token():
    """Testa a obtenção de token OAuth2"""
    print("\n=== Teste de Obtenção de Token OAuth2 ===")
    
    # Verificar credenciais
    client_id = os.getenv('NUVEM_FISCAL_CLIENT_ID')
    client_secret = os.getenv('NUVEM_FISCAL_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Credenciais não encontradas! Verifique o arquivo .env")
        return False
    
    print(f"Client ID: {client_id[:5]}***")
    print(f"Client Secret: {client_secret[:5]}***")
    
    # Obter token
    print("\nObtendo token...")
    token = Config.get_access_token()
    
    if token:
        print(f"✅ Token obtido com sucesso: {token[:10]}...")
        
        # Testar o token fazendo uma requisição
        print("\nTestando token com uma requisição...")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        url = "https://api.nuvemfiscal.com.br/empresas"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Token funcionou! Status: {response.status_code}")
            print(f"Resposta: {response.text[:100]}...")
            return True
        else:
            print(f"❌ Falha ao usar token. Status: {response.status_code}")
            print(f"Resposta: {response.text}")
    else:
        print("❌ Falha ao obter token")
    
    return False

def teste_fluxo_certificado():
    """Testa o fluxo completo de certificado usando uma instância do CertificadoService"""
    from backend.app.services.nuvem_fiscal.certificado import CertificadoService
    
    print("\n=== Teste do Fluxo Completo de Certificado ===")
    
    # CNPJ para teste
    cnpj = "48144666000140"  # Sem pontuação
    
    # Caminho do certificado
    certificado_path = os.path.abspath(os.path.join("storage", "certificados", "barbearia.pfx"))
    senha = "Mateus3286"
    
    # Verificar se o arquivo existe
    if not os.path.exists(certificado_path):
        print(f"❌ Arquivo não encontrado: {certificado_path}")
        return
    
    print(f"Arquivo encontrado: {certificado_path}")
    print(f"Tamanho: {os.path.getsize(certificado_path)} bytes")
    
    # Inicializar serviço
    service = CertificadoService(cnpj)
    
    # 1. Tentar upload
    print("\n1. Realizando upload do certificado...")
    result = service.upload_certificado(certificado_path, senha)
    
    if result:
        print("✅ Upload bem-sucedido!")
        print(f"Resposta: {json.dumps(result, indent=2)}")
        
        # 2. Consultar certificado
        print("\n2. Consultando certificado...")
        certificado = service.get_certificado()
        
        if certificado:
            print("✅ Consulta bem-sucedida!")
            print(f"Dados do certificado:")
            print(f"  - Serial Number: {certificado.get('serial_number')}")
            print(f"  - Emissor: {certificado.get('issuer_name')}")
            print(f"  - Validade: {certificado.get('not_valid_before')} até {certificado.get('not_valid_after')}")
            
            # 3. Excluir certificado
            print("\n3. Excluindo certificado...")
            if service.delete_certificado():
                print("✅ Exclusão bem-sucedida!")
            else:
                print("❌ Falha na exclusão do certificado")
        else:
            print("❌ Falha na consulta do certificado")
    else:
        print("❌ Falha no upload do certificado")

if __name__ == "__main__":
    # Testar obtenção do token
    if test_oauth2_token():
        # Se a autenticação funcionou, testar o fluxo completo
        teste_fluxo_certificado()