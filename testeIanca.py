from flask import Flask, request, jsonify
import sqlite3
import hashlib
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

DATABASE = "users.db"

def get_connection():
    return sqlite3.connect(DATABASE)

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    logging.info(f"User registered: {username}")

    return jsonify({"message": "User created"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT password FROM users WHERE username = '{username}'"

    result = cursor.execute(query).fetchone()

    conn.close()

    if not result:
        return jsonify({"error": "User not found"}), 404

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    if result[0] == hashed_password:
        return jsonify({
            "message": "Login successful",
            "token": f"{username}-authenticated"
        })

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/users", methods=["GET"])
def list_users():
    secret = request.headers.get("X-ADMIN-KEY")

    if secret != "admin123":
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_connection()
    cursor = conn.cursor()

    users = cursor.execute(
        "SELECT username FROM users"
    ).fetchall()

    conn.close()

    return jsonify(users)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development")
    })


if __name__ == "__main__":
    app.run(debug=True)