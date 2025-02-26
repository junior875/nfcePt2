import os
import json
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Base URL da API
base_url = os.getenv('API_URL', 'http://localhost:5000/api')

def test_consultar_cnpj():
    """Testa a consulta de CNPJ"""
    print("\n=== Teste de Consulta de CNPJ ===")
    
    # CNPJ da Pague Menos
    cnpj = "06626253000151"
    
    response = requests.get(f"{base_url}/empresa/consultar-cnpj/{cnpj}")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Razão Social: {data.get('razao_social')}")
        print(f"Nome Fantasia: {data.get('nome_fantasia')}")
        if 'endereco' in data:
            endereco = data['endereco']
            print(f"Endereço: {endereco.get('logradouro')}, {endereco.get('numero')} - {endereco.get('bairro')}")
            print(f"         {endereco.get('municipio')} - {endereco.get('uf')}")
    else:
        print(f"Erro: {response.text}")

def test_criar_empresa():
    """Testa a criação de empresa"""
    print("\n=== Teste de Criação de Empresa ===")
    
    # Dados da empresa
    empresa_data = {
        "cpf_cnpj": "06626253000151",
        "nome_razao_social": "EMPREENDIMENTOS PAGUE MENOS S/A",
        "nome_fantasia": "FARMÁCIAS PAGUE MENOS",
        "email": "contato@paguemenos.com.br",
        "telefone": "8532553233",
        "endereco": {
            "cep": "60175047",
            "logradouro": "R SENADOR POMPEU",
            "numero": "1520",
            "complemento": "",
            "bairro": "CENTRO",
            "municipio": "FORTALEZA",
            "uf": "CE"
        }
    }
    
    response = requests.post(f"{base_url}/empresa", json=empresa_data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"Empresa criada com ID: {data.get('id')}")
        return data.get('id')
    else:
        print(f"Erro: {response.text}")
        return None

def test_listar_empresas():
    """Testa a listagem de empresas"""
    print("\n=== Teste de Listagem de Empresas ===")
    
    response = requests.get(f"{base_url}/empresa")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        empresas = response.json()
        print(f"Total de empresas: {len(empresas)}")
        
        for i, empresa in enumerate(empresas):
            print(f"{i+1}. {empresa.get('nome_razao_social')} - CNPJ: {empresa.get('cpf_cnpj')}")
    else:
        print(f"Erro: {response.text}")

def test_atualizar_empresa(empresa_id):
    """Testa a atualização de empresa"""
    if not empresa_id:
        print("\n=== Teste de Atualização de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    print(f"\n=== Teste de Atualização de Empresa (ID: {empresa_id}) ===")
    
    # Dados atualizados
    empresa_data = {
        "telefone": "8532553234",
        "email": "newemail@paguemenos.com.br",
        "endereco": {
            "complemento": "SEDE"
        }
    }
    
    response = requests.put(f"{base_url}/empresa/{empresa_id}", json=empresa_data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Empresa atualizada: {data.get('nome_razao_social')}")
        print(f"Novo telefone: {data.get('telefone')}")
        print(f"Novo email: {data.get('email')}")
        if data.get('endereco'):
            print(f"Novo complemento: {data.get('endereco').get('complemento')}")
    else:
        print(f"Erro: {response.text}")

def test_excluir_empresa(empresa_id):
    """Testa a exclusão de empresa"""
    if not empresa_id:
        print("\n=== Teste de Exclusão de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    print(f"\n=== Teste de Exclusão de Empresa (ID: {empresa_id}) ===")
    
    response = requests.delete(f"{base_url}/empresa/{empresa_id}")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("Empresa excluída com sucesso!")
    else:
        print(f"Erro: {response.text}")

def test_desativar_empresa(empresa_id):
    """Testa a desativação de empresa"""
    if not empresa_id:
        print("\n=== Teste de Desativação de Empresa: IGNORADO (ID não fornecido) ===")
        return
        
    print(f"\n=== Teste de Desativação de Empresa (ID: {empresa_id}) ===")
    
    response = requests.put(f"{base_url}/empresa/{empresa_id}/desativar")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Empresa desativada: {data.get('nome_razao_social')}")
        print(f"Status ativo: {data.get('ativo')}")
    else:
        print(f"Erro: {response.text}")

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