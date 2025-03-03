# teste_mini_compra.py
import requests
import json
import sys

# URL da API
BASE_URL = "http://localhost:5000/api"

def emitir_nfce_mini_compra():
    """
    Testa a emissão de uma NFC-e com múltiplos produtos de baixo valor
    """
    # Endpoint para emissão de NFC-e
    url = f"{BASE_URL}/nfce/emitir"
    
    # Dados da requisição
    payload = {
        "empresa_cnpj": "48144666000140",
        "cliente": {
            "cpf": "01234567890",  # CPF válido
            "nome": "Comprador Econômico"
        },
        "pagamento": {
            "forma": "dinheiro",
            "valor_recebido": 1.00  # Pagou com 1 real
        },
        "produtos": [
            {
                "codigo": "CHIC001",
                "descricao": "Chiclete de Tutti-Frutti",
                "ncm": "17041000",  # NCM para gomas de mascar
                "quantidade": 1,
                "valor_unitario": 0.10
            },
            {
                "codigo": "BAL010",
                "descricao": "Bala de Hortelã",
                "ncm": "17049020",  # NCM para balas
                "quantidade": 2,
                "valor_unitario": 0.05
            },
            {
                "codigo": "BAL011",
                "descricao": "Bala de Café",
                "ncm": "17049020",
                "quantidade": 3,
                "valor_unitario": 0.05
            },
            {
                "codigo": "BAL012",
                "descricao": "Bala de Mel",
                "ncm": "17049020",
                "quantidade": 2,
                "valor_unitario": 0.05
            },
            {
                "codigo": "BAL013",
                "descricao": "Bala de Gengibre",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.05
            },
            {
                "codigo": "PIRJ001",
                "descricao": "Pirulito Pequeno Morango",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.15
            },
            {
                "codigo": "PIRJ002",
                "descricao": "Pirulito Pequeno Uva",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.15
            },
            {
                "codigo": "DLCE001",
                "descricao": "Doce de Leite em Tablete",
                "ncm": "17049090",  # NCM para outros doces
                "quantidade": 1,
                "valor_unitario": 0.20
            }
        ]
    }
    
    # Calcular valor total para verificação
    valor_total = sum(p["quantidade"] * p["valor_unitario"] for p in payload["produtos"])
    print(f"Valor total calculado: R$ {valor_total:.2f}")
    
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
    sucesso = emitir_nfce_mini_compra()
    
    # Definir código de saída
    sys.exit(0 if sucesso else 1)