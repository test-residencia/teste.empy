import getpass

usuario_correto = "admin"
senha_correta = "1234"
tentativas_restantes = 3

print("--- SISTEMA DE LOGIN SIMPLES ---")

while tentativas_restantes > 0:
    usuario_digitado = input("Digite o nome de usuário: ")
    senha_digitada = getpass.getpass("Digite a senha: ")

    if usuario_digitado == usuario_correto and senha_digitada == senha_correta:
        print("\n[SUCESSO] Acesso concedido! Bem-vindo de volta.")
        break
    else:
        tentativas_restantes -= 1
        print(f"\n[ERRO] Credenciais incorretas. Tentativas restantes: {tentativas_restantes}")
        
        if tentativas_restantes == 1:
            print("[DICA] Esqueceu a senha? A senha padrão tem 4 dígitos.")

if tentativas_restantes == 0:
    print("\n[BLOQUEADO] Sistema bloqueado por excesso de tentativas.")