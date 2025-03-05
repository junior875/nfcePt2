import qrcode

# Informações da NFC-e
chave_acesso = "31250348144666000140650010007210921111991017"  # Chave de Acesso da NFC-e
versao_qrcode = "2"  # Versão do QR Code
ambiente = "1"  # 1 para Produção, 2 para Homologação
csc = "SEU_CODIGO_CSC"  # Código de Segurança do Contribuinte (CSC)
id_token = "ID_TOKEN"  # Identificador do CSC

# Montando a URL do QR Code
dados_qrcode = f"{chave_acesso}|{versao_qrcode}|{ambiente}|{csc}|{id_token}"
url_qrcode = f"https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml?p={dados_qrcode}"

# Gerando o QR Code
qr = qrcode.make(url_qrcode)
qr.save("qrcode_nfce_correto.png")

print("QR Code gerado com sucesso! Verifique o arquivo 'qrcode_nfce.png'.")
