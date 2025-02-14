from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'})

@auth_bp.route('/register', methods=['POST'])
def register():
    return jsonify({'message': 'Register endpoint'})