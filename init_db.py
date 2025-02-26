# init_db.py
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from backend.app import create_app, db
from backend.app.models.empresa import Empresa, Endereco

# Criar app com contexto
app = create_app('development')

# Verificar e imprimir informações para debug
db_path = os.path.join(app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', ''))
print(f"Caminho do banco de dados: {db_path}")
print(f"O arquivo existe? {os.path.exists(db_path)}")

# Criar novo banco de dados
with app.app_context():
    print("Criando tabelas...")
    db.drop_all()  # Limpa qualquer tabela existente
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    # Listar tabelas criadas
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tabelas criadas: {tables}")
    
    # Listar colunas da tabela empresas
    if 'empresas' in tables:
        columns = [column['name'] for column in inspector.get_columns('empresas')]
        print(f"Colunas na tabela empresas: {columns}")
    
    print("Banco de dados inicializado com sucesso!")