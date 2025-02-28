import qrcode
import base64
from io import BytesIO

# Informações da NFC-e
chave_acesso = "31250248144666000140650010021987654329"
versao_qrcode = "2"
ambiente = "1"  # 1 = Produção, 2 = Homologação
csc = "SEU_CODIGO_CSC"
id_token = "ID_TOKEN"

# Montando a URL do QR Code
dados_qrcode = f"{chave_acesso}|{versao_qrcode}|{ambiente}|{csc}|{id_token}"
url_qrcode = f"https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml?p={dados_qrcode}"

# Gerando o QR Code
qr = qrcode.make(url_qrcode)

# Convertendo o QR Code para Base64
buffer = BytesIO()
qr.save(buffer, format="PNG")
qr_base64 = base64.b64encode(buffer.getvalue()).decode()

# Exibindo a string Base64 do QR Code
print("✅ QR Code gerado e convertido para Base64:")
print(qr_base64)

# Simulando salvar no banco
qr_code_banco = qr_base64
