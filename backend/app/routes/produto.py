from flask import Blueprint, request, jsonify

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify({'message': 'Listar produtos endpoint'})

@produto_bp.route('/produtos', methods=['POST'])
def criar_produto():
    return jsonify({'message': 'Criar produto endpoint'})