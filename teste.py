import getpass
import os
import sys

USUARIO_CORRETO = os.environ.get("APP_USER")
SENHA_CORRETA = os.environ.get("APP_PASS")

if not USUARIO_CORRETO or not SENHA_CORRETA:
    print("\n[ERRO] Erro interno do servidor. Inicialização abortada.")
    sys.exit(1)

tentativas_restantes = 3

print("--- SISTEMA DE AUTENTICAÇÃO ---")

while tentativas_restantes > 0:
    usuario_digitado = input("Usuário: ")
    senha_digitada = getpass.getpass("Senha: ")

    if usuario_digitado == USUARIO_CORRETO and senha_digitada == SENHA_CORRETA:
        print("\n[SUCESSO] Acesso concedido.")
        break
    else:
        tentativas_restantes -= 1
        print("\n[ERRO] Falha na autenticação.")

if tentativas_restantes == 0:
    print("\n[BLOQUEADO] Acesso negado.")