import os

from dotenv import load_dotenv
from werkzeug.security import check_password_hash


load_dotenv()


def autenticar_usuario(usuario, senha):
    """Verifica se as credenciais administrativas são válidas."""

    usuario_correto = os.getenv("ADMIN_USERNAME")
    senha_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if not usuario_correto or not senha_hash:
        return False

    if usuario != usuario_correto:
        return False

    return check_password_hash(senha_hash, senha)