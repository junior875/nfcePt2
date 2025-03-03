# teste_emissao_nfce_corrigido.py
import requests
import json
import sys

# URL da API (ajuste conforme seu ambiente)
BASE_URL = "http://localhost:5000/api"

def emitir_nfce_teste():
    """
    Testa a emissão de uma NFC-e com 5 balas e 1 refrigerante
    """
    # Endpoint para emissão de NFC-e
    url = f"{BASE_URL}/nfce/emitir"
    
    # Dados da requisição com CPF válido
    payload = {
        "empresa_cnpj": "48144666000140",
        "cliente": {
            "cpf": "01234567890",  # CPF válido
            "nome": "Cliente Teste"
        },
        "pagamento": {
            "forma": "dinheiro",
            "valor_recebido": 10.00  # Pagou com 10 reais
        },
        "produtos": [
            {
                "codigo": "BAL001",
                "descricao": "Bala de Morango",
                "ncm": "17049020",  # NCM para balas
                "quantidade": 1,
                "valor_unitario": 1.00
            },
            {
                "codigo": "BAL002",
                "descricao": "Bala de Uva",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 1.00
            },
            {
                "codigo": "BAL003",
                "descricao": "Bala de Menta",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 1.00
            },
            {
                "codigo": "BAL004",
                "descricao": "Bala de Canela",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 1.00
            },
            {
                "codigo": "BAL005",
                "descricao": "Bala de Maçã Verde",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 1.00
            },
            {
                "codigo": "REF001",
                "descricao": "Refrigerante Cola 350ml",
                "ncm": "22021000",  # NCM para refrigerantes
                "quantidade": 1,
                "valor_unitario": 5.00
            }
        ]
    }
    
    # Cabeçalhos
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Enviando requisição para emissão de NFC-e...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Enviar requisição
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Verificar resposta
        if response.status_code == 200:
            print("\n✅ NFC-e emitida com sucesso!")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            return True
        else:
            print(f"\n❌ Erro ao emitir NFC-e! Status: {response.status_code}")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            return False
    
    except Exception as e:
        print(f"\n❌ Erro ao fazer requisição: {str(e)}")
        return False

if __name__ == "__main__":
    # Executar teste
    sucesso = emitir_nfce_teste()
    
    # Definir código de saída
    sys.exit(0 if sucesso else 1)