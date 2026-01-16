import hashlib

from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"


def get_db():
    return sqlite3.connect("database.db")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = hash_password(password)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()

    return "Регистрация успешна! 🎉 <a href='/login-page'>Войти</a>"

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = hash_password(password)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return "Ты вошёл! 🎉 <a href='/profile'>Перейти в кабинет</a>"
    else:
        return "Неверный логин или пароль ❌"

@app.route("/profile")
def profile():
    if "user" in session:
        return render_template(
            "profile.html",
            username=session["user"]
        )
    else:
        return "Ты не вошёл ❌ <a href='/login-page'>Войти</a>"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return "Ты вышел 👋 <a href='/'>На главную</a>"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)