# verificar_arquivo.py
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Caminho para verificar
CERTIFICADO_PATH = os.path.abspath(os.path.join("storage", "certificados", "barbearia.pfx"))

logger.info(f"Verificando o arquivo: {CERTIFICADO_PATH}")

if os.path.exists(CERTIFICADO_PATH):
    logger.info(f"✅ O arquivo existe! Tamanho: {os.path.getsize(CERTIFICADO_PATH)} bytes")
else:
    logger.error(f"❌ O arquivo NÃO existe!")
    
    # Verificar o diretório pai
    dir_path = os.path.dirname(CERTIFICADO_PATH)
    if os.path.exists(dir_path):
        logger.info(f"Diretório existe: {dir_path}")
        logger.info(f"Arquivos no diretório: {os.listdir(dir_path)}")
    else:
        logger.error(f"O diretório não existe: {dir_path}")
        
        # Verificar a estrutura de pastas
        base_dir = "storage"
        if os.path.exists(base_dir):
            logger.info(f"Diretório base existe: {base_dir}")
            logger.info(f"Conteúdo: {os.listdir(base_dir)}")
        else:
            logger.error(f"Diretório base não existe: {base_dir}")
            logger.info(f"Diretório atual: {os.getcwd()}")
            logger.info(f"Conteúdo do diretório atual: {os.listdir('.')}")