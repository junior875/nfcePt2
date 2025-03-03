# recreate_database.py
# Script para recriar o banco de dados com a estrutura correta para NFC-e
import os
import sys
import sqlite3
from datetime import datetime

# Configurar o caminho para o banco de dados
db_path = 'database/app.db'

def recriar_banco():
    try:
        print(f"Recriando banco de dados: {db_path}")
        
        # Verificar se o diretório existe
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"Diretório {db_dir} criado.")
        
        # Se o banco já existir, remover
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Banco de dados existente removido.")
        
        # Conectar ao banco de dados (cria um novo)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criar tabela de empresas
        cursor.execute('''
        CREATE TABLE empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf_cnpj VARCHAR(18) NOT NULL UNIQUE,
            inscricao_estadual VARCHAR(30),
            inscricao_municipal VARCHAR(30),
            nome_razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            email VARCHAR(255),
            telefone VARCHAR(20),
            tipo_pessoa VARCHAR(20) NOT NULL DEFAULT 'Jurídica',
            ativo BOOLEAN NOT NULL DEFAULT 1,
            data_cadastro DATETIME NOT NULL,
            data_atualizacao DATETIME NOT NULL
        )
        ''')
        
        # Criar tabela de endereços (incluindo codigo_municipio)
        cursor.execute('''
        CREATE TABLE enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            cep VARCHAR(10) NOT NULL,
            logradouro VARCHAR(255) NOT NULL,
            numero VARCHAR(20) NOT NULL,
            complemento VARCHAR(255),
            bairro VARCHAR(255) NOT NULL,
            codigo_municipio VARCHAR(20) NOT NULL,
            municipio VARCHAR(255) NOT NULL,
            uf VARCHAR(2) NOT NULL,
            data_cadastro DATETIME NOT NULL,
            data_atualizacao DATETIME NOT NULL,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
        )
        ''')
        
        # Criar tabelas para NFC-e
        cursor.execute('''
        CREATE TABLE nfces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nuvem_fiscal_id TEXT UNIQUE,
            ambiente TEXT NOT NULL,
            created_at TEXT,
            status TEXT NOT NULL,
            data_emissao TEXT,
            serie INTEGER,
            numero INTEGER,
            valor_total REAL NOT NULL,
            chave TEXT UNIQUE,
            autorizacao_id TEXT,
            autorizacao_status TEXT,
            autorizacao_data_evento TEXT,
            autorizacao_numero_protocolo TEXT,
            autorizacao_codigo_status INTEGER,
            autorizacao_motivo_status TEXT,
            empresa_id INTEGER NOT NULL,
            data_cadastro DATETIME NOT NULL,
            data_atualizacao DATETIME NOT NULL,
            payload_enviado TEXT,
            resposta_completa TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
        )
        ''')
        
        # Criar tabela para itens da NFC-e
        cursor.execute('''
        CREATE TABLE itens_nfce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nfce_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            ncm TEXT NOT NULL,
            cfop TEXT NOT NULL,
            unidade TEXT NOT NULL,
            quantidade REAL NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL,
            icms_csosn TEXT,
            pis_cst TEXT,
            pis_valor REAL,
            cofins_cst TEXT,
            cofins_valor REAL,
            FOREIGN KEY (nfce_id) REFERENCES nfces(id) ON DELETE CASCADE
        )
        ''')
        
        # Criar índice para CNPJ
        cursor.execute('''
        CREATE UNIQUE INDEX ix_empresas_cpf_cnpj ON empresas (cpf_cnpj)
        ''')
        
        # Criar índice para empresa_id em enderecos
        cursor.execute('''
        CREATE INDEX ix_enderecos_empresa_id ON enderecos (empresa_id)
        ''')
        
        # Criar tabela de versão para alembic (se já estiver usando)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alembic_version (
            version_num VARCHAR(32) NOT NULL
        )
        ''')
        
        # Inserir a empresa da barbearia (exatamente como no seu modelo teste)
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insere a empresa
        cursor.execute('''
        INSERT INTO empresas (
            cpf_cnpj, inscricao_estadual, nome_razao_social, nome_fantasia,
            email, telefone, tipo_pessoa, ativo, data_cadastro, data_atualizacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '48144666000140',  # CNPJ exato do seu modelo
            '0048643140066',   # Inscrição Estadual
            'NUNES E BUSATO BARBEARIA LTDA',  # Razão Social exata
            '',                # Nome Fantasia
            'vivianfragoso@moveonsales.com.br',  # E-mail
            '',                # Telefone
            'Jurídica',        # Tipo de Pessoa
            1,                 # Ativo
            data_atual,        # Data de Cadastro
            data_atual         # Data de Atualização
        ))
        
        # Obter o ID da empresa inserida
        empresa_id = cursor.lastrowid
        
        # Insere o endereço
        cursor.execute('''
        INSERT INTO enderecos (
            empresa_id, cep, logradouro, numero, complemento, bairro,
            codigo_municipio, municipio, uf, data_cadastro, data_atualizacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            empresa_id,        # ID da empresa
            '30575740',        # CEP
            'RUA ELI SEABRA FILHO',  # Logradouro
            '510',             # Número
            '',                # Complemento
            'Buritis',         # Bairro
            '3106200',         # Código IBGE de Buritis - MG (exato do seu modelo)
            'Buritis',         # Município
            'MG',              # UF
            data_atual,        # Data de Cadastro
            data_atual         # Data de Atualização
        ))
        
        # Commit e fechar conexão
        conn.commit()
        print("Banco de dados recriado com sucesso!")
        
        # Verificar que tudo foi criado corretamente
        print("\nVerificando tabelas criadas:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        for tabela in tabelas:
            print(f"- {tabela[0]}")
        
        print("\nVerificando empresa inserida:")
        cursor.execute("SELECT id, cpf_cnpj, nome_razao_social FROM empresas")
        empresas = cursor.fetchall()
        for empresa in empresas:
            print(f"- ID: {empresa[0]}, CNPJ: {empresa[1]}, Nome: {empresa[2]}")
        
        print("\nVerificando endereço inserido:")
        cursor.execute("SELECT id, empresa_id, municipio, codigo_municipio FROM enderecos")
        enderecos = cursor.fetchall()
        for endereco in enderecos:
            print(f"- ID: {endereco[0]}, Empresa ID: {endereco[1]}, Município: {endereco[2]}, Código Município: {endereco[3]}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Erro SQLite: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return False
        
    except Exception as e:
        print(f"Erro: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("Este script irá DELETAR o banco de dados existente e criar um novo.")
    print("Todos os dados serão perdidos!")
    print("Deseja continuar? (s/n)")
    
    resposta = input().lower()
    if resposta != 's':
        print("Operação cancelada pelo usuário.")
        sys.exit(0)
    
    # Recriar o banco
    if recriar_banco():
        print("Operação concluída com sucesso!")
    else:
        print("Falha na operação.")
        sys.exit(1)