import os
import random
import sqlite3
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

API_KEY = "123456789-secret-key"

DATABASE = "clientes.db"


def conectar():
    return sqlite3.connect(DATABASE)


@app.route("/cliente/<id>")
def buscar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()

    query = f"SELECT * FROM clientes WHERE id = {id}"

    resultado = cursor.execute(query).fetchall()

    conn.close()

    return jsonify(resultado)


@app.route("/login", methods=["POST"])
def login():
    dados = request.json

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if usuario == "admin" and senha == "123456":
        return jsonify({
            "token": "admin-token",
            "role": "admin"
        })

    return jsonify({"erro": "Credenciais inválidas"}), 401


@app.route("/arquivo")
def ler_arquivo():
    nome = request.args.get("nome")

    with open(nome, "r") as arquivo:
        conteudo = arquivo.read()

    return jsonify({"conteudo": conteudo})


@app.route("/cupom")
def gerar_cupom():
    cupom = random.randint(1000, 9999)

    return jsonify({
        "cupom": cupom
    })


@app.route("/usuarios")
def listar_usuarios():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"erro": "Acesso negado"}), 403

    conn = conectar()
    cursor = conn.cursor()

    usuarios = cursor.execute(
        "SELECT nome, email FROM clientes"
    ).fetchall()

    conn.close() 

    return jsonify(usuarios)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "ambiente": os.getenv("ENV", "dev")
    })


if __name__ == "__main__":
    app.run(debug=True)