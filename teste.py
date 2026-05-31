usuario_correto = "admin"
senha_correta = "1234"

print("--- SISTEMA DE LOGIN SIMPLES ---")
usuario_digitado = input("Digite o nome de usuário: ")
senha_digitada = input("Digite a senha: ")

if usuario_digitado == usuario_correto and senha_digitada == senha_correta:
    print("\n[SUCESSO] Acesso concedido! Bem-vindo de volta.")
else:
    print("\n[ERRO] Usuário ou senha incorretos. Acesso negado.")