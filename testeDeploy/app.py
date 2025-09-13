from flask import Flask, request, render_template, jsonify
import os
import mysql.connector as my
from mysql.connector import pooling

app = Flask(__name__)

# ====== Credenciais lidas do ambiente (definidas no WSGI) ======
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# ====== Pool de conexões (não conecta no import do módulo) ======
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    charset="utf8mb4",
    use_pure=True,  # ajuda a evitar algumas incompatibilidades
)

def get_conn():
    return pool.get_connection()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form["user"]
    senha = request.form["senha"]
    # exemplo simples de uso do banco (ajuste conforme sua tabela)
    cnx = get_conn()
    cur = cnx.cursor()
    cur.execute("SELECT NOW()")
    cur.fetchone()
    cur.close()
    cnx.close()
    return render_template("index.html")

@app.get("/health")
def health():
    try:
        cnx = get_conn()
        cur = cnx.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        cnx.close()
        return jsonify({"status": "ok", "db": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

# IMPORTANTE: não use app.run() aqui no PythonAnywhere.
# O servidor WSGI irá importar "app" a partir do app.py.
