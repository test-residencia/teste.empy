import getpass
import os
import json
import hmac
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def carregar_mensagens() -> dict:
    try:
        with open("messages.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "prompt_user": "User: ",
            "prompt_pass": "Pass: ",
            "auth_success": "Success",
            "auth_failure": "Failure"
        }

def executar_login():
    msgs = carregar_mensagens()
    
    cred_user = os.getenv("APP_USER", "")
    cred_pass = os.getenv("APP_PASS", "")

    if not cred_user or not cred_pass or len(cred_pass) < 8:
        logger.critical("Erro de configuração: Variáveis de segurança inválidas ou ausentes.")
        sys.exit(1)

    tentativas = 3

    while tentativas > 0:
        usuario_digitado = input(msgs["prompt_user"])
        senha_digitada = getpass.getpass(msgs["prompt_pass"])

        is_user_valid = hmac.compare_digest(usuario_digitado, cred_user)
        is_pass_valid = hmac.compare_digest(senha_digitada, cred_pass)

        if is_user_valid and is_pass_valid:
            logger.info(f"Auditoria: Login bem-sucedido para '{usuario_digitado}'.")
            return
        else:
            tentativas -= 1
            logger.warning("Auditoria: Tentativa de login reprovada.")

    logger.error("Auditoria: Acesso bloqueado por múltiplas falhas.")
    sys.exit(1)

if __name__ == "__main__":
    executar_login()