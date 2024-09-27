from flask import Flask, request, render_template, session, redirect, send_file
import os, time, subprocess, uuid
import mysql.connector

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY')

DB_USER = os.environ.get('MYSQL_USER')
DB_PASS = os.environ.get('MYSQL_PASSWORD')
DB_NAME = os.environ.get('MYSQL_DATABASE')

FLAG0 = os.environ.get('FLAG0')
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
    if session.get('username') is not None:
        db = get_db()
        with db.cursor() as conn:
            conn.execute(f"SELECT secret FROM users WHERE username = '{session.get('username')}'")
            secret = conn.fetchall()[0][0]
        return render_template("index.html", flag1=FLAG1, logged=session.get('username') is not None, username=session.get('username'), secret=secret)
    return render_template("index.html", flag1=FLAG1, logged=session.get('username') is not None, is_admin=session.get('username') == 'admin')

@app.route("/health")
def health():
    return "OK"

@app.route("/source")
def source():
    if session.get('username') is None:
        return redirect("/")
    return send_file("./source.tar.gz")

@app.route("/flag0")
def flag0():
    return FLAG0

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect("/")

    if request.method == 'GET':
        return render_template("login.html")
    
    if 'username' not in request.form.keys() or 'password' not in request.form.keys():
        return render_template("login.html", hint="Invalid parameters!")
    username, password = request.form.get('username'), request.form.get('password')

    # Login logic
    db = get_db()
    with db.cursor() as conn:
        conn.execute(f"SELECT username, secret FROM users WHERE BINARY username = '{username}' AND BINARY password = '{password}'")
        result = conn.fetchall()
        if len(result) > 0 and (not result[0][0] == 'admin' or request.remote_addr == '127.0.0.1'): # Second part checks admin logic: only local can have access
            # Ok
            session['username'] = result[0][0]
            return redirect("/")
        elif len(result) > 0 and result[0][0] == 'admin':
            return render_template("login.html", hint="Admin account not available for your IP address!")
    return render_template("login.html", hint="Invalid username or password!")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/forum", methods=['GET', 'POST'])
def forum():
    if session.get('username') is None:
        return redirect("/")

    db = get_db()
    with db.cursor() as conn:
        # Fetch posts
        conn.execute("SELECT * FROM posts ORDER BY date DESC")
        posts_result = conn.fetchall()
        posts_dict = [dict(zip(['id', 'author_id', 'title', 'content', 'date'], row)) for row in posts_result]
        app.logger.debug(posts_dict)

        # Handle users
        conn.execute("SELECT id, username FROM users")
        users_result = conn.fetchall()
        users_dict = dict(users_result)
        rev_users_dict = {v: k for k, v in users_dict.items()}
        
        if request.method == 'GET':
            return render_template("forum.html", posts=posts_dict, users=users_dict)    
        elif request.method == 'POST':
            # Add post
            # Make sure the parameters are there
            if 'title' not in request.form.keys() or 'content' not in request.form.keys():
                return render_template("forum.html", hint="Invalid parameters!", posts=posts_dict, users=users_dict)
            
            title, content = request.form.get('title'), request.form.get('content')
            conn.execute(f"INSERT INTO posts (author_id, title, content, date) VALUES ('{rev_users_dict[session['username']]}', '{title}', '{content}', NOW())")
            db.commit()
            
            # Refetch data
            conn.execute("SELECT * FROM posts ORDER BY date DESC")
            posts_result = conn.fetchall()
            posts_dict = [dict(zip(['id', 'author_id', 'title', 'content', 'date'], row)) for row in posts_result]
            app.logger.debug("CHANGED:", posts_dict)
            return render_template("forum.html", posts=posts_dict, users=users_dict)  

@app.route("/code", methods=['GET', 'POST'])
def code():
    if session.get('username') != 'admin':
        return redirect("/")

    if request.method == 'GET':
        return render_template("code.html")
    elif request.method == 'POST':
        if 'password' not in request.form.keys() or 'code' not in request.form.keys():
            return render_template("code.html", hint="Invalid parameters!")
    
        password, code = request.form.get('password'), request.form.get('code')
        if password == os.environ.get('ADMIN_PASSWORD'):
            # Trust admin, run code
            id = uuid.uuid4()
            with open(f"/tmp/{id}.py", "w") as f:
                f.write(code)
                f.flush()

            completed_process = subprocess.run(["python", f"/tmp/{id}.py"], timeout=0.5, capture_output=True)
            return render_template("code.html", returncode=completed_process.returncode, output=completed_process.stdout.decode(), error=completed_process.stderr.decode())

        return render_template("code.html", hint="Invalid admin password!")


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri='memory://',
)

CHROME_ARGS = [
    '--headless=old',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--no-gpu',
    '--disable-default-apps',
    '--disable-translate',
    '--disable-device-discovery-notifications',
    '--disable-software-rasterizer',
    '--disable-xss-auditor',
    '--allow-cors',
    '--disable-notifications',
    '--disable-popup-blocking'
]
       
@app.route('/visit', methods=['GET'])
def visit_get():
    if session.get('username') is None:
        return redirect("/")

    return render_template('visit.html')

@app.route('/visit', methods=['POST'])
@limiter.limit('1 per 20 seconds')
def visit():
    if session.get('username') is None:
        return redirect("/")

    url = "http://localhost:8080"
    options = webdriver.ChromeOptions()
    for arg in CHROME_ARGS:
        options.add_argument(arg)
    driver = webdriver.Chrome(options=options)
    try:
        app.logger.fatal("Before OK")
        driver.get(url + '/login')
        driver.find_element(By.ID, 'id_username').send_keys("admin")
        driver.find_element(By.ID, 'id_password').send_keys(os.environ.get("ADMIN_PASSWORD"))
        driver.find_element(By.ID, 'id_login_submit').click()
        
        time.sleep(1)

        cookie = driver.get_cookie('session')
        driver.delete_cookie('session')
        cookie['httpOnly'] = False
        driver.add_cookie(cookie)
        app.logger.fatal(driver.get_cookies())

        # Visit forum
        driver.get(url + '/forum')
        time.sleep(2)
        return render_template('visit.html', hint='Admin has visited your URL!')
    except Exception as e:
        return render_template('visit.html', hint=str(e))
    finally:
        driver.quit()
