import os
import re

def fix_imports(directory):
    """
    Corrige as importações de 'app.' para 'backend.app.' em todos os arquivos Python
    no diretório especificado e seus subdiretórios.
    """
    pattern = re.compile(r'(from|import)\s+app\.')
    replacement = r'\1 backend.app.'
    
    # Contador para estatísticas
    files_modified = 0
    replacements_made = 0
    
    # Percorrer o diretório recursivamente
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Ler o conteúdo do arquivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Substituir importações
                new_content, count = pattern.subn(replacement, content)
                
                # Se houver substituições, escrever de volta no arquivo
                if count > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    files_modified += 1
                    replacements_made += count
                    print(f"Modificado: {file_path} ({count} substituições)")
    
    print(f"\nTotal: {files_modified} arquivos modificados, {replacements_made} substituições realizadas.")

if __name__ == "__main__":
    # Diretório raiz do projeto (ajuste conforme necessário)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    fix_imports(os.path.join(project_dir, 'backend'))