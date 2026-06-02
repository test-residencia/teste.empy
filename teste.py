import getpass
import os
import sys

try:
    USUARIO_CORRETO = os.environ["APP_USER"]
    SENHA_CORRETA = os.environ["APP_PASS"]
except KeyError as e:
    print(f"\n[ERRO CRÍTICO] Falha de configuração: A variável de ambiente {e} não foi definida.")
    print("O sistema não pode ser iniciado sem credenciais seguras.")
    sys.exit(1)

tentativas_restantes = 3

print("--- SISTEMA DE LOGIN SIMPLES ---")

while tentativas_restantes > 0:
    usuario_digitado = input("Digite o nome de usuário: ")
    senha_digitada = getpass.getpass("Digite a senha: ")

    if usuario_digitado == USUARIO_CORRETO and senha_digitada == SENHA_CORRETA:
        print("\n[SUCESSO] Acesso concedido! Bem-vindo de volta.")
        break
    else:
        tentativas_restantes -= 1
        print(f"\n[ERRO] Credenciais incorretas. Tentativas restantes: {tentativas_restantes}")
        
        if tentativas_restantes == 1:
            print("[DICA] Esqueceu a senha? Entre em contato com o administrador do sistema.")

if tentativas_restantes == 0:
    print("\n[BLOQUEADO] Sistema bloqueado por excesso de tentativas.")