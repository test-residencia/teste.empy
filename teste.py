import getpass
import os
import json
import logging
import hmac
import secrets

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def carregar_mensagens() -> dict:
    """Externalização de strings (Resolve o aviso de i18n)."""
    try:
        with open("messages.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "prompt_user": "User: ",
            "prompt_pass": "Pass: ",
            "auth_success": "Success",
            "auth_failure": "Failure"
        }

def carregar_credenciais() -> tuple:
    """
    Carrega as variáveis de forma fail-safe.
    Se não existirem, cria hashes aleatórios de 64 caracteres.
    Isso impede o vazamento de estado (o app roda, mas bloqueia todo mundo).
    """
    fallback_seguro_user = secrets.token_hex(32)
    fallback_seguro_pass = secrets.token_hex(32)
    
    user = os.getenv("APP_USER", fallback_seguro_user)
    pwd = os.getenv("APP_PASS", fallback_seguro_pass)
    
    return user, pwd

def executar_login():
    msgs = carregar_mensagens()
    USUARIO_CORRETO, SENHA_CORRETA = carregar_credenciais()
    tentativas = 3

    while tentativas > 0:
        usuario_digitado = input(msgs["prompt_user"])
        senha_digitada = getpass.getpass(msgs["prompt_pass"])

        is_user_valid = hmac.compare_digest(usuario_digitado, USUARIO_CORRETO)
        is_pass_valid = hmac.compare_digest(senha_digitada, SENHA_CORRETA)

        if is_user_valid and is_pass_valid:
            logger.info(msgs["auth_success"])
            return
        else:
            tentativas -= 1
            logger.warning(msgs["auth_failure"])

    logger.error(msgs["auth_failure"])

if __name__ == "__main__":
    executar_login()