from flask import Blueprint, request, jsonify
from backend.app.services.nuvem_fiscal.certificado import CertificadoService
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Criar blueprint
certificado_bp = Blueprint('certificado', __name__, url_prefix='/api/certificado')

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['PUT'])
def upload_certificado(cpf_cnpj):
    """
    Realiza o upload de um certificado digital
    
    Args:
        cpf_cnpj (str): CPF/CNPJ da empresa
        
    Returns:
        JSON: Detalhes do certificado enviado ou erro
    """
    try:
        # Validar requisição
        if 'file' not in request.files:
            return jsonify({"error": "Arquivo obrigatório"}), 400
            
        if 'senha' not in request.form:
            return jsonify({"error": "Senha obrigatória"}), 400
        
        # Obter arquivo e senha
        certificado_file = request.files['file']
        senha = request.form['senha']
        
        # Validar arquivo
        if certificado_file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400
        
        # Inicializar serviço
        service = CertificadoService(cpf_cnpj)
        
        # Fazer upload do certificado
        result = service.upload_certificado(certificado_file, senha)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Falha ao enviar certificado"}), 400
            
    except Exception as e:
        logger.exception(f"Erro ao processar upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['GET'])
def get_certificado(cpf_cnpj):
    """
    Consulta um certificado digital
    
    Args:
        cpf_cnpj (str): CPF/CNPJ da empresa
        
    Returns:
        JSON: Detalhes do certificado ou erro
    """
    try:
        # Inicializar serviço
        service = CertificadoService(cpf_cnpj)
        
        # Consultar certificado
        certificado = service.get_certificado()
        
        if certificado:
            return jsonify(certificado), 200
        else:
            return jsonify({"error": "Certificado não encontrado"}), 404
            
    except Exception as e:
        logger.exception(f"Erro ao consultar certificado: {str(e)}")
        return jsonify({"error": str(e)}), 500

@certificado_bp.route('/<cpf_cnpj>/certificado', methods=['DELETE'])
def delete_certificado(cpf_cnpj):
    """
    Exclui um certificado digital
    
    Args:
        cpf_cnpj (str): CPF/CNPJ da empresa
        
    Returns:
        JSON: Mensagem de sucesso ou erro
    """
    try:
        # Inicializar serviço
        service = CertificadoService(cpf_cnpj)
        
        # Excluir certificado
        success = service.delete_certificado()
        
        if success:
            return jsonify({"message": "Certificado removido com sucesso"}), 200
        else:
            return jsonify({"error": "Falha ao remover certificado"}), 400
            
    except Exception as e:
        logger.exception(f"Erro ao excluir certificado: {str(e)}")
        return jsonify({"error": str(e)}), 500