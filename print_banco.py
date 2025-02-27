import sqlite3

def listar_tabelas(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    return [tabela[0] for tabela in tabelas]

def exibir_dados_tabela(conexao, tabela):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM {tabela}")
    colunas = [descricao[0] for descricao in cursor.description]
    registros = cursor.fetchall()

    print(f"\nTabela: {tabela}")
    print("-" * (len(tabela) + 9))
    print(" | ".join(colunas))
    print("-" * (len(tabela) + 9))
    for registro in registros:
        print(" | ".join(map(str, registro)))
    print("\n")

def main():
    caminho_banco = 'app.db'  # Substitua pelo caminho do seu arquivo .db
    conexao = sqlite3.connect(caminho_banco)

    try:
        tabelas = listar_tabelas(conexao)
        if not tabelas:
            print("Nenhuma tabela encontrada no banco de dados.")
        else:
            for tabela in tabelas:
                exibir_dados_tabela(conexao, tabela)
    except sqlite3.Error as erro:
        print(f"Erro ao acessar o banco de dados: {erro}")
    finally:
        conexao.close()

if __name__ == "__main__":
    main()
