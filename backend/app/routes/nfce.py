from flask import Blueprint, request, jsonify

nfce_bp = Blueprint('nfce', __name__)

@nfce_bp.route('/emitir', methods=['POST'])
def emitir_nfce():
    return jsonify({'message': 'Emitir NFCe endpoint'})

@nfce_bp.route('/consultar/<chave>', methods=['GET'])
def consultar_nfce(chave):
    return jsonify({'message': f'Consultar NFCe {chave}'})