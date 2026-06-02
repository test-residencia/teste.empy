import getpass
import os
import sys
import logging
import hmac

logging.basicConfig(
    level=logging.INFO, # Grava de INFO para cima (INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

MESSAGES = {
    "prompt_user": "Usuário: ",
    "prompt_pass": "Senha: ",
    "auth_success": "Acesso concedido.",
    "auth_failure": "Falha de autenticação ou acesso bloqueado.",
    "sys_error": "Erro interno do servidor na inicialização."
}

def carregar_credenciais() -> tuple:
    """Carrega as credenciais usando getenv e valida a existência delas com segurança."""
    user = os.getenv("APP_USER")
    pwd = os.getenv("APP_PASS")

    if not user or not pwd:
        logger.critical(MESSAGES["sys_error"])
        sys.exit(1)

    return user, pwd

def executar_login():
    USUARIO_CORRETO, SENHA_CORRETA = carregar_credenciais()
    tentativas_restantes = 3

    logger.info("Sistema de autenticação iniciado.")

    while tentativas_restantes > 0:
        usuario_digitado = input(MESSAGES["prompt_user"])
        senha_digitada = getpass.getpass(MESSAGES["prompt_pass"])

        is_user_valid = hmac.compare_digest(usuario_digitado, USUARIO_CORRETO)
        is_pass_valid = hmac.compare_digest(senha_digitada, SENHA_CORRETA)

        if is_user_valid and is_pass_valid:
            logger.info(MESSAGES["auth_success"])
            return
        else:
            tentativas_restantes -= 1
            logger.warning(MESSAGES["auth_failure"])
 
    logger.error(MESSAGES["auth_failure"])

if __name__ == "__main__":
    executar_login()