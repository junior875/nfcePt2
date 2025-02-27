from backend.app.services.nuvem_fiscal.client import NuvemFiscalClient
import json
from datetime import datetime, timezone
from random import randint


# Inicializa o cliente da Nuvem Fiscal
nuvem_client = NuvemFiscalClient()

# Geração do ID correto para NFC-e (44 números)
chave_nfe = f"NFe{randint(10**43, 10**44 - 1)}"

# Dados da venda
valor_produto = 5.00  # Valor unitário do produto
quantidade = 1  # Quantidade vendida
valor_total = valor_produto * quantidade  # Valor total da venda
pis = round(valor_total * 0.0165, 2)  # 1.65% de PIS
cofins = round(valor_total * 0.076, 2)  # 7.60% de COFINS

# Estrutura corrigida da NFC-e
payload = {
    "infNFe": {
        "versao": "4.00",
        "Id": chave_nfe,
        "ide": {
            "cUF": 31,  # Código do estado de MG (Minas Gerais)
            "cNF": "98765432",
            "natOp": "Venda de Mercadoria",
            "mod": 65,  # NFC-e (Nota Fiscal de Consumidor Eletrônica)
            "serie": 1,
            "nNF": 1002,
            "dhEmi": datetime.now(timezone.utc).isoformat(),
            "tpNF": 1,  # Saída
            "idDest": 1,  # Operação interna
            "cMunFG": "3106200",  # Código IBGE de Buritis - MG
            "tpImp": 4,  # Formato de DANFE NFC-e (sem papel)
            "tpEmis": 1,  # Emissão normal
            "cDV": 9,
            "tpAmb": 1,  # Ambiente de Produção
            "finNFe": 1,  # Nota fiscal normal
            "indFinal": 1,  # Consumidor final
            "indPres": 1,  # Presencial
            "procEmi": 0,
            "verProc": "1.0"
        },
        "emit": {
            "CNPJ": "48144666000140",
            "xNome": "NUNES E BUSATO BARBEARIA LTDA",
            "enderEmit": {
                "xLgr": "RUA ELI SEABRA FILHO",
                "nro": "510",
                "xBairro": "Buritis",
                "cMun": "3106200",
                "xMun": "Buritis",
                "UF": "MG",
                "CEP": "30575740",  # Sem traço
                "cPais": "1058",
                "xPais": "Brasil"
            },
            "IE": "0048643140066",
            "CRT": 1  # Simples Nacional
        },
        "dest": {
            "CPF": "12345678909",  # CPF válido fictício
            "xNome": "Consumidor Final",
            "indIEDest": 9
        },
        "det": [
            {
                "nItem": 1,
                "prod": {
                    "cProd": "001",
                    "xProd": "Coca-Cola 350ml",
                    "NCM": "22021000",  # Código NCM correto para refrigerantes
                    "CFOP": "5102",  # Venda dentro do estado
                    "uCom": "UN",
                    "qCom": quantidade,
                    "vUnCom": valor_produto,
                    "vProd": valor_total,
                    "uTrib": "UN",
                    "qTrib": quantidade,
                    "vUnTrib": valor_produto,
                    "indTot": 1,  # Produto entra no total da NF
                    "cEAN": "SEM GTIN",
                    "cEANTrib": "SEM GTIN"
                },
                "imposto": {
                    "ICMS": {
                        "ICMSSN102": {  
                            "orig": 0,  # Origem nacional
                            "CSOSN": "102"  # Simples Nacional - Sem cobrança de ICMS
                        }
                    },
                    "PIS": {
                        "PISAliq": {
                            "CST": "01",  # Tributado integralmente
                            "vBC": valor_total,  # Base de cálculo do PIS
                            "pPIS": 1.65,  # Percentual do PIS
                            "vPIS": pis  # Valor do PIS
                        }
                    },
                    "COFINS": {
                        "COFINSAliq": {
                            "CST": "01",  # Tributado integralmente
                            "vBC": valor_total,  # Base de cálculo do COFINS
                            "pCOFINS": 7.60,  # Percentual do COFINS
                            "vCOFINS": cofins  # Valor do COFINS
                        }
                    }
                }
            }
        ],
        "total": {
            "ICMSTot": {
                "vBC": 0.00,  # Simples Nacional - Sem base de cálculo para ICMS
                "vICMS": 0.00,  # ICMS não destacado
                "vICMSDeson": 0.00,
                "vFCP": 0.00,
                "vBCST": 0.00,
                "vST": 0.00,
                "vFCPST": 0.00,
                "vFCPSTRet": 0.00,
                "vProd": valor_total,  # Valor total dos produtos
                "vFrete": 0.00,
                "vSeg": 0.00,
                "vDesc": 0.00,
                "vII": 0.00,
                "vIPI": 0.00,
                "vIPIDevol": 0.00,
                "vPIS": pis,  # Soma do PIS dos itens
                "vCOFINS": cofins,  # Soma do COFINS dos itens
                "vOutro": 0.00,
                "vNF": valor_total  # Valor total da nota fiscal
            }
        },
        "transp": {
            "modFrete": 9  # Sem frete
        },
        "pag": {
            "detPag": [
                {
                    "indPag": 0,  # Pagamento à vista
                    "tPag": "01",  # 01 = Dinheiro
                    "vPag": valor_total  # Valor pago
                }
            ],
            "vTroco": 0.00
        }
    },
    "ambiente": "producao"
}

# Enviar requisição para emissão da NFC-e
try:
    response = nuvem_client.post("nfce", payload)

    if response:
        status = response.get("status", "desconhecido")
        if status == "autorizado":
            print("✅ NFC-e emitida e autorizada com sucesso!")
        else:
            motivo_rejeicao = response.get("autorizacao", {}).get("motivo_status", "Motivo desconhecido")
            print(f"❌ NFC-e rejeitada! Motivo: {motivo_rejeicao}")

        print(json.dumps(response, indent=4, ensure_ascii=False))
    else:
        print("❌ Erro ao emitir NFC-e!")

except Exception as e:
    print(f"❌ Erro ao emitir NFC-e: {str(e)}")
