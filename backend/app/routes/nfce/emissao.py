# backend/app/routes/nfce/emissao.py
from flask import Blueprint, request, jsonify
from backend.app.services.nfce.emissao_service import NFCeEmissaoService
import logging

logger = logging.getLogger(__name__)

# Criar blueprint
nfce_blueprint = Blueprint('nfce', __name__, url_prefix='/api/nfce')

# Criar serviço
emissao_service = NFCeEmissaoService()

@nfce_blueprint.route('/emitir', methods=['POST'])
def emitir():
    """
    Endpoint para emitir uma NFC-e
    
    Request body:
    {
        "empresa_cnpj": "48144666000140",
        "cliente": {
            "cpf": "12345678909",  // Opcional
            "nome": "Consumidor Final"  // Opcional
        },
        "pagamento": {
            "forma": "dinheiro",  // "dinheiro", "credito", "debito", "pix"
            "valor_recebido": 50.00  // Opcional, para cálculo de troco se for dinheiro
        },
        "produtos": [
            {
                "codigo": "001",
                "descricao": "Coca-Cola 350ml",
                "ncm": "22021000",
                "quantidade": 2,
                "valor_unitario": 5.00
            },
            {
                "codigo": "002",
                "descricao": "Cerveja Original 600ml",
                "ncm": "22030000",
                "quantidade": 1,
                "valor_unitario": 12.00
            }
        ]
    }
    
    Response:
    {
        // Resposta da API da Nuvem Fiscal
    }
    """
    try:
        # Obter dados da requisição
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado foi enviado"}), 400
        
        # Processar emissão
        resposta = emissao_service.processar_emissao(dados)
        
        # Verificar se ocorreu erro
        if "erro" in resposta:
            return jsonify(resposta), 400
        
        # Retornar resposta de sucesso
        return jsonify(resposta), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {e}")
        return jsonify({"erro": str(e)}), 500

@nfce_blueprint.route('/', methods=['GET'])
def listar():
    """
    Endpoint para listar as NFC-e emitidas
    
    Query params:
    - empresa_id (opcional): ID da empresa
    - status (opcional): Status da NFC-e
    - data_inicio (opcional): Data inicial (formato: YYYY-MM-DD)
    - data_fim (opcional): Data final (formato: YYYY-MM-DD)
    
    Response:
    {
        "nfces": [
            {
                "id": 1,
                "nuvem_fiscal_id": "nfc_123456",
                "chave": "31250248144666000140650010000010021987654329",
                "status": "autorizado",
                ...
            }
        ]
    }
    """
    # Endpoint para implementação futura
    return jsonify({"mensagem": "Endpoint em implementação"}), 501

@nfce_blueprint.route('/<id>', methods=['GET'])
def obter(id):
    """
    Endpoint para obter uma NFC-e específica
    
    Path params:
    - id: ID da NFC-e
    
    Response:
    {
        "id": 1,
        "nuvem_fiscal_id": "nfc_123456",
        "chave": "31250248144666000140650010000010021987654329",
        "status": "autorizado",
        ...
    }
    """
    # Endpoint para implementação futura
    return jsonify({"mensagem": "Endpoint em implementação"}), 501

@nfce_blueprint.route('/<id>/cancelar', methods=['POST'])
def cancelar(id):
    """
    Endpoint para cancelar uma NFC-e
    
    Path params:
    - id: ID da NFC-e
    
    Request body:
    {
        "justificativa": "Justificativa do cancelamento"
    }
    
    Response:
    {
        "mensagem": "NFC-e cancelada com sucesso",
        ...
    }
    """
    # Endpoint para implementação futura
    return jsonify({"mensagem": "Endpoint em implementação"}), 501