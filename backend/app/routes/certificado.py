from flask import request, jsonify, Blueprint
from backend.app.services.nuvem_fiscal.certificado import CertificadoService

certificado_bp = Blueprint('certificado', __name__)

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['PUT'])
def upload_certificado(cpf_cnpj):
    if 'file' not in request.files or 'senha' not in request.form:
        return jsonify({"error": "Arquivo e senha são obrigatórios"}), 400
    service = CertificadoService(cpf_cnpj)
    result = service.upload_certificado(request.files['file'], request.form['senha'])
    if result:
        return jsonify(result), 200
    return jsonify({"error": "Falha ao enviar certificado"}), 400

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['GET'])
def get_certificado(cpf_cnpj):
    service = CertificadoService(cpf_cnpj)
    certificado = service.get_certificado()
    if certificado:
        return jsonify(certificado), 200
    return jsonify({"error": "Certificado não encontrado"}), 404

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['DELETE'])
def delete_certificado(cpf_cnpj):
    service = CertificadoService(cpf_cnpj)
    if service.delete_certificado():
        return jsonify({"message": "Certificado removido com sucesso"}), 200
    return jsonify({"error": "Falha ao remover certificado"}), 400