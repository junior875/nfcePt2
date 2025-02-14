from flask import Blueprint, request, jsonify

empresa_bp = Blueprint('empresa', __name__)

@empresa_bp.route('/empresa', methods=['POST'])
def criar_empresa():
    return jsonify({'message': 'Criar empresa endpoint'})

@empresa_bp.route('/empresa', methods=['GET'])
def listar_empresas():
    return jsonify({'message': 'Listar empresas endpoint'})