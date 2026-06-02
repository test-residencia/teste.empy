import getpass
import os
import sys
import logging
import hmac

logging.basicConfig(level=logging.ERROR, format='[%(levelname)s] %(message)s')

MESSAGES = {
    "prompt_user": "Usuário: ",
    "prompt_pass": "Senha: ",
    "auth_success": "Acesso concedido.",
    "auth_failure": "Falha de autenticação ou acesso bloqueado.",
    "sys_error": "Erro interno do servidor."
}

def carregar_credenciais():
    """Tenta carregar as credenciais de forma estrita."""
    try:
        user = os.environ["APP_USER"]
        pwd = os.environ["APP_PASS"]
        return user, pwd
    except KeyError:
        logging.error(MESSAGES["sys_error"])
        sys.exit(1)

def executar_login():
    USUARIO_CORRETO, SENHA_CORRETA = carregar_credenciais()
    tentativas_restantes = 3

    while tentativas_restantes > 0:
        usuario_digitado = input(MESSAGES["prompt_user"])
        senha_digitada = getpass.getpass(MESSAGES["prompt_pass"])

        is_user_valid = hmac.compare_digest(usuario_digitado, USUARIO_CORRETO)
        is_pass_valid = hmac.compare_digest(senha_digitada, SENHA_CORRETA)

        if is_user_valid and is_pass_valid:
            print(f"\n[SUCESSO] {MESSAGES['auth_success']}")
            return
        else:
            tentativas_restantes -= 1
            print(f"\n[ERRO] {MESSAGES['auth_failure']}")

    print(f"\n[ERRO] {MESSAGES['auth_failure']}")

if __name__ == "__main__":
    executar_login()