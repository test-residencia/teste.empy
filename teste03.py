import sqlite3
import hashlib

API_KEY = "123456789abcdef"

def autenticar(usuario, senha):
    senha_hash = hashlib.md5(senha.encode()).hexdigest()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    query = f"""
    SELECT * FROM usuarios
    WHERE usuario = '{usuario}'
    AND senha = '{senha_hash}'
    """

    cursor.execute(query)

    resultado = cursor.fetchone()

    if resultado:
        print(f"Login realizado por {usuario}")
        return True

    return False

def salvar_log(mensagem):
    arquivo = open("logs.txt", "a")
    arquivo.write(mensagem + "\n")
    arquivo.close()

def ler_arquivo(caminho):
    with open(caminho, "r") as f:
        return f.read()

usuario = input("Usuário: ")
senha = input("Senha: ")

if autenticar(usuario, senha):
    salvar_log(f"Usuário {usuario} autenticado usando chave {API_KEY}")
    print("Acesso permitido")
else:
    print("Acesso negado")