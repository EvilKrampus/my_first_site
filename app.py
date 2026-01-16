from flask import Flask, render_template, request, session, flash, redirect, url_for
from db import get_db
import hashlib
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login-page")
def login_page():
    return render_template("login.html")


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

    flash("Регистрация успешна! Теперь войдите.", "success")
    return redirect(url_for("login_page"))

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
        flash("Добро пожаловать!", "success")
        return redirect(url_for("profile"))
    else:
        flash("Неверный логин или пароль", "danger")
        return redirect(url_for("login_page"))

@app.route("/profile")
def profile():
    if "user" in session:
        return render_template(
            "profile.html",
            username=session["user"]
        )
    else:
        flash("Сначала войдите", "warning")
        return redirect(url_for("login_page"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
