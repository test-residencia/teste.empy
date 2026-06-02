import getpass
import os
import json
import hmac
import sys

def carregar_mensagens() -> dict:
    """Carrega as mensagens de interface de forma externa."""
    try:
        with open("messages.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
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

    if not cred_user or not cred_pass:
        sys.exit(1)

    tentativas = 3

    while tentativas > 0:
        usuario_digitado = input(msgs["prompt_user"])
        senha_digitada = getpass.getpass(msgs["prompt_pass"])

        is_user_valid = hmac.compare_digest(usuario_digitado, cred_user)
        is_pass_valid = hmac.compare_digest(senha_digitada, cred_pass)

        if is_user_valid and is_pass_valid:

            return
        else:
            tentativas -= 1

    sys.exit(1)

if __name__ == "__main__":
    executar_login()