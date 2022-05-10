from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import re
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base


app = Flask(__name__)
app.secret_key = 'secret_key'

# 1 polacznie
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '!H34tw4w3'
app.config['MYSQL_DATABASE_DB'] = 'proj'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#2 polaczenie
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:!H34tw4w3@localhost:3306/proj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Acc = db.Table('accounts', db.metadata, autoload=True, autoload_with=db.engine)
acc_res = db.session.query(Acc).all()

User = db.Table('user', db.metadata, autoload=True, autoload_with=db.engine)
user_res = db.session.query(User).all()

User = db.Table('uzytkownik', db.metadata, autoload=True, autoload_with=db.engine)
user_resyy = db.session.query(User).all()

Chck = db.Table('check_ups', db.metadata, autoload=True, autoload_with=db.engine)
check_res = db.session.query(Chck).all()

Prev = db.Table('prevention', db.metadata, autoload=True, autoload_with=db.engine)
prev_res = db.session.query(Prev).all()

Vacc = db.Table('vacc', db.metadata, autoload=True, autoload_with=db.engine)
vacc_res = db.session.query(Vacc).all()

#auto-map tables
Base = automap_base()
Base.prepare(db.engine, reflect=True)

acc = Base.classes.accounts
user = Base.classes.user
uuu = Base.classes.uzytkownik
chck = Base.classes.check_ups
prev = Base.classes.prevention
vacc = Base.classes.vacc


# Basic Form CRUD
@app.route('/basic', methods=['GET', 'POST'])
def Basic():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template("forms/basicform.html", user=account)

    else:
        return redirect(url_for('login'))

@app.route('/basic/update', methods=['GET', 'POST'])
def BasicUpdate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id']))

        if request.method == 'POST':
            my_data = db.session.query(user).get(request.form.get('id'))

            if my_data is not None:
                my_data.wiek = request.form['wiek']
                my_data.waga = request.form['waga']
                my_data.wzrost = request.form['wzrost']
                my_data.plec = request.form['plec']
                my_data.papierosy = request.form['papierosy']
                my_data.alkohol = request.form['alkohol']
                my_data.aktywnosc = request.form['aktywnosc']
                db.session.commit()
                return redirect(url_for('Basic'))
            else:
                account_id = session['id']
                wiek = request.form['wiek']
                waga = request.form['waga']
                wzrost = request.form['wzrost']
                plec = request.form['plec']
                papierosy = request.form['papierosy']
                alkohol = request.form['alkohol']
                aktywnosc = request.form['aktywnosc']
                cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc))
                conn.commit()
                return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

@app.route('/basic/delete/', methods=['GET', 'POST'])
def BasicDelete():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

            cursor.execute('DELETE FROM user WHERE account_id = %s', (session['id']))
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
        return render_template('home.html', username=session['username'], account=account)
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