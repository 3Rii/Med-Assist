from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import re
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import insert

app = Flask(__name__)
app.secret_key = 'secret_key'

# 1 polacznie
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'projekt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#2 polaczenie
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://:@localhost:3306/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# reflection Tables
Base = db.Table('Date', db.metadata, autoload=True, autoload_with=db.engine)
results = db.session.query(Base).all()

Acc = db.Table('accounts', db.metadata, autoload=True, autoload_with=db.engine)
acc_res = db.session.query(Acc).all()

User = db.Table('uzytkownik', db.metadata, autoload=True, autoload_with=db.engine)
user_res = db.session.query(User).all()

Chck = db.Table('check_ups', db.metadata, autoload=True, autoload_with=db.engine)
check_res = db.session.query(Chck).all()

Prev = db.Table('prevention', db.metadata, autoload=True, autoload_with=db.engine)
prev_res = db.session.query(Prev).all()

Vacc = db.Table('vacc', db.metadata, autoload=True, autoload_with=db.engine)
vacc_res = db.session.query(Vacc).all()

#auto-map tables
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# date = Base.classes.Date
acc = Base.classes.accounts
user = Base.classes.user
uuu = Base.classes.uzytkownik
chck = Base.classes.check_ups
prev = Base.classes.prevention
vacc = Base.classes.vacc
Date = Base.classes.Date

# Testowa tabela do CRUD
@app.route('/basic', methods=['GET', 'POST'])
def Basic():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

        cursor.execute('SELECT * FROM uzytkownik WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template("forms/basicform.html", user=account)

    else:
        return redirect(url_for('login'))

# this is our update route where we are going to update our employee
@app.route('/basic/update', methods=['GET', 'POST'])
def BasicUpdate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM uzytkownik WHERE id = %s', (session['id']))
        account = cursor.fetchone()

        if request.method == 'POST':
            my_data = db.session.query(uuu).get(request.form.get('id'))
            if my_data is not None:
                my_data.wiek = round(int(request.form['wiek']))
                my_data.waga = request.form['waga']
                my_data.wzrost = request.form['wzrost']
                my_data.plec = request.form['plec']
                my_data.papierosy = request.form['papierosy']
                my_data.alkohol = request.form['alkohol']
                my_data.aktywnosc = request.form['aktywnosc']
                db.session.commit()
                # print('zmien')
                # return redirect(url_for('Basic'))
            else:
                # print('warun dziala')
                account_id = session['id']
                wiek = round(int(request.form['wiek']))
                waga = request.form['waga']
                wzrost = request.form['wzrost']
                plec = request.form['plec']
                papierosy = request.form['papierosy']
                alkohol = request.form['alkohol']
                aktywnosc = request.form['aktywnosc']
                cursor.execute('INSERT INTO uzytkownik VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc))
                conn.commit()
                return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# This route is for deleting our employee
@app.route('/basic/delete/', methods=['GET', 'POST'])
def BasicDelete():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

            cursor.execute('DELETE FROM uzytkownik WHERE id = %s', (session['id']))
            conn.commit()
            return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# http://localhost:5000/login/
@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# http://localhost:5000/register
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

# http://localhost:5000/
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
        username = cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('homepage/home.html', username=session['username'], account=account)
    return redirect(url_for('login'))

# http://localhost:5000/logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# http://localhost:5000/profile
@app.route('/profile')
def profile():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)