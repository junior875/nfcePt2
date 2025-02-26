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

def test_consultar_cnpj():
    """Testa a consulta de CNPJ"""
    logger.info("\n=== Teste de Consulta de CNPJ ===")
    
    # CNPJ da Pague Menos
    cnpj = "06626253000151"
    
    logger.debug(f"Consultando CNPJ: {cnpj}")
    response = requests.get(f"{base_url}/empresa/consultar-cnpj/{cnpj}")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        logger.debug(f"Resposta da API: {json.dumps(data, indent=2)}")
        logger.info(f"Razão Social: {data.get('razao_social')}")
        logger.info(f"Nome Fantasia: {data.get('nome_fantasia')}")
        if 'endereco' in data:
            endereco = data['endereco']
            logger.info(f"Endereço: {endereco.get('logradouro')}, {endereco.get('numero')} - {endereco.get('bairro')}")
            logger.info(f"         {endereco.get('municipio')} - {endereco.get('uf')}")
    else:
        logger.error(f"Erro: {response.text}")

def test_criar_empresa():
    """Testa a criação de empresa"""
    logger.info("\n=== Teste de Criação de Empresa ===")
    
    empresa_data = {
    "cpf_cnpj": "06626253000151",
    "nome_razao_social": "EMPREENDIMENTOS PAGUE MENOS S/A",
    "nome_fantasia": "FARMÁCIAS PAGUE MENOS",
    "email": "contato@paguemenos.com.br",
    "telefone": "8532553233",
    "inscricao_estadual": "123456",
    "inscricao_municipal": "654321",
    "endereco": {
        "cep": "60175047",
        "logradouro": "R SENADOR POMPEU",
        "numero": "1520",
        "complemento": "",
        "bairro": "CENTRO",
        "codigo_municipio": "2304400",  # Código IBGE de Fortaleza
        "cidade": "FORTALEZA",
        "uf": "CE",
        "codigo_pais": "1058",  # Código do Brasil
        "pais": "Brasil"
    }
}
    
    logger.debug(f"Dados da empresa: {json.dumps(empresa_data, indent=2)}")
    response = requests.post(f"{base_url}/empresa", json=empresa_data)
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        logger.info(f"Empresa criada com ID: {data.get('id')}")
        return data.get('id')
    else:
        logger.error(f"Erro: {response.text}")
        return None

def test_listar_empresas():
    """Testa a listagem de empresas"""
    logger.info("\n=== Teste de Listagem de Empresas ===")
    
    response = requests.get(f"{base_url}/empresa")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        empresas = response.json()
        logger.info(f"Total de empresas: {len(empresas)}")
        
        for i, empresa in enumerate(empresas):
            logger.info(f"{i+1}. {empresa.get('nome_razao_social')} - CNPJ: {empresa.get('cpf_cnpj')}")
    else:
        logger.error(f"Erro: {response.text}")

def test_atualizar_empresa(empresa_id):
    """Testa a atualização de empresa"""
    if not empresa_id:
        logger.info("\n=== Teste de Atualização de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    logger.info(f"\n=== Teste de Atualização de Empresa (ID: {empresa_id}) ===")
    
    # Dados atualizados
    empresa_data = {
        "telefone": "8532553234",
        "email": "newemail@paguemenos.com.br",
        "endereco": {
            "complemento": "SEDE"
        }
    }
    
    logger.debug(f"Dados atualizados: {json.dumps(empresa_data, indent=2)}")
    response = requests.put(f"{base_url}/empresa/{empresa_id}", json=empresa_data)
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Empresa atualizada: {data.get('nome_razao_social')}")
        logger.info(f"Novo telefone: {data.get('telefone')}")
        logger.info(f"Novo email: {data.get('email')}")
        if data.get('endereco'):
            logger.info(f"Novo complemento: {data.get('endereco').get('complemento')}")
    else:
        logger.error(f"Erro: {response.text}")

def test_excluir_empresa(empresa_id):
    """Testa a exclusão de empresa"""
    if not empresa_id:
        logger.info("\n=== Teste de Exclusão de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    logger.info(f"\n=== Teste de Exclusão de Empresa (ID: {empresa_id}) ===")
    
    response = requests.delete(f"{base_url}/empresa/{empresa_id}")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        logger.info("Empresa excluída com sucesso!")
    else:
        logger.error(f"Erro: {response.text}")

def test_desativar_empresa(empresa_id):
    """Testa a desativação de empresa"""
    if not empresa_id:
        logger.info("\n=== Teste de Desativação de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    logger.info(f"\n=== Teste de Desativação de Empresa (ID: {empresa_id}) ===")
    
    response = requests.put(f"{base_url}/empresa/{empresa_id}/desativar")
    
    logger.debug(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Empresa desativada: {data.get('nome_razao_social')}")
        logger.info(f"Status ativo: {data.get('ativo')}")
    else:
        logger.error(f"Erro: {response.text}")

def run_tests():
    """Executa todos os testes em sequência"""
    # Teste de consulta CNPJ
    test_consultar_cnpj()
    
    # Teste de criação de empresa
    empresa_id = test_criar_empresa()
    
    # Teste de listagem de empresas
    test_listar_empresas()
    
    # Teste de atualização de empresa
    if empresa_id:
        test_atualizar_empresa(empresa_id)
    
    # Teste de desativação de empresa
    if empresa_id:
        test_desativar_empresa(empresa_id)
    
    # Teste de exclusão de empresa
    if empresa_id:
        test_excluir_empresa(empresa_id)
    
    # Verificar se empresa foi realmente excluída
    if empresa_id:
        test_listar_empresas()

if __name__ == "__main__":
    run_tests()