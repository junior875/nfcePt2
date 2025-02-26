from flask import Blueprint, request, jsonify

# Criar blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota de login (básica, a ser implementada)
    """
    return jsonify({"mensagem": "Funcionalidade de login a ser implementada"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rota de registro (básica, a ser implementada)
    """
    return jsonify({"mensagem": "Funcionalidade de registro a ser implementada"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Rota de logout (básica, a ser implementada)
    """
    return jsonify({"mensagem": "Funcionalidade de logout a ser implementada"}), 200