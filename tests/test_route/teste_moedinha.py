# teste_moedinha.py
import requests
import json
import sys

# URL da API
BASE_URL = "http://localhost:5000/api"

def emitir_nfce_moedinha():
    """
    Testa a emissão de uma NFC-e com vários produtos pequenos totalizando R$ 1,00
    usando o CNPJ da Barbearia Nunes e Busato
    """
    # Endpoint para emissão de NFC-e
    url = f"{BASE_URL}/nfce/emitir"
    
    # Dados da requisição
    payload = {
        "empresa_cnpj": "48144666000140",  # CNPJ da Nunes e Busato Barbearia
        "cliente": {
            "cpf": "01234567890",  # CPF válido
            "nome": "Cliente Economizador"
        },
        "pagamento": {
            "forma": "dinheiro",
            "valor_recebido": 1.00
        },
        "produtos": [
            {
                "codigo": "BALA001",
                "descricao": "Bala Recheada de Cereja",
                "ncm": "17049020",  # NCM para balas
                "quantidade": 2,
                "valor_unitario": 0.05
            },
            {
                "codigo": "BALA002",
                "descricao": "Bala Refrescante de Limão",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.10
            },
            {
                "codigo": "DOCE001",
                "descricao": "Mini Doce de Leite",
                "ncm": "17049090",  # NCM para outros doces
                "quantidade": 1,
                "valor_unitario": 0.15
            },
            {
                "codigo": "CHIC001",
                "descricao": "Chiclete de Menta",
                "ncm": "17041000",  # NCM para gomas de mascar
                "quantidade": 1,
                "valor_unitario": 0.20
            },
            {
                "codigo": "PIRU001",
                "descricao": "Pirulito Mini de Framboesa",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.10
            },
            {
                "codigo": "JUJU001",
                "descricao": "Jujuba Sortida",
                "ncm": "17049020",
                "quantidade": 1,
                "valor_unitario": 0.25
            },
            {
                "codigo": "CARAM001",
                "descricao": "Caramelo Pequeno",
                "ncm": "17049090",
                "quantidade": 1,
                "valor_unitario": 0.10
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
    sucesso = emitir_nfce_moedinha()
    
    # Definir código de saída
    sys.exit(0 if sucesso else 1)