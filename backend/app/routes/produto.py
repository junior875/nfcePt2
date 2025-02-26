from flask import Blueprint, request, jsonify

# Criar blueprint
produto_bp = Blueprint('produto', __name__, url_prefix='/api/produto')

@produto_bp.route('', methods=['GET'])
def listar_produtos():
    """
    Lista todos os produtos (básica, a ser implementada)
    """
    return jsonify({"mensagem": "Funcionalidade de listagem de produtos a ser implementada"}), 200

@produto_bp.route('/<int:produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    """
    Busca um produto pelo ID (básica, a ser implementada)
    """
    return jsonify({"mensagem": f"Funcionalidade de busca de produto {produto_id} a ser implementada"}), 200

@produto_bp.route('', methods=['POST'])
def criar_produto():
    """
    Cria um novo produto (básica, a ser implementada)
    """
    return jsonify({"mensagem": "Funcionalidade de criação de produto a ser implementada"}), 200

@produto_bp.route('/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """
    Atualiza um produto existente (básica, a ser implementada)
    """
    return jsonify({"mensagem": f"Funcionalidade de atualização de produto {produto_id} a ser implementada"}), 200

@produto_bp.route('/<int:produto_id>', methods=['DELETE'])
def excluir_produto(produto_id):
    """
    Exclui um produto (básica, a ser implementada)
    """
    return jsonify({"mensagem": f"Funcionalidade de exclusão de produto {produto_id} a ser implementada"}), 200