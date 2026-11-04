
import qrcode
import base64
from io import BytesIO


def gerar_qrcode(url):
    """Gera um QR Code a partir de uma URL e retorna sua imagem em Base64."""

    imagem = qrcode.make(url)

    arquivo = BytesIO()
    imagem.save(arquivo, format="PNG")

    imagem_base64 = base64.b64encode(
        arquivo.getvalue()
    ).decode("utf-8")

    return imagem_base64
