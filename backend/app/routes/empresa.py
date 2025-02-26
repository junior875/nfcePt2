from flask import Blueprint, request, jsonify
from backend.app.services.empresa_service import EmpresaService
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Criar blueprint
empresa_bp = Blueprint('empresa', __name__, url_prefix='/api/empresa')

# Instanciar serviço
empresa_service = EmpresaService()

@empresa_bp.route('/consultar-cnpj/<cnpj>', methods=['GET'])
def consultar_cnpj(cnpj):
    """
    Consulta informações de uma empresa pelo CNPJ na API da Nuvem Fiscal
    
    Args:
        cnpj (str): CNPJ a ser consultado
        
    Returns:
        JSON: Dados da empresa consultada
    """
    try:
        dados_cnpj = empresa_service.consultar_cnpj(cnpj)
        return jsonify(dados_cnpj), 200
    except Exception as e:
        logger.error(f"Erro ao consultar CNPJ {cnpj}: {str(e)}")
        return jsonify({"erro": str(e)}), 400

@empresa_bp.route('', methods=['GET'])
def listar_empresas():
    """
    Lista todas as empresas cadastradas
    
    Returns:
        JSON: Lista de empresas
    """
    try:
        # Parâmetro para filtrar apenas empresas ativas (padrão: True)
        ativas = request.args.get('ativas', 'true').lower() == 'true'
        
        empresas = empresa_service.listar_empresas(ativas=ativas)
        return jsonify([empresa.to_dict() for empresa in empresas]), 200
    except Exception as e:
        logger.error(f"Erro ao listar empresas: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['GET'])
def buscar_empresa(empresa_id):
    """
    Busca uma empresa pelo ID
    
    Args:
        empresa_id (int): ID da empresa
        
    Returns:
        JSON: Dados da empresa
    """
    try:
        empresa = empresa_service.buscar_empresa_por_id(empresa_id)
        if not empresa:
            return jsonify({"erro": f"Empresa com ID {empresa_id} não encontrada"}), 404
        
        return jsonify(empresa.to_dict()), 200
    except Exception as e:
        logger.error(f"Erro ao buscar empresa {empresa_id}: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@empresa_bp.route('', methods=['POST'])
def criar_empresa():
    """
    Cria uma nova empresa
    
    Returns:
        JSON: Dados da empresa criada
    """
    try:
        dados = request.json
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['cpf_cnpj', 'nome_razao_social', 'email']
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({"erro": f"Campo obrigatório não fornecido: {campo}"}), 400
        
        # Verificar se já existe empresa com esse CNPJ
        cnpj = dados['cpf_cnpj']
        empresa_existente = empresa_service.buscar_empresa_por_cnpj(cnpj)
        if empresa_existente:
            return jsonify({"erro": f"Já existe uma empresa cadastrada com o CNPJ {cnpj}"}), 409
        
        # Criar empresa
        nova_empresa = empresa_service.criar_empresa(dados)
        return jsonify(nova_empresa.to_dict()), 201
    
    except ValueError as e:
        # Erros de validação
        logger.error(f"Erro de validação ao criar empresa: {str(e)}")
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        # Outros erros
        logger.error(f"Erro ao criar empresa: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['PUT'])
def atualizar_empresa(empresa_id):
    """
    Atualiza uma empresa existente
    
    Args:
        empresa_id (int): ID da empresa a ser atualizada
        
    Returns:
        JSON: Dados da empresa atualizada
    """
    try:
        dados = request.json
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Verificar se a empresa existe
        empresa = empresa_service.buscar_empresa_por_id(empresa_id)
        if not empresa:
            return jsonify({"erro": f"Empresa com ID {empresa_id} não encontrada"}), 404
        
        # Atualizar empresa
        empresa_atualizada = empresa_service.atualizar_empresa(empresa_id, dados)
        return jsonify(empresa_atualizada.to_dict()), 200
    
    except ValueError as e:
        # Erros de validação
        logger.error(f"Erro de validação ao atualizar empresa {empresa_id}: {str(e)}")
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        # Outros erros
        logger.error(f"Erro ao atualizar empresa {empresa_id}: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['DELETE'])
def excluir_empresa(empresa_id):
    """
    Exclui uma empresa
    
    Args:
        empresa_id (int): ID da empresa a ser excluída
        
    Returns:
        JSON: Mensagem de sucesso
    """
    try:
        # Verificar se a empresa existe
        empresa = empresa_service.buscar_empresa_por_id(empresa_id)
        if not empresa:
            return jsonify({"erro": f"Empresa com ID {empresa_id} não encontrada"}), 404
        
        # Excluir empresa
        empresa_service.excluir_empresa(empresa_id)
        return jsonify({"mensagem": f"Empresa com ID {empresa_id} excluída com sucesso"}), 200
    
    except Exception as e:
        logger.error(f"Erro ao excluir empresa {empresa_id}: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@empresa_bp.route('/<int:empresa_id>/desativar', methods=['PUT'])
def desativar_empresa(empresa_id):
    """
    Desativa uma empresa (alternativa à exclusão)
    
    Args:
        empresa_id (int): ID da empresa a ser desativada
        
    Returns:
        JSON: Dados da empresa desativada
    """
    try:
        # Verificar se a empresa existe
        empresa = empresa_service.buscar_empresa_por_id(empresa_id)
        if not empresa:
            return jsonify({"erro": f"Empresa com ID {empresa_id} não encontrada"}), 404
        
        # Desativar empresa
        empresa_desativada = empresa_service.desativar_empresa(empresa_id)
        return jsonify(empresa_desativada.to_dict()), 200
    
    except Exception as e:
        logger.error(f"Erro ao desativar empresa {empresa_id}: {str(e)}")
        return jsonify({"erro": str(e)}), 500