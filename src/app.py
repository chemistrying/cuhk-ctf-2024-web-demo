from flask import Flask, request, render_template, session, redirect
import os, secrets
import mysql.connector

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = secrets.token_bytes()

DB_USER = os.environ.get('MYSQL_USER')
DB_PASS = os.environ.get('MYSQL_PASSWORD')
DB_NAME = os.environ.get('MYSQL_DATABASE')

FLAG1 = os.environ.get('FLAG1')

def get_db():
    return mysql.connector.connect(
        host="web-demo-db",
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route("/")
def index():
    return render_template("index.html", flag1=FLAG1, logged=session.get('username') is not None)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        return render_template("login.html", hint="Invalid parameters!")
    username, password = request.form.get('username'), request.form.get('password')

    # Login logic
    db = get_db()
    with db.cursor() as conn:
        conn.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        result = conn.fetchall()
        if len(result) > 0:
            # Ok
            session['username'] = username
            return redirect("/")
    return render_template("login.html", hint="Invalid username or password!")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")
            